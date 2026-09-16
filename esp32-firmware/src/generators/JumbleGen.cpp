#include "JumbleGen.h"
#include "JumbleDataset.h"
#include "GeneratorUtils.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

JumbleGen::JumbleGen() : _numWords(0), _riddle(""), _answer(""), _difficulty(JUMBLE_MEDIUM) {}

String JumbleGen::scrambleWord(const char* word) {
    int len = strlen(word);
    char buf[16];
    strncpy(buf, word, sizeof(buf));
    buf[sizeof(buf) - 1] = '\0';

    for (int attempts = 0; attempts < 20; attempts++) {
        mp_shuffle(buf, len);
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

    // Parse space-delimited words and unpack bitmask circles
    const char* p = chosen.words;
    for (uint8_t i = 0; i < _numWords; i++) {
        while (*p == ' ') p++;
        const char* start = p;
        while (*p != ' ' && *p != '\0') p++;
        int wLen = p - start;
        char wBuf[16];
        if (wLen >= (int)sizeof(wBuf)) wLen = sizeof(wBuf) - 1;
        memcpy(wBuf, start, wLen);
        wBuf[wLen] = '\0';

        _words[i].original = String(wBuf);
        _words[i].scrambled = scrambleWord(wBuf);

        uint8_t mask = chosen.circleMasks[i];
        _words[i].numCircles = 0;
        for (uint8_t bit = 0; bit < 8; bit++) {
            if (mask & (1 << bit)) {
                if (_words[i].numCircles < 4) {
                    _words[i].circleIndices[_words[i].numCircles++] = bit;
                }
            }
        }
    }
}

void JumbleGen::printToReceipt(EscPosPrinter& printer) {
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
    printer.println("Riddle:");
    printer.println(String("  \"") + _riddle + "\"");
    printer.println("");
    printer.println("Answer:");

    // Print blank slots matching answer format (preserving punctuation)
    String ansLine = "  ";
    for (size_t i = 0; i < strlen(_answer); i++) {
        char ch = _answer[i];
        if (ch == ' ') {
            ansLine += "   ";
        } else if (ch == '"' || ch == '\'' || ch == '-' || ch == '?' || ch == '!') {
            ansLine += ch;
            ansLine += ' ';
        } else {
            ansLine += "_ ";
        }
    }
    printer.println(ansLine);
    printer.println("");
}

struct JumbleLineSpan {
    uint8_t startIdx;
    uint8_t count;
};

bool JumbleGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t padding = 24;
    const int16_t innerWidth = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t clueSize = 66;
    const int16_t wordGap = 12;
    uint8_t count = (_numWords > 4) ? 4 : _numWords;

    // Tokenize answer words
    const int16_t ansH = 66;
    const int16_t wordSpacing = 16;
    const int16_t lineGap = 12;

    String ansWords[8];
    uint8_t numAnsWords = 0;
    String ansStr = _answer ? _answer : "";
    int16_t aStart = 0;
    for (int16_t i = 0; i <= (int16_t)ansStr.length(); i++) {
        if (i == (int16_t)ansStr.length() || ansStr[i] == ' ') {
            if (i > aStart && numAnsWords < 8) {
                ansWords[numAnsWords++] = ansStr.substring(aStart, i);
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

    JumbleLineSpan ansLines[4];
    uint8_t numAnsLines = 0;
    uint8_t curLineStart = 0;
    uint8_t curLineCount = 0;
    int16_t curLineW = 0;

    for (uint8_t i = 0; i < numAnsWords; i++) {
        int16_t wW = measureWordW(ansWords[i]);
        int16_t needed = (curLineCount == 0) ? wW : (wordSpacing + wW);
        if (curLineW + needed <= innerWidth && curLineCount > 0) {
            curLineCount++;
            curLineW += needed;
        } else {
            if (curLineCount > 0 && numAnsLines < 4) {
                ansLines[numAnsLines++] = {curLineStart, curLineCount};
            }
            curLineStart = i;
            curLineCount = 1;
            curLineW = wW;
        }
    }
    if (curLineCount > 0 && numAnsLines < 4) {
        ansLines[numAnsLines++] = {curLineStart, curLineCount};
    }

    // Format riddle into wrapped lines (~28 chars)
    String riddleStr = String("\"") + _riddle + "\"";
    String riddleLines[8];
    uint8_t numRiddleLines = 0;
    int16_t rStart = 0;
    while (rStart < (int16_t)riddleStr.length() && numRiddleLines < 8) {
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
        riddleLines[numRiddleLines++] = line;
        rStart = (rEnd < (int16_t)riddleStr.length() && riddleStr[rEnd] == ' ') ? rEnd + 1 : rEnd;
    }

    int16_t totalH = (
        12
        + count * (132 + wordGap)
        + 16
        + 20 + numRiddleLines * 28 + 6
        + 20 + 192
        + 22 + numAnsLines * (ansH + lineGap) + 4
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

        // Draw scrambled letters (top row) and circles for marked indices (bottom row)
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
    for (uint8_t r = 0; r < numRiddleLines; r++) {
        canvas.drawText(padding + 4, curY, riddleLines[r].c_str(), 3);
        curY += 28;
    }
    curY += 6;

    // 4. Scratchpad (192-dot blank writing area without dashed lines)
    canvas.drawText(padding, curY, "SCRATCHPAD:", 2);
    curY += 20 + 192;

    // 5. Answer layout with unified word frames and thin 1px inner dividers
    canvas.drawText(padding, curY, "ANSWER:", 2);
    curY += 22;

    for (uint8_t l = 0; l < numAnsLines; l++) {
        const JumbleLineSpan& span = ansLines[l];
        int16_t lineTotalW = 0;
        for (uint8_t i = 0; i < span.count; i++) {
            lineTotalW += measureWordW(ansWords[span.startIdx + i]);
            if (i > 0) lineTotalW += wordSpacing;
        }
        int16_t startX = padding + (innerWidth - lineTotalW) / 2;
        int16_t ax = startX;

        for (uint8_t i = 0; i < span.count; i++) {
            const String& w = ansWords[span.startIdx + i];
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
                    for (int16_t seg = 1; seg < k; seg++) {
                        canvas.drawVLine(ax + seg * boxW, curY, ansH, 1);
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
