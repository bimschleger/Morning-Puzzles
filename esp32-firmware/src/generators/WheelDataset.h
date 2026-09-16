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
};

static const size_t NUM_WHEEL_PUZZLES_PER_DIFF = 20;

static const WheelPuzzleDef EASY_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'E', "ANPRST", 38, 13, 24, 32 },
    { 'E', "ADGNRS", 38, 13, 24, 32 },
    { 'E', "FLORSW", 38, 13, 24, 32 },
    { 'E', "ABKLNT", 38, 13, 24, 32 },
    { 'E', "ABCINT", 38, 13, 24, 32 },
    { 'E', "AIPRST", 38, 13, 24, 32 },
    { 'E', "ADORST", 38, 13, 24, 32 },
    { 'E', "AGHINT", 38, 13, 24, 32 },
    { 'E', "GHILNP", 38, 13, 24, 32 },
    { 'E', "ADINPT", 38, 13, 24, 32 },
    { 'E', "INOPRT", 38, 13, 24, 32 },
    { 'E', "MNORST", 38, 13, 24, 32 },
    { 'E', "DNORSW", 38, 13, 24, 32 },
    { 'E', "HNRSTU", 38, 13, 24, 32 },
    { 'E', "ADLOPR", 38, 13, 24, 32 },
    { 'E', "AHNPRT", 38, 13, 24, 32 },
    { 'E', "ACILNP", 38, 13, 24, 32 },
    { 'E', "AHRSTV", 38, 13, 24, 32 },
    { 'E', "CINOST", 38, 13, 24, 32 },
    { 'E', "BLORST", 38, 13, 24, 32 },
};

static const WheelPuzzleDef MEDIUM_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'A', "GILNPY", 26, 9, 16, 22 },
    { 'A', "GIKLNW", 26, 9, 16, 22 },
    { 'O', "ABGINT", 26, 9, 16, 22 },
    { 'I', "FGNRSU", 26, 9, 16, 22 },
    { 'I', "ACGMNP", 26, 9, 16, 22 },
    { 'I', "AFGMNR", 26, 9, 16, 22 },
    { 'A', "CELNRT", 26, 9, 16, 22 },
    { 'O', "CEJPRT", 26, 9, 16, 22 },
    { 'O', "ABCLNY", 26, 9, 16, 22 },
    { 'I', "CEHMNY", 26, 9, 16, 22 },
    { 'A', "CLRSTY", 26, 9, 16, 22 },
    { 'O', "EJNRUY", 26, 9, 16, 22 },
    { 'A', "EJMSTY", 26, 9, 16, 22 },
    { 'O', "FIMNRU", 26, 9, 16, 22 },
    { 'A', "EIMPRV", 26, 9, 16, 22 },
    { 'O', "EFNRTU", 26, 9, 16, 22 },
    { 'I', "CELNPS", 26, 9, 16, 22 },
    { 'A', "CEFNRU", 26, 9, 16, 22 },
    { 'O', "ACEGRU", 26, 9, 16, 22 },
    { 'A', "BINORW", 26, 9, 16, 22 },
};

static const WheelPuzzleDef HARD_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    { 'H', "DILNOP", 16, 5, 10, 13 },
    { 'U', "HIMPRT", 16, 5, 10, 13 },
    { 'H', "IMPRTU", 16, 5, 10, 13 },
    { 'K', "DGIMNO", 16, 5, 10, 13 },
    { 'W', "BEGINR", 16, 5, 10, 13 },
    { 'U', "CGILNR", 16, 5, 10, 13 },
    { 'G', "DEHILT", 16, 5, 10, 13 },
    { 'U', "EFGIRS", 16, 5, 10, 13 },
    { 'V', "AFLORS", 16, 5, 10, 13 },
    { 'W', "ADGINR", 16, 5, 10, 13 },
    { 'B', "AINOST", 16, 5, 10, 13 },
    { 'M', "ACEINS", 16, 5, 10, 13 },
    { 'D', "ACEILT", 16, 5, 10, 13 },
    { 'U', "CLMNOS", 16, 5, 10, 13 },
    { 'D', "CEINRS", 16, 5, 10, 13 },
    { 'V', "ACELOS", 16, 5, 10, 13 },
    { 'C', "AEILRS", 16, 5, 10, 13 },
    { 'G', "AEORTU", 16, 5, 10, 13 },
    { 'M', "BELOPR", 16, 5, 10, 13 },
    { 'Z', "ACDIOS", 16, 5, 10, 13 },
};

#endif // WHEEL_DATASET_H
