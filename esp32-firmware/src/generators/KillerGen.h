#ifndef KILLER_GEN_H
#define KILLER_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum KillerDifficulty {
    KILLER_EASY    = 0, // 4x4, digits 1-4
    KILLER_MEDIUM  = 1, // 4x4, digits 1-4, zero singles
    KILLER_EXTREME = 2  // 6x6, digits 1-6, zero singles
};

class KillerGen {
public:
    static const uint8_t MAX_SIZE = 6;
    static const uint8_t MAX_CAGES = 18;

    KillerGen();

    void generate(KillerDifficulty difficulty = KILLER_MEDIUM, uint32_t seed = 0);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getSize() const { return _size; }
    uint8_t getBoxRows() const { return _boxRows; }
    uint8_t getBoxCols() const { return _boxCols; }
    uint8_t getNumCages() const { return _numCages; }
    uint8_t getCage(uint8_t r, uint8_t c) const { return (r < _size && c < _size) ? _cageMap[r][c] : 0; }
    uint8_t getCageSum(uint8_t cageId) const { return (cageId < _numCages) ? _cageSums[cageId] : 0; }
    uint8_t getSolution(uint8_t r, uint8_t c) const { return (r < _size && c < _size) ? _solution[r][c] : 0; }

private:
    uint8_t _size;
    uint8_t _boxRows;
    uint8_t _boxCols;
    uint8_t _numCages;
    uint8_t _cageMap[MAX_SIZE][MAX_SIZE];
    uint8_t _solution[MAX_SIZE][MAX_SIZE];
    uint8_t _cageSums[MAX_CAGES];

    void applyTransform(uint8_t transform);
};

#endif // KILLER_GEN_H
