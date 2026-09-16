#ifndef OFFLINE_PUZZLE_COMPOSER_H
#define OFFLINE_PUZZLE_COMPOSER_H

#include <Arduino.h>
class EscPosPrinter;
#include "../config/OfflineConfigManager.h"
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

class OfflinePuzzleComposer {
public:
    OfflinePuzzleComposer();

    // Generates a random selection of puzzles from enabled games pool and prints directly
    bool generateAndPrintReceipt(EscPosPrinter& printer, 
                                 const String& subtitle = "Enjoy your morning puzzles", 
                                 PuzzleGrade grade = (PuzzleGrade)-1,
                                 const OfflineConfigManager* config = nullptr);

    void cycleGrade();
    void setGrade(PuzzleGrade grade);
    PuzzleGrade getCurrentGrade() const;
    const char* getGradeName(PuzzleGrade grade) const;

    PuzzleGrade getGradeForSlot(uint8_t index, uint8_t totalCount) const;
    bool supportsExtreme(OfflinePuzzleType type) const;

private:
    void printSinglePuzzle(EscPosPrinter& printer, OfflinePuzzleType type, bool useRaster, PuzzleGrade grade = GRADE_MEDIUM);

    PuzzleGrade   _currentGrade;
    uint8_t       _rotationIndex;
};

#endif // OFFLINE_PUZZLE_COMPOSER_H
