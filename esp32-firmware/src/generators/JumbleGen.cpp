#include "JumbleGen.h"
#include "JumbleDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"
#include <vector>

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
    const int16_t innerWidth = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t clueSize = 66;
    const int16_t wordGap = 12;
    uint8_t count = (_numWords > 4) ? 4 : _numWords;

    // Tokenize answer words
    const int16_t ansH = 66;
    const int16_t wordSpacing = 16;
    const int16_t lineGap = 12;

    std::vector<String> ansWords;
    String ansStr = _answer ? _answer : "";
    int16_t aStart = 0;
    for (int16_t i = 0; i <= (int16_t)ansStr.length(); i++) {
        if (i == (int16_t)ansStr.length() || ansStr[i] == ' ') {
            if (i > aStart) {
                ansWords.push_back(ansStr.substring(aStart, i));
            }
            aStart = i + 1;
        }
    }

    auto getWordBoxW = [&](const String& w) -> int16_t {
        int16_t numLetters = 0;
        int16_t punctW = 0;
        for (size_t c = 0; c < w.length(); c++) {
            char ch = w[c];
            if (ch >= 'A' && ch <= 'Z') numLetters++;
            else if (ch == '"' || ch == '\'') punctW += 12;
            else if (ch == '-') punctW += 14;
        }
        if (numLetters == 0) return 66;
        if (numLetters * 66 + punctW > innerWidth) {
            return (innerWidth - punctW) / numLetters;
        }
        return 66;
    };

    auto measureWordW = [&](const String& w) -> int16_t {
        int16_t boxW = getWordBoxW(w);
        int16_t wWidth = 0;
        for (size_t c = 0; c < w.length(); c++) {
            char ch = w[c];
            if (ch >= 'A' && ch <= 'Z') wWidth += boxW;
            else if (ch == '"' || ch == '\'') wWidth += 12;
            else if (ch == '-') wWidth += 14;
        }
        return wWidth;
    };

    std::vector<std::vector<String>> ansLines;
    std::vector<String> curLine;
    int16_t curLineW = 0;

    for (const auto& w : ansWords) {
        int16_t wW = measureWordW(w);
        int16_t needed = curLine.empty() ? wW : (wordSpacing + wW);
        if (curLineW + needed <= innerWidth && !curLine.empty()) {
            curLine.push_back(w);
            curLineW += needed;
        } else {
            if (!curLine.empty()) ansLines.push_back(curLine);
            curLine = {w};
            curLineW = wW;
        }
    }
    if (!curLine.empty()) ansLines.push_back(curLine);

    // Format riddle into wrapped lines (~28 chars)
    String riddleStr = String("\"") + _riddle + "\"";
    std::vector<String> riddleLines;
    int16_t rStart = 0;
    while (rStart < (int16_t)riddleStr.length()) {
        int16_t rEnd = rStart + 28;
        if (rEnd >= (int16_t)riddleStr.length()) {
            rEnd = riddleStr.length();
        } else {
            int16_t lastSpace = -1;
            for (int16_t s = rEnd; s > rStart; s--) {
                if (riddleStr[s] == ' ') {
                    lastSpace = s;
                    break;
                }
            }
            if (lastSpace != -1) rEnd = lastSpace;
        }
        String line = riddleStr.substring(rStart, rEnd);
        line.trim();
        riddleLines.push_back(line);
        rStart = (rEnd < (int16_t)riddleStr.length() && riddleStr[rEnd] == ' ') ? rEnd + 1 : rEnd;
    }

    int16_t totalH = (
        12
        + count * (132 + wordGap)
        + 16
        + 20 + riddleLines.size() * 28 + 6
        + 20 + 192
        + 22 + ansLines.size() * (ansH + lineGap) + 4
    );
    totalH = ((totalH + 7) / 8) * 8;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    int16_t curY = 12;

    // 1. Scrambled words and answer boxes (connected 2-row grid, left-aligned)
    for (uint8_t i = 0; i < count; i++) {
        const JumbleItem& item = _words[i];
        int16_t len = item.scrambled.length();
        if (len <= 0) continue;
        int16_t blockW = len * clueSize;

        // Outer frame and middle horizontal divider
        canvas.drawRect(padding, curY, blockW, 132, 2);
        canvas.drawHLine(padding, curY + 66, blockW, 2);

        // Vertical dividers between columns
        for (int16_t c = 1; c < len; c++) {
            canvas.drawVLine(padding + c * clueSize, curY, 132, 1);
        }

        // Scrambled letters and circles
        for (int16_t c = 0; c < len; c++) {
            int16_t cx0 = padding + c * clueSize;
            int16_t charX = cx0 + (clueSize - 18) / 2;
            int16_t charY = curY + (clueSize - 21) / 2;
            canvas.drawChar(charX, charY, item.scrambled[c], 3);

            bool isCircled = false;
            for (uint8_t k = 0; k < item.numCircles; k++) {
                if (item.circleIndices[k] == c) {
                    isCircled = true;
                    break;
                }
            }
            if (isCircled) {
                canvas.drawCircle(cx0 + 33, curY + 66 + 33, 26, 2);
            }
        }

        curY += 132 + wordGap;
    }

    // 2. Dashed tear divider
    canvas.drawDashedHLine(padding, curY + 2, innerWidth, 6, 6, 2);
    curY += 16;

    // 3. Riddle Question (scale=3 for quote text)
    canvas.drawText(padding, curY, "RIDDLE QUESTION:", 2);
    curY += 20;
    for (const auto& rLine : riddleLines) {
        canvas.drawText(padding + 4, curY, rLine.c_str(), 3);
        curY += 28;
    }
    curY += 6;

    // 4. Scratchpad (192-dot blank writing area without dashed lines)
    canvas.drawText(padding, curY, "SCRATCHPAD:", 2);
    curY += 20 + 192;

    // 5. Answer layout with unified word frames and thin 1px inner dividers
    canvas.drawText(padding, curY, "ANSWER:", 2);
    curY += 22;

    for (const auto& lineWords : ansLines) {
        int16_t lineTotalW = 0;
        for (size_t i = 0; i < lineWords.size(); i++) {
            lineTotalW += measureWordW(lineWords[i]);
            if (i > 0) lineTotalW += wordSpacing;
        }
        int16_t startX = padding + (innerWidth - lineTotalW) / 2;
        int16_t ax = startX;

        for (const auto& w : lineWords) {
            int16_t boxW = getWordBoxW(w);
            size_t c = 0;
            while (c < w.length()) {
                char ch = w[c];
                if (ch >= 'A' && ch <= 'Z') {
                    size_t start = c;
                    while (c < w.length() && w[c] >= 'A' && w[c] <= 'Z') {
                        c++;
                    }
                    int16_t k = c - start;
                    int16_t segW = k * boxW;
                    canvas.drawRect(ax, curY, segW, ansH, 2);
                    for (int16_t i = 1; i < k; i++) {
                        canvas.drawVLine(ax + i * boxW, curY, ansH, 1);
                    }
                    ax += segW;
                } else if (ch == '"' || ch == '\'') {
                    canvas.drawChar(ax + 2, curY + (ansH - 14) / 2, ch, 2);
                    ax += 12;
                    c++;
                } else if (ch == '-') {
                    canvas.drawChar(ax + 3, curY + (ansH - 14) / 2, '-', 2);
                    ax += 14;
                    c++;
                } else {
                    c++;
                }
            }
            ax += wordSpacing;
        }
        curY += ansH + lineGap;
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

