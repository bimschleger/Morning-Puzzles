#ifndef SUDOKU_GEN_H
#define SUDOKU_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum SudokuDifficulty {
    SUDOKU_EASY   = 0, // ~38 clues
    SUDOKU_MEDIUM = 1, // ~30 clues
    SUDOKU_HARD   = 2  // ~25 clues
};

class SudokuGen {
public:
    SudokuGen();

    // Generates a new random board on the fly with unique solution
    void generate(SudokuDifficulty difficulty = SUDOKU_MEDIUM);

    // Prints formatted 80mm receipt section
    void printToReceipt(EscPosPrinter& printer, SudokuDifficulty diff);

    uint8_t getCell(uint8_t r, uint8_t c) const { return _puzzle[r][c]; }
    uint8_t getCluesCount() const { return _cluesCount; }

private:
    uint8_t _solution[9][9];
    uint8_t _puzzle[9][9];
    uint8_t _cluesCount;

    bool isValid(uint8_t board[9][9], uint8_t row, uint8_t col, uint8_t num);
    bool fillBoard(uint8_t board[9][9]);
    uint8_t countSolutions(uint8_t board[9][9], uint8_t maxCount = 2);
    void shuffleArray(uint8_t* arr, uint8_t n);
};

#endif // SUDOKU_GEN_H
