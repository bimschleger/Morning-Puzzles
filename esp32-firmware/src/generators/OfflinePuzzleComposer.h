#ifndef OFFLINE_PUZZLE_COMPOSER_H
#define OFFLINE_PUZZLE_COMPOSER_H

#include <Arduino.h>
class EscPosPrinter;
#include "SudokuGen.h"
#include "WordSearchGen.h"
#include "NonogramGen.h"
#include "QueensGen.h"
#include "JumbleGen.h"
#include "BinaryGen.h"
#include "MinesGen.h"

enum PuzzleGrade {
    GRADE_EASY = 0,
    GRADE_MEDIUM = 1,
    GRADE_HARD = 2,
    GRADE_ROTATING = 3
};

class OfflinePuzzleComposer {
public:
    OfflinePuzzleComposer();

    // Generates a complete random bundle of all 7 puzzles on the ESP32 and prints directly
    bool generateAndPrintReceipt(EscPosPrinter& printer, const String& dateStr = "", PuzzleGrade grade = GRADE_ROTATING);

    void cycleGrade();
    void setGrade(PuzzleGrade grade);
    PuzzleGrade getCurrentGrade() const;
    const char* getGradeName(PuzzleGrade grade) const;

private:
    SudokuGen     _sudoku;
    WordSearchGen _wordSearch;
    NonogramGen   _nonogram;
    QueensGen     _queens;
    JumbleGen     _jumble;
    BinaryGen     _binary;
    MinesGen      _mines;

    PuzzleGrade   _currentGrade;
    uint8_t       _rotationIndex;
};

#endif // OFFLINE_PUZZLE_COMPOSER_H
