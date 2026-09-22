#ifndef OFFLINE_TIME_MANAGER_H
#define OFFLINE_TIME_MANAGER_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <time.h>
#include <sys/time.h>
#include <Wire.h>
#include "config.h"

// Forward declarations
class EscPosPrinter;
class OfflineConfigManager;

class OfflineTimeManager {
public:
    OfflineTimeManager();

    void begin();
    void setConfigManager(OfflineConfigManager* config) { _configManager = config; }
    void setPrinter(EscPosPrinter* printer) { _printer = printer; }
    
    // Time status & inspection
    bool isTimeSet() const { return _timeSet; }
    String getFormattedTime(const char* format = "%Y-%m-%d %H:%M:%S");
    bool isCronTriggerTime(uint8_t targetHour = 7, uint8_t targetMinute = 0);
    void markPrintedToday();

    // SoftAP Web Setup
    void startSetupPortal();
    void stopSetupPortal();
    bool isPortalActive() const { return _portalActive; }
    void handleClient(); // Call in loop() when portal is active

    // Thermal Tickets
    void printSetupTicket(EscPosPrinter& printer, const OfflineConfigManager* config = nullptr);
    void printConfigSavedTicket(EscPosPrinter& printer, const OfflineConfigManager& config);

    // Direct Time Setter (Unix epoch seconds)
    void setSystemTime(time_t epoch, int tzOffsetMinutes = 0);

    // Optional DS3231 Hardware RTC
    bool isDs3231Present() const { return _ds3231Present; }
    bool checkAndSyncFromDs3231();
    bool writeToDs3231(const struct tm& t);

private:
    bool _timeSet;
    int _lastPrintedYear;
    int _lastPrintedDay;
    bool _portalActive;
    bool _ds3231Present;
    unsigned long _portalStartedMs;
    bool _pendingExit;
    unsigned long _pendingExitMs;

    OfflineConfigManager* _configManager;
    EscPosPrinter*        _printer;

    WebServer _server;
    DNSServer _dnsServer;

    void setupWebRoutes();

    // I2C DS3231 Helpers (Address 0x68)
    static const uint8_t DS3231_I2C_ADDR = 0x68;
    uint8_t bcdToDec(uint8_t val);
    uint8_t decToBcd(uint8_t val);
};

#endif // OFFLINE_TIME_MANAGER_H
