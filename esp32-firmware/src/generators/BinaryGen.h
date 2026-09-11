#ifndef BINARY_GEN_H
#define BINARY_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum BinaryDifficulty {
    BINARY_EASY   = 0, // 6x6, ~16 clues, trio & count rules
    BINARY_MEDIUM = 1, // 8x8, ~28 clues, 1-step lookahead
    BINARY_HARD   = 2  // 8x8, ~22 clues, line uniqueness comparison
};

class BinaryGen {
public:
    BinaryGen();

    // Generates a new random board on the fly with a unique, deducible solution
    void generate(BinaryDifficulty difficulty = BINARY_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, BinaryDifficulty diff);

    int8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getSize() const { return _size; }
    uint8_t getCluesCount() const { return _cluesCount; }
    int8_t getSolutionCell(uint8_t r, uint8_t c) const { return _solution[r][c]; }

private:
    uint8_t _size;
    uint8_t _cluesCount;
    int8_t _solution[8][8];
    int8_t _puzzle[8][8];

    // Helper functions for board generation and deduction
    bool generateFullBoard();
    bool solveDeductive(int8_t grid[8][8], uint8_t maxRule);
};

#endif // BINARY_GEN_H
