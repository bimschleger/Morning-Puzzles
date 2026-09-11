#ifndef DAILY_SCHEDULER_H
#define DAILY_SCHEDULER_H

#include <Arduino.h>
#include <time.h>
#include "config.h"

class DailyScheduler {
public:
    DailyScheduler();

    void begin();
    bool isTimeSynced();
    String getFormattedTime(const char* format = "%Y-%m-%d %H:%M:%S");
    
    // Checks if the scheduled daily cron time has arrived
    bool shouldTriggerDailyPrint();

    // Checks if user pressed the physical button (e.g. BOOT button / GPIO 0)
    bool checkManualButtonTrigger();

    // Force mark today as completed
    void markPrintedToday();

private:
    int _lastPrintedYear;
    int _lastPrintedDayOfYear;
    bool _timeSynced;
    unsigned long _lastNtpCheckMs;
    unsigned long _lastButtonPressMs;
    bool _lastButtonState;

    bool syncNtp();
};

#endif // DAILY_SCHEDULER_H
