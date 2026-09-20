#ifndef WHEEL_DATASET_H
#define WHEEL_DATASET_H

#include <Arduino.h>

struct WheelPuzzleDef {
    char center;
    char outer[7];
    uint8_t wordCount;
    uint8_t good;
    uint8_t great;
    uint8_t genius;
    uint8_t count4;
    uint8_t count5;
    uint8_t count6;
    uint8_t count7plus;
};

static const size_t NUM_WHEEL_PUZZLES_PER_DIFF = 20;

static const WheelPuzzleDef EASY_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'E', "ANPRST", 38, 13, 24, 32, 3, 6, 5, 24 },
    { 'E', "ADGNRS", 38, 13, 24, 32, 7, 10, 8, 13 },
    { 'E', "FLORSW", 38, 13, 24, 32, 12, 8, 6, 12 },
    { 'E', "ABKLNT", 38, 13, 24, 32, 7, 13, 12, 6 },
    { 'E', "ABCINT", 38, 13, 24, 32, 3, 5, 7, 23 },
    { 'E', "AIPRST", 38, 13, 24, 32, 2, 4, 3, 29 },
    { 'E', "ADORST", 38, 13, 24, 32, 4, 8, 5, 21 },
    { 'E', "AGHINT", 38, 13, 24, 32, 3, 5, 9, 21 },
    { 'E', "GHILNP", 38, 13, 24, 32, 16, 7, 11, 4 },
    { 'E', "ADINPT", 38, 13, 24, 32, 3, 7, 7, 21 },
    { 'E', "INOPRT", 38, 13, 24, 32, 0, 2, 3, 33 },
    { 'E', "MNORST", 38, 13, 24, 32, 3, 7, 7, 21 },
    { 'E', "DNORSW", 38, 13, 24, 32, 12, 7, 8, 11 },
    { 'E', "HNRSTU", 38, 13, 24, 32, 9, 9, 7, 13 },
    { 'E', "ADLOPR", 38, 13, 24, 32, 5, 13, 6, 14 },
    { 'E', "AHNPRT", 38, 13, 24, 32, 3, 14, 10, 11 },
    { 'E', "ACILNP", 38, 13, 24, 32, 7, 2, 11, 18 },
    { 'E', "AHRSTV", 38, 13, 24, 32, 4, 7, 10, 17 },
    { 'E', "CINOST", 38, 13, 24, 32, 7, 5, 3, 23 },
    { 'E', "BLORST", 38, 13, 24, 32, 7, 9, 9, 13 },
};

static const WheelPuzzleDef MEDIUM_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'A', "GILNPY", 26, 9, 16, 22, 5, 9, 3, 9 },
    { 'A', "GIKLNW", 26, 9, 16, 22, 8, 11, 3, 4 },
    { 'O', "ABGINT", 26, 9, 16, 22, 7, 5, 5, 9 },
    { 'I', "FGNRSU", 26, 9, 16, 22, 8, 4, 5, 9 },
    { 'I', "ACGMNP", 26, 9, 16, 22, 2, 9, 9, 6 },
    { 'I', "AFGMNR", 26, 9, 16, 22, 2, 10, 9, 5 },
    { 'A', "CELNRT", 26, 9, 16, 22, 3, 3, 3, 17 },
    { 'O', "CEJPRT", 26, 9, 16, 22, 6, 4, 9, 7 },
    { 'O', "ABCLNY", 26, 9, 16, 22, 3, 10, 9, 4 },
    { 'I', "CEHMNY", 26, 9, 16, 22, 5, 5, 9, 7 },
    { 'A', "CLRSTY", 26, 9, 16, 22, 8, 11, 1, 6 },
    { 'O', "EJNRUY", 26, 9, 16, 22, 7, 6, 6, 7 },
    { 'A', "EJMSTY", 26, 9, 16, 22, 12, 6, 6, 2 },
    { 'O', "FIMNRU", 26, 9, 16, 22, 6, 5, 5, 10 },
    { 'A', "EIMPRV", 26, 9, 16, 22, 9, 8, 5, 4 },
    { 'O', "EFNRTU", 26, 9, 16, 22, 4, 3, 5, 14 },
    { 'I', "CELNPS", 26, 9, 16, 22, 4, 4, 10, 8 },
    { 'A', "CEFNRU", 26, 9, 16, 22, 7, 8, 5, 6 },
    { 'O', "ACEGRU", 26, 9, 16, 22, 6, 7, 6, 7 },
    { 'A', "BINORW", 26, 9, 16, 22, 8, 12, 4, 2 },
};

static const WheelPuzzleDef HARD_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'H', "DILNOP", 16, 5, 10, 13, 5, 3, 2, 6 },
    { 'U', "HIMPRT", 16, 5, 10, 13, 7, 1, 6, 2 },
    { 'H', "IMPRTU", 16, 5, 10, 13, 11, 3, 1, 1 },
    { 'K', "DGIMNO", 16, 5, 10, 13, 9, 0, 5, 2 },
    { 'W', "BEGINR", 16, 5, 10, 13, 4, 4, 5, 3 },
    { 'U', "CGILNR", 16, 5, 10, 13, 6, 2, 2, 6 },
    { 'G', "DEHILT", 16, 5, 10, 13, 4, 5, 4, 3 },
    { 'U', "EFGIRS", 16, 5, 10, 13, 6, 2, 3, 5 },
    { 'V', "AFLORS", 16, 5, 10, 13, 3, 7, 5, 1 },
    { 'W', "ADGINR", 16, 5, 10, 13, 4, 5, 1, 6 },
    { 'B', "AINOST", 16, 5, 10, 13, 1, 2, 4, 9 },
    { 'M', "ACEINS", 16, 5, 10, 13, 2, 6, 1, 7 },
    { 'D', "ACEILT", 16, 5, 10, 13, 0, 0, 0, 16 },
    { 'U', "CLMNOS", 16, 5, 10, 13, 0, 1, 6, 9 },
    { 'D', "CEINRS", 16, 5, 10, 13, 1, 3, 3, 9 },
    { 'V', "ACELOS", 16, 5, 10, 13, 3, 5, 4, 4 },
    { 'C', "AEILRS", 16, 5, 10, 13, 3, 3, 2, 8 },
    { 'G', "AEORTU", 16, 5, 10, 13, 3, 2, 2, 9 },
    { 'M', "BELOPR", 16, 5, 10, 13, 3, 5, 4, 4 },
    { 'Z', "ACDIOS", 16, 5, 10, 13, 5, 2, 3, 6 },
};

#endif // WHEEL_DATASET_H
