#include <Arduino.h>
#include "config.h"
#include "printer/EscPosPrinter.h"
#include "time/OfflineTimeManager.h"
#include "config/OfflineConfigManager.h"
#include "generators/OfflinePuzzleComposer.h"

#if !OFFLINE_ONLY_BUILD
#include <WiFi.h>
#include "scheduler/DailyScheduler.h"
#include "net/PuzzleClient.h"
DailyScheduler         scheduler;
PuzzleClient           puzzleClient;
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
#include <WiFi.h>
#endif

// Hardware and engines
EscPosPrinter          printer;
OfflineTimeManager     timeManager;
OfflineConfigManager   configManager;
OfflinePuzzleComposer  offlineComposer;

// Button timing state
bool          lastBtnState = HIGH;
unsigned long btnPressStartMs = 0;

void blinkStatusLed(int count, int delayMs = 100) {
    for (int i = 0; i < count; i++) {
        digitalWrite(STATUS_LED_PIN, HIGH);
        delay(delayMs);
        digitalWrite(STATUS_LED_PIN, LOW);
        delay(delayMs);
    }
}

void executePrintJob(PuzzleGrade grade = (PuzzleGrade)-1) {
    uint8_t count = configManager.getPuzzleCount();
    PuzzleGrade activeGrade = (grade != (PuzzleGrade)-1) ? grade : configManager.getPuzzleGrade();

    Serial.println("\n========================================================");
    Serial.println(">>> STARTING MORNING PUZZLES 100% OFFLINE PRINT JOB <<<");
    Serial.printf(">>> Time: %s\n", timeManager.getFormattedTime().c_str());
    Serial.printf(">>> Format: %d-Puzzle Mix (%d of 13 games enabled)\n", count, configManager.getEnabledGameCount());
    Serial.printf(">>> Grade: %s\n", configManager.getGradeName(activeGrade));
    Serial.println("========================================================");

    digitalWrite(STATUS_LED_PIN, HIGH);

    // 100% Offline on-device generation from user-configured active games pool
    bool success = offlineComposer.generateAndPrintReceipt(
        printer, 
        "Enjoy your morning puzzles",
        grade,
        &configManager
    );

    digitalWrite(STATUS_LED_PIN, LOW);

    if (success) {
        Serial.println("[MAIN] Print job completed successfully!\n");
        blinkStatusLed(2, 200);
    } else {
        Serial.println("[MAIN] Print job failed. Please check printer connection/wiring.\n");
        blinkStatusLed(5, 60);
    }
}

void handleButtonPress() {
    int btnState = digitalRead(BUTTON_TRIGGER_PIN);
    unsigned long now = millis();

    // Button down
    if (btnState == LOW && lastBtnState == HIGH) {
        btnPressStartMs = now;
        delay(50); // debounce
    }
    // Button released
    else if (btnState == HIGH && lastBtnState == LOW) {
        unsigned long duration = now - btnPressStartMs;
        if (duration > 50) {
            // Instant On-Demand Print using active configuration
            Serial.println("[BTN] Hardware BOOT button pressed -> Generating & printing puzzle mix!");
            executePrintJob();
        }
        delay(50); // debounce
    }

    lastBtnState = btnState;
}

void handleSerialCommands() {
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd == 'p' || cmd == 'P' || cmd == 'r' || cmd == 'R') {
            Serial.println("[CMD] Manual print trigger (Active configured mix).");
            executePrintJob();
        } else if (cmd == '1' || cmd == '2' || cmd == '3') {
            Serial.println("[CMD] Manual print trigger (Active configured mix).");
            executePrintJob();
        } else if (cmd == 'g' || cmd == 'G') {
            offlineComposer.cycleGrade();
            Serial.printf("[CMD] Cycled active grade to: %s\n", offlineComposer.getGradeName(offlineComposer.getCurrentGrade()));
        } else if (cmd == 'w' || cmd == 'W') {
            if (timeManager.isPortalActive()) {
                timeManager.stopSetupPortal();
            } else {
                timeManager.startSetupPortal();
                timeManager.printSetupTicket(printer);
            }
        } else if (cmd == 't' || cmd == 'T') {
            Serial.println("[CMD] Printing self-test ticket...");
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
            printer.printSelfTest(ESP32_STATIC_IP, timeManager.getFormattedTime());
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
            printer.printSelfTest(WiFi.localIP().toString(), timeManager.getFormattedTime());
#else
            printer.printSelfTest("Direct Serial UART2", timeManager.getFormattedTime());
#endif
        } else if (cmd == 's' || cmd == 'S') {
            Serial.println("\n--- MORNING PUZZLES STATUS ---");
            Serial.println("Mode:         100% Standalone Offline (Zero External APIs)");
            Serial.printf("Format:       %d Puzzles per print (%d of 13 games enabled)\n", 
                          configManager.getPuzzleCount(), configManager.getEnabledGameCount());
            Serial.printf("Difficulty:   %s\n", configManager.getGradeName(configManager.getPuzzleGrade()));
            Serial.printf("Time:         %s\n", timeManager.getFormattedTime().c_str());
            Serial.printf("Time Set:     %s\n", timeManager.isTimeSet() ? "Yes" : "No (Hold BOOT or power-cycle 3x to set)");
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
            Serial.printf("Printer:      Direct W5500 RJ45 Ethernet (ESP32: %s -> %s:%d)\n", ESP32_STATIC_IP, PRINTER_IP_ADDR, PRINTER_TCP_PORT);
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_SERIAL)
            Serial.println("Printer:      Direct Hardware Serial (UART2)");
