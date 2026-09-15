#include "OfflinePuzzleComposer.h"
#include "config.h"
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
    return (type == PUZZLE_LIGHTS || type == PUZZLE_QUEENS);
}

void OfflinePuzzleComposer::printSinglePuzzle(EscPosPrinter& printer, OfflinePuzzleType type, bool useRaster, PuzzleGrade grade) {
    switch (type) {
        case PUZZLE_SUDOKU: {
            SudokuDifficulty diff = (grade == GRADE_EASY) ? SUDOKU_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? SUDOKU_HARD : SUDOKU_MEDIUM);
            Serial.println("[COMPOSER] Generating Sudoku...");
            _sudoku.generate(diff);
            if (!useRaster || !_sudoku.printRasterToReceipt(printer, diff)) {
                _sudoku.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WORDSEARCH: {
            WordSearchDifficulty diff = (grade == GRADE_EASY) ? WS_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? WS_HARD : WS_MEDIUM);
            Serial.println("[COMPOSER] Generating Word Search...");
            _wordSearch.generate(diff);
            if (!useRaster || !_wordSearch.printRasterToReceipt(printer)) {
                _wordSearch.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_NONOGRAM: {
            NonogramDifficulty diff = (grade == GRADE_EASY) ? NONO_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? NONO_HARD : NONO_MEDIUM);
            Serial.println("[COMPOSER] Generating Nonogram...");
            _nonogram.generate(diff);
            if (!useRaster || !_nonogram.printRasterToReceipt(printer)) {
                _nonogram.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_QUEENS: {
            QueensDifficulty diff = (grade == GRADE_EASY) ? QUEENS_EASY : ((grade == GRADE_EXTREME) ? QUEENS_MASTER : ((grade == GRADE_HARD) ? QUEENS_HARD : QUEENS_MEDIUM));
            Serial.println("[COMPOSER] Generating Queens puzzle...");
            _queens.generate(diff);
            if (!useRaster || !_queens.printRasterToReceipt(printer)) {
                _queens.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_JUMBLE: {
            JumbleDifficulty diff = (grade == GRADE_EASY) ? JUMBLE_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? JUMBLE_HARD : JUMBLE_MEDIUM);
            Serial.println("[COMPOSER] Generating Daily Jumble...");
            _jumble.generate(diff);
            if (!useRaster || !_jumble.printRasterToReceipt(printer)) {
                _jumble.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_BINARY: {
            BinaryDifficulty diff = (grade == GRADE_EASY) ? BINARY_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? BINARY_HARD : BINARY_MEDIUM);
            Serial.println("[COMPOSER] Generating Binary...");
            _binary.generate(diff);
            if (!useRaster || !_binary.printRasterToReceipt(printer, diff)) {
                _binary.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_MINES: {
            MinesDifficulty diff = (grade == GRADE_EASY) ? MINES_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? MINES_HARD : MINES_MEDIUM);
            Serial.println("[COMPOSER] Generating Mines...");
            _mines.generate(diff);
            if (!useRaster || !_mines.printRasterToReceipt(printer, diff)) {
                _mines.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TENTS: {
            TentsDifficulty diff = (grade == GRADE_EASY) ? TENTS_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? TENTS_HARD : TENTS_MEDIUM);
            Serial.println("[COMPOSER] Generating Tents...");
            _tents.generate(diff);
            if (!useRaster || !_tents.printRasterToReceipt(printer, diff)) {
                _tents.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_BRIDGES: {
            BridgesDifficulty diff = (grade == GRADE_EASY) ? BRIDGES_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? BRIDGES_HARD : BRIDGES_MEDIUM);
            Serial.println("[COMPOSER] Generating Bridges...");
            _bridges.generate(diff);
            if (!useRaster || !_bridges.printRasterToReceipt(printer, diff)) {
                _bridges.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TANGO: {
            TangoDifficulty diff = (grade == GRADE_EASY) ? TANGO_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? TANGO_HARD : TANGO_MEDIUM);
            Serial.println("[COMPOSER] Generating Tango...");
            _tango.generate(diff);
            if (!useRaster || !_tango.printRasterToReceipt(printer, diff)) {
                _tango.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WHEEL: {
            WheelDifficulty diff = (grade == GRADE_EASY) ? WHEEL_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? WHEEL_HARD : WHEEL_MEDIUM);
            Serial.println("[COMPOSER] Generating Wheel...");
            _wheel.generate(diff);
            if (!useRaster || !_wheel.printRasterToReceipt(printer)) {
                _wheel.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_LIGHTS: {
            LightsDifficulty diff = (grade == GRADE_EASY) ? LIGHTS_EASY : ((grade == GRADE_EXTREME) ? LIGHTS_EXTREME : ((grade == GRADE_HARD) ? LIGHTS_HARD : LIGHTS_MEDIUM));
            Serial.println("[COMPOSER] Generating Lights...");
            _lights.generate(diff);
            if (!useRaster || !_lights.printRasterToReceipt(printer, diff)) {
                _lights.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_LOOP: {
            LoopDifficulty diff = (grade == GRADE_EASY) ? LOOP_EASY : ((grade == GRADE_HARD || grade == GRADE_EXTREME) ? LOOP_HARD : LOOP_MEDIUM);
            Serial.println("[COMPOSER] Generating Loop...");
            _loop.generate(diff);
            if (!useRaster || !_loop.printRasterToReceipt(printer, diff)) {
                _loop.printToReceipt(printer, diff);
            }
            break;
        }
        default:
            break;
    }
}

bool OfflinePuzzleComposer::generateAndPrintReceipt(EscPosPrinter& printer, const String& subtitle, PuzzleGrade grade) {
    // 1. Reseed PRNG with ESP32 hardware True Random Number Generator + microsecond timer
    randomSeed(esp_random() ^ (uint32_t)micros());

    // 2. Maintain grade state for status reporting
    PuzzleGrade effectiveGrade = grade;
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

    uint8_t count = OFFLINE_PUZZLE_COUNT;
    if (count > (uint8_t)OFFLINE_PUZZLE_TOTAL) count = (uint8_t)OFFLINE_PUZZLE_TOTAL;
    if (count < 1) count = 1;

    // 1. Receipt Header
    String headerSubtitle = (subtitle.length() > 0) ? subtitle : "Enjoy your morning puzzles";
    printer.printHeader("MORNING PUZZLES", headerSubtitle);
    printer.setAlign(ALIGN_CENTER);
    printer.println(String("DAILY ") + count + "-PUZZLE MIX");
    printer.println("");

#if (OFFLINE_PRINT_STYLE == STYLE_HYBRID)
    bool useRaster = true;
#else
    bool useRaster = false;
#endif

    OfflinePuzzleType allPuzzles[OFFLINE_PUZZLE_TOTAL] = {
        PUZZLE_SUDOKU,
        PUZZLE_WORDSEARCH,
        PUZZLE_NONOGRAM,
        PUZZLE_QUEENS,
        PUZZLE_JUMBLE,
        PUZZLE_BINARY,
        PUZZLE_MINES,
        PUZZLE_TENTS,
        PUZZLE_BRIDGES,
        PUZZLE_TANGO,
        PUZZLE_WHEEL,
        PUZZLE_LIGHTS,
        PUZZLE_LOOP
    };

    // Fisher-Yates shuffle
    for (int i = (int)OFFLINE_PUZZLE_TOTAL - 1; i > 0; i--) {
        int j = random(i + 1);
        OfflinePuzzleType temp = allPuzzles[i];
        allPuzzles[i] = allPuzzles[j];
        allPuzzles[j] = temp;
    }

    for (uint8_t i = 0; i < count; i++) {
        PuzzleGrade slotGrade = effectiveGrade;
        if (effectiveGrade == GRADE_RANDOM) {
            slotGrade = getGradeForSlot(i, count);
        }
        printSinglePuzzle(printer, allPuzzles[i], useRaster, slotGrade);
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
