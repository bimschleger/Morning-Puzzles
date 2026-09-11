#include "JumbleGen.h"
#include "../printer/EscPosPrinter.h"

struct RiddleSet {
    JumbleDifficulty diff;
    const char* words[4];
    uint8_t circles[4][4];
    uint8_t numCircles[4];
    const char* riddle;
    const char* answer;
};

static const RiddleSet RIDDLES[] = {
    {
        JUMBLE_EASY,
        {"ROAST", "PLANT", "LIGHT", "CROWN"},
        {{0, 2}, {1}, {0, 4}, {2}},
        {2, 1, 2, 1},
        "Why did the coffee file a police report?",
        "IT GOT MUGGED"
    },
    {
        JUMBLE_MEDIUM,
        {"GLANCE", "SPHERE", "BREEZE", "SUMMIT"},
        {{1, 3}, {0, 4}, {2, 5}, {1}},
        {2, 2, 2, 1},
        "What do you call a sleeping dinosaur?",
        "A DINO SNORE"
    },
    {
        JUMBLE_HARD,
        {"JOURNEY", "WHISPER", "LANTERN", "THUNDER"},
        {{0, 4}, {2, 5}, {1, 3}, {0, 3}},
        {2, 2, 2, 2},
        "Why couldn't the bicycle stand up by itself?",
        "IT WAS TWO TIRED"
    },
    {
        JUMBLE_EASY,
        {"BREAD", "SPOON", "CLOCK", "TABLE"},
        {{0, 1}, {2}, {0, 4}, {1, 3}},
        {2, 1, 2, 2},
        "What did the ocean say to the sailboat?",
        "NOTHING IT JUST WAVED"
    },
    {
        JUMBLE_MEDIUM,
        {"SHADOW", "FLAVOR", "CASTLE", "GUITAR"},
        {{0, 3}, {1, 4}, {0, 2}, {1, 5}},
        {2, 2, 2, 2},
        "Why did the scarecrow win an award?",
        "OUTSTANDING IN HIS FIELD"
    },
    {
        JUMBLE_EASY,
        {"STAGE", "ACTOR", "SCENE", "VOICE"},
        {{0, 2}, {1, 3}, {0, 4}, {2}},
        {2, 2, 2, 1},
        "Why do we tell actors to 'break a leg'?",
        "EVERY PLAY HAS A CAST"
    }
};

static const size_t NUM_RIDDLES = sizeof(RIDDLES) / sizeof(RIDDLES[0]);

JumbleGen::JumbleGen() : _riddle(""), _answer("") {}

String JumbleGen::scrambleWord(const char* word) {
    int len = strlen(word);
    char buf[16];
    strncpy(buf, word, sizeof(buf));
    buf[len] = '\0';

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
    // Filter candidates by difficulty
    std::vector<size_t> candidates;
    for (size_t i = 0; i < NUM_RIDDLES; i++) {
        if (RIDDLES[i].diff == difficulty) {
            candidates.push_back(i);
        }
    }
    if (candidates.empty()) {
        for (size_t i = 0; i < NUM_RIDDLES; i++) candidates.push_back(i);
    }

    size_t chosenIdx = candidates[random(candidates.size())];
    const RiddleSet& chosen = RIDDLES[chosenIdx];

    _riddle = chosen.riddle;
    _answer = chosen.answer;

    for (int i = 0; i < 4; i++) {
        _words[i].original = chosen.words[i];
        _words[i].scrambled = scrambleWord(chosen.words[i]);
        _words[i].numCircles = chosen.numCircles[i];
        for (int c = 0; c < chosen.numCircles[i]; c++) {
            _words[i].circleIndices[c] = chosen.circles[i][c];
        }
    }
}

void JumbleGen::printToReceipt(EscPosPrinter& printer) {
    printer.setBold(true);
    printer.println("--- DAILY JUMBLE ---");
    printer.setBold(false);
    printer.println("Unscramble the letters, one letter to each square:");
    printer.println("Circled letters ( ) form the answer to the riddle!");
    printer.println("");

    for (int i = 0; i < 4; i++) {
        const JumbleItem& item = _words[i];
        String left = "  " + item.scrambled;
        while (left.length() < 12) left += " ";

        // Build letter slots representation with circles (X) and squares [X]
        String slots = "";
        for (size_t charIdx = 0; charIdx < item.scrambled.length(); charIdx++) {
            bool isCircled = false;
            for (uint8_t c = 0; c < item.numCircles; c++) {
                if (item.circleIndices[c] == charIdx) {
                    isCircled = true;
                    break;
                }
            }
            if (isCircled) {
                slots += "(" + String(item.scrambled[charIdx]) + ") ";
            } else {
                slots += "[" + String(item.scrambled[charIdx]) + "] ";
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
