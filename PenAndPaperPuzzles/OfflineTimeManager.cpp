#include "OfflineTimeManager.h"
#include "OfflineConfigManager.h"
#include "EscPosPrinter.h"
#include "ThermalCanvas.h"
#include "OfflinePuzzleComposer.h"

OfflineTimeManager::OfflineTimeManager() :
    _timeSet(false),
    _lastPrintedYear(-1),
    _lastPrintedDay(-1),
    _portalActive(false),
    _ds3231Present(false),
    _portalStartedMs(0),
    _pendingExit(false),
    _pendingExitMs(0),
    _configManager(nullptr),
    _printer(nullptr),
    _server(80) {
}

void OfflineTimeManager::begin() {
    // 1. Check for optional DS3231 hardware RTC via I2C (GPIO 21 SDA, GPIO 22 SCL)
    Wire.begin(21, 22);
    Wire.beginTransmission(DS3231_I2C_ADDR);
    if (Wire.endTransmission() == 0) {
        _ds3231Present = true;
        Serial.println("[TIME] Found DS3231 hardware RTC on I2C (0x68)!");
        checkAndSyncFromDs3231();
    } else {
        Serial.println("[TIME] No DS3231 hardware RTC detected. Using internal timer / SoftAP sync.");
    }
}

uint8_t OfflineTimeManager::bcdToDec(uint8_t val) {
    return ((val / 16 * 10) + (val % 16));
}

uint8_t OfflineTimeManager::decToBcd(uint8_t val) {
    return ((val / 10 * 16) + (val % 10));
}

bool OfflineTimeManager::checkAndSyncFromDs3231() {
    if (!_ds3231Present) return false;

    Wire.beginTransmission(DS3231_I2C_ADDR);
    Wire.write(0x00); // Start at register 0 (seconds)
    if (Wire.endTransmission() != 0) return false;

    Wire.requestFrom((uint8_t)DS3231_I2C_ADDR, (uint8_t)7);
    if (Wire.available() < 7) return false;

    uint8_t sec  = bcdToDec(Wire.read() & 0x7F);
    uint8_t min  = bcdToDec(Wire.read() & 0x7F);
    uint8_t hour = bcdToDec(Wire.read() & 0x3F);
    Wire.read(); // Day of week (unused)
    uint8_t day  = bcdToDec(Wire.read() & 0x3F);
    uint8_t mon  = bcdToDec(Wire.read() & 0x1F);
    uint16_t yr  = 2000 + bcdToDec(Wire.read());

    struct tm t;
    t.tm_sec  = sec;
    t.tm_min  = min;
    t.tm_hour = hour;
    t.tm_mday = day;
    t.tm_mon  = mon - 1;
    t.tm_year = yr - 1900;
    t.tm_isdst = -1;

    time_t epoch = mktime(&t);
    struct timeval tv = { epoch, 0 };
    settimeofday(&tv, nullptr);

    _timeSet = true;
    Serial.printf("[TIME] Synced time from DS3231: %04d-%02d-%02d %02d:%02d:%02d\n",
                  yr, mon, day, hour, min, sec);
    return true;
}

bool OfflineTimeManager::writeToDs3231(const struct tm& t) {
    if (!_ds3231Present) return false;

    Wire.beginTransmission(DS3231_I2C_ADDR);
    Wire.write(0x00);
    Wire.write(decToBcd(t.tm_sec));
    Wire.write(decToBcd(t.tm_min));
    Wire.write(decToBcd(t.tm_hour));
    Wire.write(decToBcd(t.tm_wday + 1));
    Wire.write(decToBcd(t.tm_mday));
    Wire.write(decToBcd(t.tm_mon + 1));
    Wire.write(decToBcd((t.tm_year + 1900) % 100));
    return (Wire.endTransmission() == 0);
}

