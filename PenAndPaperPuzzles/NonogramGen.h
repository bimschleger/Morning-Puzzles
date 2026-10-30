#ifndef NONOGRAM_GEN_H
#define NONOGRAM_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum NonogramDifficulty {
    NONO_EASY   = 0, // 5x5
    NONO_MEDIUM = 1, // 8x8
    NONO_HARD   = 2  // 10x10
};

struct ClueList {
    uint8_t data[5];
    uint8_t count;
    ClueList() : count(0) {}
    size_t size() const { return count; }
    uint8_t operator[](size_t i) const { return (i < count) ? data[i] : 0; }
    void push_back(uint8_t val) { if (count < 5) data[count++] = val; }
    void clear() { count = 0; }
    bool empty() const { return count == 0; }
    const uint8_t* begin() const { return data; }
    const uint8_t* end() const { return data + count; }
};

class NonogramGen {
public:
    static const uint8_t MAX_SIZE = 10;

    NonogramGen();

    void generate(NonogramDifficulty difficulty = NONO_EASY);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }
    const ClueList& getRowClues(uint8_t r) const { return _rowClues[r]; }
    const ClueList& getColClues(uint8_t c) const { return _colClues[c]; }

private:
    uint8_t _size;
    uint8_t _grid[MAX_SIZE][MAX_SIZE];
    ClueList _rowClues[MAX_SIZE];
    ClueList _colClues[MAX_SIZE];

    void calculateClues();
};

#endif // NONOGRAM_GEN_H
