#include "OfflinePuzzleComposer.h"
#include "config.h"
#include "GeneratorUtils.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"
#include "GameRulesDataset.h"

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
    return (type == PUZZLE_LIGHTS || type == PUZZLE_QUEENS || type == PUZZLE_KILLER || type == PUZZLE_TOWERS);
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
            snprintf(instr, sizeof(instr), "Find %d+ words using center letter %c (letters may repeat), including a 7-letter pangram.", 
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
        case PUZZLE_LADDER: {
            LadderDifficulty diff = (grade == GRADE_EASY) ? LADDER_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? LADDER_HARD : LADDER_MEDIUM);
            const char* diffStr = (diff == LADDER_EASY) ? "EASY" : ((diff == LADDER_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Ladder...");
            LadderGen ladder;
            ladder.generate(diff);
            uint8_t count = ladder.getIntermediateCount();
            char instr[100];
            char countPhrase[32];
            if (count == 1) {
                snprintf(countPhrase, sizeof(countPhrase), "1 English word");
            } else {
                snprintf(countPhrase, sizeof(countPhrase), "%d English words", (int)count);
            }
            snprintf(instr, sizeof(instr), "Deduce %s to link %s to %s, changing 1 letter each step.",
                     countPhrase, ladder.getStartWord(), ladder.getTargetWord());
            printPuzzleHeader(printer, "LADDER", diffStr, instr);
            if (!useRaster || !ladder.printRasterToReceipt(printer)) {
                ladder.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_TOWERS: {
            TowersDifficulty diff = (grade == GRADE_EASY) ? TOWERS_EASY : ((grade == GRADE_EXTREME) ? TOWERS_EXTREME : ((grade == GRADE_HARD) ? TOWERS_HARD : TOWERS_MEDIUM));
            const char* diffStr = (diff == TOWERS_EASY) ? "EASY" : ((diff == TOWERS_EXTREME) ? "EXTREME" : ((diff == TOWERS_HARD) ? "HARD" : "MEDIUM"));
            Serial.println("[COMPOSER] Generating Towers...");
            TowersGen towers;
            towers.generate(diff);
            char towersInstr[100];
            snprintf(towersInstr, sizeof(towersInstr), "Place heights 1-%d per line so exterior numbers match the count of visible taller buildings.", (int)towers.getSize());
            printPuzzleHeader(printer, "TOWERS", diffStr, towersInstr);
            if (!useRaster || !towers.printRasterToReceipt(printer)) {
                towers.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_FUTOSHIKI: {
            FutoshikiDifficulty diff = (grade == GRADE_EASY) ? FUTOSHIKI_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? FUTOSHIKI_HARD : FUTOSHIKI_MEDIUM);
            const char* diffStr = (diff == FUTOSHIKI_EASY) ? "EASY" : ((diff == FUTOSHIKI_HARD) ? "HARD" : "MEDIUM");
            Serial.println("[COMPOSER] Generating Futoshiki...");
            FutoshikiGen futoshiki;
            futoshiki.generate(diff);
            char futoshikiInstr[100];
            snprintf(futoshikiInstr, sizeof(futoshikiInstr), "Fill digits 1-%d in every line while satisfying all inequality signs between adjacent cells.", (int)futoshiki.getSize());
            printPuzzleHeader(printer, "FUTOSHIKI", diffStr, futoshikiInstr);
            if (!useRaster || !futoshiki.printRasterToReceipt(printer)) {
                futoshiki.printToReceipt(printer);
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

void OfflinePuzzleComposer::renderGameGuideRaster(ThermalCanvas& canvas, uint8_t gameId) {
    canvas.clear(0);
    int16_t w = canvas.getWidth();
    int16_t h = canvas.getHeight();
    int16_t midX = w / 2;

    // Outer border (thickness 2)
    canvas.drawRect(10, 8, w - 20, h - 16, 2);

    // Center dashed divider
    for (int16_t y = 10; y < h - 10; y += 8) {
        canvas.drawVLine(midX, y, 4, 1);
    }

    // Headers
    canvas.drawText(84, 16, "VALID MOVE", 2);
    canvas.drawText(360, 16, "INVALID MOVE", 2);

    // Callout labels below
    canvas.drawText(108, h - 28, "[ OK ]", 2);
    canvas.drawText(384, h - 28, "[ ERROR ]", 2);

    int16_t ly = 46;
    int16_t ry = 46;

    switch (gameId) {
        case 0: { // SUDOKU
            int16_t sz = 32;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            canvas.drawRect(lx0, ly, 3 * sz, 3 * sz, 2);
            canvas.drawRect(rx0, ry, 3 * sz, 3 * sz, 2);
            for (int i = 1; i < 3; i++) {
                canvas.drawHLine(lx0, ly + i * sz, 3 * sz, 1);
                canvas.drawVLine(lx0 + i * sz, ly, 3 * sz, 1);
                canvas.drawHLine(rx0, ry + i * sz, 3 * sz, 1);
                canvas.drawVLine(rx0 + i * sz, ry, 3 * sz, 1);
            }
            canvas.drawChar(lx0 + sz + 10, ly + sz + 6, '5', 3);
            canvas.drawChar(rx0 + 10, ry + 6, '5', 3);
            canvas.drawChar(rx0 + sz + 10, ry + sz + 6, '5', 3);
            break;
        }
        case 1: { // SEARCH
            int16_t sz = 28;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            canvas.drawRect(lx0, ly, 3 * sz, 3 * sz, 2);
            canvas.drawRect(rx0, ry, 3 * sz, 3 * sz, 2);
            for (int i = 1; i < 3; i++) {
                canvas.drawHLine(lx0, ly + i * sz, 3 * sz, 1);
                canvas.drawVLine(lx0 + i * sz, ly, 3 * sz, 1);
                canvas.drawHLine(rx0, ry + i * sz, 3 * sz, 1);
                canvas.drawVLine(rx0 + i * sz, ry, 3 * sz, 1);
            }
            canvas.drawChar(lx0 + 8, ly + 4, 'C', 3);
            canvas.drawChar(lx0 + sz + 8, ly + sz + 4, 'A', 3);
            canvas.drawChar(lx0 + 2 * sz + 8, ly + 2 * sz + 4, 'T', 3);
            canvas.drawLine(lx0 + 4, ly + 4, lx0 + 3 * sz - 4, ly + 3 * sz - 4, 2);
            canvas.drawChar(rx0 + 8, ry + 4, 'C', 3);
            canvas.drawChar(rx0 + sz + 8, ry + 4, 'A', 3);
            canvas.drawChar(rx0 + sz + 8, ry + sz + 4, 'T', 3);
            canvas.drawLine(rx0 + 4, ry + 14, rx0 + sz + 14, ry + 14, 2);
            canvas.drawLine(rx0 + sz + 14, ry + 14, rx0 + sz + 14, ry + sz + 20, 2);
            break;
        }
        case 2: { // NONOGRAM
            int16_t sz = 24;
            int16_t lx0 = 144 - (4 * sz) / 2;
            int16_t rx0 = 432 - (4 * sz) / 2;
            int16_t ny = ly + 24;
            canvas.drawRect(lx0, ny, 4 * sz, sz, 2);
            canvas.drawRect(rx0, ny, 4 * sz, sz, 2);
            for (int i = 1; i < 4; i++) {
                canvas.drawVLine(lx0 + i * sz, ny, sz, 1);
                canvas.drawVLine(rx0 + i * sz, ny, sz, 1);
            }
            canvas.fillRect(lx0 + 2, ny + 2, sz - 4, sz - 4, 1);
            canvas.fillRect(lx0 + 2 * sz + 2, ny + 2, sz - 4, sz - 4, 1);
            canvas.drawText(lx0 - 28, ny + 4, "1 1", 2);
            canvas.fillRect(rx0 + 2, ny + 2, 2 * sz - 4, sz - 4, 1);
            canvas.drawText(rx0 - 28, ny + 4, "1 1", 2);
            break;
        }
        case 3: { // STARS
            int16_t sz = 32;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            canvas.drawRect(lx0, ly, 3 * sz, 3 * sz, 2);
            canvas.drawRect(rx0, ry, 3 * sz, 3 * sz, 2);
            canvas.fillHatch(lx0, ly, sz * 2, sz, 1);
            canvas.fillHatch(rx0, ry, sz * 2, sz, 1);
            for (int i = 1; i < 3; i++) {
                canvas.drawHLine(lx0, ly + i * sz, 3 * sz, 1);
                canvas.drawVLine(lx0 + i * sz, ly, 3 * sz, 1);
                canvas.drawHLine(rx0, ry + i * sz, 3 * sz, 1);
                canvas.drawVLine(rx0 + i * sz, ry, 3 * sz, 1);
            }
            canvas.drawChar(lx0 + 10, ly + 6, '*', 3);
            canvas.drawChar(lx0 + 2 * sz + 10, ly + sz + 6, '*', 3);
            canvas.drawChar(rx0 + 10, ry + 6, '*', 3);
            canvas.drawChar(rx0 + sz + 10, ry + sz + 6, '*', 3);
            canvas.drawLine(rx0 + sz - 4, ry + sz - 4, rx0 + sz + 4, ry + sz + 4, 2);
            break;
        }
        case 4: { // JUMBLE
            int16_t sz = 24;
            int16_t lx0 = 144 - (4 * sz) / 2;
            int16_t rx0 = 432 - (4 * sz) / 2;
            int16_t jy = ly + 24;
            canvas.drawRect(lx0, jy, 4 * sz, sz, 2);
            canvas.drawRect(rx0, jy, 4 * sz, sz, 2);
            for (int i = 1; i < 4; i++) {
                canvas.drawVLine(lx0 + i * sz, jy, sz, 1);
                canvas.drawVLine(rx0 + i * sz, jy, sz, 1);
            }
            canvas.drawChar(lx0 + 6, jy + 4, 'B', 2);
            canvas.drawChar(lx0 + sz + 6, jy + 4, 'O', 2);
            canvas.drawCircle(lx0 + sz + 12, jy + 12, 10, 1);
            canvas.drawChar(lx0 + 2 * sz + 6, jy + 4, 'A', 2);
            canvas.drawChar(lx0 + 3 * sz + 6, jy + 4, 'T', 2);
            canvas.drawChar(rx0 + 6, jy + 4, 'B', 2);
            canvas.drawChar(rx0 + sz + 6, jy + 4, 'T', 2);
            canvas.drawChar(rx0 + 2 * sz + 6, jy + 4, 'O', 2);
            canvas.drawChar(rx0 + 3 * sz + 6, jy + 4, 'A', 2);
            break;
        }
        case 5: { // BINARY
            int16_t sz = 26;
            int16_t lx0 = 144 - (4 * sz) / 2;
            int16_t rx0 = 432 - (4 * sz) / 2;
            int16_t by = ly + 24;
            canvas.drawRect(lx0, by, 4 * sz, sz, 2);
            canvas.drawRect(rx0, by, 4 * sz, sz, 2);
            for (int i = 1; i < 4; i++) {
                canvas.drawVLine(lx0 + i * sz, by, sz, 1);
                canvas.drawVLine(rx0 + i * sz, by, sz, 1);
            }
            canvas.drawChar(lx0 + 8, by + 4, '1', 2);
            canvas.drawChar(lx0 + sz + 8, by + 4, '0', 2);
            canvas.drawChar(lx0 + 2 * sz + 8, by + 4, '1', 2);
            canvas.drawChar(lx0 + 3 * sz + 8, by + 4, '0', 2);
            canvas.drawChar(rx0 + 8, by + 4, '0', 2);
            canvas.drawChar(rx0 + sz + 8, by + 4, '1', 2);
            canvas.drawChar(rx0 + 2 * sz + 8, by + 4, '1', 2);
            canvas.drawChar(rx0 + 3 * sz + 8, by + 4, '1', 2);
            break;
        }
        case 6: { // MINES
            int16_t sz = 34;
            int16_t lx0 = 144 - sz;
            int16_t rx0 = 432 - sz;
            int16_t my = ly + 14;
            canvas.drawRect(lx0, my, 2 * sz, 2 * sz, 2);
            canvas.drawRect(rx0, my, 2 * sz, 2 * sz, 2);
            canvas.drawHLine(lx0, my + sz, 2 * sz, 1);
            canvas.drawVLine(lx0 + sz, my, 2 * sz, 1);
            canvas.drawHLine(rx0, my + sz, 2 * sz, 1);
            canvas.drawVLine(rx0 + sz, my, 2 * sz, 1);
            canvas.drawChar(lx0 + 10, my + sz + 6, '1', 3);
            canvas.drawChar(lx0 + 10, my + 6, '*', 3);
            canvas.drawChar(rx0 + 10, my + sz + 6, '1', 3);
            canvas.drawChar(rx0 + 10, my + 6, '*', 3);
            canvas.drawChar(rx0 + sz + 10, my + 6, '*', 3);
            break;
        }
        case 7: { // TENTS
            int16_t sz = 32;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            int16_t ty = ly + 14;
            canvas.drawRect(lx0, ty, 3 * sz, 2 * sz, 2);
            canvas.drawRect(rx0, ty, 3 * sz, 2 * sz, 2);
            for (int i = 1; i < 3; i++) {
                canvas.drawVLine(lx0 + i * sz, ty, 2 * sz, 1);
                canvas.drawVLine(rx0 + i * sz, ty, 2 * sz, 1);
            }
            canvas.drawHLine(lx0, ty + sz, 3 * sz, 1);
            canvas.drawHLine(rx0, ty + sz, 3 * sz, 1);
            canvas.drawChar(lx0 + 10, ty + 6, 'T', 3);
            canvas.drawChar(lx0 + sz + 10, ty + 6, '^', 3);
            canvas.drawChar(rx0 + 10, ty + 6, 'T', 3);
            canvas.drawChar(rx0 + sz + 10, ty + 6, '^', 3);
            canvas.drawChar(rx0 + 2 * sz + 10, ty + sz + 6, '^', 3);
            break;
        }
        case 8: { // BRIDGES
            int16_t lx1 = 100, lx2 = 188;
            int16_t rx1 = 388, rx2 = 476;
            int16_t by = ly + 36;
            canvas.drawCircle(lx1, by, 16, 2);
            canvas.drawChar(lx1 - 5, by - 8, '3', 2);
            canvas.drawCircle(lx2, by, 16, 2);
            canvas.drawChar(lx2 - 5, by - 8, '2', 2);
            canvas.drawHLine(lx1 + 16, by - 4, (lx2 - 16) - (lx1 + 16), 2);
            canvas.drawHLine(lx1 + 16, by + 4, (lx2 - 16) - (lx1 + 16), 2);
            canvas.drawCircle(rx1, by, 16, 2);
            canvas.drawChar(rx1 - 5, by - 8, '4', 2);
            canvas.drawCircle(rx2, by, 16, 2);
            canvas.drawChar(rx2 - 5, by - 8, '3', 2);
            canvas.drawHLine(rx1 + 16, by - 6, (rx2 - 16) - (rx1 + 16), 1);
            canvas.drawHLine(rx1 + 16, by, (rx2 - 16) - (rx1 + 16), 1);
            canvas.drawHLine(rx1 + 16, by + 6, (rx2 - 16) - (rx1 + 16), 1);
            break;
        }
        case 9: { // KILLER
            int16_t sz = 34;
            int16_t lx0 = 144 - sz;
            int16_t rx0 = 432 - sz;
            int16_t ky = ly + 14;
            canvas.drawRect(lx0, ky, 2 * sz, sz, 1);
            canvas.drawDashedHLine(lx0, ky, 2 * sz, 4, 3, 2);
            canvas.drawDashedHLine(lx0, ky + sz, 2 * sz, 4, 3, 2);
            canvas.drawRect(rx0, ky, 2 * sz, sz, 1);
            canvas.drawDashedHLine(rx0, ky, 2 * sz, 4, 3, 2);
            canvas.drawDashedHLine(rx0, ky + sz, 2 * sz, 4, 3, 2);
            canvas.drawText(lx0 + 2, ky + 2, "3", 1);
            canvas.drawChar(lx0 + 10, ky + 8, '1', 2);
            canvas.drawChar(lx0 + sz + 10, ky + 8, '2', 2);
            canvas.drawText(rx0 + 2, ky + 2, "4", 1);
            canvas.drawChar(rx0 + 10, ky + 8, '2', 2);
            canvas.drawChar(rx0 + sz + 10, ky + 8, '2', 2);
            break;
        }
        case 10: { // CRYPTOGRAM
            int16_t cy = ly + 20;
            canvas.drawText(100, cy, "T H E", 2);
            canvas.drawText(100, cy + 24, "W Z K", 2);
            canvas.drawHLine(96, cy + 20, 96, 1);
            canvas.drawText(390, cy, "T O", 2);
            canvas.drawText(390, cy + 24, "W K", 2);
            canvas.drawHLine(386, cy + 20, 64, 1);
            break;
        }
        case 11: { // TANGO
            int16_t sz = 28;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            int16_t ty2 = ly + 20;
            canvas.drawRect(lx0, ty2, sz, sz, 2);
            canvas.drawChar(lx0 + 8, ty2 + 4, 'O', 2);
            canvas.drawChar(lx0 + sz + 8, ty2 + 4, '=', 2);
            canvas.drawRect(lx0 + 2 * sz, ty2, sz, sz, 2);
            canvas.drawChar(lx0 + 2 * sz + 8, ty2 + 4, 'O', 2);
            canvas.drawRect(rx0, ty2, 3 * sz, sz, 2);
            canvas.drawVLine(rx0 + sz, ty2, sz, 1);
            canvas.drawVLine(rx0 + 2 * sz, ty2, sz, 1);
            canvas.drawChar(rx0 + 8, ty2 + 4, 'O', 2);
            canvas.drawChar(rx0 + sz + 8, ty2 + 4, 'O', 2);
            canvas.drawChar(rx0 + 2 * sz + 8, ty2 + 4, 'O', 2);
            break;
        }
        case 12: { // LADDER
            int16_t dy = ly + 16;
            canvas.drawText(100, dy, "C A R T", 2);
            canvas.drawText(100, dy + 28, "D A R T", 2);
            canvas.drawText(124, dy + 14, "|", 1);
            canvas.drawText(388, dy, "C A R T", 2);
            canvas.drawText(388, dy + 28, "D A R K", 2);
            canvas.drawText(412, dy + 14, "|", 1);
            break;
        }
        case 13: { // WHEEL
            int16_t wy = ly + 36;
            canvas.drawCircle(144, wy, 28, 2);
            canvas.drawCircle(144, wy, 12, 1);
            canvas.drawChar(144 - 5, wy - 8, 'O', 2);
            canvas.drawText(144 - 40, wy + 34, "GLOW (USES O)", 1);
            canvas.drawCircle(432, wy, 28, 2);
            canvas.drawCircle(432, wy, 12, 1);
            canvas.drawChar(432 - 5, wy - 8, 'O', 2);
            canvas.drawText(432 - 40, wy + 34, "WING (NO O)", 1);
            break;
        }
        case 14: { // LIGHTS
            int16_t sz = 28;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            int16_t lty = ly + 20;
            canvas.drawRect(lx0, lty, 3 * sz, sz, 2);
            canvas.fillHatch(lx0 + sz, lty, sz, sz, 1);
            canvas.drawChar(lx0 + 8, lty + 4, '*', 2);
            canvas.drawChar(lx0 + 2 * sz + 8, lty + 4, '*', 2);
            canvas.drawRect(rx0, lty, 3 * sz, sz, 2);
            canvas.drawChar(rx0 + 8, lty + 4, '*', 2);
            canvas.drawLine(rx0 + 16, lty + 14, rx0 + 3 * sz - 16, lty + 14, 1);
            canvas.drawChar(rx0 + 2 * sz + 8, lty + 4, '*', 2);
            break;
        }
        case 15: { // LOOP
            int16_t sz = 32;
            int16_t lx0 = 144 - sz / 2;
            int16_t rx0 = 432 - sz / 2;
            int16_t lpy = ly + 20;
            canvas.drawChar(lx0 + 10, lpy + 6, '3', 3);
            canvas.drawHLine(lx0, lpy, sz, 3);
            canvas.drawVLine(lx0, lpy, sz, 3);
            canvas.drawHLine(lx0, lpy + sz, sz, 3);
            canvas.drawHLine(rx0 - 10, lpy + sz / 2, sz + 20, 3);
            canvas.drawVLine(rx0 + sz / 2, lpy - 10, sz + 20, 3);
            break;
        }
        case 16: { // TOWERS
            int16_t sz = 24;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            int16_t twy = ly + 24;
            canvas.drawText(lx0 - 24, twy + 4, "1", 2);
            canvas.drawRect(lx0, twy, 3 * sz, sz, 2);
            canvas.drawChar(lx0 + 6, twy + 4, '5', 2);
            canvas.drawChar(lx0 + sz + 6, twy + 4, '4', 2);
            canvas.drawChar(lx0 + 2 * sz + 6, twy + 4, '3', 2);
            canvas.drawText(rx0 - 24, twy + 4, "1", 2);
            canvas.drawRect(rx0, twy, 3 * sz, sz, 2);
            canvas.drawChar(rx0 + 6, twy + 4, '2', 2);
            canvas.drawChar(rx0 + sz + 6, twy + 4, '5', 2);
            canvas.drawChar(rx0 + 2 * sz + 6, twy + 4, '1', 2);
            break;
        }
        case 17: { // FUTOSHIKI
            int16_t sz = 28;
            int16_t lx0 = 144 - (3 * sz) / 2;
            int16_t rx0 = 432 - (3 * sz) / 2;
            int16_t fy = ly + 20;
            canvas.drawRect(lx0, fy, sz, sz, 2);
            canvas.drawChar(lx0 + 8, fy + 4, '2', 2);
            canvas.drawChar(lx0 + sz + 8, fy + 4, '<', 2);
            canvas.drawRect(lx0 + 2 * sz, fy, sz, sz, 2);
            canvas.drawChar(lx0 + 2 * sz + 8, fy + 4, '4', 2);
            canvas.drawRect(rx0, fy, sz, sz, 2);
            canvas.drawChar(rx0 + 8, fy + 4, '5', 2);
            canvas.drawChar(rx0 + sz + 8, fy + 4, '<', 2);
            canvas.drawRect(rx0 + 2 * sz, fy, sz, sz, 2);
            canvas.drawChar(rx0 + 2 * sz + 8, fy + 4, '3', 2);
            break;
        }
    }
}

bool OfflinePuzzleComposer::printGameGuide(EscPosPrinter& printer, uint8_t gameId) {
    const GameRuleDef* def = getGameRuleDefById(gameId);
    if (!def) {
        Serial.printf("[COMPOSER] Game rule for ID %d not found!\n", gameId);
        return false;
    }

    if (!printer.connect()) {
        Serial.println("[COMPOSER] Printer connection failed for game guide!");
        return false;
    }

    printer.initialize();

    // Master Header
    printer.setAlign(ALIGN_CENTER);
    printer.printHorizontalLine('=');
    printer.setDoubleStrike(true);
    printer.println("MORNING PUZZLES");
    printer.setDoubleStrike(false);
    printer.println("GAME GUIDE & QUICK REFERENCE");
    printer.printHorizontalLine('=');
    printer.println("");

    // Game Title
    printer.setBold(true);
    printer.print("--- ");
    printer.print(def->title);
    printer.println(" ---");
    printer.setBold(false);
    printer.println("");

    // Instruction
    printWrapped(printer, def->instruction, 44);
    printer.println("");

    // Objective
    printer.setBold(true);
    printer.println("OBJECTIVE:");
    printer.setBold(false);
    printWrapped(printer, def->objective, 44);
    printer.println("");

    // Rules
    printer.setBold(true);
    printer.println("RULES OF PLAY:");
    printer.setBold(false);
    for (uint8_t i = 0; i < def->ruleCount; i++) {
        printer.print(" * ");
        printWrapped(printer, def->rules[i], 41);
    }
    printer.println("");

    // Visual Move Diagram (Thermal Canvas)
    ThermalCanvas canvas;
    if (canvas.begin(216)) {
        renderGameGuideRaster(canvas, gameId);
        canvas.printTo(printer);
        canvas.end();
    }
    printer.println("");

    // Move captions
    printer.setBold(true);
    printer.print("[VALID MOVE]: ");
    printer.setBold(false);
    printWrapped(printer, def->validCaption, 44);
    printer.println("");

    printer.setBold(true);
    printer.print("[INVALID MOVE]: ");
    printer.setBold(false);
    printWrapped(printer, def->invalidCaption, 44);
    printer.println("");

    // Where to Start
    printer.setBold(true);
    printer.println("WHERE TO START:");
    printer.setBold(false);
    for (uint8_t i = 0; i < def->anchorCount; i++) {
        printer.print(" * ");
        printWrapped(printer, def->openingAnchors[i], 41);
    }
    printer.println("");

    // FAQ
    printer.setBold(true);
    printer.println("COMMON QUESTIONS:");
    printer.setBold(false);
    for (uint8_t i = 0; i < def->faqCount; i++) {
        printer.print(" Q: ");
        printWrapped(printer, def->faq[i].question, 40);
        printer.print(" A: ");
        printWrapped(printer, def->faq[i].answer, 40);
    }
    printer.println("");

    // Master Footer
    printer.setAlign(ALIGN_CENTER);
    printer.printHorizontalLine('-');
    printer.println("Enjoy your day!");
    printer.printHorizontalLine('-');

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();

    Serial.printf("[COMPOSER] Printed Game Guide for %s (ID %d)!\n", def->title, gameId);
    return true;
}

