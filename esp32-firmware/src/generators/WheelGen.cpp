#include "WheelGen.h"
#include "WheelDataset.h"
#include "../printer/EscPosPrinter.h"

WheelGen::WheelGen()
    : _center('E'),
      _pangram(""),
      _wordCount(0),
      _good(0),
      _great(0),
      _genius(0),
      _numSampleWords(0),
      _difficulty(WHEEL_MEDIUM)
{
    _outer[0] = '\0';
}

void WheelGen::generate(WheelDifficulty difficulty) {
    _difficulty = difficulty;
    size_t chosenIdx = random(NUM_WHEEL_PUZZLES_PER_DIFF) % NUM_WHEEL_PUZZLES_PER_DIFF;

    const WheelPuzzleDef* dataset = MEDIUM_WHEEL_PUZZLES;
    if (difficulty == WHEEL_EASY) {
        dataset = EASY_WHEEL_PUZZLES;
    } else if (difficulty == WHEEL_HARD) {
        dataset = HARD_WHEEL_PUZZLES;
    }

    WheelPuzzleDef chosen;
    memcpy_P(&chosen, &dataset[chosenIdx], sizeof(WheelPuzzleDef));

    _center = chosen.center;
    strncpy(_outer, chosen.outer, sizeof(_outer));
    _outer[sizeof(_outer) - 1] = '\0';
    _pangram = chosen.pangram;
    _wordCount = chosen.wordCount;
    _good = chosen.good;
    _great = chosen.great;
    _genius = chosen.genius;
    _numSampleWords = chosen.numSampleWords;
    for (uint8_t i = 0; i < _numSampleWords && i < 16; i++) {
        _sampleWords[i] = chosen.sampleWords[i];
    }
}

void WheelGen::printToReceipt(EscPosPrinter& printer) {
    printer.setBold(true);
    printer.println("--- WHEEL ---");
    printer.setBold(false);

    if (_difficulty == WHEEL_EASY) {
        printer.println("DIFFICULTY: EASY");
    } else if (_difficulty == WHEEL_HARD) {
        printer.println("DIFFICULTY: HARD");
    } else {
        printer.println("DIFFICULTY: MEDIUM");
    }

    String instr = "Find " + String(_wordCount) + "+ words using center letter " + String(_center) + " and outer letters, including a 7-letter pangram.";
    printer.println(instr);
    printer.println("");

    char o0 = _outer[0] ? _outer[0] : ' ';
    char o1 = _outer[1] ? _outer[1] : ' ';
    char o2 = _outer[2] ? _outer[2] : ' ';
    char o3 = _outer[3] ? _outer[3] : ' ';
    char o4 = _outer[4] ? _outer[4] : ' ';
    char o5 = _outer[5] ? _outer[5] : ' ';

    printer.println("                  +---+---+");
    printer.println(String("                  | ") + o0 + " | " + o1 + " |");
    printer.println("              +---+===+===+---+");
    printer.println(String("              | ") + o2 + " | [" + _center + "] | " + o3 + " |");
    printer.println("              +---+===+===+---+");
    printer.println(String("                  | ") + o4 + " | " + o5 + " |");
    printer.println("                  +---+---+");
    printer.println("");

    printer.println("   TARGET BENCHMARKS:");
    printer.println(String("     Good: ") + _good + " words  |  Great: " + _great + " words  |  Genius: " + _genius + "+ words");
    printer.println("");
    printer.println(String("   WORDS FOUND (Must include central letter ") + _center + "):");
    printer.println("   _________________        _________________");
    printer.println("   _________________        _________________");
    printer.println("   _________________        _________________");
    printer.println("   _________________        _________________");
    printer.println("");
}
