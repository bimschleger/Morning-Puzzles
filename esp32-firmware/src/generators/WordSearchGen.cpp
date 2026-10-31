#include "WordSearchGen.h"
#include "WordSearchDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

#ifndef pgm_read_ptr
#define pgm_read_ptr(addr) (*(const void* const*)(addr))
#endif

static const int8_t WS_ALL_DIRS[8][2] = {
    {0, 1},   // E  (0)
    {0, -1},  // W  (1)
    {1, 0},   // S  (2)
    {-1, 0},  // N  (3)
    {1, 1},   // SE (4)
    {-1, 1},  // NE (5)
    {1, -1},  // SW (6)
    {-1, -1}  // NW (7)
};

WordSearchGen::WordSearchGen() : _gridSize(12), _numPlacedWords(0), _currentTheme("") {
    memset(_grid, ' ', sizeof(_grid));
}

void WordSearchGen::generate(WordSearchDifficulty difficulty, int seed) {
    if (seed >= 0) {
        randomSeed(seed);
    }

    _gridSize = (difficulty == WS_EASY) ? 10 : 12;
    uint8_t targetCount = (difficulty == WS_EASY) ? 6 : 8;
    uint8_t minIntersections = (difficulty == WS_EASY) ? 0 : ((difficulty == WS_MEDIUM) ? 2 : 3);
    _currentTheme = "";

    size_t poolCount = 0;
    const char* const* pool = getWordSearchPool(difficulty, poolCount);
    if (!pool || poolCount == 0) {
        return;
    }

    char bestGrid[MAX_GRID_SIZE][MAX_GRID_SIZE];
    const char* bestPlaced[12];
    uint8_t bestCount = 0;
    int16_t bestIntersections = -1;

    struct CandidatePos {
        int8_t r;
        int8_t c;
        int8_t dIdx;
    };

    struct WordPlacement {
        int8_t r;
        int8_t c;
        int8_t dIdx;
        uint8_t len;
    };

    WordPlacement bestPlacements[12];

    for (uint8_t restart = 0; restart < 8; restart++) {
        // Pick (targetCount + 4) words without replacement
        const uint8_t sampleSize = targetCount + 4;
        const char* sampledWords[16];
        uint16_t chosenIndices[16];
        uint8_t picked = 0;

        while (picked < sampleSize) {
            uint16_t idx = random(poolCount);
            bool dup = false;
            for (uint8_t j = 0; j < picked; j++) {
                if (chosenIndices[j] == idx) {
                    dup = true;
                    break;
                }
            }
            if (!dup) {
                chosenIndices[picked] = idx;
                sampledWords[picked] = (const char*)pgm_read_ptr(&pool[idx]);
                picked++;
            }
        }

        // Sort descending by length
        for (uint8_t i = 1; i < sampleSize; i++) {
            const char* key = sampledWords[i];
            int8_t j = i - 1;
            while (j >= 0 && strlen(sampledWords[j]) < strlen(key)) {
                sampledWords[j + 1] = sampledWords[j];
                j--;
            }
            sampledWords[j + 1] = key;
        }

        // Prepare directional assignment
        uint8_t hardDirs[8] = {0, 1, 2, 3, 4, 5, 6, 7};
        if (difficulty == WS_HARD) {
            for (int i = 7; i > 0; i--) {
                int j = random(i + 1);
                uint8_t tmp = hardDirs[i];
                hardDirs[i] = hardDirs[j];
                hardDirs[j] = tmp;
            }
        }

        char tempGrid[MAX_GRID_SIZE][MAX_GRID_SIZE];
        memset(tempGrid, ' ', sizeof(tempGrid));

        const char* currentPlaced[12];
        WordPlacement currentPlacements[12];
        uint8_t currentCount = 0;

        for (uint8_t wIdx = 0; wIdx < sampleSize && currentCount < targetCount; wIdx++) {
            const char* word = sampledWords[wIdx];
            uint8_t len = strlen(word);
            if (len > _gridSize) continue;

            uint8_t allowedDirs[8];
            uint8_t numAllowed = 0;

            if (difficulty == WS_HARD) {
                allowedDirs[0] = hardDirs[currentCount];
                numAllowed = 1;
            } else if (difficulty == WS_EASY) {
                allowedDirs[0] = 0; // E
                allowedDirs[1] = 2; // S
                numAllowed = 2;
                if (random(2) == 1) {
                    allowedDirs[0] = 2;
                    allowedDirs[1] = 0;
                }
            } else { // WS_MEDIUM
                for (uint8_t d = 0; d < 8; d++) allowedDirs[d] = d;
                numAllowed = 8;
                for (int i = 7; i > 0; i--) {
                    int j = random(i + 1);
                    uint8_t tmp = allowedDirs[i];
                    allowedDirs[i] = allowedDirs[j];
                    allowedDirs[j] = tmp;
                }
            }

            int16_t bestScore = -1000;
            CandidatePos bestCands[16];
            uint8_t numBestCands = 0;

            for (uint8_t d = 0; d < numAllowed; d++) {
                uint8_t dIdx = allowedDirs[d];
                int8_t dr = WS_ALL_DIRS[dIdx][0];
                int8_t dc = WS_ALL_DIRS[dIdx][1];

                for (uint8_t r = 0; r < _gridSize; r++) {
                    for (uint8_t c = 0; c < _gridSize; c++) {
                        int rEnd = r + dr * (len - 1);
                        int cEnd = c + dc * (len - 1);
                        if (rEnd < 0 || rEnd >= _gridSize || cEnd < 0 || cEnd >= _gridSize) continue;

                        bool fits = true;
                        int overlaps = 0;
                        for (uint8_t i = 0; i < len; i++) {
                            char cur = tempGrid[r + dr * i][c + dc * i];
                            if (cur != ' ') {
                                if (cur == word[i]) {
                                    overlaps++;
                                } else {
                                    fits = false;
                                    break;
                                }
                            }
                        }
                        if (!fits) continue;

                        int16_t score = 0;
                        if (currentCount == 0) {
                            int midR = r + dr * (len / 2);
                            int midC = c + dc * (len / 2);
                            score = 20 - (abs(midR - _gridSize / 2) + abs(midC - _gridSize / 2));
                        } else {
                            score = overlaps * 10;
                        }

                        if (score > bestScore) {
                            bestScore = score;
                            bestCands[0] = {(int8_t)r, (int8_t)c, (int8_t)dIdx};
                            numBestCands = 1;
                        } else if (score == bestScore && numBestCands < 16) {
                            bestCands[numBestCands++] = {(int8_t)r, (int8_t)c, (int8_t)dIdx};
                        }
                    }
                }
            }

            if (numBestCands > 0) {
                uint8_t chosenCand = random(numBestCands);
                int8_t r = bestCands[chosenCand].r;
                int8_t c = bestCands[chosenCand].c;
                int8_t dIdx = bestCands[chosenCand].dIdx;
                int8_t dr = WS_ALL_DIRS[dIdx][0];
                int8_t dc = WS_ALL_DIRS[dIdx][1];

                for (uint8_t i = 0; i < len; i++) {
                    tempGrid[r + dr * i][c + dc * i] = word[i];
                }

                currentPlacements[currentCount] = {r, c, dIdx, len};
                currentPlaced[currentCount] = word;
                currentCount++;
            }
        }

        // Count cell intersections
        uint8_t cellUsage[MAX_GRID_SIZE][MAX_GRID_SIZE];
        memset(cellUsage, 0, sizeof(cellUsage));
        for (uint8_t p = 0; p < currentCount; p++) {
            int8_t r = currentPlacements[p].r;
            int8_t c = currentPlacements[p].c;
            int8_t dIdx = currentPlacements[p].dIdx;
            uint8_t len = currentPlacements[p].len;
            int8_t dr = WS_ALL_DIRS[dIdx][0];
            int8_t dc = WS_ALL_DIRS[dIdx][1];
            for (uint8_t i = 0; i < len; i++) {
                cellUsage[r + dr * i][c + dc * i]++;
            }
        }

        int16_t intersections = 0;
        for (uint8_t r = 0; r < _gridSize; r++) {
            for (uint8_t c = 0; c < _gridSize; c++) {
                if (cellUsage[r][c] >= 2) {
                    intersections++;
                }
            }
        }

        if (currentCount == targetCount) {
            if (intersections > bestIntersections) {
                bestIntersections = intersections;
                memcpy(bestGrid, tempGrid, sizeof(bestGrid));
                memcpy(bestPlaced, currentPlaced, sizeof(bestPlaced));
                memcpy(bestPlacements, currentPlacements, sizeof(bestPlacements));
                bestCount = currentCount;
            }
            if (intersections >= minIntersections) {
                break;
            }
        }
    }

    if (bestCount > 0) {
        memcpy(_grid, bestGrid, sizeof(_grid));
        memcpy(_placedWords, bestPlaced, sizeof(_placedWords));
        _numPlacedWords = bestCount;
    } else {
        _numPlacedWords = 0;
    }

    // Fill remaining blank cells with random uppercase letters
    for (uint8_t r = 0; r < _gridSize; r++) {
        for (uint8_t c = 0; c < _gridSize; c++) {
            if (_grid[r][c] == ' ') {
                _grid[r][c] = (char)('A' + random(26));
            }
        }
    }
}

