#include <Arduino.h>
#include "config.h"
#include "printer/EscPosPrinter.h"
#include "time/OfflineTimeManager.h"
#include "generators/OfflinePuzzleComposer.h"

#if !OFFLINE_ONLY_BUILD
#include <WiFi.h>
#include "scheduler/DailyScheduler.h"
#include "net/PuzzleClient.h"
DailyScheduler         scheduler;
PuzzleClient           puzzleClient;
#endif

// Hardware and engines
EscPosPrinter          printer;
OfflineTimeManager     timeManager;
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

void executePrintJob(PuzzleGrade grade = GRADE_ROTATING) {
    Serial.println("\n========================================================");
    Serial.println(">>> STARTING MORNING PUZZLES 100% OFFLINE PRINT JOB <<<");
    Serial.printf(">>> Time: %s\n", timeManager.getFormattedTime().c_str());
    Serial.printf(">>> Target Grade: %s\n", (grade == GRADE_ROTATING) ? "ROTATING" : offlineComposer.getGradeName(grade));
    Serial.println("========================================================");

    digitalWrite(STATUS_LED_PIN, HIGH);

    // 100% Offline on-device generation across all 7 puzzles
    bool success = offlineComposer.generateAndPrintReceipt(
        printer, 
        timeManager.getFormattedTime("%A, %B %d, %Y"),
        grade
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

        if (duration >= 2500) {
            // Long Press (>2.5s) -> Toggle SoftAP Setup Portal (local phone time sync)
            if (timeManager.isPortalActive()) {
                timeManager.stopSetupPortal();
            } else {
                timeManager.startSetupPortal();
            }
        } else if (duration > 80) {
            // Short Press -> Instant On-Demand Print with a fresh grade!
            Serial.println("[BTN] Hardware BOOT button pressed -> Generating & printing new grade of puzzles!");
            executePrintJob(GRADE_ROTATING);
        }
        delay(50); // debounce
    }

    lastBtnState = btnState;
}

void handleSerialCommands() {
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd == 'p' || cmd == 'P') {
            Serial.println("[CMD] Manual print trigger (Rotating Grade).");
            executePrintJob(GRADE_ROTATING);
        } else if (cmd == '1') {
            Serial.println("[CMD] Generating EASY grade puzzle bundle...");
            executePrintJob(GRADE_EASY);
        } else if (cmd == '2') {
            Serial.println("[CMD] Generating MEDIUM grade puzzle bundle...");
            executePrintJob(GRADE_MEDIUM);
        } else if (cmd == '3') {
            Serial.println("[CMD] Generating HARD grade puzzle bundle...");
            executePrintJob(GRADE_HARD);
        } else if (cmd == 'g' || cmd == 'G') {
            offlineComposer.cycleGrade();
            Serial.printf("[CMD] Cycled active grade to: %s\n", offlineComposer.getGradeName(offlineComposer.getCurrentGrade()));
        } else if (cmd == 'w' || cmd == 'W') {
            if (timeManager.isPortalActive()) timeManager.stopSetupPortal();
            else timeManager.startSetupPortal();
        } else if (cmd == 't' || cmd == 'T') {
            Serial.println("[CMD] Printing self-test ticket...");
            printer.printSelfTest("Offline Standalone", timeManager.getFormattedTime());
        } else if (cmd == 's' || cmd == 'S') {
            Serial.println("\n--- MORNING PUZZLES STATUS ---");
            Serial.println("Mode:         100% Standalone Offline (Zero External APIs)");
            Serial.printf("Active Grade: %s\n", offlineComposer.getGradeName(offlineComposer.getCurrentGrade()));
            Serial.printf("Time:         %s\n", timeManager.getFormattedTime().c_str());
            Serial.printf("Time Set:     %s\n", timeManager.isTimeSet() ? "Yes" : "No (Hold BOOT 3s to set)");
            Serial.printf("Printer:      %s (Mode %d)\n", (ACTIVE_PRINTER_MODE == PRINTER_MODE_SERIAL) ? "Direct Hardware Serial (UART2)" : "Ethernet TCP", ACTIVE_PRINTER_MODE);
            Serial.printf("Daily Cron:   %02d:%02d every morning\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
            Serial.printf("Hotspot:      %s\n", timeManager.isPortalActive() ? "Active (Morning-Puzzles-Setup)" : "Inactive");
            Serial.println("Controls:     [P]rint (Next Grade) | [1] Easy | [2] Medium | [3] Hard | [G]ycle Grade | [W]i-Fi Setup | [S]tatus");
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

    // Initialize printer hardware driver (Serial UART or local raw TCP)
    printer.begin();

    // Initialize offline timekeeping (checks for optional DS3231 RTC on I2C)
    timeManager.begin();

    Serial.println("[MAIN] Operating in 100% STANDALONE OFFLINE mode.");
    Serial.println("[MAIN] All 7 puzzles generate directly on the ESP32 chip on-demand.");
    Serial.printf("[MAIN] Initial puzzle grade: %s\n", offlineComposer.getGradeName(offlineComposer.getCurrentGrade()));

    Serial.println("\n--- CONTROLS & HOW TO USE ---");
    Serial.println("1. Short-press BOOT button (GPIO 0) -> Instantly generates & prints a new grade of puzzles!");
    Serial.println("2. Long-press BOOT button (3 sec)   -> Starts local Wi-Fi hotspot to sync time from phone!");
    Serial.printf("3. Daily scheduled auto-print       -> Every morning at %02d:%02d\n", DAILY_PRINT_HOUR, DAILY_PRINT_MINUTE);
    Serial.println("4. Auto-print on Printer Power-ON   -> Flip printer switch ON to print automatically!");
    Serial.println("5. Serial Monitor (115200 baud)     -> [P]rint | [1] Easy | [2] Med | [3] Hard | [G]rade | [S]tatus\n");

#if AUTO_PRINT_ON_BOOT
    Serial.println("[MAIN] AUTO_PRINT_ON_BOOT active. Checking printer readiness...");
    delay(PRINTER_READY_SETTLE_MS);
    if (printer.isPrinterOnline(1000)) {
        Serial.println("[MAIN] Printer online at boot -> Executing auto-print job!");
        executePrintJob(GRADE_ROTATING);
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

    unsigned long now = millis();
    if (now - lastPollMs < PRINTER_POLL_INTERVAL_MS) {
        return;
    }
    lastPollMs = now;

    bool isOnline = printer.isPrinterOnline(300);

    if (!initializedState) {
        lastPrinterOnline = isOnline;
        initializedState = true;
        return;
    }

    // Detected transition from OFF -> ON!
    if (isOnline && !lastPrinterOnline) {
        Serial.println("\n[PRINTER] >>> PRINTER POWER-ON DETECTED! <<<");
        Serial.println("[PRINTER] Waiting for thermal head homing and motor boot...");
        delay(PRINTER_READY_SETTLE_MS);
        Serial.println("[PRINTER] Starting automatic print job...");
        executePrintJob(GRADE_ROTATING);
    }

    lastPrinterOnline = isOnline;
}
#endif

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
        executePrintJob(GRADE_ROTATING);
    }

#if AUTO_PRINT_ON_PRINTER_POWER
    // 5. Monitor printer power switch (auto-print when printer turns ON)
    checkPrinterPowerTransition();
#endif

    delay(20);
}