void OfflineTimeManager::setSystemTime(time_t epoch, int tzOffsetMinutes) {
    // Convert UTC epoch to local wall-clock epoch based on client timezone offset.
    // In JavaScript, Date.getTimezoneOffset() returns minutes that UTC is ahead of local time
    // (e.g. UTC-5 US Central is +300 min; UTC+9 Tokyo is -540 min).
    // Subtracting (tzOffsetMinutes * 60) converts UTC epoch to the client's local wall-clock time.
    time_t localEpoch = epoch - ((time_t)tzOffsetMinutes * 60);

    struct timeval tv = { localEpoch, 0 };
    settimeofday(&tv, nullptr);
    _timeSet = true;

    time_t now = time(nullptr);
    struct tm* t = localtime(&now);

    Serial.printf("[TIME] System clock set to local wall-clock: %04d-%02d-%02d %02d:%02d:%02d (TZ Offset: %d min applied)\n",
                  t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
                  t->tm_hour, t->tm_min, t->tm_sec, tzOffsetMinutes);

    if (_ds3231Present) {
        writeToDs3231(*t);
        Serial.println("[TIME] Persisted new local time to DS3231 hardware RTC.");
    }
}

void OfflineTimeManager::setSystemTime(int year, int month, int day, int hour, int minute, int second) {
    struct tm t;
    memset(&t, 0, sizeof(t));
    t.tm_sec  = second;
    t.tm_min  = minute;
    t.tm_hour = hour;
    t.tm_mday = day;
    t.tm_mon  = month - 1;
    t.tm_year = year - 1900;
    t.tm_isdst = -1;

    time_t localEpoch = mktime(&t);
    struct timeval tv = { localEpoch, 0 };
    settimeofday(&tv, nullptr);
    _timeSet = true;

    Serial.printf("[TIME] System clock set to device local wall-clock: %04d-%02d-%02d %02d:%02d:%02d\n",
                  year, month, day, hour, minute, second);

    if (_ds3231Present) {
        writeToDs3231(t);
        Serial.println("[TIME] Persisted new local time to DS3231 hardware RTC.");
    }
}

String OfflineTimeManager::getFormattedTime(const char* format) {
    if (!_timeSet) return "Time Not Set (Pending Sync)";

    time_t now = time(nullptr);
    struct tm* t = localtime(&now);
    char buf[64];
    strftime(buf, sizeof(buf), format, t);
    return String(buf);
}

bool OfflineTimeManager::isCronTriggerTime(uint8_t targetHour, uint8_t targetMinute) {
    if (!_timeSet) return false;

    time_t now = time(nullptr);
    struct tm* t = localtime(&now);

    if (t->tm_hour == targetHour && t->tm_min == targetMinute) {
        if (t->tm_year != _lastPrintedYear || t->tm_yday != _lastPrintedDay) {
            Serial.printf("[TIME] 7:00 AM Cron triggered at %02d:%02d!\n", targetHour, targetMinute);
            markPrintedToday();
            return true;
        }
    }
    return false;
}

void OfflineTimeManager::markPrintedToday() {
    time_t now = time(nullptr);
    struct tm* t = localtime(&now);
    _lastPrintedYear = t->tm_year;
    _lastPrintedDay  = t->tm_yday;
}

// -----------------------------------------------------------------------------
// SoftAP Web Setup Portal
// -----------------------------------------------------------------------------
void OfflineTimeManager::startSetupPortal() {
    Serial.println("\n[PORTAL] Starting SoftAP Web Configurator...");
    WiFi.mode(WIFI_AP);
    WiFi.setSleep(false); // Keep Wi-Fi radio fully active so beacons broadcast continuously
    IPAddress myIP(192, 168, 4, 1);
    IPAddress gateway(192, 168, 4, 1);
    IPAddress subnet(255, 255, 255, 0);
    WiFi.softAPConfig(myIP, gateway, subnet);
    WiFi.softAP("Pen-And-Paper-Puzzles", nullptr, 1, 0, 4);
    Serial.printf("[PORTAL] Hotspot started! SSID: Pen-And-Paper-Puzzles (Open Network)\n");
    Serial.printf("[PORTAL] Connect phone and visit: http://%s\n", myIP.toString().c_str());

    // Captive portal DNS server (redirect all domains to 192.168.4.1)
    _dnsServer.start(53, "*", myIP);

    setupWebRoutes();
    _server.begin();
    _portalActive = true;
    _portalStartedMs = millis();
    _pendingExit = false;
}

