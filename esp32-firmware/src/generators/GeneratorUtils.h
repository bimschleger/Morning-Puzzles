#ifndef GENERATOR_UTILS_H
#define GENERATOR_UTILS_H

#include <Arduino.h>
#include "../printer/EscPosPrinter.h"

template <typename T>
inline void mp_shuffle(T* arr, uint8_t n) {
    for (int i = (int)n - 1; i > 0; i--) {
        int j = random(i + 1);
        T tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

inline void printWrapped(EscPosPrinter& printer, const char* text, int maxWidth = 44) {
    if (!text || text[0] == '\0') return;

    char lineBuffer[128];
    int lineLen = 0;
    lineBuffer[0] = '\0';

    const char* p = text;
    while (*p != '\0') {
        // Skip leading whitespace
        while (*p == ' ') p++;
        if (*p == '\0') break;

        // Find word end
        const char* wordStart = p;
        while (*p != '\0' && *p != ' ') p++;
        int wordLen = (int)(p - wordStart);

        if (lineLen == 0) {
            // First word on the line
            if (wordLen < (int)sizeof(lineBuffer) - 1) {
                memcpy(lineBuffer, wordStart, wordLen);
                lineBuffer[wordLen] = '\0';
                lineLen = wordLen;
            } else {
                char tmp[128];
                int copyLen = (wordLen < (int)sizeof(tmp) - 1) ? wordLen : (int)sizeof(tmp) - 1;
                memcpy(tmp, wordStart, copyLen);
                tmp[copyLen] = '\0';
                printer.println(tmp);
            }
        } else if (lineLen + 1 + wordLen <= maxWidth && lineLen + 1 + wordLen < (int)sizeof(lineBuffer) - 1) {
            lineBuffer[lineLen++] = ' ';
            memcpy(lineBuffer + lineLen, wordStart, wordLen);
            lineLen += wordLen;
            lineBuffer[lineLen] = '\0';
        } else {
            // Flush current line
            printer.println(lineBuffer);
            // Start new line with current word
            if (wordLen < (int)sizeof(lineBuffer) - 1) {
                memcpy(lineBuffer, wordStart, wordLen);
                lineBuffer[wordLen] = '\0';
                lineLen = wordLen;
            } else {
                char tmp[128];
                int copyLen = (wordLen < (int)sizeof(tmp) - 1) ? wordLen : (int)sizeof(tmp) - 1;
                memcpy(tmp, wordStart, copyLen);
                tmp[copyLen] = '\0';
                printer.println(tmp);
                lineBuffer[0] = '\0';
                lineLen = 0;
            }
        }
    }

    if (lineLen > 0) {
        printer.println(lineBuffer);
    }
}

inline void printPuzzleHeader(EscPosPrinter& printer, const char* title, const char* diffStr, const char* instr1, const char* instr2 = nullptr) {
    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.print("--- ");
    printer.print(title);
    printer.println(" ---");
    printer.setBold(false);
    if (diffStr && diffStr[0] != '\0') {
        printer.print("DIFFICULTY: ");
        printer.println(diffStr);
    }
    if (instr1 && instr1[0] != '\0') {
        printWrapped(printer, instr1, 44);
    }
    if (instr2 && instr2[0] != '\0') {
        printWrapped(printer, instr2, 44);
    }
    printer.println("");
    printer.setAlign(ALIGN_LEFT);
}

#endif // GENERATOR_UTILS_H
