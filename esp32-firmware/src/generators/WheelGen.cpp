#include "WheelGen.h"
#include "WheelDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

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
    printer.setAlign(ALIGN_CENTER);
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
    printer.setAlign(ALIGN_LEFT);

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

bool WheelGen::printRasterToReceipt(EscPosPrinter& printer) {
    printer.setAlign(ALIGN_CENTER);
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
    printer.setAlign(ALIGN_LEFT);

    const int16_t totalHeight = 368;
    ThermalCanvas canvas;
    if (!canvas.begin(totalHeight)) {
        return false;
    }

    const int16_t xc = 288;
    const int16_t yc = 135;
    const int16_t cellRadius = 26;

    // 6 outer honeycomb positions around (xc, yc)
    // Distance spacing ~ 80 dots
    const int16_t outerX[6] = { 288, 357, 357, 288, 219, 219 };
    const int16_t outerY[6] = {  55,  95, 175, 215, 175,  95 };

    // Draw outer 6 honeycomb cells
    for (int i = 0; i < 6; i++) {
        char ch = _outer[i] ? _outer[i] : ' ';
        canvas.drawCircle(outerX[i], outerY[i], cellRadius, 2);
        canvas.drawChar(outerX[i] - 7, outerY[i] - 10, ch, 3);
    }

    // Draw center cell (double ring for emphasis)
    canvas.drawCircle(xc, yc, cellRadius + 4, 2);
    canvas.drawCircle(xc, yc, cellRadius, 1);
    canvas.drawChar(xc - 7, yc - 10, _center, 3);

    // Target Benchmarks box
    const int16_t boxW = 420;
    const int16_t boxH = 34;
    const int16_t boxX = (THERMAL_CANVAS_WIDTH - boxW) / 2;
    const int16_t boxY = 260;
    canvas.drawRect(boxX, boxY, boxW, boxH, 2);

    String benchText = "GOOD: " + String(_good) + "   GREAT: " + String(_great) + "   GENIUS: " + String(_genius) + "+";
    canvas.drawCenteredText(boxY + 8, benchText.c_str(), 2);

    // Ruled handwriting lines
    canvas.drawHLine(48, 315, 220, 1);
    canvas.drawHLine(308, 315, 220, 1);
    canvas.drawHLine(48, 345, 220, 1);
    canvas.drawHLine(308, 345, 220, 1);

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

