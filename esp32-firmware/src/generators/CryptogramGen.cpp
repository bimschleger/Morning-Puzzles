#include "CryptogramGen.h"
#include "CryptogramDataset.h"
#include "GeneratorUtils.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

CryptogramGen::CryptogramGen() :
    _phrase(""),
    _author(""),
    _ciphertext(""),
    _clueStr(""),
    _clueCount(2),
    _difficulty(CRYPTO_MEDIUM) {
}

void CryptogramGen::generateDerangement(char* p2c, char* c2p) {
    char letters[26];
    char shuffled[26];
    for (uint8_t i = 0; i < 26; i++) {
        letters[i] = 'A' + i;
        shuffled[i] = 'A' + i;
    }

    // Try up to 100 times to generate a derangement (no letter maps to itself)
    bool success = false;
    for (uint8_t attempt = 0; attempt < 100; attempt++) {
        mp_shuffle(shuffled, 26);
        bool valid = true;
        for (uint8_t i = 0; i < 26; i++) {
            if (letters[i] == shuffled[i]) {
                valid = false;
                break;
            }
        }
        if (valid) {
            success = true;
            break;
        }
    }

    // Fallback: cyclic shift by 1 if loop exhausted
    if (!success) {
        for (uint8_t i = 0; i < 26; i++) {
            shuffled[i] = 'A' + ((i + 1) % 26);
        }
    }

    for (uint8_t i = 0; i < 26; i++) {
        p2c[i] = shuffled[i];
        c2p[shuffled[i] - 'A'] = letters[i];
    }
}

void CryptogramGen::selectClues(const char* p2c) {
    // 1. Identify distinct letters in phrase
    bool present[26] = { false };
    for (size_t i = 0; i < _phrase.length(); i++) {
        char ch = _phrase[i];
        if (ch >= 'A' && ch <= 'Z') {
            present[ch - 'A'] = true;
        }
    }

    // 2. Frequency table prioritization (common English letters)
    const char commonOrder[] = "ETAOINSHRDLCUMWFGYPBVKJXQZ";
    char sortedInPhrase[26];
    uint8_t numDistinct = 0;

    for (uint8_t i = 0; i < 26; i++) {
        char c = commonOrder[i];
        if (present[c - 'A']) {
            sortedInPhrase[numDistinct++] = c;
        }
    }

    uint8_t count = _clueCount;
    if (count > numDistinct) count = numDistinct;
    _clueCount = count;

    // Pick top candidates from common letters with slight randomization
    uint8_t poolSize = (count * 2 <= numDistinct) ? (count * 2) : numDistinct;
    char samplePool[26];
    for (uint8_t i = 0; i < poolSize; i++) {
        samplePool[i] = sortedInPhrase[i];
    }
    mp_shuffle(samplePool, poolSize);

    for (uint8_t i = 0; i < count; i++) {
        char pChar = samplePool[i];
        char cChar = p2c[pChar - 'A'];
        _clues[i].cipher = cChar;
        _clues[i].plain = pChar;
    }

    // 3. Sort clues alphabetically by cipher letter for clean presentation
    for (uint8_t i = 0; i < count; i++) {
        for (uint8_t j = i + 1; j < count; j++) {
            if (_clues[j].cipher < _clues[i].cipher) {
                CryptogramClue temp = _clues[i];
                _clues[i] = _clues[j];
                _clues[j] = temp;
            }
        }
    }

    // 4. Format clue string
    if (_clueCount == 1) {
        _clueStr = String("CLUE: ") + _clues[0].cipher + " = " + _clues[0].plain;
    } else {
        _clueStr = "CLUES: ";
        for (uint8_t i = 0; i < _clueCount; i++) {
            if (i > 0) _clueStr += ", ";
            _clueStr += String(_clues[i].cipher) + " = " + String(_clues[i].plain);
        }
    }
}

