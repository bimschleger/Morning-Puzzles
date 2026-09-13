#ifndef NONOGRAM_GEN_H
#define NONOGRAM_GEN_H

#include <Arduino.h>
#include <vector>
class EscPosPrinter;

enum NonogramDifficulty {
    NONO_EASY   = 0, // 5x5
    NONO_MEDIUM = 1, // 8x8
    NONO_HARD   = 2  // 10x10
};

class NonogramGen {
public:
    static const uint8_t MAX_SIZE = 10;

    NonogramGen();

    void generate(NonogramDifficulty difficulty = NONO_EASY);
    void printToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }

private:
    uint8_t _size;
    uint8_t _grid[MAX_SIZE][MAX_SIZE];
    std::vector<uint8_t> _rowClues[MAX_SIZE];
    std::vector<uint8_t> _colClues[MAX_SIZE];

    void calculateClues();
};

#endif // NONOGRAM_GEN_H
