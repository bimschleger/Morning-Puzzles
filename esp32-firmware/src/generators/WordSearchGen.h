#ifndef WORD_SEARCH_GEN_H
#define WORD_SEARCH_GEN_H

#include <Arduino.h>
#include <vector>
class EscPosPrinter;

enum WordSearchDifficulty {
    WS_EASY   = 0, // Horizontal & Vertical forward
    WS_MEDIUM = 1, // Forward directions + diagonals
    WS_HARD   = 2  // All 8 directions including backwards
};

struct PlacedWord {
    String word;
    uint8_t row;
    uint8_t col;
    int8_t dr;
    int8_t dc;
};

class WordSearchGen {
public:
    static const uint8_t GRID_SIZE = 12;

    WordSearchGen();

    void generate(WordSearchDifficulty difficulty = WS_MEDIUM, int themeIndex = -1);
    void printToReceipt(EscPosPrinter& printer);

    const char* getThemeName() const { return _currentTheme; }
    size_t getWordCount() const { return _placedWords.size(); }

private:
    char _grid[GRID_SIZE][GRID_SIZE];
    std::vector<PlacedWord> _placedWords;
    const char* _currentTheme;

    bool tryPlaceWord(const char* word, const int8_t dirs[][2], uint8_t numDirs);
};

#endif // WORD_SEARCH_GEN_H
