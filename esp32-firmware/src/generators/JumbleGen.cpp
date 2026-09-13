#include "JumbleGen.h"
#include "JumbleDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

JumbleGen::JumbleGen() : _numWords(0), _riddle(""), _answer(""), _difficulty(JUMBLE_MEDIUM) {}

String JumbleGen::scrambleWord(const char* word) {
    int len = strlen(word);
    char buf[16];
    strncpy(buf, word, sizeof(buf));
    buf[sizeof(buf) - 1] = '\0';

    for (int attempts = 0; attempts < 20; attempts++) {
        for (int i = len - 1; i > 0; i--) {
            int j = random(i + 1);
            char tmp = buf[i];
            buf[i] = buf[j];
            buf[j] = tmp;
        }
        if (strcmp(buf, word) != 0) {
            return String(buf);
        }
    }
    return String(buf);
}

void JumbleGen::generate(JumbleDifficulty difficulty) {
    _difficulty = difficulty;
    size_t startIdx = 0;
    size_t count = 100;
    if (difficulty == JUMBLE_MEDIUM) {
        startIdx = 100;
    } else if (difficulty == JUMBLE_HARD) {
        startIdx = 200;
    }

    size_t chosenIdx = startIdx + (random(count) % count);
    if (chosenIdx >= TOTAL_JUMBLE_PUZZLES) {
        chosenIdx = 0;
    }

    const CompactRiddleSet& chosen = JUMBLE_DATASET[chosenIdx];

    _numWords = chosen.numWords;
    if (_numWords > MAX_WORDS) _numWords = MAX_WORDS;
    _riddle = chosen.riddle;
    _answer = chosen.answer;

    for (uint8_t i = 0; i < _numWords; i++) {
        _words[i].original = chosen.words[i];
        _words[i].scrambled = scrambleWord(chosen.words[i]);
        _words[i].numCircles = chosen.numCircles[i];
        for (uint8_t c = 0; c < chosen.numCircles[i] && c < 4; c++) {
            _words[i].circleIndices[c] = chosen.circles[i][c];
        }
    }
}

void JumbleGen::printToReceipt(EscPosPrinter& printer) {
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- JUMBLE ---");
    printer.setBold(false);
    if (_difficulty == JUMBLE_EASY) {
        printer.println("DIFFICULTY: EASY");
    } else if (_difficulty == JUMBLE_HARD) {
        printer.println("DIFFICULTY: HARD");
    } else {
        printer.println("DIFFICULTY: MEDIUM");
    }
    printer.println("Unscramble each word, then use the circled");
    printer.println("letters to solve the riddle.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    for (uint8_t i = 0; i < _numWords; i++) {
        const JumbleItem& item = _words[i];
        String left = "  " + item.scrambled;
        while (left.length() < 12) left += " ";

        // Build letter slots representation with circles ( ) and squares [ ]
        String slots = "";
        for (size_t charIdx = 0; charIdx < item.original.length(); charIdx++) {
            bool isCircled = false;
            for (uint8_t c = 0; c < item.numCircles; c++) {
                if (item.circleIndices[c] == charIdx) {
                    isCircled = true;
                    break;
                }
            }
            if (isCircled) {
                slots += "( ) ";
            } else {
                slots += "[ ] ";
            }
        }
        printer.printKeyValue(left, slots + "   ___________", 46);
    }

    printer.println("");
    printer.println("Arrange the circled letters to answer this riddle:");
    printer.println(String("Q: \"") + _riddle + "\"");
    printer.println("A: _________________________________________");
    printer.println("");
}

bool JumbleGen::printRasterToReceipt(EscPosPrinter& printer) {
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- JUMBLE ---");
    printer.setBold(false);
    if (_difficulty == JUMBLE_EASY) {
        printer.println("DIFFICULTY: EASY");
    } else if (_difficulty == JUMBLE_HARD) {
        printer.println("DIFFICULTY: HARD");
    } else {
        printer.println("DIFFICULTY: MEDIUM");
    }
    printer.println("Unscramble each word, then use the circled");
    printer.println("letters to solve the riddle.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t padding = 24;
    const int16_t rowH = 48;
    const int16_t totalH = padding + _numWords * rowH + padding;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    for (uint8_t i = 0; i < _numWords; i++) {
        const JumbleItem& item = _words[i];
        int16_t y = padding + i * rowH;

        // Scrambled word text on left
        canvas.drawText(padding, y + 10, item.scrambled.c_str(), 3);

        // Letter boxes / circles in middle
        int16_t slotStartX = padding + 180;
        int16_t boxSize = 28;
        for (size_t charIdx = 0; charIdx < item.original.length(); charIdx++) {
            int16_t bx = slotStartX + charIdx * (boxSize + 8);
            bool isCircled = false;
            for (uint8_t c = 0; c < item.numCircles; c++) {
                if (item.circleIndices[c] == charIdx) {
                    isCircled = true;
                    break;
                }
            }
            if (isCircled) {
                canvas.drawCircle(bx + boxSize / 2, y + 8 + boxSize / 2, boxSize / 2, 2);
            } else {
                canvas.drawRect(bx, y + 8, boxSize, boxSize, 2);
            }
        }

        // Handwriting underline line on right
        int16_t lineStartX = slotStartX + item.original.length() * (boxSize + 8) + 16;
        if (lineStartX < THERMAL_CANVAS_WIDTH - padding) {
            canvas.drawHLine(lineStartX, y + 36, THERMAL_CANVAS_WIDTH - padding - lineStartX, 2);
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();

    if (ok) {
        printer.println("");
        printer.println("Arrange the circled letters to answer this riddle:");
        printer.println(String("Q: \"") + _riddle + "\"");
        printer.println("A: _________________________________________");
        printer.println("");
    }

    return ok;
}

