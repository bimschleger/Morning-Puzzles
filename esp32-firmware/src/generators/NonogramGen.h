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
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }
    const std::vector<uint8_t>& getRowClues(uint8_t r) const { return _rowClues[r]; }
    const std::vector<uint8_t>& getColClues(uint8_t c) const { return _colClues[c]; }

private:
    uint8_t _size;
    uint8_t _grid[MAX_SIZE][MAX_SIZE];
    std::vector<uint8_t> _rowClues[MAX_SIZE];
    std::vector<uint8_t> _colClues[MAX_SIZE];

    void calculateClues();
};

#endif // NONOGRAM_GEN_H