void WordSearchGen::printToReceipt(EscPosPrinter& printer) {
    // Print grid centered
    for (uint8_t r = 0; r < _gridSize; r++) {
        String line = (_gridSize == 10) ? "      " : "    ";
        for (uint8_t c = 0; c < _gridSize; c++) {
            line += _grid[r][c];
            line += " ";
        }
        printer.println(line);
    }

    printer.println("");
    if (_currentTheme && _currentTheme[0] != '\0') {
        printer.println(String("Theme: ") + _currentTheme);
    }
    printer.println("Words to find:");

    // Print word list in 2 columns
    for (size_t i = 0; i < _numPlacedWords; i += 2) {
        String col1 = String("[ ] ") + _placedWords[i];
        String col2 = (i + 1 < _numPlacedWords) ? (String("[ ] ") + _placedWords[i + 1]) : "";
        printer.printKeyValue(col1, col2, 44);
    }
    printer.println("");
}

bool WordSearchGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t cellSize = (THERMAL_CANVAS_WIDTH - 48) / _gridSize;
    const int16_t innerWidth = cellSize * _gridSize;
    const int16_t padding = (THERMAL_CANVAS_WIDTH - innerWidth) / 2;
    const int16_t gridH = cellSize * _gridSize;

    const int16_t checklistRows = (int16_t)((_numPlacedWords + 1) / 2);
    const int16_t checklistH = 40 + checklistRows * 28;
    const int16_t totalH = 12 + gridH + 20 + checklistH + 12;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    const int16_t gridY = 12;

    // Outer border
    canvas.drawRect(padding, gridY, innerWidth, gridH, 4);

    // Letter matrix & inner grid lines
    for (uint8_t r = 0; r < _gridSize; r++) {
        for (uint8_t c = 0; c < _gridSize; c++) {
            char letter = _grid[r][c];
            int16_t cx = padding + c * cellSize + (cellSize - 18) / 2;
            int16_t cy = gridY + r * cellSize + (cellSize - 21) / 2;
            canvas.drawChar(cx, cy, letter, 3);
            if (c > 0) {
                canvas.drawVLine(padding + c * cellSize, gridY, gridH, 1);
            }
        }
        if (r > 0) {
            canvas.drawHLine(padding, gridY + r * cellSize, innerWidth, 1);
        }
    }

    // Divider line
    int16_t curY = gridY + gridH + 16;
    canvas.drawHLine(padding, curY, innerWidth, 2);
    curY += 18;

    if (_currentTheme && _currentTheme[0] != '\0') {
        String themeStr = String("THEME: ") + _currentTheme;
        themeStr.toUpperCase();
        canvas.drawText(padding, curY, themeStr.c_str(), 2);
    } else {
        canvas.drawText(padding, curY, "WORDS TO FIND:", 2);
    }
    curY += 28;

    // Word checklist
    int16_t colW = innerWidth / 2;
    for (size_t i = 0; i < _numPlacedWords; i++) {
        int16_t colIdx = i % 2;
        int16_t rowIdx = i / 2;
        int16_t ix = padding + colIdx * colW;
        int16_t iy = curY + rowIdx * 28;
        canvas.drawRect(ix, iy + 2, 16, 16, 2);
        String w = _placedWords[i];
        w.toUpperCase();
        canvas.drawText(ix + 24, iy + 2, w.c_str(), 2);
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}
