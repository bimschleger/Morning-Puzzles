#include "TangoGen.h"
#include "EscPosPrinter.h"
#include <string.h>

static const uint8_t TANGO_VALID_LINES_6[14] = {
    0x0b, 0x0d, 0x13, 0x15, 0x16, 0x19, 0x1a, 0x25, 0x26, 0x29, 0x2a, 0x2c, 0x32, 0x34
};

static const uint8_t TANGO_VALID_LINES_8[34] = {
    0x2b, 0x2d, 0x33, 0x35, 0x36, 0x4b, 0x4d, 0x53, 0x55, 0x56, 0x59, 0x5a,
    0x65, 0x66, 0x69, 0x6a, 0x6c, 0x93, 0x95, 0x96, 0x99, 0x9a, 0xa5, 0xa6,
    0xa9, 0xaa, 0xac, 0xb2, 0xb4, 0xc9, 0xca, 0xcc, 0xd2, 0xd4
};

TangoGen::TangoGen() : _size(6), _numbersCount(0), _edgesCount(0) {
    memset(_solution, -1, sizeof(_solution));
    memset(_puzzle, -1, sizeof(_puzzle));
    memset(_edgesH, 0, sizeof(_edgesH));
    memset(_edgesV, 0, sizeof(_edgesV));
}

static void tangoShuffleArray(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

bool TangoGen::generateFullBoard() {
    const uint8_t* valids = (_size == 6) ? TANGO_VALID_LINES_6 : TANGO_VALID_LINES_8;
    const uint8_t numValids = (_size == 6) ? 14 : 34;
    const uint8_t half = _size / 2;

    struct State {
        uint8_t candIdx;
        uint8_t order[34];
    } stack[8];

    int r = 0;
    for (uint8_t i = 0; i < numValids; i++) stack[0].order[i] = i;
    tangoShuffleArray(stack[0].order, numValids);
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

        // Check column constraints (duplicate rows are permitted in Tango)
        bool valid = true;
        for (uint8_t c = 0; c < _size; c++) {
            int8_t val = cand[c];
            // Trio check in column
            if (r >= 2 && _solution[r - 1][c] == val && _solution[r - 2][c] == val) {
                valid = false;
                break;
            }
            // Count check in column
            uint8_t count = 1;
            for (int pr = 0; pr < r; pr++) {
                if (_solution[pr][c] == val) count++;
            }
            if (count > half) {
                valid = false;
                break;
            }
        }

        if (valid) {
            for (uint8_t c = 0; c < _size; c++) {
                _solution[r][c] = cand[c];
            }
            r++;
            if (r < _size) {
                for (uint8_t i = 0; i < numValids; i++) stack[r].order[i] = i;
                tangoShuffleArray(stack[r].order, numValids);
                stack[r].candIdx = 0;
            }
        } else {
            stack[r].candIdx++;
        }
    }

    return (r == _size);
}

bool TangoGen::isCandidateValid(int8_t g[8][8], uint8_t r, uint8_t c, int8_t val) {
    const uint8_t half = _size / 2;

    // Check row count
    uint8_t rCount = 0;
    for (uint8_t j = 0; j < _size; j++) {
        if (g[r][j] == val) rCount++;
    }
    if (rCount + 1 > half) return false;

    // Check col count
    uint8_t cCount = 0;
    for (uint8_t i = 0; i < _size; i++) {
        if (g[i][c] == val) cCount++;
    }
    if (cCount + 1 > half) return false;

    // Row trios
    if (c >= 2 && g[r][c - 2] == val && g[r][c - 1] == val) return false;
    if (c > 0 && c < _size - 1 && g[r][c - 1] == val && g[r][c + 1] == val) return false;
    if (c <= _size - 3 && g[r][c + 1] == val && g[r][c + 2] == val) return false;

    // Col trios
    if (r >= 2 && g[r - 2][c] == val && g[r - 1][c] == val) return false;
    if (r > 0 && r < _size - 1 && g[r - 1][c] == val && g[r + 1][c] == val) return false;
    if (r <= _size - 3 && g[r + 1][c] == val && g[r + 2][c] == val) return false;

    // Edge constraints
    if (c > 0) {
        uint8_t e = _edgesH[r][c - 1];
        if (e == 1 && g[r][c - 1] != -1 && g[r][c - 1] != val) return false;
        if (e == 2 && g[r][c - 1] != -1 && g[r][c - 1] == val) return false;
    }
    if (c < _size - 1) {
        uint8_t e = _edgesH[r][c];
        if (e == 1 && g[r][c + 1] != -1 && g[r][c + 1] != val) return false;
        if (e == 2 && g[r][c + 1] != -1 && g[r][c + 1] == val) return false;
    }
    if (r > 0) {
        uint8_t e = _edgesV[r - 1][c];
        if (e == 1 && g[r - 1][c] != -1 && g[r - 1][c] != val) return false;
        if (e == 2 && g[r - 1][c] != -1 && g[r - 1][c] == val) return false;
    }
    if (r < _size - 1) {
        uint8_t e = _edgesV[r][c];
        if (e == 1 && g[r + 1][c] != -1 && g[r + 1][c] != val) return false;
        if (e == 2 && g[r + 1][c] != -1 && g[r + 1][c] == val) return false;
    }

    return true;
}

