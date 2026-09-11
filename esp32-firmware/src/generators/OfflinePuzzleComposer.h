#ifndef OFFLINE_PUZZLE_COMPOSER_H
#define OFFLINE_PUZZLE_COMPOSER_H

#include <Arduino.h>
class EscPosPrinter;
#include "SudokuGen.h"
#include "WordSearchGen.h"
#include "NonogramGen.h"
#include "QueensGen.h"
#include "JumbleGen.h"

class OfflinePuzzleComposer {
public:
    OfflinePuzzleComposer();

    // Generates a complete random bundle of all 5 puzzles on the ESP32 and prints directly
    bool generateAndPrintReceipt(EscPosPrinter& printer, const String& dateStr = "");

private:
    SudokuGen     _sudoku;
    WordSearchGen _wordSearch;
    NonogramGen   _nonogram;
    QueensGen     _queens;
    JumbleGen     _jumble;
};

#endif // OFFLINE_PUZZLE_COMPOSER_H
