#ifndef QUEENS_GEN_H
#define QUEENS_GEN_H

#include <Arduino.h>
#include <vector>
class EscPosPrinter;

enum QueensDifficulty {
    QUEENS_EASY   = 0, // 6x6, 1-Star
    QUEENS_MEDIUM = 1, // 8x8, 1-Star
    QUEENS_HARD   = 2, // 9x9, 2-Star
    QUEENS_MASTER = 3  // 10x10, 2-Star
};

struct StarPos {
    uint8_t row;
    uint8_t col;
};

class QueensGen {
public:
    static const uint8_t MAX_SIZE = 10;

    QueensGen();

    void generate(QueensDifficulty difficulty = QUEENS_MEDIUM);
    void printToReceipt(EscPosPrinter& printer);

    bool validate();

    uint8_t getSize() const { return _size; }
    uint8_t getStarsPerUnit() const { return _starsPerUnit; }

private:
    uint8_t _size;
    uint8_t _starsPerUnit;
    int8_t _regions[MAX_SIZE][MAX_SIZE];
    std::vector<StarPos> _stars;

    bool placeStarsBacktrack(uint8_t row, uint8_t starsPlacedInRow, uint8_t* colCounts);
    bool canPlaceStar(uint8_t r, uint8_t c, uint8_t* colCounts);
    void growRegions();
};

#endif // QUEENS_GEN_H