void OfflineTimeManager::stopSetupPortal() {
    if (_portalActive) {
        _server.stop();
        _dnsServer.stop();
        WiFi.softAPdisconnect(true);
        WiFi.mode(WIFI_OFF);
        _portalActive = false;
        _pendingExit = false;
        Serial.println("[PORTAL] SoftAP Setup Portal closed.");
    }
}

void OfflineTimeManager::handleClient() {
    if (_portalActive) {
        _dnsServer.processNextRequest();
        _server.handleClient();

        // 5-minute auto-timeout (300,000 ms)
        if (millis() - _portalStartedMs > 300000) {
            Serial.println("[PORTAL] 5-minute inactivity timeout reached -> Auto-closing hotspot.");
            stopSetupPortal();
            return;
        }

        // Pending delayed exit after saving config
        if (_pendingExit && millis() - _pendingExitMs > 1200) {
            _pendingExit = false;
            stopSetupPortal();
        }
    }
}

void OfflineTimeManager::printSetupTicket(EscPosPrinter& printer, const OfflineConfigManager* config) {
    if (!config) {
        config = _configManager;
    }

    if (!printer.isConnected()) {
        if (!printer.connect()) {
            Serial.println("[PORTAL] ERROR: Failed to connect to printer for setup ticket.");
            return;
        }
    }

    printer.init();
    printer.printDoubleLine();
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.setTextSize(2, 2);
    printer.println("PEN + PAPER PUZZLES");
    printer.setTextSize(1, 1);
    printer.setBold(false);
    printer.printDoubleLine();
    printer.println("");

    // Welcome intro
    printer.setAlign(ALIGN_CENTER);
    printer.println("These are the games that are currently");
    printer.println("active to print:");
    printer.println("");

    if (config) {
        // Categorize active games
        OfflinePuzzleType activeGames[OFFLINE_PUZZLE_TOTAL];
        uint8_t activeCount = 0;

        for (uint8_t i = 0; i < (uint8_t)OFFLINE_PUZZLE_TOTAL; i++) {
            if (config->isGameEnabled((OfflinePuzzleType)i)) {
                activeGames[activeCount++] = (OfflinePuzzleType)i;
            }
        }

        // Two-column active games list in newspaper order (24 cols left, 24 cols right)
        printer.setAlign(ALIGN_LEFT);
        uint8_t rows = (activeCount + 1) / 2;
        if (rows == 0) {
            rows = 1;
        }

        for (uint8_t r = 0; r < rows; r++) {
            String leftCol = "";
            if (r < activeCount) {
                leftCol = String(" * ") + config->getPuzzleName(activeGames[r]);
            } else if (activeCount == 0 && r == 0) {
                leftCol = "  (None)";
            }
            while (leftCol.length() < 24) {
                leftCol += ' ';
            }

            String rightCol = "";
            uint8_t rightIdx = r + rows;
            if (rightIdx < activeCount) {
                rightCol = String(" * ") + config->getPuzzleName(activeGames[rightIdx]);
            }

            printer.println(leftCol + rightCol);
        }

        // Current default settings summary
        printer.println("");
        printer.setAlign(ALIGN_LEFT);
        printer.printKeyValue("Daily Count:", String(config->getPuzzleCount()) + " Puzzles");
        printer.printKeyValue("Difficulty:", config->getGradeName(config->getPuzzleGrade()));
        if (!_timeSet) {
            printer.printKeyValue("Daily Schedule:", "(Setup instructions below)");
        } else {
            printer.printKeyValue("Daily Schedule:", config->getDailyScheduleTimeString());
        }
        printer.println("");
    }

    // Setup Mode Section
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- SETUP MODE ---");
    printer.setBold(false);
    printer.println("To customize your games, schedule, or clock,");
    printer.println("follow the instructions below:");
    printer.println("");

    // Step 1: Wi-Fi
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- STEP 1: JOIN WI-FI ---");
    printer.setBold(false);
    printer.println("Scan the QR code below to");
    printer.println("connect to the setup hotspot:");
    printer.println("");

    ThermalCanvas canvas;
    if (canvas.begin(240)) {
        canvas.clear(0);
        canvas.drawQrCode(288, 120, "WIFI:T:nopass;S:Pen-And-Paper-Puzzles;;", 6);
        canvas.printTo(printer);
        canvas.end();
    }
    printer.setAlign(ALIGN_CENTER);
    printer.println("Network: Pen-And-Paper-Puzzles");
    printer.println("(Open Network - No Password)");
    printer.println("");

    // Step 2: Settings URL
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- STEP 2: OPEN SETTINGS ---");
    printer.setBold(false);
    printer.println("Scan the QR code to set up your games:");
    printer.println("");

    if (canvas.begin(216)) {
        canvas.clear(0);
        canvas.drawQrCode(288, 108, "http://192.168.4.1", 6);
        canvas.printTo(printer);
        canvas.end();
    }
    printer.setAlign(ALIGN_CENTER);
    printer.println("URL: http://192.168.4.1");
    printer.println("");

    // Step 3: Customize & Save
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- STEP 3: CUSTOMIZE & SAVE ---");
    printer.setBold(false);
    printer.println("Customize your game selection and schedule:");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);
    printer.println("      * Select which games to get");
    printer.println("      * How many games to print");
    printer.println("      * Choose your difficulty level");
    printer.println("      * Set if you want daily prints");
    printer.println("");

    // Save Instruction & Notices
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("Click Save to apply your settings.");
    printer.setBold(false);
    printer.println("");

    // Footer
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.println("Enjoy your day!");
    printer.println("");
    printer.println("For more puzzles, toggle the power");
    printer.println("on the front of the printer.");
    printer.println("");
    printer.println("To change settings, toggle the power");
    printer.println("on the cable behind the printer.");
    if (!config || !config->isDailyScheduleEnabled()) {
        printer.println("");
        printer.println("To schedule daily puzzles, go to settings.");
    }
    printer.printHorizontalLine('-');

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();
    Serial.println("[PORTAL] Printed setup ticket with dual QR codes!");
}

