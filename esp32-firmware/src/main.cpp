#include <Arduino.h>
#include <WiFi.h>
#include "config.h"
#include "printer/EscPosPrinter.h"
#include "time/OfflineTimeManager.h"
#include "generators/OfflinePuzzleComposer.h"
#include "scheduler/DailyScheduler.h"
#include "net/PuzzleClient.h"

// Hardware and engines
EscPosPrinter          printer;
OfflineTimeManager     timeManager;
OfflinePuzzleComposer  offlineComposer;
DailyScheduler         scheduler;
PuzzleClient           puzzleClient;

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

void executePrintJob(bool forceOffline = false) {
    Serial.println("\n========================================================");
    Serial.println(">>> STARTING MORNING PUZZLES PRINT JOB <<<");
    Serial.printf(">>> Time: %s\n", timeManager.getFormattedTime().c_str());
    Serial.println("========================================================");

    digitalWrite(STATUS_LED_PIN, HIGH);
    bool success = false;

#if (ACTIVE_OPERATION_MODE == MODE_STANDALONE_OFFLINE)
    // 100% Offline on-device generation
    success = offlineComposer.generateAndPrintReceipt(printer, timeManager.getFormattedTime("%A, %B %d, %Y"));
#elif (ACTIVE_OPERATION_MODE == MODE_NETWORK_SERVER)
    // Remote web service fetch
    success = puzzleClient.fetchAndPrintDailyPuzzles(printer);
#elif (ACTIVE_OPERATION_MODE == MODE_HYBRID)
    // Try remote server first; fall back to local generation if offline
    if (!forceOffline && WiFi.status() == WL_CONNECTED) {
        Serial.println("[MAIN] Hybrid Mode: Attempting remote API fetch...");
        success = puzzleClient.fetchAndPrintDailyPuzzles(printer);
    }
    if (!success) {
        Serial.println("[MAIN] Hybrid Mode: Falling back to on-device generation...");
        success = offlineComposer.generateAndPrintReceipt(printer, timeManager.getFormattedTime("%A, %B %d, %Y"));
    }
#endif

    digitalWrite(STATUS_LED_PIN, LOW);

    if (success) {
        Serial.println("[MAIN] Print job completed successfully!\n");
        blinkStatusLed(2, 200);
    } else {
        Serial.println("[MAIN] Print job failed. Please check printer connection/IP.\n");
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

        if (duration >= 2500) {
            // Long Press (>2.5s) -> Toggle SoftAP Setup Portal
            if (timeManager.isPortalActive()) {
                timeManager.stopSetupPortal();
            } else {
                timeManager.startSetupPortal();
            }
        } else if (duration > 80) {
            // Short Press -> Instant On-Demand Print!
            Serial.println("[BTN] Short press detected -> Triggering instant random puzzle print!");
            executePrintJob();
        }
        delay(50); // debounce
    }

    lastBtnState = btnState;
}

void handleSerialCommands() {
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd == 'p' || cmd == 'P') {
            Serial.println("[CMD] Manual print trigger requested.");
            executePrintJob();
        } else if (cmd == 'w' || cmd == 'W') {
            if (timeManager.isPortalActive()) timeManager.stopSetupPortal();
            else timeManager.startSetupPortal();
        } else if (cmd == 't' || cmd == 'T') {
            Serial.println("[CMD] Printing self-test ticket...");
            printer.printSelfTest(WiFi.localIP().toString(), timeManager.getFormattedTime());
        } else if (cmd == 's' || cmd == 'S') {
            Serial.println("\n--- MORNING PUZZLES STATUS ---");
            Serial.printf("Mode:       %s\n", (ACTIVE_OPERATION_MODE == MODE_STANDALONE_OFFLINE) ? "100% Standalone Offline" : "Network/Hybrid");
            Serial.printf("Time:       %s\n", timeManager.getFormattedTime().c_str());
            Serial.printf("Time Set:   %s\n", timeManager.isTimeSet() ? "Yes" : "No (Hold BOOT 3s to set)");
            Serial.printf("Printer:    %s:%d\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
            Serial.printf("Daily Cron: %02d:%02d every morning\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
            Serial.printf("Hotspot:    %s\n", timeManager.isPortalActive() ? "Active (Morning-Puzzles-Setup)" : "Inactive");
            Serial.println("Controls:   [P]rint on demand | [W]i-Fi Setup | [T]est | [S]tatus");
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
    Serial.println("*      100% On-Device Standalone & Offline Ready       *");
    Serial.println("********************************************************");

    // Initialize printer hardware driver
    printer.begin();

    // Initialize offline timekeeping (checks for optional DS3231 RTC)
    timeManager.begin();

#if (ACTIVE_OPERATION_MODE != MODE_STANDALONE_OFFLINE)
    // Connect Wi-Fi in network/hybrid modes
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("[WIFI] Connecting");
    unsigned long startMs = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startMs < WIFI_CONNECT_TIMEOUT_MS) {
        delay(500);
        Serial.print(".");
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("\n[WIFI] Connected! IP: %s\n", WiFi.localIP().toString().c_str());
        scheduler.begin(); // Sync NTP
    } else {
        Serial.println("\n[WIFI] Could not connect to Wi-Fi. Standalone mode ready.");
    }
#else
    Serial.println("[MAIN] Operating in 100% STANDALONE OFFLINE mode.");
    Serial.println("[MAIN] All 5 puzzles will generate on the ESP32 chip on-demand.");
#endif

    Serial.println("\n--- CONTROLS & HOW TO USE ---");
    Serial.println("1. Short-press BOOT button (GPIO 0) -> Instantly generates & prints random puzzles!");
    Serial.println("2. Long-press BOOT button (3 sec)   -> Starts Wi-Fi hotspot to sync time from your phone!");
    Serial.printf("3. Daily scheduled auto-print       -> Every morning at %02d:%02d\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
    Serial.println("4. Serial Monitor (115200 baud)     -> Type 'P' (print), 'W' (hotspot), 'S' (status)\n");
}

void loop() {
    // 1. Handle SoftAP captive portal requests if user opened setup mode
    timeManager.handleClient();

    // 2. Monitor physical BOOT button (short click vs long press)
    handleButtonPress();

    // 3. Monitor Serial console commands
    handleSerialCommands();

    // 4. Check for daily morning 7:00 AM cron trigger
    if (timeManager.isCronTriggerTime(DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE)) {
        Serial.println("[MAIN] 7:00 AM Morning Cron Trigger! Starting daily print job...");
        executePrintJob();
    }

    delay(20);
}
