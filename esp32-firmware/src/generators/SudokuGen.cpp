#include "SudokuGen.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

SudokuGen::SudokuGen() : _cluesCount(81) {
    memset(_solution, 0, sizeof(_solution));
    memset(_puzzle, 0, sizeof(_puzzle));
}

void SudokuGen::shuffleArray(uint8_t* arr, uint8_t n) {
    for (uint8_t i = n - 1; i > 0; i--) {
        uint8_t j = random(i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

bool SudokuGen::isValid(uint8_t board[9][9], uint8_t row, uint8_t col, uint8_t num) {
    for (uint8_t i = 0; i < 9; i++) {
        if (board[row][i] == num || board[i][col] == num) {
            return false;
        }
    }
    uint8_t boxR = (row / 3) * 3;
    uint8_t boxC = (col / 3) * 3;
    for (uint8_t r = boxR; r < boxR + 3; r++) {
        for (uint8_t c = boxC; c < boxC + 3; c++) {
            if (board[r][c] == num) {
                return false;
            }
        }
    }
    return true;
}

bool SudokuGen::fillBoard(uint8_t board[9][9]) {
    for (uint8_t r = 0; r < 9; r++) {
        for (uint8_t c = 0; c < 9; c++) {
            if (board[r][c] == 0) {
                uint8_t nums[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
                shuffleArray(nums, 9);
                for (uint8_t i = 0; i < 9; i++) {
                    uint8_t num = nums[i];
                    if (isValid(board, r, c, num)) {
                        board[r][c] = num;
                        if (fillBoard(board)) {
                            return true;
                        }
                        board[r][c] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

uint8_t SudokuGen::countSolutions(uint8_t board[9][9], uint8_t maxCount) {
    for (uint8_t r = 0; r < 9; r++) {
        for (uint8_t c = 0; c < 9; c++) {
            if (board[r][c] == 0) {
                uint8_t count = 0;
                for (uint8_t num = 1; num <= 9; num++) {
                    if (isValid(board, r, c, num)) {
                        board[r][c] = num;
                        count += countSolutions(board, maxCount);
                        board[r][c] = 0;
                        if (count >= maxCount) {
                            return count;
                        }
                    }
                }
                return count;
            }
        }
    }
    return 1;
}

void SudokuGen::generate(SudokuDifficulty difficulty) {
    uint8_t targetClues = 30;
    if (difficulty == SUDOKU_EASY) targetClues = 38;
    else if (difficulty == SUDOKU_HARD) targetClues = 25;

    // 1. Fill random solved board
    memset(_solution, 0, sizeof(_solution));
    fillBoard(_solution);

    // 2. Clone to puzzle
    memcpy(_puzzle, _solution, sizeof(_puzzle));

    // 3. Prepare list of 81 coordinates
    uint8_t cells[81];
    for (uint8_t i = 0; i < 81; i++) cells[i] = i;
    shuffleArray(cells, 81);

    _cluesCount = 81;
    for (uint8_t i = 0; i < 81; i++) {
        if (_cluesCount <= targetClues) break;

        uint8_t pos = cells[i];
        uint8_t r = pos / 9;
        uint8_t c = pos % 9;

        uint8_t backup = _puzzle[r][c];
        _puzzle[r][c] = 0;

        // Check if solution remains unique
        if (countSolutions(_puzzle, 2) != 1) {
            _puzzle[r][c] = backup; // Restore
        } else {
            _cluesCount--;
        }
    }
}

void SudokuGen::printToReceipt(EscPosPrinter& printer, SudokuDifficulty diff) {
    const char* diffStr = (diff == SUDOKU_EASY) ? "EASY" : ((diff == SUDOKU_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- SUDOKU ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Fill every row, column, and 3x3 box with digits");
    printer.println("1-9 without repeating.");
    printer.println("");

    printer.println("   +-------+-------+-------+");
    for (uint8_t r = 0; r < 9; r++) {
        String line = "   | ";
        for (uint8_t c = 0; c < 9; c++) {
            uint8_t val = _puzzle[r][c];
            if (val == 0) line += ". ";
            else line += String(val) + " ";
            if (c == 2 || c == 5) line += "| ";
        }
        line += "|";
        printer.println(line);

        if (r == 2 || r == 5) {
            printer.println("   +-------+-------+-------+");
        }
    }
    printer.println("   +-------+-------+-------+");
    printer.println("");
}

bool SudokuGen::printRasterToReceipt(EscPosPrinter& printer, SudokuDifficulty diff) {
    const char* diffStr = (diff == SUDOKU_EASY) ? "EASY" : ((diff == SUDOKU_HARD) ? "HARD" : "MEDIUM");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- SUDOKU ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Fill every row, column, and 3x3 box with digits");
    printer.println("1-9 without repeating.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t padding = 24;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2; // 528
    const int16_t cellSize = boardSize / 9; // 58
    const int16_t totalH = padding + cellSize * 9 + padding; // 570

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Grid lines
    for (int i = 0; i <= 9; i++) {
        int16_t pos = padding + i * cellSize;
        bool isMajor = (i % 3 == 0);
        canvas.drawHLine(padding, pos, cellSize * 9, isMajor ? 4 : 1);
        canvas.drawVLine(pos, padding, cellSize * 9, isMajor ? 4 : 1);
    }

    // Digits
    for (uint8_t r = 0; r < 9; r++) {
        for (uint8_t c = 0; c < 9; c++) {
            uint8_t val = _puzzle[r][c];
            if (val != 0) {
                int16_t cx = padding + c * cellSize + (cellSize - 18) / 2;
                int16_t cy = padding + r * cellSize + (cellSize - 21) / 2;
                canvas.drawChar(cx, cy, '0' + val, 3);
            }
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