void CryptogramGen::generate(CryptogramDifficulty difficulty) {
    _difficulty = difficulty;
    size_t idx = random(NUM_CRYPTOGRAMS_PER_DIFF) % NUM_CRYPTOGRAMS_PER_DIFF;

    const CryptogramQuote* quotePtr = nullptr;
    if (difficulty == CRYPTO_EASY) {
        quotePtr = &EASY_CRYPTOGRAMS[idx];
        _clueCount = 3;
    } else if (difficulty == CRYPTO_HARD) {
        quotePtr = &HARD_CRYPTOGRAMS[idx];
        _clueCount = 1;
    } else {
        quotePtr = &MEDIUM_CRYPTOGRAMS[idx];
        _clueCount = 2;
    }

    generateWithQuote(quotePtr->phrase, quotePtr->author, difficulty, 0);
}

void CryptogramGen::generateWithQuote(const char* phrase, const char* author, CryptogramDifficulty difficulty, uint32_t seed) {
    _difficulty = difficulty;
    _phrase = String(phrase);
    _author = String(author);
    _clueCount = (difficulty == CRYPTO_EASY) ? 3 : ((difficulty == CRYPTO_HARD) ? 1 : 2);

    char p2c[26];
    char c2p[26];
    generateDerangement(p2c, c2p);

    // Encrypt phrase into ciphertext (preserving non-alpha)
    _ciphertext = "";
    for (size_t i = 0; i < _phrase.length(); i++) {
        char ch = _phrase[i];
        if (ch >= 'A' && ch <= 'Z') {
            _ciphertext += p2c[ch - 'A'];
        } else {
            _ciphertext += ch;
        }
    }

    selectClues(p2c);
}

void CryptogramGen::printToReceipt(EscPosPrinter& printer) {
    if (_clueStr.length() > 0) {
        printer.setAlign(ALIGN_CENTER);
        printer.println(_clueStr);
        printer.println("");
        printer.setAlign(ALIGN_LEFT);
    }

    // Word wrapping to <= 42 columns in spaced format
    // A word of length L in spaced representation takes 2*L - 1 chars.
    int lineLen = 0;
    String currentWords[12];
    uint8_t numWordsInLine = 0;

    int p = 0;
    int totalLen = _ciphertext.length();

    auto flushAsciiLine = [&]() {
        if (numWordsInLine == 0) return;
        String slotLine = "   ";
        String cipherLine = "   ";

        for (uint8_t w = 0; w < numWordsInLine; w++) {
            if (w > 0) {
                slotLine += "  ";
                cipherLine += "  ";
            }
            for (size_t c = 0; c < currentWords[w].length(); c++) {
                if (c > 0) {
                    slotLine += " ";
                    cipherLine += " ";
                }
                char ch = currentWords[w][c];
                if (ch >= 'A' && ch <= 'Z') {
                    slotLine += "_";
                } else {
                    slotLine += " ";
                }
                cipherLine += ch;
            }
        }

        printer.println(slotLine);
        printer.println(cipherLine);
        printer.println("");
        numWordsInLine = 0;
        lineLen = 0;
    };

    while (p < totalLen) {
        while (p < totalLen && _ciphertext[p] == ' ') p++;
        if (p >= totalLen) break;
        int start = p;
        while (p < totalLen && _ciphertext[p] != ' ') p++;
        String word = _ciphertext.substring(start, p);
        int wordSpacedLen = (int)word.length() * 2 - 1;
        int needed = wordSpacedLen + (numWordsInLine > 0 ? 2 : 0);

        if (numWordsInLine > 0 && lineLen + needed > 42) {
            flushAsciiLine();
        }
        if (numWordsInLine < 12) {
            currentWords[numWordsInLine++] = word;
            lineLen += needed;
        }
    }
    flushAsciiLine();

    if (_author.length() > 0) {
        printer.println(String("   -- ") + _author);
        printer.println("");
    }

    // Alphabet Tracker & Scratchpad
    printer.println("  - - - - - - - - - - - - - - - - - - - - - - - -");
    printer.println("  ALPHABET TRACKER:");
    printer.println("  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z");
    printer.println("  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _");
    printer.println("");
    printer.println("  SCRATCHPAD:");
    for (uint8_t i = 0; i < 4; i++) {
        printer.println("  ______________________________________________");
        printer.println("");
    }
}

