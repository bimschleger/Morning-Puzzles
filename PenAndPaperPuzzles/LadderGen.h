#ifndef LADDER_GEN_H
#define LADDER_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum LadderDifficulty {
    LADDER_EASY   = 0,
    LADDER_MEDIUM = 1,
    LADDER_HARD   = 2
};

class LadderGen {
public:
    LadderGen();

    void generate(LadderDifficulty difficulty = LADDER_MEDIUM);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    uint8_t getWordLen() const { return _wordLen; }
    uint8_t getTotalWords() const { return _totalWords; }
    uint8_t getIntermediateCount() const { return (_totalWords > 2) ? (_totalWords - 2) : 0; }
    const char* getStartWord() const { return _words[0]; }
    const char* getTargetWord() const { return (_totalWords > 0) ? _words[_totalWords - 1] : ""; }
    const char* getWord(uint8_t idx) const { return (idx < _totalWords) ? _words[idx] : ""; }

private:
    static const uint8_t MAX_RUNGS = 8;
    static const uint8_t MAX_WORD_LEN = 6;
    char _words[MAX_RUNGS][MAX_WORD_LEN];
    uint8_t _wordLen;
    uint8_t _totalWords;
    LadderDifficulty _difficulty;
};

#endif // LADDER_GEN_H
