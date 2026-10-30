#ifndef JUMBLE_GEN_H
#define JUMBLE_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum JumbleDifficulty {
    JUMBLE_EASY   = 0,
    JUMBLE_MEDIUM = 1,
    JUMBLE_HARD   = 2
};

struct JumbleItem {
    String original;
    String scrambled;
    uint8_t circleIndices[4];
    uint8_t numCircles;
};

class JumbleGen {
public:
    JumbleGen();

    void generate(JumbleDifficulty difficulty = JUMBLE_MEDIUM);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    const char* getRiddle() const { return _riddle; }
    const char* getAnswer() const { return _answer; }
    uint8_t getNumWords() const { return _numWords; }
    const JumbleItem& getWord(uint8_t idx) const { return _words[idx]; }

private:
    static const uint8_t MAX_WORDS = 6;
    JumbleItem _words[MAX_WORDS];
    uint8_t _numWords;
    const char* _riddle;
    const char* _answer;
    JumbleDifficulty _difficulty;

    String scrambleWord(const char* word);
};

#endif // JUMBLE_GEN_H
