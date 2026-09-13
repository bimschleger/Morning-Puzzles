#include "OfflinePuzzleComposer.h"
#include "EscPosPrinter.h"

OfflinePuzzleComposer::OfflinePuzzleComposer() : 
    _currentGrade(GRADE_MEDIUM), 
    _rotationIndex(0) {
}

void OfflinePuzzleComposer::cycleGrade() {
    _rotationIndex = (_rotationIndex + 1) % 3;
    _currentGrade = (PuzzleGrade)_rotationIndex;
}

void OfflinePuzzleComposer::setGrade(PuzzleGrade grade) {
    _currentGrade = grade;
}

PuzzleGrade OfflinePuzzleComposer::getCurrentGrade() const {
    return _currentGrade;
}

const char* OfflinePuzzleComposer::getGradeName(PuzzleGrade grade) const {
    switch (grade) {
        case GRADE_EASY: return "EASY";
        case GRADE_HARD: return "HARD";
        case GRADE_MEDIUM:
        default: return "MEDIUM";
    }
}

bool OfflinePuzzleComposer::generateAndPrintReceipt(EscPosPrinter& printer, const String& dateStr, PuzzleGrade grade) {
    // 1. Reseed PRNG with ESP32 hardware True Random Number Generator + microsecond timer
    randomSeed(esp_random() ^ (uint32_t)micros());

    // 2. Resolve effective grade for this print job
    PuzzleGrade effectiveGrade = grade;
    if (effectiveGrade == GRADE_ROTATING) {
        effectiveGrade = (PuzzleGrade)(_rotationIndex % 3);
        _rotationIndex = (_rotationIndex + 1) % 3;
    }
    _currentGrade = effectiveGrade;

    unsigned long startMs = millis();
    Serial.printf("\n[COMPOSER] Starting 100%% offline generation for EDITION GRADE: %s...\n", getGradeName(effectiveGrade));

    if (!printer.connect()) {
        Serial.println("[COMPOSER] ERROR: Failed to connect to printer.");
        return false;
    }

    printer.init();

    // 1. Receipt Header
    String headerDate = (dateStr.length() > 0) ? dateStr : "Daily On-Demand Edition";
    printer.printHeader("MORNING PUZZLES", headerDate);
    printer.setAlign(ALIGN_CENTER);
    printer.println(String("EDITION GRADE: ") + getGradeName(effectiveGrade));
    printer.println("");

    // Resolve individual puzzle difficulty parameters matching the requested grade
    SudokuDifficulty     sDiff = (effectiveGrade == GRADE_EASY) ? SUDOKU_EASY : ((effectiveGrade == GRADE_HARD) ? SUDOKU_HARD : SUDOKU_MEDIUM);
    WordSearchDifficulty wsDiff = (effectiveGrade == GRADE_EASY) ? WS_EASY : ((effectiveGrade == GRADE_HARD) ? WS_HARD : WS_MEDIUM);
    NonogramDifficulty   nDiff = (effectiveGrade == GRADE_EASY) ? NONO_EASY : ((effectiveGrade == GRADE_HARD) ? NONO_HARD : NONO_MEDIUM);
    QueensDifficulty     qDiff = (effectiveGrade == GRADE_EASY) ? QUEENS_EASY : ((effectiveGrade == GRADE_HARD) ? QUEENS_HARD : QUEENS_MEDIUM);
    JumbleDifficulty     jDiff = (effectiveGrade == GRADE_EASY) ? JUMBLE_EASY : ((effectiveGrade == GRADE_HARD) ? JUMBLE_HARD : JUMBLE_MEDIUM);
    BinaryDifficulty     bDiff = (effectiveGrade == GRADE_EASY) ? BINARY_EASY : ((effectiveGrade == GRADE_HARD) ? BINARY_HARD : BINARY_MEDIUM);
    MinesDifficulty      mDiff = (effectiveGrade == GRADE_EASY) ? MINES_EASY : ((effectiveGrade == GRADE_HARD) ? MINES_HARD : MINES_MEDIUM);
    TentsDifficulty      tDiff = (effectiveGrade == GRADE_EASY) ? TENTS_EASY : ((effectiveGrade == GRADE_HARD) ? TENTS_HARD : TENTS_MEDIUM);
    BridgesDifficulty    brDiff = (effectiveGrade == GRADE_EASY) ? BRIDGES_EASY : ((effectiveGrade == GRADE_HARD) ? BRIDGES_HARD : BRIDGES_MEDIUM);
    TangoDifficulty      tgDiff = (effectiveGrade == GRADE_EASY) ? TANGO_EASY : ((effectiveGrade == GRADE_HARD) ? TANGO_HARD : TANGO_MEDIUM);
    LightsDifficulty     lDiff = (effectiveGrade == GRADE_EASY) ? LIGHTS_EASY : ((effectiveGrade == GRADE_HARD) ? LIGHTS_HARD : LIGHTS_MEDIUM);

    // 2. Generate and print Sudoku
    Serial.println("[COMPOSER] Generating Sudoku...");
    _sudoku.generate(sDiff);
    _sudoku.printToReceipt(printer, sDiff);
    printer.printHorizontalLine('-');

    // 3. Generate and print Word Search
    Serial.println("[COMPOSER] Generating Word Search...");
    _wordSearch.generate(wsDiff);
    _wordSearch.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 4. Generate and print Nonogram
    Serial.println("[COMPOSER] Generating Nonogram...");
    _nonogram.generate(nDiff);
    _nonogram.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 5. Generate and print Queens / Star Battle
    Serial.println("[COMPOSER] Generating Queens puzzle...");
    _queens.generate(qDiff);
    _queens.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 6. Generate and print Jumble
    Serial.println("[COMPOSER] Generating Daily Jumble...");
    _jumble.generate(jDiff);
    _jumble.printToReceipt(printer);
    printer.printHorizontalLine('-');

    // 7. Generate and print Binary
    Serial.println("[COMPOSER] Generating Binary...");
    _binary.generate(bDiff);
    _binary.printToReceipt(printer, bDiff);
    printer.printHorizontalLine('-');

    // 8. Generate and print Mines
    Serial.println("[COMPOSER] Generating Mines...");
    _mines.generate(mDiff);
    _mines.printToReceipt(printer, mDiff);
    printer.printHorizontalLine('-');

    // 9. Generate and print Tents
    Serial.println("[COMPOSER] Generating Tents...");
    _tents.generate(tDiff);
    _tents.printToReceipt(printer, tDiff);
    printer.printHorizontalLine('-');

    // 10. Generate and print Bridges
    Serial.println("[COMPOSER] Generating Bridges...");
    _bridges.generate(brDiff);
    _bridges.printToReceipt(printer, brDiff);
    printer.printHorizontalLine('-');

    // 11. Generate and print Tango
    Serial.println("[COMPOSER] Generating Tango...");
    _tango.generate(tgDiff);
    _tango.printToReceipt(printer, tgDiff);
    printer.printHorizontalLine('-');

    // 12. Generate and print Lights
    Serial.println("[COMPOSER] Generating Lights...");
    _lights.generate(lDiff);
    _lights.printToReceipt(printer, lDiff);

    // Footer
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
    Serial.printf("[COMPOSER] Generation & printing for %s completed in %lu ms!\n\n", 
                  getGradeName(effectiveGrade), elapsed);
    return true;
}
