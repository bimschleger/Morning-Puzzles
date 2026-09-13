#ifndef LIGHTS_GEN_H
#define LIGHTS_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum LightsDifficulty {
    LIGHTS_EASY    = 0, // 6x6 grid
    LIGHTS_MEDIUM  = 1, // 8x8 grid
    LIGHTS_HARD    = 2, // 10x10 grid
    LIGHTS_EXTREME = 3  // 12x12 grid
};

class LightsGen {
public:
    LightsGen();

    // Generates a 100% deducible no-guess Lights (Akari) puzzle
    void generate(LightsDifficulty difficulty = LIGHTS_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, LightsDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, LightsDifficulty diff);

    int8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getSize() const { return _size; }
    uint8_t getTotalBulbs() const { return _totalBulbs; }
    bool isBulb(uint8_t r, uint8_t c) const { return _solution[r][c] == 1; }

private:
    uint8_t _size;
    uint8_t _totalBulbs;
    int8_t  _puzzle[12][12];   // -1 = white cell, -2 = unnumbered wall, 0..4 = numbered wall
    int8_t  _solution[12][12]; // 1 = bulb, 0 = no bulb

    bool solveDeductive(int8_t puz[12][12], uint8_t size, int8_t sol[12][12]);
};

#endif // LIGHTS_GEN_H