void OfflineTimeManager::printConfigSavedTicket(EscPosPrinter& printer, const OfflineConfigManager& config) {
    if (!printer.isConnected()) {
        if (!printer.connect()) {
            Serial.println("[PORTAL] ERROR: Failed to connect to printer for config saved ticket.");
            return;
        }
    }

    printer.init();
    printer.printDoubleLine();
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.setTextSize(2, 2);
    printer.println("PEN + PAPER PUZZLES");
    printer.setTextSize(1, 1);
    printer.setBold(false);
    printer.println("Configuration Saved");
    printer.printDoubleLine();
    printer.println("");

    // Categorize active and inactive games
    OfflinePuzzleType activeGames[OFFLINE_PUZZLE_TOTAL];
    uint8_t activeCount = 0;
    OfflinePuzzleType inactiveGames[OFFLINE_PUZZLE_TOTAL];
    uint8_t inactiveCount = 0;

    for (uint8_t i = 0; i < (uint8_t)OFFLINE_PUZZLE_TOTAL; i++) {
        if (config.isGameEnabled((OfflinePuzzleType)i)) {
            activeGames[activeCount++] = (OfflinePuzzleType)i;
        } else {
            inactiveGames[inactiveCount++] = (OfflinePuzzleType)i;
        }
    }

    // Two-column game list (24 cols left, 24 cols right)
    printer.setAlign(ALIGN_LEFT);
    String leftHdr = String("ACTIVE (") + activeCount + ")";
    while (leftHdr.length() < 24) {
        leftHdr += ' ';
    }
    String rightHdr = String("INACTIVE (") + inactiveCount + ")";
    printer.setBold(true);
    printer.println(leftHdr + rightHdr);
    printer.setBold(false);

    uint8_t maxRows = (activeCount > inactiveCount) ? activeCount : inactiveCount;
    if (maxRows == 0) {
        maxRows = 1;
    }

    for (uint8_t row = 0; row < maxRows; row++) {
        String leftCol = "";
        if (row < activeCount) {
            leftCol = String(" * ") + config.getPuzzleName(activeGames[row]);
        } else if (activeCount == 0 && row == 0) {
            leftCol = "  (None)";
        }
        while (leftCol.length() < 24) {
            leftCol += ' ';
        }

        String rightCol = "";
        if (row < inactiveCount) {
            rightCol = String(" * ") + config.getPuzzleName(inactiveGames[row]);
        } else if (inactiveCount == 0 && row == 0) {
            rightCol = "  (None)";
        }

        printer.println(leftCol + rightCol);
    }

    // Settings Section with Standard Separator
    printer.println("");
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- SETTINGS ---");
    printer.setBold(false);
    printer.println("");

    printer.setAlign(ALIGN_LEFT);
    printer.printKeyValue("Daily Count:", String(config.getPuzzleCount()) + " Puzzles");
    printer.printKeyValue("Difficulty:", config.getGradeName(config.getPuzzleGrade()));
    printer.printKeyValue("Daily Schedule:", config.getDailyScheduleTimeString());
    printer.printKeyValue("Clock:", getFormattedTime("%I:%M %p"));

    // Footer
    printer.println("");
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.println("Setup complete. Ready for printing!");
    printer.println("");
    printer.println("For more puzzles, toggle the power");
    printer.println("on the front of the printer.");
    printer.println("");
    printer.println("To change settings, toggle the power");
    printer.println("on the cable behind the printer.");
    if (!config.isDailyScheduleEnabled()) {
        printer.println("");
        printer.println("To schedule daily puzzles, go to settings.");
    }
    printer.printHorizontalLine('-');

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();
    Serial.println("[PORTAL] Printed configuration saved confirmation ticket!");
}

