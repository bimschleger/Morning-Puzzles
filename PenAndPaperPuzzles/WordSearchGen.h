#ifndef WORD_SEARCH_GEN_H
#define WORD_SEARCH_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum WordSearchDifficulty {
    WS_EASY   = 0, // Horizontal & Vertical forward (10x10)
    WS_MEDIUM = 1, // All 8 directions, multi-intersection (12x12)
    WS_HARD   = 2  // All 8 directions, 8-way compass spread, multi-intersection (12x12)
};

class WordSearchGen {
public:
    static const uint8_t MAX_GRID_SIZE = 12;

    WordSearchGen();

    void generate(WordSearchDifficulty difficulty = WS_MEDIUM, int seed = -1);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    const char* getThemeName() const { return _currentTheme; }
    size_t getWordCount() const { return _numPlacedWords; }
    uint8_t getGridSize() const { return _gridSize; }
    char getGridChar(uint8_t r, uint8_t c) const { return _grid[r][c]; }
    String getPlacedWord(size_t i) const { return (i < _numPlacedWords) ? String(_placedWords[i]) : String(""); }
    const char* getPlacedWordRaw(size_t i) const { return (i < _numPlacedWords) ? _placedWords[i] : ""; }

private:
    uint8_t _gridSize;
    char _grid[MAX_GRID_SIZE][MAX_GRID_SIZE];
    const char* _placedWords[12];
    uint8_t _numPlacedWords;
    const char* _currentTheme;
};

#endif // WORD_SEARCH_GEN_H
