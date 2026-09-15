#include "WordSearchGen.h"
#include "WordSearchDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

WordSearchGen::WordSearchGen() : _gridSize(12), _currentTheme("General") {
    memset(_grid, ' ', sizeof(_grid));
}

bool WordSearchGen::tryPlaceWord(const char* word, const int8_t dirs[][2], uint8_t numDirs) {
    uint8_t len = strlen(word);
    if (len > _gridSize) return false;

    for (int attempts = 0; attempts < 150; attempts++) {
        uint8_t dIdx = random(numDirs);
        int8_t dr = dirs[dIdx][0];
        int8_t dc = dirs[dIdx][1];

        int rStart = random(_gridSize);
        int cStart = random(_gridSize);

        int rEnd = rStart + dr * (len - 1);
        int cEnd = cStart + dc * (len - 1);

        if (rEnd >= 0 && rEnd < _gridSize && cEnd >= 0 && cEnd < _gridSize) {
            bool fits = true;
            for (int i = 0; i < len; i++) {
                char current = _grid[rStart + dr * i][cStart + dc * i];
                if (current != ' ' && current != word[i]) {
                    fits = false;
                    break;
                }
            }

            if (fits) {
                for (int i = 0; i < len; i++) {
                    _grid[rStart + dr * i][cStart + dc * i] = word[i];
                }
                _placedWords.push_back({String(word), (uint8_t)rStart, (uint8_t)cStart, dr, dc});
                return true;
            }
        }
    }
    return false;
}

void WordSearchGen::generate(WordSearchDifficulty difficulty, int themeIndex) {
    _gridSize = (difficulty == WS_EASY) ? 10 : 12;
    memset(_grid, ' ', sizeof(_grid));
    _placedWords.clear();

    size_t poolCount = 0;
    const ThemeDef* pool = getWordSearchPool(difficulty, poolCount);

    if (themeIndex < 0 || themeIndex >= (int)poolCount) {
        themeIndex = random(poolCount);
    }
    const ThemeDef& chosenTheme = pool[themeIndex];
    _currentTheme = chosenTheme.name;

    int8_t dirs[8][2];
    uint8_t numDirs = 0;
    uint8_t targetWords = 8;

    if (difficulty == WS_EASY) {
        // Left-to-Right only (E)
        dirs[0][0] = 0; dirs[0][1] = 1;
        numDirs = 1;
        targetWords = 6;
    } else if (difficulty == WS_HARD) {
        // All 8 directions
        int8_t allDirs[8][2] = {
            {0, 1},   // E
            {0, -1},  // W
            {1, 0},   // S
            {-1, 0},  // N
            {1, 1},   // SE
            {-1, 1},  // NE
            {1, -1},  // SW
            {-1, -1}  // NW
        };
        memcpy(dirs, allDirs, sizeof(allDirs));
        numDirs = 8;
        targetWords = 10;
    } else {
        // WS_MEDIUM: E, W, S
        int8_t medDirs[3][2] = {
            {0, 1},   // E
            {0, -1},  // W
            {1, 0}    // S
        };
        memcpy(dirs, medDirs, sizeof(medDirs));
        numDirs = 3;
        targetWords = 8;
    }

    // Sort words by length descending to place longer words first on empty grid
    const char* sortedWords[12];
    for (int i = 0; i < 12; i++) {
        sortedWords[i] = chosenTheme.words[i];
    }
    std::sort(sortedWords, sortedWords + 12, [](const char* a, const char* b) {
        return strlen(a) > strlen(b);
    });

    char bestGrid[MAX_GRID_SIZE][MAX_GRID_SIZE];
    std::vector<PlacedWord> bestPlaced;

    for (int retry = 0; retry < 5; retry++) {
        memset(_grid, ' ', sizeof(_grid));
        _placedWords.clear();

        for (int i = 0; i < 12; i++) {
            if (_placedWords.size() >= targetWords) break;
            tryPlaceWord(sortedWords[i], dirs, numDirs);
        }

        if (_placedWords.size() > bestPlaced.size()) {
            memcpy(bestGrid, _grid, sizeof(_grid));
            bestPlaced = _placedWords;
        }

        if (bestPlaced.size() >= targetWords) break;
    }

    memcpy(_grid, bestGrid, sizeof(_grid));
    _placedWords = bestPlaced;

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
    printer.setBold(true);
    printer.println("--- SEARCH ---");
    printer.setBold(false);
    printer.println(String("Find all ") + _placedWords.size() + " hidden words listed below.");
    printer.println("");

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
    printer.println(String("Theme: ") + _currentTheme);

    // Print word list in 2 columns
    for (size_t i = 0; i < _placedWords.size(); i += 2) {
        String col1 = "[ ] " + _placedWords[i].word;
        String col2 = (i + 1 < _placedWords.size()) ? ("[ ] " + _placedWords[i + 1].word) : "";
        printer.printKeyValue(col1, col2, 44);
    }
    printer.println("");
}

bool WordSearchGen::printRasterToReceipt(EscPosPrinter& printer) {
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- SEARCH ---");
    printer.setBold(false);
    printer.println(String("Find all ") + _placedWords.size() + " hidden words listed below.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t cellSize = (THERMAL_CANVAS_WIDTH - 48) / _gridSize;
    const int16_t innerWidth = cellSize * _gridSize;
    const int16_t padding = (THERMAL_CANVAS_WIDTH - innerWidth) / 2;
    const int16_t gridH = cellSize * _gridSize;

    const int16_t checklistRows = (int16_t)((_placedWords.size() + 1) / 2);
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

    // Theme banner
    String themeStr = String("THEME: ") + _currentTheme;
    themeStr.toUpperCase();
    canvas.drawText(padding, curY, themeStr.c_str(), 2);
    curY += 28;

    // Word checklist
    int16_t colW = innerWidth / 2;
    for (size_t i = 0; i < _placedWords.size(); i++) {
        int16_t colIdx = i % 2;
        int16_t rowIdx = i / 2;
        int16_t ix = padding + colIdx * colW;
        int16_t iy = curY + rowIdx * 28;
        canvas.drawRect(ix, iy + 2, 16, 16, 2);
        String w = _placedWords[i].word;
        w.toUpperCase();
        canvas.drawText(ix + 24, iy + 2, w.c_str(), 2);
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

