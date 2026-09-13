#ifndef BRIDGES_GEN_H
#define BRIDGES_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum BridgesDifficulty {
    BRIDGES_EASY   = 0, // 6x6, 8 islands, max degree 4
    BRIDGES_MEDIUM = 1, // 8x8, 10 islands, max degree 6
    BRIDGES_HARD   = 2  // 8x8, 14 islands, max degree 8
};

struct IslandInfo {
    uint8_t r;
    uint8_t c;
    uint8_t count;
};

struct BridgeEdge {
    uint8_t r1, c1;
    uint8_t r2, c2;
    uint8_t count; // 1 or 2
};

class BridgesGen {
public:
    BridgesGen();

    void generate(BridgesDifficulty difficulty = BRIDGES_MEDIUM);
    void printToReceipt(EscPosPrinter& printer, BridgesDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, BridgesDifficulty diff);

    uint8_t getSize() const { return _size; }
    uint8_t getIslandCount() const { return _islandCount; }
    IslandInfo getIsland(uint8_t i) const { return _islands[i]; }
    uint8_t getBridgeCount() const { return _bridgeCount; }
    BridgeEdge getBridge(uint8_t i) const { return _bridges[i]; }

private:
    uint8_t _size;
    uint8_t _islandCount;
    IslandInfo _islands[16];
    uint8_t _bridgeCount;
    BridgeEdge _bridges[32];
};

#endif // BRIDGES_GEN_H
