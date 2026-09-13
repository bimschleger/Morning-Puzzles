#include "WordSearchGen.h"
#include "WordSearchDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

WordSearchGen::WordSearchGen() : _currentTheme("General") {
    memset(_grid, ' ', sizeof(_grid));
}

bool WordSearchGen::tryPlaceWord(const char* word, const int8_t dirs[][2], uint8_t numDirs) {
    uint8_t len = strlen(word);
    if (len > GRID_SIZE) return false;

    for (int attempts = 0; attempts < 100; attempts++) {
        uint8_t dIdx = random(numDirs);
        int8_t dr = dirs[dIdx][0];
        int8_t dc = dirs[dIdx][1];

        int rStart = random(GRID_SIZE);
        int cStart = random(GRID_SIZE);

        int rEnd = rStart + dr * (len - 1);
        int cEnd = cStart + dc * (len - 1);

        if (rEnd >= 0 && rEnd < GRID_SIZE && cEnd >= 0 && cEnd < GRID_SIZE) {
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
    memset(_grid, ' ', sizeof(_grid));
    _placedWords.clear();

    size_t poolCount = 0;
    const ThemeDef* pool = getWordSearchPool(difficulty, poolCount);

    if (themeIndex < 0 || themeIndex >= (int)poolCount) {
        themeIndex = random(poolCount);
    }
    const ThemeDef& chosenTheme = pool[themeIndex];
    _currentTheme = chosenTheme.name;

    // Define direction vectors according to difficulty
    int8_t dirs[8][2] = {
        {0, 1},   // E
        {1, 0},   // S
        {1, 1},   // SE
        {-1, 1},  // NE
        {0, -1},  // W
        {-1, 0},  // N
        {1, -1},  // SW
        {-1, -1}  // NW
    };

    uint8_t numDirs = 2; // Easy: E, S
    if (difficulty == WS_MEDIUM) numDirs = 4; // Medium: E, S, SE, NE
    else if (difficulty == WS_HARD) numDirs = 8; // Hard: all 8 directions

    // Sort words by length descending to place longer words first on empty grid
    const char* sortedWords[12];
    for (int i = 0; i < 12; i++) {
        sortedWords[i] = chosenTheme.words[i];
    }
    std::sort(sortedWords, sortedWords + 12, [](const char* a, const char* b) {
        return strlen(a) > strlen(b);
    });

    char bestGrid[GRID_SIZE][GRID_SIZE];
    std::vector<PlacedWord> bestPlaced;

    for (int retry = 0; retry < 5; retry++) {
        memset(_grid, ' ', sizeof(_grid));
        _placedWords.clear();

        for (int i = 0; i < 12; i++) {
            if (_placedWords.size() >= 8) break;
            tryPlaceWord(sortedWords[i], dirs, numDirs);
        }

        if (_placedWords.size() > bestPlaced.size()) {
            memcpy(bestGrid, _grid, sizeof(_grid));
            bestPlaced = _placedWords;
        }

        if (bestPlaced.size() >= 8) break;
    }

    memcpy(_grid, bestGrid, sizeof(_grid));
    _placedWords = bestPlaced;

    // Fill remaining blank cells with random uppercase letters
    for (uint8_t r = 0; r < GRID_SIZE; r++) {
        for (uint8_t c = 0; c < GRID_SIZE; c++) {
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

    // Print 12x12 grid centered
    for (uint8_t r = 0; r < GRID_SIZE; r++) {
        String line = "    ";
        for (uint8_t c = 0; c < GRID_SIZE; c++) {
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

    const int16_t padding = 24;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t cellSize = boardSize / GRID_SIZE;
    const int16_t gridH = cellSize * GRID_SIZE;
    const int16_t totalH = padding + gridH + padding;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Outer border
    canvas.drawRect(padding, padding, gridH, gridH, 3);

    // Letter matrix
    for (uint8_t r = 0; r < GRID_SIZE; r++) {
        for (uint8_t c = 0; c < GRID_SIZE; c++) {
            char letter = _grid[r][c];
            int16_t cx = padding + c * cellSize + (cellSize - 12) / 2;
            int16_t cy = padding + r * cellSize + (cellSize - 14) / 2;
            canvas.drawChar(cx, cy, letter, 2);
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();

    if (ok) {
        printer.println("");
        printer.println(String("Theme: ") + _currentTheme);
        for (size_t i = 0; i < _placedWords.size(); i += 2) {
            String col1 = "[ ] " + _placedWords[i].word;
            String col2 = (i + 1 < _placedWords.size()) ? ("[ ] " + _placedWords[i + 1].word) : "";
            printer.printKeyValue(col1, col2, 44);
        }
        printer.println("");
    }

    return ok;
}

