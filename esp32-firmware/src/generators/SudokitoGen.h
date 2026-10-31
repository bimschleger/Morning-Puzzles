#ifndef SUDOKITO_GEN_H
#define SUDOKITO_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum SudokitoDifficulty {
    SUDOKITO_EASY   = 0, // 18 clues
    SUDOKITO_MEDIUM = 1, // 14 clues
    SUDOKITO_HARD   = 2  // 11 clues
};

class SudokitoGen {
public:
    SudokitoGen();

    // Generates a new random board on the fly with unique solution and 180-deg rotational symmetry
    void generate(SudokitoDifficulty difficulty = SUDOKITO_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, SudokitoDifficulty diff);
    bool printRasterToReceipt(EscPosPrinter& printer, SudokitoDifficulty diff);

    uint8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getCluesCount() const { return _cluesCount; }

private:
    uint8_t _puzzle[6][6];
    uint8_t _cluesCount;

    bool isValid(uint8_t board[6][6], uint8_t row, uint8_t col, uint8_t num);
    bool fillBoard(uint8_t board[6][6]);
    uint8_t countSolutions(uint8_t board[6][6], uint8_t maxCount = 2);
};

#endif // SUDOKITO_GEN_H
