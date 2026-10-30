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
    bool printRasterToReceipt(EscPosPrinter& printer);

    char getCenterLetter() const { return _center; }
    const char* getOuterLetters() const { return _outer; }
    uint8_t getWordCount() const { return _wordCount; }
    uint8_t getGood() const { return _good; }
    uint8_t getGreat() const { return _great; }
    uint8_t getGenius() const { return _genius; }
    uint8_t getCount4() const { return _count4; }
    uint8_t getCount5() const { return _count5; }
    uint8_t getCount6() const { return _count6; }
    uint8_t getCount7Plus() const { return _count7plus; }

private:
    char _center;
    char _outer[7];
    uint8_t _wordCount;
    uint8_t _good;
    uint8_t _great;
    uint8_t _genius;
    uint8_t _count4;
    uint8_t _count5;
    uint8_t _count6;
    uint8_t _count7plus;
    WheelDifficulty _difficulty;
};

#endif // WHEEL_GEN_H
