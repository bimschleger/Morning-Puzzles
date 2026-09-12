#include "MinesGen.h"
#include "../printer/EscPosPrinter.h"
#include <string.h>

static void shuffleCoords(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

static uint8_t getNeighbors(uint8_t r, uint8_t c, uint8_t nRow[8], uint8_t nCol[8]) {
    uint8_t count = 0;
    for (int dr = -1; dr <= 1; dr++) {
        for (int dc = -1; dc <= 1; dc++) {
            if (dr == 0 && dc == 0) continue;
            int nr = r + dr;
            int nc = c + dc;
            if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                nRow[count] = nr;
                nCol[count] = nc;
                count++;
            }
        }
    }
    return count;
}

MinesGen::MinesGen() : _totalMines(12), _cluesCount(0) {
    memset(_puzzle, -1, sizeof(_puzzle));
    memset(_solution, 0, sizeof(_solution));
}

bool MinesGen::solveDeductive(int8_t puz[8][8], uint8_t totalMines) {
    int8_t state[8][8];
    memset(state, -1, sizeof(state));

    // Clue cells are known safe
    for (uint8_t r = 0; r < 8; r++) {
        for (uint8_t c = 0; c < 8; c++) {
            if (puz[r][c] != -1) {
                state[r][c] = 0;
            }
        }
    }

    bool changed = true;
    while (changed) {
        changed = false;

        // Rules 1 & 2: Local saturation & clearing
        for (uint8_t r = 0; r < 8; r++) {
            for (uint8_t c = 0; c < 8; c++) {
                int8_t val = puz[r][c];
                if (val == -1) continue;

                uint8_t nRow[8], nCol[8];
                uint8_t nCount = getNeighbors(r, c, nRow, nCol);

                uint8_t uCount = 0;
                uint8_t mCount = 0;
                uint8_t uRow[8], uCol[8];

                for (uint8_t i = 0; i < nCount; i++) {
                    int8_t st = state[nRow[i]][nCol[i]];
                    if (st == -1) {
                        uRow[uCount] = nRow[i];
                        uCol[uCount] = nCol[i];
                        uCount++;
                    } else if (st == 1) {
                        mCount++;
                    }
                }

                int rem = val - mCount;
                if (rem < 0 || (uCount + mCount) < val) {
                    return false; // Contradiction
                }

                if (rem == 0 && uCount > 0) {
                    for (uint8_t i = 0; i < uCount; i++) {
                        state[uRow[i]][uCol[i]] = 0;
                        changed = true;
                    }
                } else if (rem == uCount && uCount > 0) {
                    for (uint8_t i = 0; i < uCount; i++) {
                        state[uRow[i]][uCol[i]] = 1;
                        changed = true;
                    }
                }
            }
        }

        if (changed) continue;

        // Rule 3: Subset difference logic between adjacent clue pairs
        for (uint8_t r1 = 0; r1 < 8; r1++) {
            for (uint8_t c1 = 0; c1 < 8; c1++) {
                int8_t v1 = puz[r1][c1];
                if (v1 == -1) continue;

                uint8_t nRow1[8], nCol1[8];
                uint8_t nCount1 = getNeighbors(r1, c1, nRow1, nCol1);
                uint8_t uCount1 = 0, mCount1 = 0;
                uint8_t u1[8]; // indices encoded as r * 8 + c
                for (uint8_t i = 0; i < nCount1; i++) {
                    if (state[nRow1[i]][nCol1[i]] == -1) u1[uCount1++] = nRow1[i] * 8 + nCol1[i];
                    else if (state[nRow1[i]][nCol1[i]] == 1) mCount1++;
                }
                if (uCount1 == 0) continue;
                int rem1 = v1 - mCount1;

                // Compare against other clues within 2 steps
                for (int dr = -2; dr <= 2; dr++) {
                    for (int dc = -2; dc <= 2; dc++) {
                        if (dr == 0 && dc == 0) continue;
                        int r2 = r1 + dr;
                        int c2 = c1 + dc;
                        if (r2 < 0 || r2 >= 8 || c2 < 0 || c2 >= 8) continue;
                        int8_t v2 = puz[r2][c2];
                        if (v2 == -1) continue;

                        uint8_t nRow2[8], nCol2[8];
                        uint8_t nCount2 = getNeighbors(r2, c2, nRow2, nCol2);
                        uint8_t uCount2 = 0, mCount2 = 0;
                        uint8_t u2[8];
                        for (uint8_t i = 0; i < nCount2; i++) {
                            if (state[nRow2[i]][nCol2[i]] == -1) u2[uCount2++] = nRow2[i] * 8 + nCol2[i];
                            else if (state[nRow2[i]][nCol2[i]] == 1) mCount2++;
                        }
                        if (uCount2 == 0) continue;
                        int rem2 = v2 - mCount2;

                        // Check if u1 is subset of u2
                        bool isSubset = true;
                        for (uint8_t a = 0; a < uCount1; a++) {
                            bool found = false;
                            for (uint8_t b = 0; b < uCount2; b++) {
                                if (u1[a] == u2[b]) { found = true; break; }
                            }
                            if (!found) { isSubset = false; break; }
                        }

                        if (isSubset) {
                            uint8_t diff[8];
                            uint8_t diffCount = 0;
                            for (uint8_t b = 0; b < uCount2; b++) {
                                bool inU1 = false;
                                for (uint8_t a = 0; a < uCount1; a++) {
                                    if (u2[b] == u1[a]) { inU1 = true; break; }
                                }
                                if (!inU1) diff[diffCount++] = u2[b];
                            }

                            int remDiff = rem2 - rem1;
                            if (remDiff < 0) return false;
                            if (remDiff == 0 && diffCount > 0) {
                                for (uint8_t d = 0; d < diffCount; d++) {
                                    state[diff[d] / 8][diff[d] % 8] = 0;
                                    changed = true;
                                }
                            } else if (remDiff == diffCount && diffCount > 0) {
                                for (uint8_t d = 0; d < diffCount; d++) {
                                    state[diff[d] / 8][diff[d] % 8] = 1;
                                    changed = true;
                                }
                            }
                        }
                    }
                }
            }
        }

        if (changed) continue;

        // Rule 4: Global mine count
        uint8_t foundMines = 0;
        uint8_t totalUnknowns = 0;
        uint8_t uCoords[64];
        for (uint8_t r = 0; r < 8; r++) {
            for (uint8_t c = 0; c < 8; c++) {
                if (state[r][c] == 1) foundMines++;
                else if (state[r][c] == -1) uCoords[totalUnknowns++] = r * 8 + c;
            }
        }

        int remGlobal = totalMines - foundMines;
        if (remGlobal == 0 && totalUnknowns > 0) {
            for (uint8_t i = 0; i < totalUnknowns; i++) {
                state[uCoords[i] / 8][uCoords[i] % 8] = 0;
                changed = true;
            }
        } else if (remGlobal == totalUnknowns && totalUnknowns > 0) {
            for (uint8_t i = 0; i < totalUnknowns; i++) {
                state[uCoords[i] / 8][uCoords[i] % 8] = 1;
                changed = true;
            }
        }
    }

    for (uint8_t r = 0; r < 8; r++) {
        for (uint8_t c = 0; c < 8; c++) {
            if (state[r][c] == -1) return false;
        }
    }
    return true;
}

