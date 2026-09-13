#include "OfflineTimeManager.h"

OfflineTimeManager::OfflineTimeManager() :
    _timeSet(false),
    _lastPrintedYear(-1),
    _lastPrintedDay(-1),
    _portalActive(false),
    _ds3231Present(false),
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
    WiFi.softAP("Morning-Puzzles-Setup", "puzzles123");
    IPAddress myIP = WiFi.softAPIP();
    Serial.printf("[PORTAL] Hotspot started! SSID: Morning-Puzzles-Setup\n");
    Serial.printf("[PORTAL] Connect phone and visit: http://%s\n", myIP.toString().c_str());

    // Captive portal DNS server (redirect all domains to 192.168.4.1)
    _dnsServer.start(53, "*", myIP);

    setupWebRoutes();
    _server.begin();
    _portalActive = true;
}

void OfflineTimeManager::stopSetupPortal() {
    if (_portalActive) {
        _server.stop();
        _dnsServer.stop();
        WiFi.softAPdisconnect(true);
        _portalActive = false;
        Serial.println("[PORTAL] SoftAP Setup Portal closed.");
    }
}

void OfflineTimeManager::handleClient() {
    if (_portalActive) {
        _dnsServer.processNextRequest();
        _server.handleClient();
    }
}

void OfflineTimeManager::setupWebRoutes() {
    _server.on("/", HTTP_GET, [this]() {
        _server.send(200, "text/html", buildWebPageHtml());
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
        _server.send(200, "text/html", "<h2>Setup portal closing. Ready for morning puzzles!</h2>");
        delay(500);
        stopSetupPortal();
    });

    // Captive portal handler for mobile redirect
    _server.onNotFound([this]() {
        _server.sendHeader("Location", "http://192.168.4.1/", true);
        _server.send(302, "text/plain", "");
    });
}

String OfflineTimeManager::buildWebPageHtml() {
    String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morning Puzzles Setup</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: #121212; color: #f0f0f0; padding: 20px; text-align: center; }
        .card { background: #1e1e1e; border-radius: 12px; padding: 24px; max-width: 420px; 
                margin: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        h1 { font-size: 1.6rem; color: #ffb74d; margin-bottom: 8px; }
        p { color: #aaa; font-size: 0.95rem; }
        .btn { background: #ff9800; color: #121212; border: none; padding: 14px 24px; 
               border-radius: 8px; font-weight: bold; font-size: 1rem; cursor: pointer; 
               width: 100%; margin: 12px 0; transition: background 0.2s; }
        .btn:hover { background: #ffa726; }
        .btn-sec { background: #333; color: #fff; }
        .status-box { background: #2a2a2a; border-radius: 8px; padding: 12px; margin: 16px 0; font-size: 1.1rem; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; }
        .badge-green { background: #2e7d32; color: white; }
        .badge-orange { background: #ef6c00; color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Morning Puzzles</h1>
        <p>Offline Time & Schedule Configurator</p>
        
        <div class="status-box">
            <div>Current ESP32 Time:</div>
            <strong id="espTime">)rawliteral";

    html += getFormattedTime();

    html += R"rawliteral(</strong>
        </div>

        <button class="btn" onclick="syncFromPhone()">Sync Time from This Phone</button>
        <button class="btn btn-sec" onclick="window.location.href='/api/exit'">Save & Exit Setup</button>
        
        <p id="msg" style="color: #4caf50; font-weight: bold;"></p>
    </div>

    <script>
        function syncFromPhone() {
            const now = new Date();
            const epoch = Math.floor(now.getTime() / 1000);
            const tz = now.getTimezoneOffset();
            document.getElementById('msg').innerText = 'Syncing...';

            fetch('/api/set-time?epoch=' + epoch + '&tz=' + tz)
                .then(r => r.json())
                .then(d => {
                    document.getElementById('espTime').innerText = d.time;
                    document.getElementById('msg').innerText = '✓ Time synchronized successfully!';
                })
                .catch(e => {
                    document.getElementById('msg').innerText = 'Error syncing time.';
                });
        }
    </script>
</body>
</html>
)rawliteral";
    return html;
}
