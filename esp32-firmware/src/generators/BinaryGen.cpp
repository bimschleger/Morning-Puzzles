#include "BinaryGen.h"
#include "../printer/EscPosPrinter.h"
#include <string.h>

static const uint8_t VALID_LINES_6[14] = {
    0x0b, 0x0d, 0x13, 0x15, 0x16, 0x19, 0x1a, 0x25, 0x26, 0x29, 0x2a, 0x2c, 0x32, 0x34
};

static const uint8_t VALID_LINES_8[34] = {
    0x2b, 0x2d, 0x33, 0x35, 0x36, 0x4b, 0x4d, 0x53, 0x55, 0x56, 0x59, 0x5a,
    0x65, 0x66, 0x69, 0x6a, 0x6c, 0x93, 0x95, 0x96, 0x99, 0x9a, 0xa5, 0xa6,
    0xa9, 0xaa, 0xac, 0xb2, 0xb4, 0xc9, 0xca, 0xcc, 0xd2, 0xd4
};

BinaryGen::BinaryGen() : _size(8), _cluesCount(0) {
    memset(_solution, -1, sizeof(_solution));
    memset(_puzzle, -1, sizeof(_puzzle));
}

static void shuffleArray(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

bool BinaryGen::generateFullBoard() {
    const uint8_t* valids = (_size == 6) ? VALID_LINES_6 : VALID_LINES_8;
    const uint8_t numValids = (_size == 6) ? 14 : 34;
    const uint8_t half = _size / 2;

    uint8_t rowOrder[34];
    for (uint8_t i = 0; i < numValids; i++) rowOrder[i] = i;

    struct State {
        uint8_t candIdx;
        uint8_t order[34];
    } stack[8];

    int r = 0;
    for (uint8_t i = 0; i < numValids; i++) stack[0].order[i] = i;
    shuffleArray(stack[0].order, numValids);
    stack[0].candIdx = 0;

    while (r >= 0 && r < _size) {
        if (stack[r].candIdx >= numValids) {
            // Backtrack
            for (uint8_t c = 0; c < _size; c++) _solution[r][c] = -1;
            r--;
            if (r >= 0) stack[r].candIdx++;
            continue;
        }

        uint8_t mask = valids[stack[r].order[stack[r].candIdx]];
        int8_t cand[8];
        for (uint8_t c = 0; c < _size; c++) {
            cand[c] = (mask >> (_size - 1 - c)) & 1;
        }

        // Rule 4: Row uniqueness
        bool valid = true;
        for (int pr = 0; pr < r; pr++) {
            bool same = true;
            for (uint8_t c = 0; c < _size; c++) {
                if (_solution[pr][c] != cand[c]) { same = false; break; }
            }
            if (same) { valid = false; break; }
        }

        // Column constraints
        if (valid) {
            for (uint8_t c = 0; c < _size; c++) {
                int8_t val = cand[c];
                // Trio check in column
                if (r >= 2 && _solution[r - 1][c] == val && _solution[r - 2][c] == val) {
                    valid = false; break;
                }
                // Count check
                uint8_t count = 1;
                for (int pr = 0; pr < r; pr++) {
                    if (_solution[pr][c] == val) count++;
                }
                if (count > half) { valid = false; break; }

                // If last row, check column uniqueness
                if (r == _size - 1) {
                    for (int pc = 0; pc < c; pc++) {
                        bool colSame = true;
                        for (int pr = 0; pr < _size - 1; pr++) {
                            if (_solution[pr][pc] != _solution[pr][c]) { colSame = false; break; }
                        }
                        if (colSame && _solution[r][pc] == val) {
                            valid = false; break;
                        }
                    }
                    if (!valid) break;
                }
            }
        }

        if (valid) {
            for (uint8_t c = 0; c < _size; c++) _solution[r][c] = cand[c];
            r++;
            if (r < _size) {
                for (uint8_t i = 0; i < numValids; i++) stack[r].order[i] = i;
                shuffleArray(stack[r].order, numValids);
                stack[r].candIdx = 0;
            }
        } else {
            stack[r].candIdx++;
        }
    }

    return (r == _size);
}

bool BinaryGen::solveDeductive(int8_t grid[8][8], uint8_t maxRule) {
    int8_t g[8][8];
    memcpy(g, grid, sizeof(g));
    const uint8_t half = _size / 2;
    bool changed = true;

    while (changed) {
        changed = false;

        // Rule 1: Trio avoidance
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size - 2; c++) {
                int8_t v0 = g[r][c], v1 = g[r][c + 1], v2 = g[r][c + 2];
                if (v0 == v1 && v0 != -1 && v2 == -1) { g[r][c + 2] = 1 - v0; changed = true; }
                if (v1 == v2 && v1 != -1 && v0 == -1) { g[r][c] = 1 - v1; changed = true; }
                if (v0 == v2 && v0 != -1 && v1 == -1) { g[r][c + 1] = 1 - v0; changed = true; }
            }
        }
        for (uint8_t c = 0; c < _size; c++) {
            for (uint8_t r = 0; r < _size - 2; r++) {
                int8_t v0 = g[r][c], v1 = g[r + 1][c], v2 = g[r + 2][c];
                if (v0 == v1 && v0 != -1 && v2 == -1) { g[r + 2][c] = 1 - v0; changed = true; }
                if (v1 == v2 && v1 != -1 && v0 == -1) { g[r][c] = 1 - v1; changed = true; }
                if (v0 == v2 && v0 != -1 && v1 == -1) { g[r + 1][c] = 1 - v0; changed = true; }
            }
        }
        if (changed) continue;

        // Rule 2: Line count
        for (uint8_t r = 0; r < _size; r++) {
            uint8_t c0 = 0, c1 = 0;
            for (uint8_t c = 0; c < _size; c++) {
                if (g[r][c] == 0) c0++;
                else if (g[r][c] == 1) c1++;
            }
            if (c0 == half && c1 < half) {
                for (uint8_t c = 0; c < _size; c++) {
                    if (g[r][c] == -1) { g[r][c] = 1; changed = true; }
                }
            } else if (c1 == half && c0 < half) {
                for (uint8_t c = 0; c < _size; c++) {
                    if (g[r][c] == -1) { g[r][c] = 0; changed = true; }
                }
            }
        }
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t c0 = 0, c1 = 0;
            for (uint8_t r = 0; r < _size; r++) {
                if (g[r][c] == 0) c0++;
                else if (g[r][c] == 1) c1++;
            }
            if (c0 == half && c1 < half) {
                for (uint8_t r = 0; r < _size; r++) {
                    if (g[r][c] == -1) { g[r][c] = 1; changed = true; }
                }
            } else if (c1 == half && c0 < half) {
                for (uint8_t r = 0; r < _size; r++) {
                    if (g[r][c] == -1) { g[r][c] = 0; changed = true; }
                }
            }
        }
        if (changed) continue;

        // Rule 3: Line uniqueness (Rule 4 from binarypuzzle.com)
        if (maxRule >= 3) {
            for (uint8_t r = 0; r < _size; r++) {
                int emptyIdx[2];
                uint8_t emptyCount = 0, c0 = 0, c1 = 0;
                for (uint8_t c = 0; c < _size; c++) {
                    if (g[r][c] == -1) {
                        if (emptyCount < 2) emptyIdx[emptyCount] = c;
                        emptyCount++;
                    } else if (g[r][c] == 0) c0++;
                    else if (g[r][c] == 1) c1++;
                }
                if (emptyCount == 2 && c0 == half - 1 && c1 == half - 1) {
                    int8_t ta[8];
                    memcpy(ta, g[r], _size);
                    ta[emptyIdx[0]] = 0; ta[emptyIdx[1]] = 1;
                    bool matchA = false;
                    for (uint8_t o = 0; o < _size; o++) {
                        if (o == r) continue;
                        bool hasEmpty = false;
                        for (uint8_t c = 0; c < _size; c++) if (g[o][c] == -1) { hasEmpty = true; break; }
                        if (hasEmpty) continue;
                        if (memcmp(g[o], ta, _size) == 0) { matchA = true; break; }
                    }
                    if (matchA) {
                        g[r][emptyIdx[0]] = 1; g[r][emptyIdx[1]] = 0;
                        changed = true;
                    } else {
                        int8_t tb[8];
                        memcpy(tb, g[r], _size);
                        tb[emptyIdx[0]] = 1; tb[emptyIdx[1]] = 0;
                        bool matchB = false;
                        for (uint8_t o = 0; o < _size; o++) {
                            if (o == r) continue;
                            bool hasEmpty = false;
                            for (uint8_t c = 0; c < _size; c++) if (g[o][c] == -1) { hasEmpty = true; break; }
                            if (hasEmpty) continue;
                            if (memcmp(g[o], tb, _size) == 0) { matchB = true; break; }
                        }
                        if (matchB) {
                            g[r][emptyIdx[0]] = 0; g[r][emptyIdx[1]] = 1;
                            changed = true;
                        }
                    }
                }
            }
        }
    }

    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            if (g[r][c] == -1) return false;
        }
    }
    return true;
}

