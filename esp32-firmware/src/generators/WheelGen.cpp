#include "WheelGen.h"
#include "WheelDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

WheelGen::WheelGen()
    : _center('E'),
      _wordCount(0),
      _good(0),
      _great(0),
      _genius(0),
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
    _wordCount = chosen.wordCount;
    _good = chosen.good;
    _great = chosen.great;
    _genius = chosen.genius;
}

void WheelGen::printToReceipt(EscPosPrinter& printer) {
    // Visual ASCII Honeycomb Layout (60mm / 48 columns)
    printer.println("             / \\     / \\");
    printer.println(String("            / ") + _outer[5] + " \\---/ " + _outer[0] + " \\");
    printer.println("            \\   /   \\   /");
    printer.println(String("           / \\ / [") + _center + "] \\ / \\");
    printer.println(String("          / ") + _outer[4] + " |     | " + _outer[1] + " \\");
    printer.println("          \\   / \\   / \\   /");
    printer.println(String("           \\ / ") + _outer[3] + " \\ / " + _outer[2] + " \\ /");
    printer.println("            \\   /---\\   /");
    printer.println("             \\ /     \\ /");
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

static void drawHexCell(ThermalCanvas& canvas, int16_t cx, int16_t cy, int16_t r, uint8_t thickness = 2) {
    int16_t h = (int16_t)((r * 866 + 500) / 1000);
    int16_t halfR = r / 2;
    int16_t px[6] = { (int16_t)(cx + r), (int16_t)(cx + halfR), (int16_t)(cx - halfR), (int16_t)(cx - r), (int16_t)(cx - halfR), (int16_t)(cx + halfR) };
    int16_t py[6] = { cy, (int16_t)(cy + h), (int16_t)(cy + h), cy, (int16_t)(cy - h), (int16_t)(cy - h) };
    canvas.drawPolygon(px, py, 6, thickness);
}

bool WheelGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t totalHeight = 368;
    ThermalCanvas canvas;
    if (!canvas.begin(totalHeight)) {
        return false;
    }

    const int16_t xc = 288;
    const int16_t yc = 135;
    const int16_t hexRadius = 46;

    // 6 outer honeycomb positions around (xc, yc)
    // Distance spacing ~ 80 dots
    const int16_t outerX[6] = { 288, 357, 357, 288, 219, 219 };
    const int16_t outerY[6] = {  55,  95, 175, 215, 175,  95 };

    // Draw outer 6 honeycomb cells
    for (int i = 0; i < 6; i++) {
        char ch = _outer[i] ? _outer[i] : ' ';
        drawHexCell(canvas, outerX[i], outerY[i], hexRadius, 2);
        canvas.drawChar(outerX[i] - 9, outerY[i] - 10, ch, 3);
    }

    // Draw center cell (double frame for emphasis)
    drawHexCell(canvas, xc, yc, hexRadius, 2);
    drawHexCell(canvas, xc, yc, hexRadius - 4, 2);
    canvas.drawChar(xc - 9, yc - 10, _center, 3);

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
