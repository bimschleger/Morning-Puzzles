#include "OfflinePuzzleComposer.h"
#include "config.h"
#include "GeneratorUtils.h"
#include "EscPosPrinter.h"

OfflinePuzzleComposer::OfflinePuzzleComposer() : 
    _currentGrade(GRADE_MEDIUM), 
    _rotationIndex(0) {
}

void OfflinePuzzleComposer::cycleGrade() {
    _rotationIndex = (_rotationIndex + 1) % 3;
    _currentGrade = (PuzzleGrade)_rotationIndex;
}

void OfflinePuzzleComposer::setGrade(PuzzleGrade grade) {
    _currentGrade = grade;
}

PuzzleGrade OfflinePuzzleComposer::getCurrentGrade() const {
    return _currentGrade;
}

const char* OfflinePuzzleComposer::getGradeName(PuzzleGrade grade) const {
    switch (grade) {
        case GRADE_EASY:     return "EASY";
        case GRADE_HARD:     return "HARD";
        case GRADE_ROTATING: return "ROTATING";
        case GRADE_RANDOM:   return "RANDOM";
        case GRADE_EXTREME:  return "EXTREME";
        case GRADE_MEDIUM:
        default:             return "MEDIUM";
    }
}

PuzzleGrade OfflinePuzzleComposer::getGradeForSlot(uint8_t index, uint8_t totalCount) const {
    if (totalCount <= 1) return GRADE_MEDIUM;
    float p = (float)index / (float)(totalCount - 1);
    if (p < 0.25f) return GRADE_EASY;
    if (p < 0.65f) return GRADE_MEDIUM;
    if (p < 0.85f) return GRADE_HARD;
    return GRADE_EXTREME;
}

bool OfflinePuzzleComposer::supportsExtreme(OfflinePuzzleType type) const {
    return (type == PUZZLE_LIGHTS || type == PUZZLE_QUEENS || type == PUZZLE_KILLER);
}

