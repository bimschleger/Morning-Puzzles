#ifndef WHEEL_GEN_H
#define WHEEL_GEN_H

#include <Arduino.h>
class EscPosPrinter;

enum WheelDifficulty {
    WHEEL_EASY   = 0,
    WHEEL_MEDIUM = 1,
    WHEEL_HARD   = 2
};

class WheelGen {
public:
    WheelGen();

    void generate(WheelDifficulty difficulty = WHEEL_MEDIUM);
    void printToReceipt(EscPosPrinter& printer);

    char getCenterLetter() const { return _center; }
    const char* getOuterLetters() const { return _outer; }
    const char* getPangram() const { return _pangram; }
    uint8_t getWordCount() const { return _wordCount; }

private:
    char _center;
    char _outer[7];
    const char* _pangram;
    uint8_t _wordCount;
    uint8_t _good;
    uint8_t _great;
    uint8_t _genius;
    const char* _sampleWords[16];
    uint8_t _numSampleWords;
    WheelDifficulty _difficulty;
};

#endif // WHEEL_GEN_H
