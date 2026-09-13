#include "LightsGen.h"
#include "EscPosPrinter.h"
#include <string.h>

static void shuffleLightsIndices(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

static uint8_t getOrthogonal(uint8_t r, uint8_t c, uint8_t size, uint8_t nR[4], uint8_t nC[4]) {
    uint8_t count = 0;
    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};
    for (int i = 0; i < 4; i++) {
        int nr = (int)r + dr[i];
        int nc = (int)c + dc[i];
        if (nr >= 0 && nr < size && nc >= 0 && nc < size) {
            nR[count] = (uint8_t)nr;
            nC[count] = (uint8_t)nc;
            count++;
        }
    }
    return count;
}

LightsGen::LightsGen() : _size(8), _totalBulbs(0) {
    memset(_puzzle, -1, sizeof(_puzzle));
    memset(_solution, 0, sizeof(_solution));
}

bool LightsGen::solveDeductive(int8_t puz[12][12], uint8_t size, int8_t sol[12][12]) {
    bool isBulb[12][12];
    bool canBeBulb[12][12];
    bool isLit[12][12];

    memset(isBulb, 0, sizeof(isBulb));
    memset(isLit, 0, sizeof(isLit));
    for (uint8_t r = 0; r < size; r++) {
        for (uint8_t c = 0; c < size; c++) {
            canBeBulb[r][c] = (puz[r][c] == -1);
        }
    }

    auto placeBulb = [&](uint8_t br, uint8_t bc, bool& changed) {
        if (isBulb[br][bc]) return;
        isBulb[br][bc] = true;
        isLit[br][bc] = true;
        changed = true;

        // Radiate light in 4 directions
        // Up
        for (int r = (int)br - 1; r >= 0; r--) {
            if (puz[r][bc] != -1) break;
            isLit[r][bc] = true;
            if (canBeBulb[r][bc]) { canBeBulb[r][bc] = false; changed = true; }
        }
        // Down
        for (int r = (int)br + 1; r < size; r++) {
            if (puz[r][bc] != -1) break;
            isLit[r][bc] = true;
            if (canBeBulb[r][bc]) { canBeBulb[r][bc] = false; changed = true; }
        }
        // Left
        for (int c = (int)bc - 1; c >= 0; c--) {
            if (puz[br][c] != -1) break;
            isLit[br][c] = true;
            if (canBeBulb[br][c]) { canBeBulb[br][c] = false; changed = true; }
        }
        // Right
        for (int c = (int)bc + 1; c < size; c++) {
            if (puz[br][c] != -1) break;
            isLit[br][c] = true;
            if (canBeBulb[br][c]) { canBeBulb[br][c] = false; changed = true; }
        }
    };

    auto forbidBulb = [&](uint8_t fr, uint8_t fc, bool& changed) {
        if (canBeBulb[fr][fc]) {
            canBeBulb[fr][fc] = false;
            changed = true;
        }
    };

    bool changed = true;
    uint8_t iter = 0;
    while (changed && iter < 100) {
        changed = false;
        iter++;

        // Rule 1: Numbered wall constraints
        for (uint8_t r = 0; r < size; r++) {
            for (uint8_t c = 0; c < size; c++) {
                int8_t clue = puz[r][c];
                if (clue < 0) continue;

                uint8_t nR[4], nC[4];
                uint8_t nCnt = getOrthogonal(r, c, size, nR, nC);
                uint8_t confirmed = 0;
                uint8_t candidates = 0;
                for (uint8_t i = 0; i < nCnt; i++) {
                    uint8_t nr = nR[i], nc = nC[i];
                    if (puz[nr][nc] == -1) {
                        if (isBulb[nr][nc]) confirmed++;
                        else if (canBeBulb[nr][nc]) candidates++;
                    }
                }

                if (confirmed > clue || confirmed + candidates < clue) return false;

                if (confirmed == clue && candidates > 0) {
                    for (uint8_t i = 0; i < nCnt; i++) {
                        uint8_t nr = nR[i], nc = nC[i];
                        if (puz[nr][nc] == -1 && canBeBulb[nr][nc] && !isBulb[nr][nc]) {
                            forbidBulb(nr, nc, changed);
                        }
                    }
                } else if (confirmed + candidates == clue && candidates > 0) {
                    for (uint8_t i = 0; i < nCnt; i++) {
                        uint8_t nr = nR[i], nc = nC[i];
                        if (puz[nr][nc] == -1 && canBeBulb[nr][nc] && !isBulb[nr][nc]) {
                            placeBulb(nr, nc, changed);
                        }
                    }
                }
            }
        }

        // Rule 2: Unlit white cells
        for (uint8_t r = 0; r < size; r++) {
            for (uint8_t c = 0; c < size; c++) {
                if (puz[r][c] != -1 || isLit[r][c]) continue;

                uint8_t candR = 0, candC = 0;
                uint8_t candPlacers = 0;

                // Check self
                if (canBeBulb[r][c]) { candR = r; candC = c; candPlacers++; }

                // Check ray up
                for (int cr = (int)r - 1; cr >= 0; cr--) {
                    if (puz[cr][c] != -1) break;
                    if (canBeBulb[cr][c]) { candR = cr; candC = c; candPlacers++; }
                }
                // Down
                for (int cr = (int)r + 1; cr < size; cr++) {
                    if (puz[cr][c] != -1) break;
                    if (canBeBulb[cr][c]) { candR = cr; candC = c; candPlacers++; }
                }
                // Left
                for (int cc = (int)c - 1; cc >= 0; cc--) {
                    if (puz[r][cc] != -1) break;
                    if (canBeBulb[r][cc]) { candR = r; candC = cc; candPlacers++; }
                }
                // Right
                for (int cc = (int)c + 1; cc < size; cc++) {
                    if (puz[r][cc] != -1) break;
                    if (canBeBulb[r][cc]) { candR = r; candC = cc; candPlacers++; }
                }

                if (candPlacers == 0) return false;
                if (candPlacers == 1) {
                    placeBulb(candR, candC, changed);
                }
            }
        }
    }

    // Verify all walls and lit status
    for (uint8_t r = 0; r < size; r++) {
        for (uint8_t c = 0; c < size; c++) {
            if (puz[r][c] == -1) {
                if (!isLit[r][c]) return false;
                if (sol) sol[r][c] = isBulb[r][c] ? 1 : 0;
            } else {
                if (sol) sol[r][c] = 0;
                if (puz[r][c] >= 0) {
                    uint8_t nR[4], nC[4];
                    uint8_t nCnt = getOrthogonal(r, c, size, nR, nC);
                    uint8_t adjB = 0;
                    for (uint8_t i = 0; i < nCnt; i++) {
                        if (isBulb[nR[i]][nC[i]]) adjB++;
                    }
                    if (adjB != puz[r][c]) return false;
                }
            }
        }
    }

    return true;
}

