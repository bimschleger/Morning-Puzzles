#ifndef MAZE_GEN_H
#define MAZE_GEN_H

#include <Arduino.h>

class EscPosPrinter;

enum MazeDifficulty {
    MAZE_EASY    = 0, // 10x10, cell_size=48, wall_t=4
    MAZE_MEDIUM  = 1, // 20x20, cell_size=24, wall_t=3
    MAZE_HARD    = 2, // 30x30, cell_size=16, wall_t=2
    MAZE_EXTREME = 3  // 40x40, cell_size=12, wall_t=2
};

class MazeGen {
public:
    MazeGen();

    void generate(MazeDifficulty diff = MAZE_MEDIUM, uint32_t seed = 0);

    void printToReceipt(EscPosPrinter& printer, MazeDifficulty diff = MAZE_MEDIUM);
    bool printRasterToReceipt(EscPosPrinter& printer, MazeDifficulty diff = MAZE_MEDIUM);

    uint8_t getSize() const { return _size; }
    uint8_t getCellSize() const { return _cellSize; }
    uint8_t getWallThickness() const { return _wallThickness; }
    uint8_t getWallH(uint8_t r, uint8_t c) const;
    uint8_t getWallV(uint8_t r, uint8_t c) const;

    uint16_t getSolutionMoveCount() const { return _solutionMoveCount; }
    char getSolutionMoveDir(uint16_t idx) const { return _solutionMoves[idx].dir; }
    uint8_t getSolutionMoveSteps(uint16_t idx) const { return _solutionMoves[idx].steps; }

private:
    struct MoveStep {
        char dir;
        uint8_t steps;
    };

    uint8_t _size;
    uint8_t _cellSize;
    uint8_t _wallThickness;

    // Max size 40x40:
    // walls_h: (N-1) * N <= 39 * 40 = 1560 bits = 195 bytes
    // walls_v: N * (N-1) <= 40 * 39 = 1560 bits = 195 bytes
    uint8_t _wallsH[195];
    uint8_t _wallsV[195];

    MoveStep _solutionMoves[300];
    uint16_t _solutionMoveCount;

    void setWallH(uint8_t r, uint8_t c, uint8_t val);
    void setWallV(uint8_t r, uint8_t c, uint8_t val);
    void solvePath();
};

#endif // MAZE_GEN_H
