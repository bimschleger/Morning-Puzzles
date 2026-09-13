#include "LoopGen.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

static void shuffleLoopIndices(uint8_t* arr, uint8_t n) {
    for (uint8_t i = n - 1; i > 0; i--) {
        uint8_t j = (uint8_t)random(i + 1);
        uint8_t tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

LoopGen::LoopGen() : _size(7) {
    for (uint8_t r = 0; r < 9; r++) {
        for (uint8_t c = 0; c < 9; c++) {
            _clues[r][c] = -1;
        }
    }
    for (uint8_t r = 0; r < 10; r++) {
        for (uint8_t c = 0; c < 9; c++) {
            _solutionH[r][c] = 0;
        }
    }
    for (uint8_t r = 0; r < 9; r++) {
        for (uint8_t c = 0; c < 10; c++) {
            _solutionV[r][c] = 0;
        }
    }
}

bool LoopGen::generatePolyominoLoop(uint8_t n) {
    uint8_t totalCells = n * n;
    uint8_t targetCount = totalCells * 45 / 100;
    if (targetCount < 4) targetCount = 4;

    for (uint16_t attempt = 0; attempt < 250; attempt++) {
        uint8_t grid[9][9] = {0};

        uint8_t startR = (n > 3) ? (1 + random(n - 2)) : random(n);
        uint8_t startC = (n > 3) ? (1 + random(n - 2)) : random(n);
        grid[startR][startC] = 1;
        uint8_t SCount = 1;

        uint8_t frontier[81];
        uint8_t frontierCount = 0;

        auto addFrontier = [&](uint8_t r, uint8_t c) {
            const int8_t dr[4] = {-1, 1, 0, 0};
            const int8_t dc[4] = {0, 0, -1, 1};
            for (uint8_t i = 0; i < 4; i++) {
                int8_t nr = (int8_t)r + dr[i];
                int8_t nc = (int8_t)c + dc[i];
                if (nr >= 0 && nr < (int8_t)n && nc >= 0 && nc < (int8_t)n && grid[nr][nc] == 0) {
                    uint8_t idx = (uint8_t)(nr * n + nc);
                    bool exists = false;
                    for (uint8_t f = 0; f < frontierCount; f++) {
                        if (frontier[f] == idx) { exists = true; break; }
                    }
                    if (!exists) frontier[frontierCount++] = idx;
                }
            }
        };

        addFrontier(startR, startC);

        auto isValidToAdd = [&](uint8_t r, uint8_t c) -> bool {
            int8_t r0_list[4] = {(int8_t)((int)r - 1), (int8_t)((int)r - 1), (int8_t)r, (int8_t)r};
            int8_t c0_list[4] = {(int8_t)((int)c - 1), (int8_t)c, (int8_t)((int)c - 1), (int8_t)c};
            for (uint8_t i = 0; i < 4; i++) {
                int8_t r0 = r0_list[i];
                int8_t c0 = c0_list[i];
                if (r0 >= 0 && r0 < (int8_t)n - 1 && c0 >= 0 && c0 < (int8_t)n - 1) {
                    uint8_t b0 = (r0 == r && c0 == c) ? 1 : grid[r0][c0];
                    uint8_t b1 = (r0 == r && c0 + 1 == c) ? 1 : grid[r0][c0 + 1];
                    uint8_t b2 = (r0 + 1 == r && c0 == c) ? 1 : grid[r0 + 1][c0];
                    uint8_t b3 = (r0 + 1 == r && c0 + 1 == c) ? 1 : grid[r0 + 1][c0 + 1];
                    if ((b0 == 1 && b1 == 0 && b2 == 0 && b3 == 1) ||
                        (b0 == 0 && b1 == 1 && b2 == 1 && b3 == 0)) {
                        return false;
                    }
                }
            }
            return true;
        };

        auto complementConnected = [&]() -> bool {
            uint8_t visited[9][9] = {0};
            uint8_t qR[81], qC[81];
            uint8_t qHead = 0, qTail = 0;

            for (uint8_t r = 0; r < n; r++) {
                for (uint8_t c = 0; c < n; c++) {
                    if ((r == 0 || r == n - 1 || c == 0 || c == n - 1) && grid[r][c] == 0) {
                        visited[r][c] = 1;
                        qR[qTail] = r;
                        qC[qTail] = c;
                        qTail++;
                    }
                }
            }

            const int8_t dr[4] = {-1, 1, 0, 0};
            const int8_t dc[4] = {0, 0, -1, 1};
            while (qHead < qTail) {
                uint8_t cr = qR[qHead];
                uint8_t cc = qC[qHead];
                qHead++;
                for (uint8_t i = 0; i < 4; i++) {
                    int8_t nr = (int8_t)cr + dr[i];
                    int8_t nc = (int8_t)cc + dc[i];
                    if (nr >= 0 && nr < (int8_t)n && nc >= 0 && nc < (int8_t)n && !visited[nr][nc] && grid[nr][nc] == 0) {
                        visited[nr][nc] = 1;
                        qR[qTail] = (uint8_t)nr;
                        qC[qTail] = (uint8_t)nc;
                        qTail++;
                    }
                }
            }
            uint8_t zeroCount = 0;
            for (uint8_t r = 0; r < n; r++) {
                for (uint8_t c = 0; c < n; c++) {
                    if (grid[r][c] == 0) zeroCount++;
                }
            }
            return qTail == zeroCount;
        };

        while (SCount < targetCount && frontierCount > 0) {
            uint8_t fIdx = (uint8_t)random(frontierCount);
            uint8_t cand = frontier[fIdx];
            frontier[fIdx] = frontier[frontierCount - 1];
            frontierCount--;

            uint8_t cr = cand / n;
            uint8_t cc = cand % n;

            if (isValidToAdd(cr, cc)) {
                grid[cr][cc] = 1;
                if (complementConnected()) {
                    SCount++;
                    addFrontier(cr, cc);
                } else {
                    grid[cr][cc] = 0;
                }
            }
        }

        if (SCount >= targetCount / 2 && SCount >= 3) {
            // Build H and V
            for (uint8_t r = 0; r <= n; r++) {
                for (uint8_t c = 0; c < n; c++) {
                    uint8_t top = (r > 0) ? grid[r - 1][c] : 0;
                    uint8_t bot = (r < n) ? grid[r][c] : 0;
                    _solutionH[r][c] = (top != bot) ? 1 : 0;
                }
            }
            for (uint8_t r = 0; r < n; r++) {
                for (uint8_t c = 0; c <= n; c++) {
                    uint8_t left = (c > 0) ? grid[r][c - 1] : 0;
                    uint8_t right = (c < n) ? grid[r][c] : 0;
                    _solutionV[r][c] = (left != right) ? 1 : 0;
                }
            }
            for (uint8_t r = 0; r < n; r++) {
                for (uint8_t c = 0; c < n; c++) {
                    _clues[r][c] = _solutionH[r][c] + _solutionH[r + 1][c] + _solutionV[r][c] + _solutionV[r][c + 1];
                }
            }

            // Verify single closed loop on dot lattice
            uint8_t deg[10][10] = {0};
            for (uint8_t r = 0; r <= n; r++) {
                for (uint8_t c = 0; c < n; c++) {
                    if (_solutionH[r][c]) {
                        deg[r][c]++;
                        deg[r][c + 1]++;
                    }
                }
            }
            for (uint8_t r = 0; r < n; r++) {
                for (uint8_t c = 0; c <= n; c++) {
                    if (_solutionV[r][c]) {
                        deg[r][c]++;
                        deg[r + 1][c]++;
                    }
                }
            }

            bool validDeg = true;
            uint8_t activeNodes = 0;
            for (uint8_t r = 0; r <= n; r++) {
                for (uint8_t c = 0; c <= n; c++) {
                    if (deg[r][c] != 0 && deg[r][c] != 2) validDeg = false;
                    if (deg[r][c] == 2) activeNodes++;
                }
            }
            if (!validDeg || activeNodes < 8) continue;

            return true;
        }
    }
    return false;
}

bool LoopGen::solveDeductive(int8_t clues[9][9], uint8_t n, int8_t H[10][9], int8_t V[9][10]) {
    // 0 = UNKNOWN, 1 = LOOP, -1 = EMPTY
    for (uint8_t r = 0; r <= n; r++) {
        for (uint8_t c = 0; c < n; c++) H[r][c] = 0;
    }
    for (uint8_t r = 0; r < n; r++) {
        for (uint8_t c = 0; c <= n; c++) V[r][c] = 0;
    }

    bool changed = true;
    while (changed) {
        changed = false;

        // 1. Clue propagation
        for (uint8_t r = 0; r < n; r++) {
            for (uint8_t c = 0; c < n; c++) {
                int8_t k = clues[r][c];
                if (k < 0) continue;

                int8_t edgeVals[4] = {H[r][c], H[r + 1][c], V[r][c], V[r][c + 1]};
                uint8_t loopCnt = 0, emptyCnt = 0, unkCnt = 0;
                for (uint8_t i = 0; i < 4; i++) {
                    if (edgeVals[i] == 1) loopCnt++;
                    else if (edgeVals[i] == -1) emptyCnt++;
                    else unkCnt++;
                }

                if (loopCnt > k || loopCnt + unkCnt < k) return false;

                if (unkCnt > 0) {
                    if (loopCnt == k) {
                        if (H[r][c] == 0) { H[r][c] = -1; changed = true; }
                        if (H[r + 1][c] == 0) { H[r + 1][c] = -1; changed = true; }
                        if (V[r][c] == 0) { V[r][c] = -1; changed = true; }
                        if (V[r][c + 1] == 0) { V[r][c + 1] = -1; changed = true; }
                    } else if (loopCnt + unkCnt == k) {
                        if (H[r][c] == 0) { H[r][c] = 1; changed = true; }
                        if (H[r + 1][c] == 0) { H[r + 1][c] = 1; changed = true; }
                        if (V[r][c] == 0) { V[r][c] = 1; changed = true; }
                        if (V[r][c + 1] == 0) { V[r][c + 1] = 1; changed = true; }
                    }
                }
            }
        }

        // 2. Vertex degree conservation
        for (uint8_t r = 0; r <= n; r++) {
            for (uint8_t c = 0; c <= n; c++) {
                int8_t incVals[4];
                uint8_t incCnt = 0;
                if (c > 0) incVals[incCnt++] = H[r][c - 1];
                if (c < n) incVals[incCnt++] = H[r][c];
                if (r > 0) incVals[incCnt++] = V[r - 1][c];
                if (r < n) incVals[incCnt++] = V[r][c];

                uint8_t dLoop = 0, dEmpty = 0, dUnk = 0;
                for (uint8_t i = 0; i < incCnt; i++) {
                    if (incVals[i] == 1) dLoop++;
                    else if (incVals[i] == -1) dEmpty++;
                    else dUnk++;
                }

                if (dLoop > 2 || (dLoop == 1 && dUnk == 0)) return false;

                if (dLoop == 2 && dUnk > 0) {
                    if (c > 0 && H[r][c - 1] == 0) { H[r][c - 1] = -1; changed = true; }
                    if (c < n && H[r][c] == 0) { H[r][c] = -1; changed = true; }
                    if (r > 0 && V[r - 1][c] == 0) { V[r - 1][c] = -1; changed = true; }
                    if (r < n && V[r][c] == 0) { V[r][c] = -1; changed = true; }
                } else if (dLoop == 1 && dUnk == 1) {
                    if (c > 0 && H[r][c - 1] == 0) { H[r][c - 1] = 1; changed = true; }
                    if (c < n && H[r][c] == 0) { H[r][c] = 1; changed = true; }
                    if (r > 0 && V[r - 1][c] == 0) { V[r - 1][c] = 1; changed = true; }
                    if (r < n && V[r][c] == 0) { V[r][c] = 1; changed = true; }
                } else if (dLoop == 0 && dUnk == 1) {
                    if (c > 0 && H[r][c - 1] == 0) { H[r][c - 1] = -1; changed = true; }
                    if (c < n && H[r][c] == 0) { H[r][c] = -1; changed = true; }
                    if (r > 0 && V[r - 1][c] == 0) { V[r - 1][c] = -1; changed = true; }
                    if (r < n && V[r][c] == 0) { V[r][c] = -1; changed = true; }
                }
            }
        }
    }

    // Check if any edge remains unknown
    for (uint8_t r = 0; r <= n; r++) {
        for (uint8_t c = 0; c < n; c++) {
            if (H[r][c] == 0) return false;
        }
    }
    for (uint8_t r = 0; r < n; r++) {
        for (uint8_t c = 0; c <= n; c++) {
            if (V[r][c] == 0) return false;
        }
    }
    return true;
}

void LoopGen::generate(LoopDifficulty difficulty) {
    _size = (difficulty == LOOP_EASY) ? 6 : ((difficulty == LOOP_HARD) ? 9 : 7);

    for (uint8_t attempt = 0; attempt < 20; attempt++) {
        if (!generatePolyominoLoop(_size)) continue;

        // Thin clues
        uint8_t cellCoords[81];
        for (uint8_t i = 0; i < _size * _size; i++) cellCoords[i] = i;
        shuffleLoopIndices(cellCoords, _size * _size);

        float retainPct = (difficulty == LOOP_EASY) ? 0.58f : ((difficulty == LOOP_HARD) ? 0.38f : 0.48f);
        uint8_t targetClues = (uint8_t)(_size * _size * retainPct);
        uint8_t currentClues = _size * _size;

        int8_t testH[10][9], testV[9][10];
        for (uint8_t i = 0; i < _size * _size; i++) {
            if (currentClues <= targetClues) break;
            uint8_t r = cellCoords[i] / _size;
            uint8_t c = cellCoords[i] % _size;
            int8_t saved = _clues[r][c];
            _clues[r][c] = -1;

            if (solveDeductive(_clues, _size, testH, testV)) {
                currentClues--;
            } else {
                _clues[r][c] = saved;
            }
        }
        return;
    }
}

void LoopGen::printToReceipt(EscPosPrinter& printer, LoopDifficulty diff) {
    const char* diffStr = (diff == LOOP_EASY) ? "EASY" : ((diff == LOOP_HARD) ? "HARD" : "MEDIUM");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- LOOP ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Draw a single continuous closed loop connecting dots");
    printer.println("so each number matches its edge count.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    for (uint8_t r = 0; r < _size; r++) {
        String dotLine = "      ";
        for (uint8_t c = 0; c < _size; c++) dotLine += ".   ";
        dotLine += ".";
        printer.println(dotLine);

        String clueLine = "      ";
        for (uint8_t c = 0; c < _size; c++) {
            int8_t k = _clues[r][c];
            if (k >= 0) clueLine += String("  ") + k + " ";
            else clueLine += "    ";
        }
        clueLine += " ";
        printer.println(clueLine);
    }
    String lastDotLine = "      ";
    for (uint8_t c = 0; c < _size; c++) lastDotLine += ".   ";
    lastDotLine += ".";
    printer.println(lastDotLine);
    printer.println("");
}

bool LoopGen::printRasterToReceipt(EscPosPrinter& printer, LoopDifficulty diff) {
    const char* diffStr = (diff == LOOP_EASY) ? "EASY" : ((diff == LOOP_HARD) ? "HARD" : "MEDIUM");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- LOOP ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Draw a single continuous closed loop connecting dots");
    printer.println("so each number matches its edge count.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    int16_t cellSize = (_size == 6) ? 54 : ((_size == 9) ? 36 : 46);
    int16_t padding = (_size == 7) ? 27 : 26;
    int16_t boardSize = cellSize * _size;
    int16_t leftMargin = (THERMAL_CANVAS_WIDTH - boardSize) / 2;
    int16_t totalH = padding + boardSize + padding;
    totalH = ((totalH + 7) / 8) * 8;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Draw dots (clean Nikoli style: 4px diameter filled circles)
    for (uint8_t r = 0; r <= _size; r++) {
        int16_t py = padding + r * cellSize;
        for (uint8_t c = 0; c <= _size; c++) {
            int16_t px = leftMargin + c * cellSize;
            canvas.fillCircle(px, py, 2, 1);
        }
    }

    // Draw clue numbers
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            int8_t k = _clues[r][c];
            if (k >= 0) {
                int16_t tx = leftMargin + c * cellSize + (cellSize - 18) / 2;
                int16_t ty = padding + r * cellSize + (cellSize - 21) / 2;
                canvas.drawChar(tx, ty, '0' + k, 3, 1);
            }
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}
