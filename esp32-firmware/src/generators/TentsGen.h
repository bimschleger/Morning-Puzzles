#ifndef TENTS_GEN_H
#define TENTS_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum TentsDifficulty {
    TENTS_EASY   = 0, // 6x6, 4 trees/tents
    TENTS_MEDIUM = 1, // 8x8, 8 trees/tents
    TENTS_HARD   = 2  // 8x8, 11 trees/tents
};

class TentsGen {
public:
    TentsGen();

    void generate(TentsDifficulty difficulty = TENTS_MEDIUM);
    void printToReceipt(EscPosPrinter& printer, TentsDifficulty diff);

    uint8_t getSize() const { return _size; }
    uint8_t getTreeCount() const { return _treeCount; }
    uint8_t getRowClue(uint8_t r) const { return _rowClues[r]; }
    uint8_t getColClue(uint8_t c) const { return _colClues[c]; }
    bool isTree(uint8_t r, uint8_t c) const { return _puzzle[r][c] == 1; }
    bool isTent(uint8_t r, uint8_t c) const { return _solution[r][c] == 2; }

private:
    uint8_t _size;
    uint8_t _treeCount;
    uint8_t _rowClues[8];
    uint8_t _colClues[8];
    int8_t  _puzzle[8][8];   // 0 = empty, 1 = tree
    int8_t  _solution[8][8]; // 0 = empty, 1 = tree, 2 = tent
};

#endif // TENTS_GEN_H