#else
            Serial.printf("Printer:      Wi-Fi TCP (%s:%d)\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
#endif
            Serial.printf("Daily Cron:   %02d:%02d every morning\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
            Serial.printf("Hotspot:      %s\n", timeManager.isPortalActive() ? "Active (Morning-Puzzles-Setup)" : "Inactive");
            Serial.println("Controls:     [P]rint | [W]i-Fi Setup | [S]tatus");
            Serial.println("-------------------------------\n");
        }
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    pinMode(BUTTON_TRIGGER_PIN, INPUT_PULLUP);
    pinMode(STATUS_LED_PIN, OUTPUT);
    digitalWrite(STATUS_LED_PIN, LOW);

    Serial.println("\n");
    Serial.println("********************************************************");
    Serial.println("*      MORNING PUZZLES - ESP32 THERMAL PRINTER         *");
    Serial.println("*      100% On-Device Standalone & Offline Appliance   *");
    Serial.println("*      Zero External Network / API Calls Required      *");
    Serial.println("********************************************************");

    // Initialize printer hardware driver (Serial UART, W5500 Ethernet, or Wi-Fi TCP)
    printer.begin();

#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
    if (String(WIFI_SSID) == "YOUR_WIFI_SSID") {
        Serial.println("\n[WIFI] ----------------------------------------------------");
        Serial.println("[WIFI] WARNING: WIFI_SSID is still set to 'YOUR_WIFI_SSID'!");
        Serial.println("[WIFI] Set your home Wi-Fi credentials in config.h so the");
        Serial.println("[WIFI] ESP32 can connect to your router to reach the printer.");
        Serial.println("[WIFI] ----------------------------------------------------\n");
    } else {
        Serial.printf("\n[WIFI] Connecting to '%s' to reach Ethernet printer (%s:%d)...\n", 
                      WIFI_SSID, PRINTER_IP_ADDR, PRINTER_TCP_PORT);
        WiFi.mode(WIFI_STA);
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        unsigned long wifiStart = millis();
        while (WiFi.status() != WL_CONNECTED && millis() - wifiStart < WIFI_CONNECT_TIMEOUT_MS) {
            delay(500);
            Serial.print(".");
        }
        if (WiFi.status() == WL_CONNECTED) {
            Serial.printf("\n[WIFI] Connected! ESP32 IP: %s | Gateway: %s\n\n", 
                          WiFi.localIP().toString().c_str(), WiFi.gatewayIP().toString().c_str());
        } else {
            Serial.println("\n[WIFI] ERROR: Wi-Fi connection timed out. Check credentials in config.h.");
        }
    }
#endif

    // Initialize offline persistent configuration (NVS Flash)
    configManager.begin();

    // Initialize offline timekeeping (checks for optional DS3231 RTC on I2C)
    timeManager.begin();
    timeManager.setConfigManager(&configManager);
    timeManager.setPrinter(&printer);

    Serial.println("[MAIN] Operating in 100% STANDALONE OFFLINE mode.");
    Serial.printf("[MAIN] Configuration: %d puzzles per print from %d enabled games (Difficulty: %s)\n",
                  configManager.getPuzzleCount(), configManager.getEnabledGameCount(),
                  configManager.getGradeName(configManager.getPuzzleGrade()));

    Serial.println("\n--- CONTROLS & HOW TO USE ---");
    Serial.println("1. Press BOOT button (GPIO 0)       -> Instantly generates & prints current configured puzzle mix!");
    Serial.println("2. Power-cycle printer 3x in 5 sec  -> Activates Setup Hotspot with Dual QR code receipt ticket!");
    Serial.printf("3. Daily scheduled auto-print       -> Every morning at %02d:%02d\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
    Serial.println("4. Auto-print on Printer Power-ON   -> Flip printer switch ON to print automatically!");
    Serial.println("5. Serial Monitor (115200 baud)     -> [P]rint | [W]i-Fi Setup | [S]tatus\n");

#if AUTO_PRINT_ON_BOOT
    Serial.println("[MAIN] AUTO_PRINT_ON_BOOT active. Checking printer readiness...");
    delay(PRINTER_READY_SETTLE_MS);
    if (printer.isPrinterOnline(1000)) {
        Serial.println("[MAIN] Printer online at boot -> Executing auto-print job!");
        executePrintJob();
    } else {
        Serial.println("[MAIN] Printer not reachable yet at boot. Will auto-print when printer switch is turned ON.");
    }
#endif
}

#if AUTO_PRINT_ON_PRINTER_POWER
void checkPrinterPowerTransition() {
    static unsigned long lastPollMs = 0;
    static bool lastPrinterOnline = false;
    static bool initializedState = false;

    static int powerCycleCount = 0;
    static unsigned long firstToggleMs = 0;
    static unsigned long steadyOnStartMs = 0;
    static bool setupModeTriggered = false;

    unsigned long now = millis();
    if (now - lastPollMs < PRINTER_POLL_INTERVAL_MS) {
        return;
    }
    lastPollMs = now;

    bool isOnline = printer.isPrinterOnline(150);

    if (!initializedState) {
        lastPrinterOnline = isOnline;
        initializedState = true;
        if (isOnline) steadyOnStartMs = now;
        return;
    }

    // 1. Detected transition from OFF -> ON!
    if (isOnline && !lastPrinterOnline) {
        if (powerCycleCount == 0 || (now - firstToggleMs > 5000)) {
            firstToggleMs = now;
            powerCycleCount = 1;
        } else {
            powerCycleCount++;
        }
        steadyOnStartMs = now;
        setupModeTriggered = false;
        Serial.printf("\n[PRINTER] Power ON transition #%d detected! (Elapsed in window: %lu ms)\n", 
                      powerCycleCount, now - firstToggleMs);
    }
    // 2. Detected transition from ON -> OFF!
    else if (!isOnline && lastPrinterOnline) {
        Serial.println("[PRINTER] Printer powered OFF.");
        steadyOnStartMs = 0;
    }

    // 3. Steady state processing while printer remains ON
    if (isOnline) {
        // Did user perform 3 toggles within 5 seconds?
        if (powerCycleCount >= 3) {
            // Wait for 3 seconds of steady ON to confirm user is finished toggling
            if (!setupModeTriggered && (now - steadyOnStartMs >= 3000)) {
                setupModeTriggered = true;
                Serial.println("\n[PRINTER] >>> 3-CYCLE GESTURE CONFIRMED! ENTERING SETUP MODE <<<");
                powerCycleCount = 0;

                // Start Wi-Fi hotspot immediately (broadcasts in ~150ms)
                timeManager.startSetupPortal();

                // Print setup ticket with dual stacked QR codes
                timeManager.printSetupTicket(printer);
            }
        }
        // Normal single power-on: steady ON for 3 seconds with no further toggles
        else if (powerCycleCount == 1) {
            if (now - steadyOnStartMs >= 3000) {
                Serial.println("\n[PRINTER] Normal power-on confirmed. Starting automatic daily print job...");
                powerCycleCount = 0;
                executePrintJob();
            }
        }
        // 2 toggles where 5s window expired without reaching 3
        else if (powerCycleCount == 2) {
            if (now - firstToggleMs > 5000 && now - steadyOnStartMs >= 3000) {
                Serial.println("[PRINTER] Incomplete power-cycle sequence. Resetting toggle counter.");
                powerCycleCount = 0;
            }
        }
    }

    lastPrinterOnline = isOnline;
}
#endif

void loop() {
    // 1. Handle SoftAP captive portal requests if user opened setup mode
    timeManager.handleClient();

    // 2. Monitor physical BOOT button (simple on-demand print)
    handleButtonPress();

    // 3. Monitor Serial console commands
    handleSerialCommands();

    // 4. Check for daily morning 7:00 AM cron trigger
    if (timeManager.isCronTriggerTime(DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE)) {
        Serial.println("[MAIN] 7:00 AM Morning Cron Trigger! Starting daily print job...");
        executePrintJob();
    }

#if AUTO_PRINT_ON_PRINTER_POWER
    // 5. Monitor printer power switch (auto-print or rapid 3x toggle setup trigger)
    checkPrinterPowerTransition();
#endif

    delay(20);
}
