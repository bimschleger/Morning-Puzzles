#ifndef FUTOSHIKI_GEN_H
#define FUTOSHIKI_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum FutoshikiDifficulty {
    FUTOSHIKI_EASY   = 0, // 4x4
    FUTOSHIKI_MEDIUM = 1, // 5x5
    FUTOSHIKI_HARD   = 2  // 6x6
};

class FutoshikiGen {
public:
    static const uint8_t MAX_SIZE = 6;

    FutoshikiGen();

    void generate(FutoshikiDifficulty difficulty = FUTOSHIKI_MEDIUM, uint32_t seed = 0);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }
    uint8_t getSolution(uint8_t r, uint8_t c) const { return (r < _size && c < _size) ? _solution[r][c] : 0; }
    uint8_t getGiven(uint8_t r, uint8_t c) const { return (r < _size && c < _size) ? _givens[r][c] : 0; }
    uint8_t getEdgeH(uint8_t r, uint8_t c) const { return (r < _size && c < _size - 1) ? _edges_h[r][c] : 0; }
    uint8_t getEdgeV(uint8_t r, uint8_t c) const { return (r < _size - 1 && c < _size) ? _edges_v[r][c] : 0; }

private:
    uint8_t _size;
    uint8_t _cellSize;
    uint16_t _height;
    uint8_t _solution[MAX_SIZE][MAX_SIZE];
    uint8_t _givens[MAX_SIZE][MAX_SIZE];
    uint8_t _edges_h[MAX_SIZE][MAX_SIZE - 1];
    uint8_t _edges_v[MAX_SIZE - 1][MAX_SIZE];

    void applyTransform(uint8_t transform);
};

#endif // FUTOSHIKI_GEN_H