void LightsGen::generate(LightsDifficulty difficulty) {
    if (difficulty == LIGHTS_EASY) _size = 6;
    else if (difficulty == LIGHTS_HARD) _size = 10;
    else if (difficulty == LIGHTS_EXTREME) _size = 12;
    else _size = 8;

    uint8_t targetWalls = (_size * _size * 21) / 100;
    if (targetWalls % 2 != 0) targetWalls++;

    for (uint8_t attempt = 0; attempt < 50; attempt++) {
        memset(_puzzle, -1, sizeof(_puzzle));
        memset(_solution, 0, sizeof(_solution));

        // 1. Symmetrical barrier placement
        uint8_t numPairs = targetWalls / 2;
        uint8_t placed = 0;
        uint8_t coords[144];
        uint8_t totalCells = _size * _size;
        for (uint8_t i = 0; i < totalCells; i++) coords[i] = i;
        shuffleLightsIndices(coords, totalCells);

        for (uint8_t i = 0; i < totalCells && placed < numPairs; i++) {
            uint8_t r = coords[i] / _size;
            uint8_t c = coords[i] % _size;
            uint8_t sr = _size - 1 - r;
            uint8_t sc = _size - 1 - c;

            if (_puzzle[r][c] == -1 && _puzzle[sr][sc] == -1) {
                _puzzle[r][c] = -2;
                _puzzle[sr][sc] = -2;
                placed++;
            }
        }

        // 2. Place bulbs randomly covering corridors
        bool bulbs[12][12];
        bool lit[12][12];
        memset(bulbs, 0, sizeof(bulbs));
        memset(lit, 0, sizeof(lit));

        uint8_t whiteCoords[144];
        uint8_t whiteCount = 0;
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (_puzzle[r][c] == -1) whiteCoords[whiteCount++] = r * _size + c;
            }
        }
        if (whiteCount < (_size * _size * 65) / 100) continue;

        shuffleLightsIndices(whiteCoords, whiteCount);

        for (uint8_t i = 0; i < whiteCount; i++) {
            uint8_t r = whiteCoords[i] / _size;
            uint8_t c = whiteCoords[i] % _size;
            if (lit[r][c]) continue;

            // Check if (r, c) sees any existing bulb
            bool seesBulb = false;
            for (int cr = (int)r - 1; cr >= 0; cr--) {
                if (_puzzle[cr][c] != -1) break;
                if (bulbs[cr][c]) { seesBulb = true; break; }
            }
            if (!seesBulb) {
                for (int cr = (int)r + 1; cr < _size; cr++) {
                    if (_puzzle[cr][c] != -1) break;
                    if (bulbs[cr][c]) { seesBulb = true; break; }
                }
            }
            if (!seesBulb) {
                for (int cc = (int)c - 1; cc >= 0; cc--) {
                    if (_puzzle[r][cc] != -1) break;
                    if (bulbs[r][cc]) { seesBulb = true; break; }
                }
            }
            if (!seesBulb) {
                for (int cc = (int)c + 1; cc < _size; cc++) {
                    if (_puzzle[r][cc] != -1) break;
                    if (bulbs[r][cc]) { seesBulb = true; break; }
                }
            }

            if (!seesBulb) {
                bulbs[r][c] = true;
                lit[r][c] = true;
                for (int cr = (int)r - 1; cr >= 0; cr--) {
                    if (_puzzle[cr][c] != -1) break;
                    lit[cr][c] = true;
                }
                for (int cr = (int)r + 1; cr < _size; cr++) {
                    if (_puzzle[cr][c] != -1) break;
                    lit[cr][c] = true;
                }
                for (int cc = (int)c - 1; cc >= 0; cc--) {
                    if (_puzzle[r][cc] != -1) break;
                    lit[r][cc] = true;
                }
                for (int cc = (int)c + 1; cc < _size; cc++) {
                    if (_puzzle[r][cc] != -1) break;
                    lit[r][cc] = true;
                }
            }
        }

        // Check if all white cells are lit
        bool allLit = true;
        _totalBulbs = 0;
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (_puzzle[r][c] == -1) {
                    if (!lit[r][c]) { allLit = false; break; }
                    if (bulbs[r][c]) _totalBulbs++;
                }
            }
            if (!allLit) break;
        }
        if (!allLit || _totalBulbs == 0) continue;

        // 3. Assign wall clues
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (_puzzle[r][c] == -2) {
                    uint8_t nR[4], nC[4];
                    uint8_t nCnt = getOrthogonal(r, c, _size, nR, nC);
                    uint8_t adjB = 0;
                    for (uint8_t i = 0; i < nCnt; i++) {
                        if (bulbs[nR[i]][nC[i]]) adjB++;
                    }
                    _puzzle[r][c] = (int8_t)adjB;
                }
            }
        }

        // 4. Test deductive solvability
        if (!solveDeductive(_puzzle, _size, _solution)) continue;

        // 5. Clue thinning
        uint8_t wallCoords[144];
        uint8_t wallCount = 0;
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (_puzzle[r][c] >= 0) wallCoords[wallCount++] = r * _size + c;
            }
        }
        shuffleLightsIndices(wallCoords, wallCount);

        float retainPct = (difficulty == LIGHTS_EASY) ? 0.85f : ((difficulty == LIGHTS_HARD) ? 0.45f : ((difficulty == LIGHTS_EXTREME) ? 0.35f : 0.65f));
        uint8_t targetClues = (uint8_t)(wallCount * retainPct);

        uint8_t currentClues = wallCount;
        for (uint8_t i = 0; i < wallCount; i++) {
            if (currentClues <= targetClues) break;
            uint8_t r = wallCoords[i] / _size;
            uint8_t c = wallCoords[i] % _size;
            int8_t saved = _puzzle[r][c];
            _puzzle[r][c] = -2; // unnumbered

            if (solveDeductive(_puzzle, _size, _solution)) {
                currentClues--;
            } else {
                _puzzle[r][c] = saved;
            }
        }

        // Final verification
        if (solveDeductive(_puzzle, _size, _solution)) {
            return; // Successfully generated
        }
    }
}

void LightsGen::printToReceipt(EscPosPrinter& printer, LightsDifficulty diff) {
    const char* diffStr = (diff == LIGHTS_EASY) ? "EASY" : ((diff == LIGHTS_HARD) ? "HARD" : ((diff == LIGHTS_EXTREME) ? "EXTREME" : "MEDIUM"));

    printer.setBold(true);
    printer.println("--- LIGHTS ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println(String("Place ") + String(_totalBulbs) + " bulbs to light all corridors without");
    printer.println("bulbs shining on each other or exceeding numbers.");
    printer.println(String("TOTAL BULBS: ") + String(_totalBulbs));
    printer.println("");

    String sep = "   ";
    for (uint8_t c = 0; c < _size; c++) sep += "+---";
    sep += "+";
    printer.println(sep);

    for (uint8_t r = 0; r < _size; r++) {
        String line = "   |";
        for (uint8_t c = 0; c < _size; c++) {
            int8_t val = _puzzle[r][c];
            if (val >= 0) line += String(" ") + val + " |";
            else if (val == -2) line += " # |";
            else line += "   |";
        }
        printer.println(line);
        printer.println(sep);
    }
    printer.println("");
}
