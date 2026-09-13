#ifndef MINES_GEN_H
#define MINES_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum MinesDifficulty {
    MINES_EASY   = 0, // 8x8, 8 mines, ~28 clues
    MINES_MEDIUM = 1, // 8x8, 12 mines, ~22 clues
    MINES_HARD   = 2  // 8x8, 15 mines, ~17 clues
};

class MinesGen {
public:
    MinesGen();

    // Generates a 100% deducible no-guess Minesweeper puzzle
    void generate(MinesDifficulty difficulty = MINES_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, MinesDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, MinesDifficulty diff);

    int8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getRows() const { return 8; }
    uint8_t getCols() const { return 8; }
    uint8_t getTotalMines() const { return _totalMines; }
    uint8_t getCluesCount() const { return _cluesCount; }
    bool isMine(uint8_t r, uint8_t c) const { return _solution[r][c] == 1; }

private:
    uint8_t _totalMines;
    uint8_t _cluesCount;
    int8_t _puzzle[8][8];   // -1 = unrevealed, 0..8 = clue count
    int8_t _solution[8][8]; // 0 = safe, 1 = mine

    bool solveDeductive(int8_t puzzle[8][8], uint8_t totalMines);
};

#endif // MINES_GEN_H
