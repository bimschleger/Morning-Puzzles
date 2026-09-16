#include "OfflineTimeManager.h"
#include "../config/OfflineConfigManager.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

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
    struct timeval tv = { epoch, 0 };
    settimeofday(&tv, nullptr);
    _timeSet = true;

    time_t now = time(nullptr);
    struct tm* t = localtime(&now);

    Serial.printf("[TIME] System clock set to: %04d-%02d-%02d %02d:%02d:%02d (TZ Offset: %d min)\n",
                  t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
                  t->tm_hour, t->tm_min, t->tm_sec, tzOffsetMinutes);

    if (_ds3231Present) {
        writeToDs3231(*t);
        Serial.println("[TIME] Persisted new time to DS3231 hardware RTC.");
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
    WiFi.softAP("Morning-Puzzles-Setup"); // Open network (zero password)
    IPAddress myIP = WiFi.softAPIP();
    Serial.printf("[PORTAL] Hotspot started! SSID: Morning-Puzzles-Setup (Open Network)\n");
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

void OfflineTimeManager::printSetupTicket(EscPosPrinter& printer) {
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
    printer.println("SETUP MODE");
    printer.setTextSize(1, 1);
    printer.setBold(false);
    printer.printDoubleLine();
    printer.println("");

    // Step 1: Wi-Fi
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("[ STEP 1: SCAN TO JOIN WI-FI ]");
    printer.setBold(false);

    ThermalCanvas canvas;
    if (canvas.begin(224)) {
        canvas.clear(0);
        canvas.drawQrCode(288, 112, "WIFI:S:Morning-Puzzles-Setup;T:nopass;;", 6);
        canvas.printTo(printer);
        canvas.end();
    }
    printer.setAlign(ALIGN_CENTER);
    printer.println("Network: Morning-Puzzles-Setup");
    printer.println("(Open Network - No Password)");
    printer.println("");

    // Step 2: Settings URL
    printer.setBold(true);
    printer.println("[ STEP 2: SCAN TO OPEN SETTINGS ]");
    printer.setBold(false);

    if (canvas.begin(192)) {
        canvas.clear(0);
        canvas.drawQrCode(288, 96, "http://192.168.4.1", 6);
        canvas.printTo(printer);
        canvas.end();
    }
    printer.setAlign(ALIGN_CENTER);
    printer.println("URL: http://192.168.4.1");
    printer.println("");
    printer.println("(Hotspot auto-closes after 5 minutes)");
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
    printer.println("CONFIGURATION SAVED");
    printer.setTextSize(1, 1);
    printer.setBold(false);
    printer.printDoubleLine();
    printer.println("");

    printer.setAlign(ALIGN_LEFT);
    uint8_t enabledCount = config.getEnabledGameCount();
    printer.println(String("Active Games (") + enabledCount + " of 13):");
    for (uint8_t i = 0; i < (uint8_t)OFFLINE_PUZZLE_TOTAL; i++) {
        if (config.isGameEnabled((OfflinePuzzleType)i)) {
            printer.println(String("  * ") + config.getPuzzleName((OfflinePuzzleType)i));
        }
    }
    printer.println("");
    printer.printKeyValue("Print Count:", String(config.getPuzzleCount()) + " Puzzles");
    printer.printKeyValue("Difficulty:", config.getGradeName(config.getPuzzleGrade()));
    printer.printKeyValue("Clock:", getFormattedTime());
    printer.println("");
    printer.printHorizontalLine('-');
    printer.setAlign(ALIGN_CENTER);
    printer.println("Setup complete. Ready for printing!");
    printer.printHorizontalLine('-');

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();
    Serial.println("[PORTAL] Printed configuration saved confirmation ticket!");
}

void OfflineTimeManager::setupWebRoutes() {
    _server.on("/", HTTP_GET, [this]() {
        _server.send(200, "text/html", buildWebPageHtml());
    });

    _server.on("/api/config", HTTP_GET, [this]() {
        uint16_t mask = _configManager ? _configManager->getGameMask() : 0x1FFF;
        uint8_t count = _configManager ? _configManager->getPuzzleCount() : 5;
        uint8_t grade = _configManager ? (uint8_t)_configManager->getPuzzleGrade() : 3;
        String json = "{\"mask\":" + String(mask) +
                      ",\"count\":" + String(count) +
                      ",\"grade\":" + String(grade) +
                      ",\"time\":\"" + getFormattedTime() + "\"" +
                      ",\"timeSet\":" + (_timeSet ? "true" : "false") + "}";
        _server.send(200, "application/json", json);
    });

    _server.on("/api/save-config", HTTP_GET, [this]() {
        if (_server.hasArg("mask") && _server.hasArg("count") && _server.hasArg("grade")) {
            uint16_t mask = (uint16_t)_server.arg("mask").toInt();
            uint8_t count = (uint8_t)_server.arg("count").toInt();
            uint8_t grade = (uint8_t)_server.arg("grade").toInt();

            if (_configManager) {
                _configManager->setGameMask(mask);
                _configManager->setPuzzleCount(count);
                _configManager->setPuzzleGrade((PuzzleGrade)grade);
                _configManager->save();
                Serial.printf("[PORTAL] Saved configuration: Mask=0x%04X, Count=%d, Grade=%d\n", mask, count, grade);

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
        if (_server.hasArg("epoch")) {
            long epoch = _server.arg("epoch").toInt();
            int tzOffset = _server.hasArg("tz") ? _server.arg("tz").toInt() : 0;
            setSystemTime(epoch, tzOffset);

            String json = "{\"status\":\"ok\",\"time\":\"" + getFormattedTime() + "\"}";
            _server.send(200, "application/json", json);
        } else {
            _server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing epoch\"}");
        }
    });

    _server.on("/api/status", HTTP_GET, [this]() {
        String json = "{\"timeSet\":" + String(_timeSet ? "true" : "false") +
                      ",\"time\":\"" + getFormattedTime() + "\"}";
        _server.send(200, "application/json", json);
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

String OfflineTimeManager::buildWebPageHtml() {
    String html = R"rawliteral(<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Morning Puzzles Setup</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  body {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    padding: 16px;
    display: flex;
    justify-content: center;
  }
  .app-container {
    width: 100%;
    max-width: 460px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding-bottom: 24px;
  }
  .header {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }
  .header-icon {
    background: #f59e0b;
    color: #020617;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: bold;
    flex-shrink: 0;
  }
  .header-title { font-size: 1.25rem; font-weight: 700; color: #f8fafc; }
  .badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.12);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 9999px;
    margin-top: 3px;
  }
  .card {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f1f5f9;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .card-subtitle {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-bottom: 12px;
  }

  /* Count Stepper */
  .stepper-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin: 8px 0;
  }
  .btn-step {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: #1e293b;
    border: 1px solid #334155;
    color: #f8fafc;
    font-size: 1.5rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.15s;
  }
  .btn-step:active { background: #334155; transform: scale(0.96); }
  .count-display {
    font-size: 2.4rem;
    font-weight: 800;
    color: #f59e0b;
    min-width: 60px;
    text-align: center;
  }

  /* Difficulty Selector */
  .diff-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }
  .diff-option {
    border: 1px solid #1e293b;
    background: #0f172a;
    border-radius: 12px;
    padding: 12px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: border 0.15s, background 0.15s;
  }
  .diff-option.active {
    border-color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
  }
  .diff-name { font-weight: 600; font-size: 0.9rem; color: #f8fafc; }
  .diff-desc { font-size: 0.75rem; color: #94a3b8; }
  .diff-radio {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid #475569;
    position: relative;
    flex-shrink: 0;
  }
  .diff-option.active .diff-radio {
    border-color: #f59e0b;
    background: #f59e0b;
  }

  /* Game Selection List */
  .quick-actions {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
  }
  .btn-quick {
    font-size: 0.75rem;
    font-weight: 600;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.25);
    padding: 4px 10px;
    border-radius: 8px;
    cursor: pointer;
  }
  .games-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .game-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.15s;
  }
  .game-row.active {
    border-color: rgba(245, 158, 11, 0.4);
  }
  .game-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .game-title { font-weight: 600; font-size: 0.9rem; color: #f1f5f9; }
  .game-tag {
    font-size: 0.7rem;
    color: #64748b;
  }
  .custom-checkbox {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #475569;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.15s;
  }
  .game-row.active .custom-checkbox {
    background: #f59e0b;
    border-color: #f59e0b;
  }
  .custom-checkbox::after {
    content: "";
    width: 6px;
    height: 10px;
    border: solid #020617;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
    display: none;
    margin-bottom: 2px;
  }
  .game-row.active .custom-checkbox::after {
    display: block;
  }

  /* Time Sync Card */
  .time-status {
    font-family: monospace;
    font-size: 0.95rem;
    color: #fbbf24;
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 10px;
    text-align: center;
  }
  .btn-sec {
    width: 100%;
    background: #1e293b;
    border: 1px solid #334155;
    color: #f8fafc;
    padding: 12px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
  }
  .btn-sec:active { background: #334155; }

  /* Save & Exit Button */
  .btn-primary {
    width: 100%;
    background: #f59e0b;
    color: #020617;
    border: none;
    padding: 16px;
    border-radius: 14px;
    font-size: 1.05rem;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    transition: transform 0.1s, background 0.15s;
  }
  .btn-primary:active { transform: scale(0.98); background: #d97706; }

  /* Toast Notification */
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #22c55e;
    color: #020617;
    font-weight: 700;
    padding: 12px 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    display: none;
    z-index: 100;
    text-align: center;
    max-width: 90%;
  }
</style>
</head>
<body>
<div class="app-container">
  
  <!-- Header -->
  <div class="header">
    <div class="header-icon">&#128240;</div>
    <div>
      <div class="header-title">Morning Puzzles</div>
      <span class="badge">Appliance Configurator</span>
    </div>
  </div>

  <!-- Daily Puzzle Count -->
  <div class="card">
    <div class="card-header">
      <div class="card-title">&#128221; Daily Print Count</div>
      <div id="countSub" style="font-size:0.8rem; color:#94a3b8;">Max: 13</div>
    </div>
    <div class="card-subtitle">Number of games to randomly draw and print per daily mix receipt.</div>
    <div class="stepper-row">
      <button class="btn-step" onclick="changeCount(-1)">-</button>
      <div class="count-display" id="countDisplay">5</div>
      <button class="btn-step" onclick="changeCount(1)">+</button>
    </div>
  </div>

  <!-- Difficulty Setting -->
  <div class="card">
    <div class="card-title">&#9878; Receipt Difficulty</div>
    <div class="card-subtitle">Select progression curve or uniform difficulty for all selected puzzles.</div>
    <div class="diff-grid">
      <div class="diff-option active" id="diff-opt-3" onclick="setDiff(3)">
        <div>
          <div class="diff-name">Escalating (Easy &rarr; Hard)</div>
          <div class="diff-desc">Starts easy, scales progressively, ending with hard/extreme</div>
        </div>
        <div class="diff-radio"></div>
      </div>
      <div class="diff-option" id="diff-opt-0" onclick="setDiff(0)">
        <div>
          <div class="diff-name">Easy</div>
          <div class="diff-desc">All selected games generated at Easy difficulty</div>
        </div>
        <div class="diff-radio"></div>
      </div>
      <div class="diff-option" id="diff-opt-1" onclick="setDiff(1)">
        <div>
          <div class="diff-name">Medium</div>
          <div class="diff-desc">All selected games generated at Medium difficulty</div>
        </div>
        <div class="diff-radio"></div>
      </div>
      <div class="diff-option" id="diff-opt-2" onclick="setDiff(2)">
        <div>
          <div class="diff-name">Hard</div>
          <div class="diff-desc">All selected games generated at Hard difficulty</div>
        </div>
        <div class="diff-radio"></div>
      </div>
    </div>
  </div>

  <!-- Game Pool Checkboxes -->
  <div class="card">
    <div class="card-header">
      <div class="card-title">&#127918; Eligible Games (<span id="enabledNum">13</span>/13)</div>
      <div class="quick-actions">
        <button class="btn-quick" onclick="selectAllGames(true)">All</button>
        <button class="btn-quick" onclick="selectAllGames(false)">None</button>
      </div>
    </div>
    <div class="card-subtitle">Uncheck games to disable them from the daily receipt draw.</div>
    <div class="games-list" id="gamesList"></div>
  </div>

  <!-- Time Sync -->
  <div class="card">
    <div class="card-title">&#128337; Clock Synchronization</div>
    <div class="time-status" id="espClock">Loading time...</div>
    <button class="btn-sec" onclick="syncClock()">Sync Clock from This Device</button>
  </div>

  <!-- Save Button -->
  <button class="btn-primary" onclick="saveAndExit()">Save Settings & Exit Setup</button>

</div>

<div class="toast" id="toast">Settings Saved! Printing confirmation ticket...</div>

<script>
const GAMES = [
  { id: 0,  name: "Sudoku",          cat: "Number Placement" },
  { id: 1,  name: "Word Search",     cat: "Word Puzzle" },
  { id: 2,  name: "Nonogram",        cat: "Picture Logic" },
  { id: 3,  name: "Queens",          cat: "Grid Logic" },
  { id: 4,  name: "Daily Jumble",    cat: "Word Puzzle" },
  { id: 5,  name: "Binary Grid",     cat: "Binary Logic" },
  { id: 6,  name: "Minesweeper",     cat: "Deduction" },
  { id: 7,  name: "Tents & Trees",   cat: "Grid Logic" },
  { id: 8,  name: "Bridges",         cat: "Network Logic" },
  { id: 9,  name: "Tango",           cat: "Grid Logic" },
  { id: 10, name: "Word Wheel",      cat: "Word Puzzle" },
  { id: 11, name: "Lights Out",      cat: "Illumination" },
  { id: 12, name: "Numberlink Loop",  cat: "Path Puzzle" }
];

let currentMask = 0x1FFF;
let currentCount = 5;
let currentGrade = 3;

function renderGames() {
  const list = document.getElementById('gamesList');
  list.innerHTML = '';
  let enabledTotal = 0;

  GAMES.forEach(g => {
    const isChecked = (currentMask & (1 << g.id)) !== 0;
    if (isChecked) enabledTotal++;

    const row = document.createElement('div');
    row.className = 'game-row' + (isChecked ? ' active' : '');
    row.onclick = () => toggleGame(g.id);
    row.innerHTML = `
      <div class="game-left">
        <div class="custom-checkbox"></div>
        <div>
          <div class="game-title">${g.name}</div>
          <div class="game-tag">${g.cat}</div>
        </div>
      </div>
    `;
    list.appendChild(row);
  });

  document.getElementById('enabledNum').innerText = enabledTotal;
  document.getElementById('countSub').innerText = 'Max: ' + enabledTotal;
  if (currentCount > enabledTotal) currentCount = Math.max(1, enabledTotal);
  document.getElementById('countDisplay').innerText = currentCount;
}

function toggleGame(id) {
  const willDisable = (currentMask & (1 << id)) !== 0;
  let newMask = willDisable ? (currentMask & ~(1 << id)) : (currentMask | (1 << id));
  if ((newMask & 0x1FFF) === 0) return; // Prevent disabling all games
  currentMask = newMask;
  renderGames();
}

function selectAllGames(selectAll) {
  currentMask = selectAll ? 0x1FFF : 0x0001; // Keep at least Sudoku if none
  renderGames();
}

function changeCount(delta) {
  const maxAllowed = document.getElementById('enabledNum').innerText;
  let next = currentCount + delta;
  if (next < 1) next = 1;
  if (next > maxAllowed) next = maxAllowed;
  currentCount = next;
  document.getElementById('countDisplay').innerText = currentCount;
}

function setDiff(g) {
  currentGrade = g;
  [3, 0, 1, 2].forEach(id => {
    const el = document.getElementById('diff-opt-' + id);
    if (el) el.className = 'diff-option' + (id === g ? ' active' : '');
  });
}

function syncClock() {
  const now = new Date();
  const epoch = Math.floor(now.getTime() / 1000);
  const tz = now.getTimezoneOffset();
  fetch('/api/set-time?epoch=' + epoch + '&tz=' + tz)
    .then(r => r.json())
    .then(d => {
      document.getElementById('espClock').innerText = d.time;
      showToast('✓ Clock synced with phone!');
    });
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.innerText = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 3000);
}

function saveAndExit() {
  showToast('Saving settings & printing confirmation...');
  fetch(`/api/save-config?mask=${currentMask}&count=${currentCount}&grade=${currentGrade}`)
    .then(r => r.json())
    .then(d => {
      document.body.innerHTML = `
        <div style="max-width:420px;margin:50px auto;text-align:center;color:#f8fafc;padding:24px;background:#020617;border:1px solid #1e293b;border-radius:16px;">
          <h2 style="color:#22c55e;margin-bottom:12px;">&#10003; Configuration Saved!</h2>
          <p style="color:#94a3b8;margin-bottom:16px;">Your receipt printer is now printing your confirmation ticket.</p>
          <p style="color:#64748b;font-size:0.85rem;">The setup hotspot is shutting down. You can now close this browser tab.</p>
        </div>
      `;
    })
    .catch(e => {
      showToast('Error saving configuration.');
    });
}

// Initial fetch from device
fetch('/api/config')
  .then(r => r.json())
  .then(d => {
    currentMask = d.mask || 0x1FFF;
    currentCount = d.count || 5;
    currentGrade = (d.grade !== undefined) ? d.grade : 3;
    document.getElementById('espClock').innerText = d.time || 'Time Not Set';
    setDiff(currentGrade);
    renderGames();
  })
  .catch(() => {
    renderGames();
  });
</script>
</body>
</html>
)rawliteral";
    return html;
}
