#include "WordSearchGen.h"
#include "../printer/EscPosPrinter.h"

struct ThemeDef {
    const char* name;
    const char* words[12];
};

static const ThemeDef THEMES[] = {
    {
        "Morning Routine",
        {"COFFEE", "SUNRISE", "PANCAKE", "WAFFLE", "TOAST", "OATMEAL", 
         "SHOWER", "ALARM", "PAPER", "JOGGING", "TEAPOT", "KITCHEN"}
    },
    {
        "Great Outdoors",
        {"FOREST", "CANYON", "RIVER", "SUMMIT", "VALLEY", "STREAM", 
         "MEADOW", "GLACIER", "BOULDER", "ISLAND", "DESERT", "TRAIL"}
    },
    {
        "Space & Cosmos",
        {"PLANET", "GALAXY", "METEOR", "ORBIT", "NEBULA", "COMET", 
         "ECLIPSE", "PULSAR", "ROCKET", "GRAVITY", "STELLAR", "SOLAR"}
    },
    {
        "Wildlife",
        {"FALCON", "DOLPHIN", "BADGER", "JAGUAR", "OTTER", "COUGAR", 
         "PENGUIN", "CHEETAH", "GIRAFFE", "BEAVER", "OSPREY", "PANTHER"}
    },
    {
        "Technology",
        {"SYSTEM", "SERVER", "ROUTER", "MEMORY", "SOCKET", "SENSOR", 
         "CIRCUIT", "BINARY", "BUFFER", "KERNEL", "PYTHON", "DEVICE"}
    }
};

static const size_t NUM_THEMES = sizeof(THEMES) / sizeof(THEMES[0]);

WordSearchGen::WordSearchGen() : _currentTheme("General") {
    memset(_grid, ' ', sizeof(_grid));
}

bool WordSearchGen::tryPlaceWord(const char* word, int8_t dr, int8_t dc) {
    uint8_t len = strlen(word);
    if (len > GRID_SIZE) return false;

    for (int attempts = 0; attempts < 50; attempts++) {
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

    if (themeIndex < 0 || themeIndex >= (int)NUM_THEMES) {
        themeIndex = random(NUM_THEMES);
    }
    const ThemeDef& chosenTheme = THEMES[themeIndex];
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

    // Try placing words (aim for 8 words)
    for (int i = 0; i < 12; i++) {
        if (_placedWords.size() >= 8) break;
        uint8_t dIdx = random(numDirs);
        tryPlaceWord(chosenTheme.words[i], dirs[dIdx][0], dirs[dIdx][1]);
    }

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
    printer.println("Find and circle all of the listed words hidden");
    printer.println("horizontally, vertically, or diagonally.");
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
