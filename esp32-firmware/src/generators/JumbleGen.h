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

    const char* getRiddle() const { return _riddle; }

private:
    JumbleItem _words[4];
    const char* _riddle;
    const char* _answer;

    String scrambleWord(const char* word);
};

#endif // JUMBLE_GEN_H
