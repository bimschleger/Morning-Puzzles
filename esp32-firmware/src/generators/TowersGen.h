#ifndef TOWERS_GEN_H
#define TOWERS_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum TowersDifficulty {
    TOWERS_EASY   = 0, // 4x4
    TOWERS_MEDIUM = 1, // 5x5
    TOWERS_HARD   = 2  // 6x6
};

class TowersGen {
public:
    static const uint8_t MAX_SIZE = 6;

    TowersGen();

    void generate(TowersDifficulty difficulty = TOWERS_MEDIUM, uint32_t seed = 0);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }
    uint8_t getSolution(uint8_t r, uint8_t c) const { return (r < _size && c < _size) ? _solution[r][c] : 0; }
    uint8_t getTopClue(uint8_t c) const { return (c < _size) ? _top[c] : 0; }
    uint8_t getBottomClue(uint8_t c) const { return (c < _size) ? _bottom[c] : 0; }
    uint8_t getLeftClue(uint8_t r) const { return (r < _size) ? _left[r] : 0; }
    uint8_t getRightClue(uint8_t r) const { return (r < _size) ? _right[r] : 0; }

private:
    uint8_t _size;
    uint8_t _cellSize;
    uint16_t _height;
    uint8_t _solution[MAX_SIZE][MAX_SIZE];
    uint8_t _top[MAX_SIZE];
    uint8_t _bottom[MAX_SIZE];
    uint8_t _left[MAX_SIZE];
    uint8_t _right[MAX_SIZE];

    void applyTransform(uint8_t transform);
};

#endif // TOWERS_GEN_H
