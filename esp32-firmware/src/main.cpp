// ==============================================================================
// Morning Puzzles - 100% Offline Standalone Daily Receipt Printer Firmware
// 
// Arduino IDE Configuration:
//   Board: "ESP32 Dev Module" or "ESP32S3 Dev Module" (e.g. LilyGO T-ETH-Lite)
//   Partition Scheme: "Huge APP (3MB No OTA / 1MB SPIFFS)" (CRITICAL for flash headroom)
//   Upload Speed: 921600
// ==============================================================================

#include <Arduino.h>
#include "config.h"
#include "printer/EscPosPrinter.h"
#include "time/OfflineTimeManager.h"
#include "config/OfflineConfigManager.h"
#include "generators/OfflinePuzzleComposer.h"
#include <Preferences.h>

#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
#include <WiFi.h>
#endif

// Hardware and engines
EscPosPrinter          printer;
OfflineTimeManager     timeManager;
OfflineConfigManager   configManager;
OfflinePuzzleComposer  offlineComposer;

// Setup mode and boot timing state
bool          g_setupModeTriggeredAtBoot = false;
bool          g_bootAutoPrintPending = false;
unsigned long g_bootTimeMs = 0;

// Coordinated print state & refractory cooldown across all triggers
unsigned long g_lastPrintCompletedMs = 0;
bool          g_autoPrintSatisfiedThisCycle = true; // Default true so cold boots stay quiet

