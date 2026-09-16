#ifndef CRYPTOGRAM_GEN_H
#define CRYPTOGRAM_GEN_H

#include <Arduino.h>

class EscPosPrinter;

enum CryptogramDifficulty {
    CRYPTO_EASY   = 0,
    CRYPTO_MEDIUM = 1,
    CRYPTO_HARD   = 2
};

struct CryptogramClue {
    char cipher;
    char plain;
};

class CryptogramGen {
public:
    CryptogramGen();

    void generate(CryptogramDifficulty difficulty = CRYPTO_MEDIUM);
    void printToReceipt(EscPosPrinter& printer);
    bool printRasterToReceipt(EscPosPrinter& printer);

    const char* getPhrase() const { return _phrase.c_str(); }
    const char* getAuthor() const { return _author.c_str(); }
    const char* getCiphertext() const { return _ciphertext.c_str(); }
    const char* getClueString() const { return _clueStr.c_str(); }
    uint8_t getClueCount() const { return _clueCount; }
    CryptogramDifficulty getDifficulty() const { return _difficulty; }

    // Seeded generation for deterministic verification testing
    void generateWithQuote(const char* phrase, const char* author, CryptogramDifficulty difficulty, uint32_t seed = 0);

private:
    void generateDerangement(char* p2c, char* c2p);
    void selectClues(const char* p2c);

    String _phrase;
    String _author;
    String _ciphertext;
    String _clueStr;
    CryptogramClue _clues[3];
    uint8_t _clueCount;
    CryptogramDifficulty _difficulty;
};

#endif // CRYPTOGRAM_GEN_H
