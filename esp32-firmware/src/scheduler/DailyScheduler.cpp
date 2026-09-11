#include "DailyScheduler.h"

DailyScheduler::DailyScheduler() :
    _lastPrintedYear(-1),
    _lastPrintedDayOfYear(-1),
    _timeSynced(false),
    _lastNtpCheckMs(0),
    _lastButtonPressMs(0),
    _lastButtonState(HIGH) {
}

void DailyScheduler::begin() {
    pinMode(BUTTON_TRIGGER_PIN, INPUT_PULLUP);

    Serial.println("[SCHEDULER] Configuring NTP Time with timezone...");
    // configTzTime is an ESP-IDF / Arduino function that applies POSIX TZ rules
    configTzTime(TIMEZONE_SPEC, NTP_SERVER_PRIMARY, NTP_SERVER_BACKUP);
    
    syncNtp();
}

bool DailyScheduler::syncNtp() {
    struct tm timeinfo;
    if (getLocalTime(&timeinfo, 5000)) { // 5s timeout
        _timeSynced = true;
        char buffer[64];
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);
        Serial.printf("[SCHEDULER] NTP Synchronized! Current local time: %s\n", buffer);
        return true;
    }

    Serial.println("[SCHEDULER] WARNING: NTP sync timed out. Will retry in background.");
    _timeSynced = false;
    return false;
}

bool DailyScheduler::isTimeSynced() {
    return _timeSynced;
}

String DailyScheduler::getFormattedTime(const char* format) {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo, 100)) {
        return "Time Not Set";
    }
    char buffer[64];
    strftime(buffer, sizeof(buffer), format, &timeinfo);
    return String(buffer);
}

bool DailyScheduler::shouldTriggerDailyPrint() {
    // Re-check NTP periodically if not yet synced
    if (!_timeSynced) {
        if (millis() - _lastNtpCheckMs > 30000) { // Every 30s
            _lastNtpCheckMs = millis();
            syncNtp();
        }
        return false;
    }

    struct tm timeinfo;
    if (!getLocalTime(&timeinfo, 100)) {
        return false;
    }

    // Check if we hit the target hour & minute
    if (timeinfo.tm_hour == DAILY_PRINT_HOUR && timeinfo.tm_min == DAILY_PRINT_MINUTE) {
        // Check if we already printed today
        if (timeinfo.tm_year != _lastPrintedYear || timeinfo.tm_yday != _lastPrintedDayOfYear) {
            Serial.printf("[SCHEDULER] Cron Trigger! Target time reached: %02d:%02d\n", 
                          DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
            markPrintedToday();
            return true;
        }
    }

    return false;
}

bool DailyScheduler::checkManualButtonTrigger() {
    int currentState = digitalRead(BUTTON_TRIGGER_PIN);
    unsigned long now = millis();

    // Active LOW button with 300ms debounce
    if (currentState == LOW && _lastButtonState == HIGH) {
        if (now - _lastButtonPressMs > 300) {
            _lastButtonPressMs = now;
            _lastButtonState = currentState;
            Serial.println("[SCHEDULER] Manual push button trigger detected!");
            return true;
        }
    }
    _lastButtonState = currentState;
    return false;
}

void DailyScheduler::markPrintedToday() {
    struct tm timeinfo;
    if (getLocalTime(&timeinfo, 100)) {
        _lastPrintedYear = timeinfo.tm_year;
        _lastPrintedDayOfYear = timeinfo.tm_yday;
        Serial.printf("[SCHEDULER] Marked day %d (%d) as printed.\n", _lastPrintedDayOfYear, _lastPrintedYear + 1900);
    }
}
