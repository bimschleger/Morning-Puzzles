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
#include "TentsGen.h"
#include "BridgesGen.h"
#include "TangoGen.h"
#include "WheelGen.h"
#include "LightsGen.h"
#include "LoopGen.h"

enum PuzzleGrade {
    GRADE_EASY = 0,
    GRADE_MEDIUM = 1,
    GRADE_HARD = 2,
    GRADE_ROTATING = 3,
    GRADE_RANDOM = 4,
    GRADE_EXTREME = 5
};

enum OfflinePuzzleType {
    PUZZLE_SUDOKU = 0,
    PUZZLE_WORDSEARCH,
    PUZZLE_NONOGRAM,
    PUZZLE_QUEENS,
    PUZZLE_JUMBLE,
    PUZZLE_BINARY,
    PUZZLE_MINES,
    PUZZLE_TENTS,
    PUZZLE_BRIDGES,
    PUZZLE_TANGO,
    PUZZLE_WHEEL,
    PUZZLE_LIGHTS,
    PUZZLE_LOOP,
    OFFLINE_PUZZLE_TOTAL
};

class OfflinePuzzleComposer {
public:
    OfflinePuzzleComposer();

    // Generates a random selection of puzzles (OFFLINE_PUZZLE_COUNT) and prints directly
    bool generateAndPrintReceipt(EscPosPrinter& printer, const String& subtitle = "Enjoy your morning puzzles", PuzzleGrade grade = GRADE_RANDOM);

    void cycleGrade();
    void setGrade(PuzzleGrade grade);
    PuzzleGrade getCurrentGrade() const;
    const char* getGradeName(PuzzleGrade grade) const;

    PuzzleGrade getGradeForSlot(uint8_t index, uint8_t totalCount) const;
    bool supportsExtreme(OfflinePuzzleType type) const;

private:
    void printSinglePuzzle(EscPosPrinter& printer, OfflinePuzzleType type, bool useRaster, PuzzleGrade grade = GRADE_MEDIUM);

    SudokuGen     _sudoku;
    WordSearchGen _wordSearch;
    NonogramGen   _nonogram;
    QueensGen     _queens;
    JumbleGen     _jumble;
    BinaryGen     _binary;
    MinesGen      _mines;
    TentsGen      _tents;
    BridgesGen    _bridges;
    TangoGen      _tango;
    WheelGen      _wheel;
    LightsGen     _lights;
    LoopGen       _loop;

    PuzzleGrade   _currentGrade;
    uint8_t       _rotationIndex;
};

#endif // OFFLINE_PUZZLE_COMPOSER_H
