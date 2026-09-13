#include "OfflinePuzzleComposer.h"
#include "config.h"
#include "../printer/EscPosPrinter.h"

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
        case GRADE_EASY:     return "EASY";
        case GRADE_HARD:     return "HARD";
        case GRADE_ROTATING: return "ROTATING";
        case GRADE_RANDOM:   return "RANDOM";
        case GRADE_MEDIUM:
        default:             return "MEDIUM";
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

    // Resolve individual puzzle difficulty parameters.
    // If effectiveGrade is GRADE_RANDOM (default), each game independently generates a random difficulty.
    auto pickDiff = [&](int easyVal, int medVal, int hardVal) -> int {
        if (effectiveGrade == GRADE_EASY) return easyVal;
        if (effectiveGrade == GRADE_HARD) return hardVal;
        if (effectiveGrade == GRADE_MEDIUM) return medVal;
        int r = random(3) % 3;
        return (r == 0) ? easyVal : ((r == 2) ? hardVal : medVal);
    };

    SudokuDifficulty     sDiff  = (SudokuDifficulty)pickDiff(SUDOKU_EASY, SUDOKU_MEDIUM, SUDOKU_HARD);
    WordSearchDifficulty wsDiff = (WordSearchDifficulty)pickDiff(WS_EASY, WS_MEDIUM, WS_HARD);
    NonogramDifficulty   nDiff  = (NonogramDifficulty)pickDiff(NONO_EASY, NONO_MEDIUM, NONO_HARD);
    QueensDifficulty     qDiff  = (QueensDifficulty)pickDiff(QUEENS_EASY, QUEENS_MEDIUM, QUEENS_HARD);
    JumbleDifficulty     jDiff  = (JumbleDifficulty)pickDiff(JUMBLE_EASY, JUMBLE_MEDIUM, JUMBLE_HARD);
    BinaryDifficulty     bDiff  = (BinaryDifficulty)pickDiff(BINARY_EASY, BINARY_MEDIUM, BINARY_HARD);
    MinesDifficulty      mDiff  = (MinesDifficulty)pickDiff(MINES_EASY, MINES_MEDIUM, MINES_HARD);
    TentsDifficulty      tDiff  = (TentsDifficulty)pickDiff(TENTS_EASY, TENTS_MEDIUM, TENTS_HARD);
    BridgesDifficulty    brDiff = (BridgesDifficulty)pickDiff(BRIDGES_EASY, BRIDGES_MEDIUM, BRIDGES_HARD);
    TangoDifficulty      tgDiff = (TangoDifficulty)pickDiff(TANGO_EASY, TANGO_MEDIUM, TANGO_HARD);
    WheelDifficulty      wDiff  = (WheelDifficulty)pickDiff(WHEEL_EASY, WHEEL_MEDIUM, WHEEL_HARD);
    LightsDifficulty     lDiff  = (LightsDifficulty)pickDiff(LIGHTS_EASY, LIGHTS_MEDIUM, LIGHTS_HARD);

#if (OFFLINE_PRINT_STYLE == STYLE_HYBRID)
    bool useRaster = true;
#else
    bool useRaster = false;
#endif

    // 2. Generate and print Sudoku
    Serial.println("[COMPOSER] Generating Sudoku...");
    _sudoku.generate(sDiff);
    if (!useRaster || !_sudoku.printRasterToReceipt(printer, sDiff)) {
        _sudoku.printToReceipt(printer, sDiff);
    }
    printer.printHorizontalLine('-');

    // 3. Generate and print Word Search
    Serial.println("[COMPOSER] Generating Word Search...");
    _wordSearch.generate(wsDiff);
    if (!useRaster || !_wordSearch.printRasterToReceipt(printer)) {
        _wordSearch.printToReceipt(printer);
    }
    printer.printHorizontalLine('-');

    // 4. Generate and print Nonogram
    Serial.println("[COMPOSER] Generating Nonogram...");
    _nonogram.generate(nDiff);
    if (!useRaster || !_nonogram.printRasterToReceipt(printer)) {
        _nonogram.printToReceipt(printer);
    }
    printer.printHorizontalLine('-');

    // 5. Generate and print Queens / Star Battle
    Serial.println("[COMPOSER] Generating Queens puzzle...");
    _queens.generate(qDiff);
    if (!useRaster || !_queens.printRasterToReceipt(printer)) {
        _queens.printToReceipt(printer);
    }
    printer.printHorizontalLine('-');

    // 6. Generate and print Jumble
    Serial.println("[COMPOSER] Generating Daily Jumble...");
    _jumble.generate(jDiff);
    if (!useRaster || !_jumble.printRasterToReceipt(printer)) {
        _jumble.printToReceipt(printer);
    }
    printer.printHorizontalLine('-');

    // 7. Generate and print Binary
    Serial.println("[COMPOSER] Generating Binary...");
    _binary.generate(bDiff);
    if (!useRaster || !_binary.printRasterToReceipt(printer, bDiff)) {
        _binary.printToReceipt(printer, bDiff);
    }
    printer.printHorizontalLine('-');

    // 8. Generate and print Mines
    Serial.println("[COMPOSER] Generating Mines...");
    _mines.generate(mDiff);
    if (!useRaster || !_mines.printRasterToReceipt(printer, mDiff)) {
        _mines.printToReceipt(printer, mDiff);
    }
    printer.printHorizontalLine('-');

    // 9. Generate and print Tents
    Serial.println("[COMPOSER] Generating Tents...");
    _tents.generate(tDiff);
    if (!useRaster || !_tents.printRasterToReceipt(printer, tDiff)) {
        _tents.printToReceipt(printer, tDiff);
    }
    printer.printHorizontalLine('-');

    // 10. Generate and print Bridges
    Serial.println("[COMPOSER] Generating Bridges...");
    _bridges.generate(brDiff);
    if (!useRaster || !_bridges.printRasterToReceipt(printer, brDiff)) {
        _bridges.printToReceipt(printer, brDiff);
    }
    printer.printHorizontalLine('-');

    // 11. Generate and print Tango
    Serial.println("[COMPOSER] Generating Tango...");
    _tango.generate(tgDiff);
    if (!useRaster || !_tango.printRasterToReceipt(printer, tgDiff)) {
        _tango.printToReceipt(printer, tgDiff);
    }
    printer.printHorizontalLine('-');

    // 12. Generate and print Wheel
    Serial.println("[COMPOSER] Generating Wheel...");
    _wheel.generate(wDiff);
    if (!useRaster || !_wheel.printRasterToReceipt(printer)) {
        _wheel.printToReceipt(printer);
    }
    printer.printHorizontalLine('-');

    // 13. Generate and print Lights
    Serial.println("[COMPOSER] Generating Lights...");
    _lights.generate(lDiff);
    if (!useRaster || !_lights.printRasterToReceipt(printer, lDiff)) {
        _lights.printToReceipt(printer, lDiff);
    }

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
