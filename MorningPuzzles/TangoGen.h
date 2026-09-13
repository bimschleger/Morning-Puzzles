#ifndef TANGO_GEN_H
#define TANGO_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum TangoDifficulty {
    TANGO_EASY   = 0, // 6x6, 6 numbers, 6 edges
    TANGO_MEDIUM = 1, // 6x6, 4 numbers, 8 edges
    TANGO_HARD   = 2  // 8x8, 10 numbers, 14 edges
};

class TangoGen {
public:
    TangoGen();

    // Generates a new random board on the fly with a unique, deducible solution
    void generate(TangoDifficulty difficulty = TANGO_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, TangoDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, TangoDifficulty diff);

    int8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getEdgeH(uint8_t r, uint8_t c) const { return _edgesH[r][c]; }
    uint8_t getEdgeV(uint8_t r, uint8_t c) const { return _edgesV[r][c]; }
    uint8_t getSize() const { return _size; }
    uint8_t getNumbersCount() const { return _numbersCount; }
    uint8_t getEdgesCount() const { return _edgesCount; }
    int8_t getSolutionCell(uint8_t r, uint8_t c) const { return _solution[r][c]; }

private:
    uint8_t _size;
    uint8_t _numbersCount;
    uint8_t _edgesCount;
    int8_t _solution[8][8];
    int8_t _puzzle[8][8];
    uint8_t _edgesH[8][7];
    uint8_t _edgesV[7][8];

    // Helper functions for board generation and deduction
    bool generateFullBoard();
    bool isCandidateValid(int8_t g[8][8], uint8_t r, uint8_t c, int8_t val);
    bool solveDeductive(int8_t grid[8][8]);
};

#endif // TANGO_GEN_H