void OfflinePuzzleComposer::printSinglePuzzle(EscPosPrinter& printer, OfflinePuzzleType type, bool useRaster, PuzzleGrade grade) {
    switch (type) {
        case PUZZLE_SUDOKU: {
            SudokuDifficulty diff = (grade == GRADE_EASY) ? SUDOKU_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? SUDOKU_HARD : SUDOKU_MEDIUM);
            const char* diffStr = (diff == SUDOKU_EASY) ? "EASY" : ((diff == SUDOKU_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Sudoku...");
            SudokuGen sudoku;
            sudoku.generate(diff);
            printPuzzleHeader(printer, "SUDOKU", diffStr, 
                              "Fill every row, column, and 3x3 box with digits", 
                              "1-9 without repeating.");
            if (!useRaster || !sudoku.printRasterToReceipt(printer, diff)) {
                sudoku.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WORDSEARCH: {
            WordSearchDifficulty diff = (grade == GRADE_EASY) ? WS_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? WS_HARD : WS_MEDIUM);
            Serial.println("[COMPOSER] Generating Word Search...");
            WordSearchGen wordSearch;
            wordSearch.generate(diff);
            char wsInstr[64];
            snprintf(wsInstr, sizeof(wsInstr), "Find all %d hidden words listed below.", (int)wordSearch.getWordCount());
            printPuzzleHeader(printer, "SEARCH", nullptr, wsInstr);
            if (!useRaster || !wordSearch.printRasterToReceipt(printer)) {
                wordSearch.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_NONOGRAM: {
            NonogramDifficulty diff = (grade == GRADE_EASY) ? NONO_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? NONO_HARD : NONO_MEDIUM);
            const char* diffStr = (diff == NONO_EASY) ? "EASY" : ((diff == NONO_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Nonogram...");
            NonogramGen nonogram;
            nonogram.generate(diff);
            printPuzzleHeader(printer, "NONOGRAM", diffStr, 
                              "Shade blocks of cells matching each clue in", 
                              "order, separated by at least one empty cell.");
            if (!useRaster || !nonogram.printRasterToReceipt(printer)) {
                nonogram.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_QUEENS: {
            QueensDifficulty diff = (grade == GRADE_EASY) ? QUEENS_EASY : ((grade == GRADE_EXTREME) ? QUEENS_MASTER : ((grade == GRADE_HARD) ? QUEENS_HARD : QUEENS_MEDIUM));
            const char* diffStr = (diff == QUEENS_EASY) ? "EASY" : ((diff == QUEENS_MASTER) ? "EXTREME" : ((diff == QUEENS_HARD) ? "HARD" : "MEDIUM"));
            Serial.println("[COMPOSER] Generating Queens puzzle...");
            QueensGen queens;
            queens.generate(diff);
            const char* instr1 = (diff == QUEENS_HARD || diff == QUEENS_MASTER) 
                ? "Place 2 stars in each row, column, and region" 
                : "Place 1 star in each row, column, and region";
            printPuzzleHeader(printer, "STARS", diffStr, instr1, "with no stars touching, even diagonally.");
            if (!useRaster || !queens.printRasterToReceipt(printer)) {
                queens.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_JUMBLE: {
            JumbleDifficulty diff = (grade == GRADE_EASY) ? JUMBLE_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? JUMBLE_HARD : JUMBLE_MEDIUM);
            const char* diffStr = (diff == JUMBLE_EASY) ? "EASY" : ((diff == JUMBLE_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Daily Jumble...");
            JumbleGen jumble;
            jumble.generate(diff);
            printPuzzleHeader(printer, "JUMBLE", diffStr,
                              "Unscramble each word, then use the circled",
                              "letters to solve the riddle.");
            if (!useRaster || !jumble.printRasterToReceipt(printer)) {
                jumble.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_BINARY: {
            BinaryDifficulty diff = (grade == GRADE_EASY) ? BINARY_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? BINARY_HARD : BINARY_MEDIUM);
            const char* diffStr = (diff == BINARY_EASY) ? "EASY" : ((diff == BINARY_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Binary...");
            BinaryGen binary;
            binary.generate(diff);
            const char* binInstr1 = (diff == BINARY_EASY)
                ? "Fill each row and column with three 0s and"
                : "Fill each row and column with four 0s and";
            const char* binInstr2 = (diff == BINARY_EASY)
                ? "three 1s, with no more than two consecutive of each type."
                : "four 1s, with no more than two consecutive of each type.";
            printPuzzleHeader(printer, "BINARY", diffStr, binInstr1, binInstr2);
            if (!useRaster || !binary.printRasterToReceipt(printer, diff)) {
                binary.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_MINES: {
            MinesDifficulty diff = (grade == GRADE_EASY) ? MINES_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? MINES_HARD : MINES_MEDIUM);
            const char* diffStr = (diff == MINES_EASY) ? "EASY" : ((diff == MINES_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Mines...");
            MinesGen mines;
            mines.generate(diff);
            char instr[64];
            snprintf(instr, sizeof(instr), "Deduce all %d hidden mines using the adjacent numbered clues.", (int)mines.getTotalMines());
            printPuzzleHeader(printer, "MINES", diffStr, instr);
            if (!useRaster || !mines.printRasterToReceipt(printer, diff)) {
                mines.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TENTS: {
            TentsDifficulty diff = (grade == GRADE_EASY) ? TENTS_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? TENTS_HARD : TENTS_MEDIUM);
            const char* diffStr = (diff == TENTS_EASY) ? "EASY" : ((diff == TENTS_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Tents...");
            TentsGen tents;
            tents.generate(diff);
            char tentsInstr1[64];
            snprintf(tentsInstr1, sizeof(tentsInstr1), "Pitch %d tents next to trees without tents", (int)tents.getTreeCount());
            printPuzzleHeader(printer, "TENTS", diffStr, tentsInstr1, "touching, matching row and column counts.");
            if (!useRaster || !tents.printRasterToReceipt(printer, diff)) {
                tents.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_BRIDGES: {
            BridgesDifficulty diff = (grade == GRADE_EASY) ? BRIDGES_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? BRIDGES_HARD : BRIDGES_MEDIUM);
            const char* diffStr = (diff == BRIDGES_EASY) ? "EASY" : ((diff == BRIDGES_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Bridges...");
            BridgesGen bridges;
            bridges.generate(diff);
            printPuzzleHeader(printer, "BRIDGES", diffStr, 
                              "Connect all islands into one network using", 
                              "1 or 2 lines matching each island's number.");
            if (!useRaster || !bridges.printRasterToReceipt(printer, diff)) {
                bridges.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TANGO: {
            TangoDifficulty diff = (grade == GRADE_EASY) ? TANGO_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? TANGO_HARD : TANGO_MEDIUM);
            const char* diffStr = (diff == TANGO_EASY) ? "EASY" : ((diff == TANGO_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Tango...");
            TangoGen tango;
            tango.generate(diff);
            const char* tangoInstr1 = (diff == TANGO_HARD)
                ? "Fill each line with four 0s and four 1s"
                : "Fill each line with three 0s and three 1s";
            printPuzzleHeader(printer, "TANGO", diffStr, tangoInstr1, "without trios; = means same, x means opposite.");
            if (!useRaster || !tango.printRasterToReceipt(printer, diff)) {
                tango.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WHEEL: {
            WheelDifficulty diff = (grade == GRADE_EASY) ? WHEEL_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? WHEEL_HARD : WHEEL_MEDIUM);
            const char* diffStr = (diff == WHEEL_EASY) ? "EASY" : ((diff == WHEEL_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Wheel...");
            WheelGen wheel;
            wheel.generate(diff);
            char instr[110];
            snprintf(instr, sizeof(instr), "Find %d+ words using center letter %c and outer letters, including a 7-letter pangram.", 
                     (int)wheel.getWordCount(), wheel.getCenterLetter());
            printPuzzleHeader(printer, "WHEEL", diffStr, instr);
            if (!useRaster || !wheel.printRasterToReceipt(printer)) {
                wheel.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_LIGHTS: {
            LightsDifficulty diff = (grade == GRADE_EASY) ? LIGHTS_EASY : ((grade == GRADE_EXTREME) ? LIGHTS_EXTREME : ((grade == GRADE_HARD) ? LIGHTS_HARD : LIGHTS_MEDIUM));
            const char* diffStr = (diff == LIGHTS_EASY) ? "EASY" : ((diff == LIGHTS_EXTREME) ? "EXTREME" : ((diff == LIGHTS_HARD) ? "HARD" : "MEDIUM"));
            Serial.println("[COMPOSER] Generating Lights...");
            LightsGen lights;
            lights.generate(diff);
            char lightsInstr[64];
            snprintf(lightsInstr, sizeof(lightsInstr), "Place %d bulbs to light all corridors without", (int)lights.getTotalBulbs());
            printPuzzleHeader(printer, "LIGHTS", diffStr, lightsInstr, "bulbs shining together or exceeding numbers.");
            if (!useRaster || !lights.printRasterToReceipt(printer, diff)) {
                lights.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_LOOP: {
            LoopDifficulty diff = (grade == GRADE_EASY) ? LOOP_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? LOOP_HARD : LOOP_MEDIUM);
            const char* diffStr = (diff == LOOP_EASY) ? "EASY" : ((diff == LOOP_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Loop...");
            LoopGen loop;
            loop.generate(diff);
            printPuzzleHeader(printer, "LOOP", diffStr, 
                              "Draw a single continuous closed loop connecting dots", 
                              "so each number matches its edge count.");
            if (!useRaster || !loop.printRasterToReceipt(printer, diff)) {
                loop.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_KILLER: {
            KillerDifficulty diff = (grade == GRADE_EASY) ? KILLER_EASY : ((grade == GRADE_EXTREME) ? KILLER_EXTREME : KILLER_MEDIUM);
            const char* diffStr = (diff == KILLER_EASY) ? "EASY" : ((diff == KILLER_EXTREME) ? "EXTREME" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Killer Sudoku...");
            KillerGen killer;
            killer.generate(diff);
            const char* rangeStr = (diff == KILLER_EXTREME) ? "1-6" : "1-4";
            char killerInstr[100];
            snprintf(killerInstr, sizeof(killerInstr), "Fill every row, column, and box with digits %s, matching cage sums without repeats.", rangeStr);
            printPuzzleHeader(printer, "KILLER", diffStr, killerInstr);
            if (!useRaster || !killer.printRasterToReceipt(printer)) {
                killer.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_CRYPTOGRAM: {
            CryptogramDifficulty diff = (grade == GRADE_EASY) ? CRYPTO_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? CRYPTO_HARD : CRYPTO_MEDIUM);
            const char* diffStr = (diff == CRYPTO_EASY) ? "EASY" : ((diff == CRYPTO_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Cryptogram...");
            CryptogramGen cryptogram;
            cryptogram.generate(diff);
            uint8_t clueCnt = cryptogram.getClueCount();
            char cryptoInstr[100];
            snprintf(cryptoInstr, sizeof(cryptoInstr), "Deduce the hidden phrase using the %s and substitution logic.",
                     (clueCnt == 1) ? "1 letter clue" : (clueCnt == 3 ? "3 letter clues" : "2 letter clues"));
            printPuzzleHeader(printer, "CRYPTOGRAM", diffStr, cryptoInstr);
            if (!useRaster || !cryptogram.printRasterToReceipt(printer)) {
                cryptogram.printToReceipt(printer);
            }
            break;
        }
        default:
            break;
    }
}

bool OfflinePuzzleComposer::generateAndPrintReceipt(EscPosPrinter& printer, const String& subtitle, PuzzleGrade grade, const OfflineConfigManager* config) {
    // 1. Reseed PRNG with ESP32 hardware True Random Number Generator + microsecond timer
    randomSeed(esp_random() ^ (uint32_t)micros());

    // 2. Maintain grade state for status reporting
    PuzzleGrade effectiveGrade;
    if (grade != (PuzzleGrade)-1) {
        effectiveGrade = grade;
    } else if (config) {
        effectiveGrade = config->getPuzzleGrade();
    } else {
        effectiveGrade = GRADE_ESCALATING;
    }

    if (effectiveGrade == GRADE_ROTATING) {
        effectiveGrade = (PuzzleGrade)(_rotationIndex % 3);
        _rotationIndex = (_rotationIndex + 1) % 3;
    }
    _currentGrade = effectiveGrade;

    unsigned long startMs = millis();
    Serial.println("\n[COMPOSER] Starting 100% offline generation for DAILY PUZZLE MIX...");

    if (!printer.connect()) {
        Serial.println("[COMPOSER] ERROR: Failed to connect to printer.");
        return false;
    }

    printer.init();

    // 3. Determine enabled puzzle list and puzzle count
    OfflinePuzzleType activePuzzles[OFFLINE_PUZZLE_TOTAL];
    uint8_t totalAvailable = 0;

    if (config) {
        totalAvailable = config->getEnabledPuzzles(activePuzzles, OFFLINE_PUZZLE_TOTAL);
    }
    if (totalAvailable == 0) {
        totalAvailable = (uint8_t)OFFLINE_PUZZLE_TOTAL;
        for (uint8_t i = 0; i < totalAvailable; i++) {
            activePuzzles[i] = (OfflinePuzzleType)i;
        }
    }

    uint8_t count = config ? config->getPuzzleCount() : OFFLINE_PUZZLE_COUNT;
    if (count > totalAvailable) count = totalAvailable;
    if (count < 1) count = 1;

    // 4. Receipt Header
    String headerSubtitle = (subtitle.length() > 0) ? subtitle : "Enjoy your morning puzzles";
    printer.printHeader("MORNING PUZZLES", headerSubtitle);
    printer.setAlign(ALIGN_CENTER);
    char mixHeader[32];
    snprintf(mixHeader, sizeof(mixHeader), "DAILY %d-PUZZLE MIX", (int)count);
    printer.println(mixHeader);
    printer.println("");

#if (OFFLINE_PRINT_STYLE == STYLE_HYBRID)
    bool useRaster = true;
#else
    bool useRaster = false;
#endif

    // Fisher-Yates shuffle on available enabled puzzles
    mp_shuffle(activePuzzles, totalAvailable);

    for (uint8_t i = 0; i < count; i++) {
        PuzzleGrade slotGrade = effectiveGrade;
        if (effectiveGrade == GRADE_ESCALATING) {
            slotGrade = getGradeForSlot(i, count);
        }
        printSinglePuzzle(printer, activePuzzles[i], useRaster, slotGrade);
        printer.printHorizontalLine('-');
    }

    // Footer
    printer.setAlign(ALIGN_CENTER);
    printer.println("Enjoy your day!");
    printer.printHorizontalLine('-');

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();

    unsigned long elapsed = millis() - startMs;
    Serial.printf("[COMPOSER] Generation & printing of %d puzzles completed in %lu ms!\n\n", 
                  count, elapsed);
    return true;
}
