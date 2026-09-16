#include "LadderGen.h"
#include "LadderDataset.h"
#include "GeneratorUtils.h"
#include "EscPosPrinter.h"
#include "ThermalCanvas.h"

LadderGen::LadderGen() : _wordLen(4), _totalWords(5), _difficulty(LADDER_MEDIUM) {
    memset(_words, 0, sizeof(_words));
}

void LadderGen::generate(LadderDifficulty difficulty) {
    _difficulty = difficulty;
    const LadderDef* pool = nullptr;

    if (difficulty == LADDER_EASY) {
        pool = EASY_LADDERS;
    } else if (difficulty == LADDER_HARD) {
        pool = HARD_LADDERS;
    } else {
        pool = MEDIUM_LADDERS;
    }

    size_t chosenIdx = random(NUM_LADDER_PUZZLES_PER_DIFF) % NUM_LADDER_PUZZLES_PER_DIFF;
    const LadderDef& chosen = pool[chosenIdx];

    _wordLen = chosen.wordLen;
    _totalWords = chosen.totalWords;
    if (_totalWords > MAX_RUNGS) _totalWords = MAX_RUNGS;

    // Parse space-separated words
    const char* p = chosen.words;
    for (uint8_t i = 0; i < _totalWords; i++) {
        while (*p == ' ') p++;
        const char* start = p;
        while (*p != ' ' && *p != '\0') p++;
        int wLen = p - start;
        if (wLen >= MAX_WORD_LEN) wLen = MAX_WORD_LEN - 1;
        memcpy(_words[i], start, wLen);
        _words[i][wLen] = '\0';
    }
}

void LadderGen::printToReceipt(EscPosPrinter& printer) {
    // Monospaced ASCII layout
    // Format: centered box "+---+---+---+"
    // 1. | C | O | L | D |
    // ...
    // N. | W | A | R | M |
    const uint8_t COLS = 48;
    char boxSep[32];
    boxSep[0] = '\0';
    for (uint8_t c = 0; c < _wordLen; c++) {
        strcat(boxSep, "+---");
    }
    strcat(boxSep, "+");

    int boxLen = strlen(boxSep);
    int padLen = (COLS - (3 + boxLen)) / 2;
    if (padLen < 0) padLen = 0;
    char indent[32];
    memset(indent, ' ', padLen);
    indent[padLen] = '\0';

    for (uint8_t r = 0; r < _totalWords; r++) {
        char lineBuf[64];
        char cellsBuf[48];
        cellsBuf[0] = '\0';

        if (r == 0 || r == _totalWords - 1) {
            for (uint8_t c = 0; c < _wordLen; c++) {
                char cell[8];
                snprintf(cell, sizeof(cell), "| %c ", _words[r][c]);
                strcat(cellsBuf, cell);
            }
            strcat(cellsBuf, "|");
        } else {
            for (uint8_t c = 0; c < _wordLen; c++) {
                strcat(cellsBuf, "|   ");
            }
            strcat(cellsBuf, "|");
        }

        printer.print(indent);
        printer.print("   ");
        printer.println(boxSep);

        snprintf(lineBuf, sizeof(lineBuf), "%s%2d. %s", indent, r + 1, cellsBuf);
        printer.println(lineBuf);
    }

    printer.print(indent);
    printer.print("   ");
    printer.println(boxSep);
}

bool LadderGen::printRasterToReceipt(EscPosPrinter& printer) {
    const uint16_t targetWidth = 576;
    const uint16_t tileSize = 66;
    const uint16_t gapY = 14;
    const uint16_t boxWidth = _wordLen * tileSize;
    const uint16_t numWidth = 36;
    const uint16_t gapX = 14;
    const uint16_t totalContentW = numWidth + gapX + boxWidth;
    const uint16_t startX = (targetWidth - totalContentW) / 2;
    const uint16_t boxX = startX + numWidth + gapX;

    const uint16_t marginTop = 24;
    uint16_t ladderHeight = _totalWords * tileSize + (_totalWords - 1) * gapY;
    uint16_t totalHeight = marginTop + ladderHeight + marginTop;
    totalHeight = (totalHeight + 7) & ~7;

    ThermalCanvas canvas;
    if (!canvas.begin(totalHeight)) {
        return false;
    }
    canvas.clear(0);

    for (uint8_t r = 0; r < _totalWords; r++) {
        uint16_t ry = marginTop + r * (tileSize + gapY);

        // Step number on left (scale=2, right-aligned)
        char numText[8];
        snprintf(numText, sizeof(numText), "%d.", r + 1);
        int textW = strlen(numText) * 12;
        int textX = boxX - gapX - textW;
        int textY = ry + (tileSize - 14) / 2;
        canvas.drawText(textX, textY, numText, 2);

        // 2px outer rectangle for word box
        canvas.drawRect(boxX, ry, boxWidth, tileSize, 2);

        // 1px internal vertical cell dividers
        for (uint8_t c = 1; c < _wordLen; c++) {
            uint16_t divX = boxX + c * tileSize;
            canvas.drawVLine(divX, ry, tileSize, 1);
        }

        // Start and target word glyphs (scale=3)
        if (r == 0 || r == _totalWords - 1) {
            const char* word = _words[r];
            for (uint8_t c = 0; c < _wordLen; c++) {
                uint16_t charX = boxX + c * tileSize + (tileSize - 15) / 2;
                uint16_t charY = ry + (tileSize - 21) / 2;
                canvas.drawChar(charX, charY, word[c], 3);
            }
        }
    }

    return canvas.printTo(printer);
}