// Button timing state
bool          lastBtnState = HIGH;
unsigned long btnPressStartMs = 0;
bool          btnLongPressActive = false;

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
    Serial.printf(">>> Format: %d-Puzzle Mix (%d of 16 games enabled)\n", count, configManager.getEnabledGameCount());
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

    // Mark print job completed: record cooldown
    g_lastPrintCompletedMs = millis();
    g_bootAutoPrintPending = false;

    if (success) {
        g_autoPrintSatisfiedThisCycle = true;
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

    // Button down (transition HIGH -> LOW)
    if (btnState == LOW && lastBtnState == HIGH) {
        btnPressStartMs = now;
        btnLongPressActive = false;
        delay(BUTTON_DEBOUNCE_MS);
    }
    // Button held down (remains LOW)
    else if (btnState == LOW && lastBtnState == LOW) {
        if (!btnLongPressActive && (now - btnPressStartMs >= BUTTON_LONG_PRESS_MS)) {
            btnLongPressActive = true;
            // Visual indicator: solid ON status LED indicates setup threshold reached
            digitalWrite(STATUS_LED_PIN, HIGH);
            Serial.println("[BTN] Long-press threshold reached (>= 2.5s). Release button to activate Wi-Fi Setup Mode.");
        }
    }
    // Button released (transition LOW -> HIGH)
    else if (btnState == HIGH && lastBtnState == LOW) {
        digitalWrite(STATUS_LED_PIN, LOW);
        unsigned long duration = now - btnPressStartMs;

        if (btnLongPressActive || duration >= BUTTON_LONG_PRESS_MS) {
            // Long press released -> Enter or toggle Wi-Fi Setup Mode
            Serial.println("\n[BTN] >>> LONG PRESS CONFIRMED! ENTERING WI-FI SETUP MODE <<<");
            blinkStatusLed(3, 100);

            if (timeManager.isPortalActive()) {
                Serial.println("[BTN] Setup portal already active -> stopping portal.");
                timeManager.stopSetupPortal();
            } else {
                timeManager.startSetupPortal();
                timeManager.printSetupTicket(printer);
            }
        } else if (duration > BUTTON_DEBOUNCE_MS) {
            // Short press released -> Instant On-Demand Print
            Serial.println("[BTN] Short press detected -> Generating & printing active puzzle mix!");
            blinkStatusLed(1, 150);
            executePrintJob();
        }

        btnLongPressActive = false;
        delay(BUTTON_DEBOUNCE_MS);
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
            Serial.printf("Format:       %d Puzzles per print (%d of 16 games enabled)\n", 
                          configManager.getPuzzleCount(), configManager.getEnabledGameCount());
            Serial.printf("Difficulty:   %s\n", configManager.getGradeName(configManager.getPuzzleGrade()));
            Serial.printf("Time:         %s\n", timeManager.getFormattedTime().c_str());
            Serial.printf("Time Set:     %s\n", timeManager.isTimeSet() ? "Yes" : "No (Hold BOOT button >= 2.5s to set)");
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
            Serial.printf("Printer:      Direct W5500 RJ45 Ethernet (ESP32: %s -> %s:%d)\n", ESP32_STATIC_IP, PRINTER_IP_ADDR, PRINTER_TCP_PORT);
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_SERIAL)
            Serial.println("Printer:      Direct Hardware Serial (UART2)");
#else
            Serial.printf("Printer:      Wi-Fi TCP (%s:%d)\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
#endif
            if (configManager.isDailyScheduleEnabled()) {
                Serial.printf("Daily Cron:   %s every day (%02d:%02d)\n", 
                              configManager.getDailyScheduleTimeString().c_str(),
                              configManager.getDailyScheduleHour(), configManager.getDailyScheduleMinute());
            } else {
                Serial.println("Daily Cron:   Disabled (Manual / Power-on trigger only)");
            }
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
    Serial.println("1. Setup Mode: Leave printer ON & replug ESP32 power -> Launches Setup Portal + QR slip");
    Serial.println("2. On-Demand Print: Flip printer switch OFF, wait 3s, then ON -> Prints active puzzle mix!");
    if (configManager.isDailyScheduleEnabled()) {
        Serial.printf("3. Daily scheduled auto-print        -> %s every day\n", 
                      configManager.getDailyScheduleTimeString().c_str());
    } else {
        Serial.println("3. Daily scheduled auto-print        -> Disabled (Manual / Power switch trigger only)");
    }
    Serial.println("4. BOOT Button (Dev Fallback): Short press = print, Hold >= 2.5s = setup portal");
    Serial.println("5. Serial Monitor (115200 baud): [P]rint | [W]i-Fi Setup | [S]tatus\n");

    // -------------------------------------------------------------------------
    // Zero-Button Power Gesture: Check if printer is already online at boot
    // -------------------------------------------------------------------------
#if SETUP_MODE_ON_PRINTER_ONLINE_BOOT
    Serial.printf("[MAIN] Checking for printer-first boot gesture (window: %d ms)...\n", PRINTER_BOOT_PROBE_WINDOW_MS);
    if (printer.isPrinterOnline(PRINTER_BOOT_PROBE_WINDOW_MS)) {
        Serial.println("\n************************************************************");
        Serial.println("* >>> PRINTER-FIRST BOOT DETECTED! ENTERING SETUP MODE <<< *");
        Serial.println("************************************************************\n");

        g_setupModeTriggeredAtBoot = true;
        g_autoPrintSatisfiedThisCycle = true;

        // Start Wi-Fi hotspot immediately (broadcasts in ~150ms)
        timeManager.startSetupPortal();

        // Print setup ticket with dual stacked QR codes
        timeManager.printSetupTicket(printer);
    } else {
        Serial.println("[MAIN] Printer not online at boot (Normal / Simultaneous start).");
        g_setupModeTriggeredAtBoot = false;
        g_autoPrintSatisfiedThisCycle = true; // Stay quiet until scheduled daily cron or switch toggle
    }
#else
    g_autoPrintSatisfiedThisCycle = true;
#endif

    g_bootTimeMs = millis();
#if AUTO_PRINT_ON_BOOT
    g_bootAutoPrintPending = true;
#endif
}

#if AUTO_PRINT_ON_PRINTER_POWER
void checkPrinterPowerTransition() {
    static unsigned long lastPollMs = 0;
    static bool lastPrinterOnline = false;
    static bool initializedState = false;
    static unsigned long steadyOnStartMs = 0;
    static unsigned long steadyOffStartMs = 0;

    unsigned long now = millis();
    if (now - lastPollMs < PRINTER_POLL_INTERVAL_MS) {
        return;
    }
    lastPollMs = now;

    bool isOnline = printer.isPrinterOnline(100);

    // Initial state detection on boot
    if (!initializedState) {
        lastPrinterOnline = isOnline;
        initializedState = true;
        if (isOnline) {
            steadyOnStartMs = now;
        } else {
            steadyOffStartMs = now;
        }
        return;
    }

    // Guard against power outage recovery / simultaneous cold boots:
    // If ESP32 booted with printer offline, give the printer up to 5 seconds
    // to finish its hardware/Ethernet boot without re-arming an on-demand print.
    bool inBootGracePeriod = (now - g_bootTimeMs < 5000);

    // 1. Detected transition from OFF -> ON!
    if (isOnline && !lastPrinterOnline) {
        steadyOnStartMs = now;
        steadyOffStartMs = 0;
        Serial.println("\n[PRINTER] Printer power ON detected! Waiting for printer mechanism to settle...");
    }
    // 2. Detected transition from ON -> OFF with debouncing!
    else if (!isOnline && lastPrinterOnline) {
        if (steadyOffStartMs == 0) {
            steadyOffStartMs = now;
        }
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
        // Direct physical Ethernet cable: link drop confirms power loss quickly (>= 400ms)
        bool fastPhyDrop = (Ethernet.linkStatus() == LinkOFF && (now - steadyOffStartMs >= 400));
#else
        bool fastPhyDrop = false;
#endif
        // Continuous offline duration (PRINTER_OFFLINE_DEBOUNCE_MS, 1.0s)
        // to filter out socket teardown, cutter cycling, and transient network jitter.
        if (fastPhyDrop || (now - steadyOffStartMs >= PRINTER_OFFLINE_DEBOUNCE_MS)) {
            Serial.println("[PRINTER] Printer powered OFF confirmed (debounced). On-demand print re-armed for next power-on.");
            lastPrinterOnline = false;
            steadyOnStartMs = 0;
            steadyOffStartMs = 0;
            g_autoPrintSatisfiedThisCycle = false;
        }
        return; // Do not clear lastPrinterOnline or arm new triggers until debounce elapses
    }

    // Reset offline dwell timer if online
    if (isOnline) {
        steadyOffStartMs = 0;
    }

    // 3. Steady state processing while printer remains ON
    if (isOnline && !g_autoPrintSatisfiedThisCycle && !inBootGracePeriod) {
        // Enforce post-print refractory cooldown period (15 seconds)
        bool inCooldown = (g_lastPrintCompletedMs > 0) && (now - g_lastPrintCompletedMs < PRINTER_POST_PRINT_COOLDOWN_MS);

        if (!inCooldown && (now - steadyOnStartMs >= PRINTER_READY_SETTLE_MS)) {
            if (!g_bootAutoPrintPending) {
                // If user toggles printer power while Setup Portal is active,
                // treat this physical gesture as exiting setup mode to execute the print.
                if (timeManager.isPortalActive()) {
                    Serial.println("\n[PRINTER] Printer power toggle detected while Setup Portal active -> Closing hotspot and printing on-demand puzzle mix.");
                    timeManager.stopSetupPortal();
                }
                Serial.println("\n[PRINTER] Printer ready (settle elapsed). Executing on-demand print job...");
                executePrintJob();
            }
        }
    }

    lastPrinterOnline = isOnline;
}
#endif

void loop() {
#if AUTO_PRINT_ON_BOOT
    // Optional boot auto-print if enabled in config.h
    static bool bootDwellCompleted = false;
    if (!bootDwellCompleted && !g_setupModeTriggeredAtBoot) {
        if (millis() - g_bootTimeMs >= 2500) {
            bootDwellCompleted = true;
            if (g_bootAutoPrintPending) {
                g_bootAutoPrintPending = false;
                if (printer.isPrinterOnline(200)) {
                    Serial.println("[MAIN] Auto-print on boot trigger! Executing daily print job...");
                    executePrintJob();
                }
            }
        }
    }
#endif

    // 1. Handle SoftAP captive portal requests if user opened setup mode
    timeManager.handleClient();

    // 2. Monitor physical BOOT button (short = print, hold >= 2.5s = setup) [Dev Fallback]
    handleButtonPress();

    // 3. Monitor Serial console commands
    handleSerialCommands();

    // 4. Check for daily scheduled cron trigger
    if (configManager.isDailyScheduleEnabled() &&
        timeManager.isCronTriggerTime(configManager.getDailyScheduleHour(), configManager.getDailyScheduleMinute())) {
        Serial.printf("[MAIN] Scheduled Daily Cron Trigger (%s)! Starting daily print job...\n",
                      configManager.getDailyScheduleTimeString().c_str());
        executePrintJob();
    }

#if AUTO_PRINT_ON_PRINTER_POWER
    // 5. Monitor printer power switch (on-demand print when printer is flipped OFF then ON)
    checkPrinterPowerTransition();
#endif

    delay(20);
}
