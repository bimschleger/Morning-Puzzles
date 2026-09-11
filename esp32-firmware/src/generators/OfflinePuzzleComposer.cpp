#include "OfflinePuzzleComposer.h"
#include "../printer/EscPosPrinter.h"

OfflinePuzzleComposer::OfflinePuzzleComposer() {}

bool OfflinePuzzleComposer::generateAndPrintReceipt(EscPosPrinter& printer, const String& dateStr) {
    // Seed with ESP32 true hardware random number generator
    randomSeed(esp_random());

    unsigned long startMs = millis();
    Serial.println("\n[COMPOSER] Starting on-chip offline puzzle generation...");

    if (!printer.connect()) {
        Serial.println("[COMPOSER] ERROR: Failed to connect to printer.");
        return false;
    }

    printer.init();

    // 1. Receipt Header
    String headerDate = (dateStr.length() > 0) ? dateStr : "Daily On-Demand Edition";
    printer.printHeader("MORNING PUZZLES", headerDate);
    printer.println("");

    // 2. Generate and print Sudoku
    Serial.println("[COMPOSER] Generating Sudoku...");
    _sudoku.generate(SUDOKU_MEDIUM);
    _sudoku.printToReceipt(printer, SUDOKU_MEDIUM);
    printer.printHorizontalLine('-');

    // 3. Generate and print Word Search
    Serial.println("[COMPOSER] Generating Word Search...");
    _wordSearch.generate(WS_MEDIUM);
    _wordSearch.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 4. Generate and print Nonogram
    Serial.println("[COMPOSER] Generating Nonogram...");
    _nonogram.generate(NONO_EASY); // 5x5 for fast solving
    _nonogram.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 5. Generate and print Queens / Star Battle
    Serial.println("[COMPOSER] Generating Queens puzzle...");
    _queens.generate(QUEENS_MEDIUM); // 8x8 1-Star Queens
    _queens.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 6. Generate and print Jumble
    Serial.println("[COMPOSER] Generating Daily Jumble...");
    _jumble.generate(JUMBLE_MEDIUM);
    _jumble.printToReceipt(printer);

    // 7. Footer
    printer.printDoubleLine();
    printer.setAlign(ALIGN_CENTER);
    printer.println("Printed on ESP32 80mm Thermal Receipt");
    printer.println("Puzzles generated 100% on-device (Offline)");
    printer.println("Good luck & have a wonderful day!");
    printer.printDoubleLine();

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();

    unsigned long elapsed = millis() - startMs;
    Serial.printf("[COMPOSER] Generation & printing completed in %lu ms!\n\n", elapsed);
    return true;
}