#include "PortalHtml.h"

void OfflineTimeManager::setupWebRoutes() {
    _server.on("/", HTTP_GET, [this]() {
        _server.sendHeader("Content-Encoding", "gzip");
        _server.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
        _server.send_P(200, "text/html", (const char*)PORTAL_HTML_GZ, sizeof(PORTAL_HTML_GZ));
    });

    _server.on("/api/config", HTTP_GET, [this]() {
        uint32_t mask = _configManager ? _configManager->getGameMask() : 0x3FFFF;
        uint8_t count = _configManager ? _configManager->getPuzzleCount() : 5;
        uint8_t grade = _configManager ? (uint8_t)_configManager->getPuzzleGrade() : 3;
        bool schedEn = _configManager ? _configManager->isDailyScheduleEnabled() : true;
        uint8_t schedHr = _configManager ? _configManager->getDailyScheduleHour() : 7;
        uint8_t schedMin = _configManager ? _configManager->getDailyScheduleMinute() : 0;
        String json = "{\"mask\":" + String(mask) +
                      ",\"count\":" + String(count) +
                      ",\"grade\":" + String(grade) +
                      ",\"schedEnabled\":" + (schedEn ? "true" : "false") +
                      ",\"schedHour\":" + String(schedHr) +
                      ",\"schedMinute\":" + String(schedMin) +
                      ",\"time\":\"" + getFormattedTime("%I:%M %p") + "\"" +
                      ",\"timeSet\":" + (_timeSet ? "true" : "false") + "}";
        _server.send(200, "application/json", json);
    });

    _server.on("/api/save-config", HTTP_GET, [this]() {
        if (_server.hasArg("mask") && _server.hasArg("count") && _server.hasArg("grade")) {
            uint32_t mask = (uint32_t)strtoul(_server.arg("mask").c_str(), NULL, 10);
            uint8_t count = (uint8_t)_server.arg("count").toInt();
            uint8_t grade = (uint8_t)_server.arg("grade").toInt();

            // Automatically sync device clock from client device local time
            if (_server.hasArg("year") && _server.hasArg("hour")) {
                int y  = _server.arg("year").toInt();
                int mo = _server.hasArg("month") ? _server.arg("month").toInt() : 1;
                int d  = _server.hasArg("day") ? _server.arg("day").toInt() : 1;
                int h  = _server.arg("hour").toInt();
                int mi = _server.hasArg("min") ? _server.arg("min").toInt() : 0;
                int s  = _server.hasArg("sec") ? _server.arg("sec").toInt() : 0;
                setSystemTime(y, mo, d, h, mi, s);
            } else if (_server.hasArg("epoch")) {
                long epoch = (long)strtoul(_server.arg("epoch").c_str(), NULL, 10);
                int tzOffset = _server.hasArg("tz") ? _server.arg("tz").toInt() : 0;
                setSystemTime(epoch, tzOffset);
            }

            if (_configManager) {
                _configManager->setGameMask(mask);
                _configManager->setPuzzleCount(count);
                _configManager->setPuzzleGrade((PuzzleGrade)grade);

                if (_server.hasArg("schedEnabled")) {
                    bool schedEn = (_server.arg("schedEnabled") == "1" || _server.arg("schedEnabled") == "true");
                    _configManager->setDailyScheduleEnabled(schedEn);
                }
                if (_server.hasArg("schedHour")) {
                    uint8_t schedHr = (uint8_t)_server.arg("schedHour").toInt();
                    _configManager->setDailyScheduleHour(schedHr);
                }
                if (_server.hasArg("schedMinute")) {
                    uint8_t schedMin = (uint8_t)_server.arg("schedMinute").toInt();
                    _configManager->setDailyScheduleMinute(schedMin);
                }

                _configManager->save();
                Serial.printf("[PORTAL] Saved configuration: Mask=0x%04X, Count=%d, Grade=%d, Schedule=%s\n",
                              mask, count, grade, _configManager->getDailyScheduleTimeString().c_str());

                if (_printer) {
                    printConfigSavedTicket(*_printer, *_configManager);
                }
            }

            _server.send(200, "application/json", "{\"status\":\"ok\"}");
            _pendingExit = true;
            _pendingExitMs = millis();
        } else {
            _server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing parameters\"}");
        }
    });

    _server.on("/api/set-time", HTTP_GET, [this]() {
        if (_server.hasArg("year") && _server.hasArg("hour")) {
            int y  = _server.arg("year").toInt();
            int mo = _server.hasArg("month") ? _server.arg("month").toInt() : 1;
            int d  = _server.hasArg("day") ? _server.arg("day").toInt() : 1;
            int h  = _server.arg("hour").toInt();
            int mi = _server.hasArg("min") ? _server.arg("min").toInt() : 0;
            int s  = _server.hasArg("sec") ? _server.arg("sec").toInt() : 0;
            setSystemTime(y, mo, d, h, mi, s);

            String json = "{\"status\":\"ok\",\"time\":\"" + getFormattedTime("%I:%M %p") + "\"}";
            _server.send(200, "application/json", json);
        } else if (_server.hasArg("epoch")) {
            long epoch = (long)strtoul(_server.arg("epoch").c_str(), NULL, 10);
            int tzOffset = _server.hasArg("tz") ? _server.arg("tz").toInt() : 0;
            setSystemTime(epoch, tzOffset);

            String json = "{\"status\":\"ok\",\"time\":\"" + getFormattedTime("%I:%M %p") + "\"}";
            _server.send(200, "application/json", json);
        } else {
            _server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing time parameters\"}");
        }
    });

    _server.on("/api/status", HTTP_GET, [this]() {
        String json = "{\"timeSet\":" + String(_timeSet ? "true" : "false") +
                      ",\"time\":\"" + getFormattedTime() + "\"}";
        _server.send(200, "application/json", json);
    });

    _server.on("/api/print-guide", HTTP_GET, [this]() {
        if (_server.hasArg("game")) {
            uint8_t gameId = (uint8_t)_server.arg("game").toInt();
            if (_printer) {
                OfflinePuzzleComposer composer;
                bool success = composer.printGameGuide(*_printer, gameId);
                if (success) {
                    _server.send(200, "application/json", "{\"status\":\"ok\",\"game\":" + String(gameId) + "}");
                    return;
                }
            }
            _server.send(500, "application/json", "{\"status\":\"error\",\"message\":\"Printing failed\"}");
        } else {
            _server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing game parameter\"}");
        }
    });

    _server.on("/api/exit", HTTP_GET, [this]() {
        _server.send(200, "text/html", "<body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:30px;text-align:center;'><h2>Setup portal closing.</h2><p>Ready for morning puzzles!</p></body>");
        _pendingExit = true;
        _pendingExitMs = millis();
    });

    // Captive portal handler for mobile redirect
    _server.onNotFound([this]() {
        _server.sendHeader("Location", "http://192.168.4.1/", true);
        _server.send(302, "text/plain", "");
    });
}