bool CryptogramGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t padding = 24;
    const int16_t innerWidth = THERMAL_CANVAS_WIDTH - padding * 2; // 528

    // Word wrap ciphertext to lines of <= 24 characters
    String lines[8];
    uint8_t numLines = 0;
    String currentLine = "";

    int p = 0;
    int totalLen = _ciphertext.length();
    while (p < totalLen && numLines < 8) {
        while (p < totalLen && _ciphertext[p] == ' ') p++;
        if (p >= totalLen) break;
        int start = p;
        while (p < totalLen && _ciphertext[p] != ' ') p++;
        String word = _ciphertext.substring(start, p);

        if (currentLine.length() == 0) {
            currentLine = word;
        } else if (currentLine.length() + 1 + word.length() <= 24) {
            currentLine += " " + word;
        } else {
            lines[numLines++] = currentLine;
            currentLine = word;
        }
    }
    if (currentLine.length() > 0 && numLines < 8) {
        lines[numLines++] = currentLine;
    }

    const int16_t rowHeight = 76;
    const int16_t rowGap = 20;
    const int16_t headerGap = 16;
    const int16_t authorHeight = (_author.length() > 0) ? 36 : 0;
    const int16_t trackerHeight = 80;
    const int16_t scratchpadHeight = 140;

    int16_t totalH = headerGap + numLines * (rowHeight + rowGap) + authorHeight + trackerHeight + scratchpadHeight + 40;
    totalH = ((totalH + 7) / 8) * 8; // Align to 8 dots

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }
    canvas.clear(0);

    int16_t curY = 16;

    // 1. Ciphertext rows with handwriting slot underlines
    for (uint8_t l = 0; l < numLines; l++) {
        const String& lineStr = lines[l];
        int16_t lineLen = lineStr.length();
        int16_t charW = (lineLen > 0) ? (innerWidth / lineLen) : 24;
        if (charW > 24) charW = 24;

        int16_t startX = padding + (innerWidth - lineLen * charW) / 2;
        int16_t slotY = curY + 24;
        int16_t charY = curY + 34;

        for (int16_t i = 0; i < lineLen; i++) {
            char ch = lineStr[i];
            int16_t cx = startX + i * charW;
            if (ch >= 'A' && ch <= 'Z') {
                int16_t barW = charW - 6;
                if (barW < 1) barW = 1;
                canvas.drawHLine(cx + 3, slotY, barW, 2);
            }
            canvas.drawChar(cx + 4, charY, ch, 2, 1);
        }
        curY += rowHeight + rowGap;
    }

    // 2. Author line
    if (_author.length() > 0) {
        String authStr = String("-- ") + _author;
        canvas.drawText(padding + 12, curY, authStr.c_str(), 2, 1);
        curY += authorHeight;
    }

    // 3. Dashed divider
    for (int16_t dx = padding; dx < padding + innerWidth; dx += 8) {
        int16_t w = (dx + 4 <= padding + innerWidth) ? 4 : (padding + innerWidth - dx);
        canvas.drawHLine(dx, curY, w, 2);
    }
    curY += 18;

    // 4. Alphabet Tracker
    canvas.drawText(padding, curY, "ALPHABET TRACKER:", 2, 1);
    curY += 20;
    int16_t colW = innerWidth / 26; // 20 dots per letter
    for (uint8_t i = 0; i < 26; i++) {
        int16_t lx = padding + i * colW;
        canvas.drawChar(lx + 4, curY, 'A' + i, 2, 1);
        int16_t barW = colW - 4;
        if (barW < 1) barW = 1;
        canvas.drawHLine(lx + 2, curY + 18, barW, 2);
    }
    curY += 32;

    // 5. Scratchpad (4 handwriting dashed lines)
    canvas.drawText(padding, curY, "SCRATCHPAD:", 2, 1);
    curY += 22;
    for (uint8_t line = 0; line < 4; line++) {
        for (int16_t dx = padding; dx < padding + innerWidth; dx += 10) {
            int16_t w = (dx + 5 <= padding + innerWidth) ? 5 : (padding + innerWidth - dx);
            canvas.drawHLine(dx, curY, w, 1);
        }
        curY += 26;
    }

    return canvas.printTo(printer);
}