void BinaryGen::generate(BinaryDifficulty difficulty) {
    uint8_t targetClues = 28;
    uint8_t maxRule = 2;

    if (difficulty == BINARY_EASY) {
        _size = 6;
        targetClues = 16;
        maxRule = 2;
    } else if (difficulty == BINARY_MEDIUM) {
        _size = 8;
        targetClues = 28;
        maxRule = 2;
    } else {
        _size = 8;
        targetClues = 22;
        maxRule = 3;
    }

    generateFullBoard();
    memcpy(_puzzle, _solution, sizeof(_puzzle));

    // Create coordinate array and shuffle
    uint8_t coords[64];
    uint8_t totalCells = _size * _size;
    for (uint8_t i = 0; i < totalCells; i++) coords[i] = i;
    shuffleArray(coords, totalCells);

    _cluesCount = totalCells;
    for (uint8_t i = 0; i < totalCells; i++) {
        if (_cluesCount <= targetClues) break;
        uint8_t r = coords[i] / _size;
        uint8_t c = coords[i] % _size;

        int8_t saved = _puzzle[r][c];
        _puzzle[r][c] = -1;

        if (solveDeductive(_puzzle, maxRule)) {
            _cluesCount--;
        } else {
            _puzzle[r][c] = saved;
        }
    }
}

void BinaryGen::printToReceipt(EscPosPrinter& printer, BinaryDifficulty diff) {
    const char* diffStr = (diff == BINARY_EASY) ? "EASY" : ((diff == BINARY_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- BINARY ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    if (_size == 6) {
        printer.println("Fill each row and column with three 0s and");
        printer.println("three 1s, with no more than two consecutive");
    } else {
        printer.println("Fill each row and column with four 0s and");
        printer.println("four 1s, with no more than two consecutive");
    }
    printer.println("of each type.");
    printer.println("");

    String sep = "   +";
    for (uint8_t c = 0; c < _size; c++) sep += "---+";
    printer.println(sep);

    for (uint8_t r = 0; r < _size; r++) {
        String line = "   |";
        for (uint8_t c = 0; c < _size; c++) {
            int8_t val = _puzzle[r][c];
            if (val == -1) line += "   |";
            else line += String(" ") + val + " |";
        }
        printer.println(line);
        printer.println(sep);
    }
    printer.println("");
}
