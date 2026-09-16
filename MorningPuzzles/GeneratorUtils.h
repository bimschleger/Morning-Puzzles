#ifndef GENERATOR_UTILS_H
#define GENERATOR_UTILS_H

#include <Arduino.h>
#include "EscPosPrinter.h"

template <typename T>
inline void mp_shuffle(T* arr, uint8_t n) {
    for (int i = (int)n - 1; i > 0; i--) {
        int j = random(i + 1);
        T tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
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
        printer.println(instr1);
    }
    if (instr2 && instr2[0] != '\0') {
        printer.println(instr2);
    }
    printer.println("");
    printer.setAlign(ALIGN_LEFT);
}

#endif // GENERATOR_UTILS_H
