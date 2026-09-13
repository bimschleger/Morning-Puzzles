#ifndef LOOP_GEN_H
#define LOOP_GEN_H

#include <Arduino.h>

class EscPosPrinter;

enum LoopDifficulty {
    LOOP_EASY   = 0, // 6x6 grid
    LOOP_MEDIUM = 1, // 7x7 grid
    LOOP_HARD   = 2  // 9x9 grid
};

class LoopGen {
public:
    LoopGen();

    void generate(LoopDifficulty difficulty = LOOP_MEDIUM);

    void printToReceipt(EscPosPrinter& printer, LoopDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, LoopDifficulty diff);

    uint8_t getSize() const { return _size; }
    int8_t  getClue(uint8_t r, uint8_t c) const { return _clues[r][c]; }
    uint8_t getH(uint8_t r, uint8_t c) const { return _solutionH[r][c]; }
    uint8_t getV(uint8_t r, uint8_t c) const { return _solutionV[r][c]; }

private:
    uint8_t _size;
    int8_t  _clues[9][9];       // -1 = unhinted, 0..3 = edge count clue
    uint8_t _solutionH[10][9];  // (size + 1) x size horizontal loop segments
    uint8_t _solutionV[9][10];  // size x (size + 1) vertical loop segments

    bool generatePolyominoLoop(uint8_t n);
    bool solveDeductive(int8_t clues[9][9], uint8_t n, int8_t H[10][9], int8_t V[9][10]);
};

#endif // LOOP_GEN_H