void MinesGen::generate(MinesDifficulty difficulty) {
    uint8_t targetClues = 22;
    if (difficulty == MINES_EASY) {
        _totalMines = 8;
        targetClues = 28;
    } else if (difficulty == MINES_MEDIUM) {
        _totalMines = 12;
        targetClues = 22;
    } else {
        _totalMines = 15;
        targetClues = 17;
    }

    uint8_t allCoords[64];
    for (uint8_t i = 0; i < 64; i++) allCoords[i] = i;

    for (uint8_t attempt = 0; attempt < 50; attempt++) {
        shuffleCoords(allCoords, 64);
        memset(_solution, 0, sizeof(_solution));
        for (uint8_t i = 0; i < _totalMines; i++) {
            _solution[allCoords[i] / 8][allCoords[i] % 8] = 1;
        }

        // Full clues for all non-mine cells
        int8_t fullClues[8][8];
        memset(fullClues, -1, sizeof(fullClues));
        for (uint8_t r = 0; r < 8; r++) {
            for (uint8_t c = 0; c < 8; c++) {
                if (_solution[r][c] == 0) {
                    uint8_t nRow[8], nCol[8];
                    uint8_t nCount = getNeighbors(r, c, nRow, nCol);
                    uint8_t mineCount = 0;
                    for (uint8_t i = 0; i < nCount; i++) {
                        if (_solution[nRow[i]][nCol[i]] == 1) mineCount++;
                    }
                    fullClues[r][c] = mineCount;
                }
            }
        }

        if (!solveDeductive(fullClues, _totalMines)) {
            continue;
        }

        // Prune clues down to targetClues
        memcpy(_puzzle, fullClues, sizeof(_puzzle));
        uint8_t nonMineCoords[64];
        uint8_t nonMineCount = 0;
        for (uint8_t i = _totalMines; i < 64; i++) {
            nonMineCoords[nonMineCount++] = allCoords[i];
        }
        shuffleCoords(nonMineCoords, nonMineCount);

        _cluesCount = nonMineCount;
        for (uint8_t i = 0; i < nonMineCount; i++) {
            if (_cluesCount <= targetClues) break;
            uint8_t r = nonMineCoords[i] / 8;
            uint8_t c = nonMineCoords[i] % 8;
            int8_t saved = _puzzle[r][c];
            _puzzle[r][c] = -1;

            if (solveDeductive(_puzzle, _totalMines)) {
                _cluesCount--;
            } else {
                _puzzle[r][c] = saved;
            }
        }

        return; // Successfully generated!
    }
}

void MinesGen::printToReceipt(EscPosPrinter& printer, MinesDifficulty diff) {
    const char* diffStr = (diff == MINES_EASY) ? "EASY" : ((diff == MINES_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- MINES ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Use the numbered clues showing adjacent mine counts");
    printer.println("to deduce and mark every hidden mine across the grid.");
    printer.println(String("TOTAL MINES: ") + String(_totalMines));
    printer.println("");

    String sep = "   +---+---+---+---+---+---+---+---+";
    printer.println(sep);

    for (uint8_t r = 0; r < 8; r++) {
        String line = "   |";
        for (uint8_t c = 0; c < 8; c++) {
            int8_t val = _puzzle[r][c];
            if (val == -1) line += "   |";
            else line += String(" ") + val + " |";
        }
        printer.println(line);
        printer.println(sep);
    }
    printer.println("");
}