bool TangoGen::solveDeductive(int8_t grid[8][8]) {
    int8_t g[8][8];
    memcpy(g, grid, sizeof(g));
    const uint8_t half = _size / 2;
    bool changed = true;

    while (changed) {
        changed = false;

        // Pass 1: Direct edge clues
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size - 1; c++) {
                uint8_t e = _edgesH[r][c];
                if (e == 1) { // '='
                    if (g[r][c] != -1 && g[r][c + 1] == -1) { g[r][c + 1] = g[r][c]; changed = true; }
                    else if (g[r][c + 1] != -1 && g[r][c] == -1) { g[r][c] = g[r][c + 1]; changed = true; }
                } else if (e == 2) { // 'x'
                    if (g[r][c] != -1 && g[r][c + 1] == -1) { g[r][c + 1] = 1 - g[r][c]; changed = true; }
                    else if (g[r][c + 1] != -1 && g[r][c] == -1) { g[r][c] = 1 - g[r][c + 1]; changed = true; }
                }
            }
        }

        for (uint8_t r = 0; r < _size - 1; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                uint8_t e = _edgesV[r][c];
                if (e == 1) { // '='
                    if (g[r][c] != -1 && g[r + 1][c] == -1) { g[r + 1][c] = g[r][c]; changed = true; }
                    else if (g[r + 1][c] != -1 && g[r][c] == -1) { g[r][c] = g[r + 1][c]; changed = true; }
                } else if (e == 2) { // 'x'
                    if (g[r][c] != -1 && g[r + 1][c] == -1) { g[r + 1][c] = 1 - g[r][c]; changed = true; }
                    else if (g[r + 1][c] != -1 && g[r][c] == -1) { g[r][c] = 1 - g[r + 1][c]; changed = true; }
                }
            }
        }
        if (changed) continue;

        // Pass 2: Trio avoidance
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

        // Pass 3: Edge-trio interaction
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size - 1; c++) {
                if (_edgesH[r][c] == 1) {
                    if (c > 0 && g[r][c - 1] != -1) {
                        if (g[r][c] == -1) { g[r][c] = 1 - g[r][c - 1]; changed = true; }
                        if (g[r][c + 1] == -1) { g[r][c + 1] = 1 - g[r][c - 1]; changed = true; }
                    }
                    if (c > 0 && g[r][c] != -1 && g[r][c - 1] == -1) {
                        g[r][c - 1] = 1 - g[r][c]; changed = true;
                    }
                    if (c + 2 < _size && g[r][c + 2] != -1) {
                        if (g[r][c] == -1) { g[r][c] = 1 - g[r][c + 2]; changed = true; }
                        if (g[r][c + 1] == -1) { g[r][c + 1] = 1 - g[r][c + 2]; changed = true; }
                    }
                    if (c + 2 < _size && g[r][c + 1] != -1 && g[r][c + 2] == -1) {
                        g[r][c + 2] = 1 - g[r][c + 1]; changed = true;
                    }
                }
            }
        }
        for (uint8_t c = 0; c < _size; c++) {
            for (uint8_t r = 0; r < _size - 1; r++) {
                if (_edgesV[r][c] == 1) {
                    if (r > 0 && g[r - 1][c] != -1) {
                        if (g[r][c] == -1) { g[r][c] = 1 - g[r - 1][c]; changed = true; }
                        if (g[r + 1][c] == -1) { g[r + 1][c] = 1 - g[r - 1][c]; changed = true; }
                    }
                    if (r > 0 && g[r][c] != -1 && g[r - 1][c] == -1) {
                        g[r - 1][c] = 1 - g[r][c]; changed = true;
                    }
                    if (r + 2 < _size && g[r + 2][c] != -1) {
                        if (g[r][c] == -1) { g[r][c] = 1 - g[r + 2][c]; changed = true; }
                        if (g[r + 1][c] == -1) { g[r + 1][c] = 1 - g[r + 2][c]; changed = true; }
                    }
                    if (r + 2 < _size && g[r + 1][c] != -1 && g[r + 2][c] == -1) {
                        g[r + 2][c] = 1 - g[r + 1][c]; changed = true;
                    }
                }
            }
        }
        if (changed) continue;

        // Pass 4: Line count balance
        for (uint8_t r = 0; r < _size; r++) {
            uint8_t c0 = 0, c1 = 0;
            for (uint8_t c = 0; c < _size; c++) {
                if (g[r][c] == 0) c0++;
                else if (g[r][c] == 1) c1++;
            }
            if (c0 == half && c1 < half) {
                for (uint8_t c = 0; c < _size; c++) if (g[r][c] == -1) { g[r][c] = 1; changed = true; }
            } else if (c1 == half && c0 < half) {
                for (uint8_t c = 0; c < _size; c++) if (g[r][c] == -1) { g[r][c] = 0; changed = true; }
            }
        }
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t c0 = 0, c1 = 0;
            for (uint8_t r = 0; r < _size; r++) {
                if (g[r][c] == 0) c0++;
                else if (g[r][c] == 1) c1++;
            }
            if (c0 == half && c1 < half) {
                for (uint8_t r = 0; r < _size; r++) if (g[r][c] == -1) { g[r][c] = 1; changed = true; }
            } else if (c1 == half && c0 < half) {
                for (uint8_t r = 0; r < _size; r++) if (g[r][c] == -1) { g[r][c] = 0; changed = true; }
            }
        }
        if (changed) continue;

        // Pass 5: 1-step lookahead
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (g[r][c] == -1) {
                    bool can0 = isCandidateValid(g, r, c, 0);
                    bool can1 = isCandidateValid(g, r, c, 1);
                    if (!can0 && can1) { g[r][c] = 1; changed = true; }
                    else if (!can1 && can0) { g[r][c] = 0; changed = true; }
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

void TangoGen::generate(TangoDifficulty difficulty) {
    uint8_t targetNumbers = 4;
    uint8_t targetEdges = 8;

    if (difficulty == TANGO_EASY) {
        _size = 6;
        targetNumbers = 6;
        targetEdges = 6;
    } else if (difficulty == TANGO_MEDIUM) {
        _size = 6;
        targetNumbers = 4;
        targetEdges = 8;
    } else {
        _size = 8;
        targetNumbers = 10;
        targetEdges = 14;
    }

    for (uint8_t attempt = 0; attempt < 50; attempt++) {
        if (!generateFullBoard()) continue;

        memset(_edgesH, 0, sizeof(_edgesH));
        memset(_edgesV, 0, sizeof(_edgesV));

        // Pool of all edges
        uint8_t numH = _size * (_size - 1);
        uint8_t numV = (_size - 1) * _size;
        uint8_t totalEdges = numH + numV;
        uint8_t edgeIndices[112];
        for (uint8_t i = 0; i < totalEdges; i++) edgeIndices[i] = i;
        tangoShuffleArray(edgeIndices, totalEdges);

        for (uint8_t i = 0; i < targetEdges && i < totalEdges; i++) {
            uint8_t idx = edgeIndices[i];
            if (idx < numH) {
                uint8_t r = idx / (_size - 1);
                uint8_t c = idx % (_size - 1);
                _edgesH[r][c] = (_solution[r][c] == _solution[r][c + 1]) ? 1 : 2;
            } else {
                uint8_t vIdx = idx - numH;
                uint8_t r = vIdx / _size;
                uint8_t c = vIdx % _size;
                _edgesV[r][c] = (_solution[r][c] == _solution[r + 1][c]) ? 1 : 2;
            }
        }

        memcpy(_puzzle, _solution, sizeof(_puzzle));
        uint8_t coords[64];
        uint8_t totalCells = _size * _size;
        for (uint8_t i = 0; i < totalCells; i++) coords[i] = i;
        tangoShuffleArray(coords, totalCells);

        _numbersCount = totalCells;
        for (uint8_t i = 0; i < totalCells; i++) {
            if (_numbersCount <= targetNumbers) break;
            uint8_t r = coords[i] / _size;
            uint8_t c = coords[i] % _size;

            int8_t saved = _puzzle[r][c];
            _puzzle[r][c] = -1;

            if (solveDeductive(_puzzle)) {
                _numbersCount--;
            } else {
                _puzzle[r][c] = saved;
            }
        }

        if (solveDeductive(_puzzle) && _numbersCount <= targetNumbers + 2) {
            _edgesCount = targetEdges;
            return;
        }
    }
}

void TangoGen::printToReceipt(EscPosPrinter& printer, TangoDifficulty diff) {
    const char* diffStr = (diff == TANGO_EASY) ? "EASY" : ((diff == TANGO_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- TANGO ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    if (_size == 6) {
        printer.println("Fill each line with three 0s and three 1s");
    } else {
        printer.println("Fill each line with four 0s and four 1s");
    }
    printer.println("without trios; = means same, x means opposite.");
    printer.println("");

    String sepTop = "   +";
    for (uint8_t c = 0; c < _size; c++) sepTop += "---+";
    printer.println(sepTop);

    for (uint8_t r = 0; r < _size; r++) {
        String line = "   |";
        for (uint8_t c = 0; c < _size; c++) {
            int8_t val = _puzzle[r][c];
            if (val == 0 || val == 1) {
                line += String(" ") + val + " ";
            } else {
                line += "   ";
            }

            if (c < _size - 1) {
                uint8_t e = _edgesH[r][c];
                if (e == 1) line += "=";
                else if (e == 2) line += "x";
                else line += "|";
            } else {
                line += "|";
            }
        }
        printer.println(line);

        if (r < _size - 1) {
            String divLine = "   +";
            for (uint8_t c = 0; c < _size; c++) {
                uint8_t e = _edgesV[r][c];
                if (e == 1) divLine += "-=-+";
                else if (e == 2) divLine += "-x-+";
                else divLine += "---+";
            }
            printer.println(divLine);
        } else {
            printer.println(sepTop);
        }
    }
    printer.println("");
}
