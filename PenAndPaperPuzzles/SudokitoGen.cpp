#include "SudokitoGen.h"
#include "GeneratorUtils.h"
#include "EscPosPrinter.h"
#include "ThermalCanvas.h"

SudokitoGen::SudokitoGen() : _cluesCount(36) {
    memset(_puzzle, 0, sizeof(_puzzle));
}

bool SudokitoGen::isValid(uint8_t board[6][6], uint8_t row, uint8_t col, uint8_t num) {
    for (uint8_t i = 0; i < 6; i++) {
        if (board[row][i] == num || board[i][col] == num) {
            return false;
        }
    }
    uint8_t boxR = (row / 2) * 2;
    uint8_t boxC = (col / 3) * 3;
    for (uint8_t r = boxR; r < boxR + 2; r++) {
        for (uint8_t c = boxC; c < boxC + 3; c++) {
            if (board[r][c] == num) {
                return false;
            }
        }
    }
    return true;
}

bool SudokitoGen::fillBoard(uint8_t board[6][6]) {
    for (uint8_t r = 0; r < 6; r++) {
        for (uint8_t c = 0; c < 6; c++) {
            if (board[r][c] == 0) {
                uint8_t nums[6] = {1, 2, 3, 4, 5, 6};
                mp_shuffle(nums, 6);
                for (uint8_t i = 0; i < 6; i++) {
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

uint8_t SudokitoGen::countSolutions(uint8_t board[6][6], uint8_t maxCount) {
    for (uint8_t r = 0; r < 6; r++) {
        for (uint8_t c = 0; c < 6; c++) {
            if (board[r][c] == 0) {
                uint8_t count = 0;
                for (uint8_t num = 1; num <= 6; num++) {
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

void SudokitoGen::generate(SudokitoDifficulty difficulty) {
    uint8_t targetClues = 14;
    if (difficulty == SUDOKITO_EASY) targetClues = 18;
    else if (difficulty == SUDOKITO_HARD) targetClues = 11;

    // 1. Fill random solved 6x6 board
    uint8_t solution[6][6] = {0};
    fillBoard(solution);

    // 2. Clone to puzzle
    memcpy(_puzzle, solution, sizeof(_puzzle));

    // 3. Prepare 18 cell pairs with 180-degree rotational symmetry:
    // Pair i corresponds to (r, c) and (5 - r, 5 - c)
    uint8_t pairCoords[18][2];
    uint8_t pairCount = 0;
    bool visited[6][6] = {false};

    for (uint8_t r = 0; r < 6; r++) {
        for (uint8_t c = 0; c < 6; c++) {
            if (!visited[r][c]) {
                pairCoords[pairCount][0] = r * 6 + c;
                pairCoords[pairCount][1] = (5 - r) * 6 + (5 - c);
                visited[r][c] = true;
                visited[5 - r][5 - c] = true;
                pairCount++;
            }
        }
    }

    uint8_t pairOrder[18];
    for (uint8_t i = 0; i < 18; i++) pairOrder[i] = i;
    mp_shuffle(pairOrder, 18);

    _cluesCount = 36;
    for (uint8_t i = 0; i < 18; i++) {
        if (_cluesCount <= targetClues) break;

        uint8_t pIdx = pairOrder[i];
        uint8_t c1 = pairCoords[pIdx][0];
        uint8_t c2 = pairCoords[pIdx][1];

        uint8_t r1 = c1 / 6, col1 = c1 % 6;
        uint8_t r2 = c2 / 6, col2 = c2 % 6;

        uint8_t backup1 = _puzzle[r1][col1];
        uint8_t backup2 = _puzzle[r2][col2];

        _puzzle[r1][col1] = 0;
        _puzzle[r2][col2] = 0;

        if (countSolutions(_puzzle, 2) != 1) {
            _puzzle[r1][col1] = backup1;
            _puzzle[r2][col2] = backup2;
        } else {
            _cluesCount -= 2;
        }
    }

    // Secondary pass for odd targets (e.g. 11 clues)
    if (_cluesCount > targetClues) {
        uint8_t singles[36];
        uint8_t sCount = 0;
        for (uint8_t i = 0; i < 36; i++) {
            if (_puzzle[i / 6][i % 6] != 0) {
                singles[sCount++] = i;
            }
        }
        mp_shuffle(singles, sCount);
        for (uint8_t i = 0; i < sCount; i++) {
            if (_cluesCount <= targetClues) break;
            uint8_t pos = singles[i];
            uint8_t r = pos / 6, c = pos % 6;
            uint8_t backup = _puzzle[r][c];
            _puzzle[r][c] = 0;
            if (countSolutions(_puzzle, 2) != 1) {
                _puzzle[r][c] = backup;
            } else {
                _cluesCount--;
            }
        }
    }
}

void SudokitoGen::printToReceipt(EscPosPrinter& printer, SudokitoDifficulty /*diff*/) {
    printer.println("      +-------+-------+");
    for (uint8_t r = 0; r < 6; r++) {
        String line = "      | ";
        for (uint8_t c = 0; c < 6; c++) {
            uint8_t val = _puzzle[r][c];
            if (val == 0) line += ". ";
            else line += String(val) + " ";
            if (c == 2) line += "| ";
        }
        line += "|";
        printer.println(line);

        if (r == 1 || r == 3) {
            printer.println("      +-------+-------+");
        }
    }
    printer.println("      +-------+-------+");
    printer.println("");
}

bool SudokitoGen::printRasterToReceipt(EscPosPrinter& printer, SudokitoDifficulty /*diff*/) {
    const int16_t padding = 24;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2; // 528
    const int16_t cellSize = boardSize / 6; // 88
    const int16_t totalH = padding + cellSize * 6 + padding; // 576

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Horizontal grid lines
    for (int i = 0; i <= 6; i++) {
        int16_t pos = padding + i * cellSize;
        bool isMajor = (i % 2 == 0);
        canvas.drawHLine(padding, pos, cellSize * 6, isMajor ? 4 : 1);
    }

    // Vertical grid lines
    for (int i = 0; i <= 6; i++) {
        int16_t pos = padding + i * cellSize;
        bool isMajor = (i % 3 == 0);
        canvas.drawVLine(pos, padding, cellSize * 6, isMajor ? 4 : 1);
    }

    // Digits
    for (uint8_t r = 0; r < 6; r++) {
        for (uint8_t c = 0; c < 6; c++) {
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
