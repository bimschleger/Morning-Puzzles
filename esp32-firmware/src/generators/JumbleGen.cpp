#include "JumbleGen.h"
#include "JumbleDataset.h"
#include "../printer/EscPosPrinter.h"

JumbleGen::JumbleGen() : _numWords(0), _riddle(""), _answer("") {}

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
    printer.setBold(true);
    printer.println("--- JUMBLE ---");
    printer.setBold(false);
    printer.println("DIFFICULTY: MEDIUM");
    printer.println("Unscramble each word, then use the circled");
    printer.println("letters to solve the riddle.");
    printer.println("");

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
