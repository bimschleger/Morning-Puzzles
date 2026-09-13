#include "OfflinePuzzleComposer.h"
#include "config.h"
#include "../printer/EscPosPrinter.h"

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
        case GRADE_MEDIUM:
        default:             return "MEDIUM";
    }
}

void OfflinePuzzleComposer::printSinglePuzzle(EscPosPrinter& printer, OfflinePuzzleType type, bool useRaster) {
    int r = random(3);
    switch (type) {
        case PUZZLE_SUDOKU: {
            SudokuDifficulty diff = (r == 0) ? SUDOKU_EASY : ((r == 1) ? SUDOKU_MEDIUM : SUDOKU_HARD);
            Serial.println("[COMPOSER] Generating Sudoku...");
            _sudoku.generate(diff);
            if (!useRaster || !_sudoku.printRasterToReceipt(printer, diff)) {
                _sudoku.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WORDSEARCH: {
            WordSearchDifficulty diff = (r == 0) ? WS_EASY : ((r == 1) ? WS_MEDIUM : WS_HARD);
            Serial.println("[COMPOSER] Generating Word Search...");
            _wordSearch.generate(diff);
            if (!useRaster || !_wordSearch.printRasterToReceipt(printer)) {
                _wordSearch.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_NONOGRAM: {
            NonogramDifficulty diff = (r == 0) ? NONO_EASY : ((r == 1) ? NONO_MEDIUM : NONO_HARD);
            Serial.println("[COMPOSER] Generating Nonogram...");
            _nonogram.generate(diff);
            if (!useRaster || !_nonogram.printRasterToReceipt(printer)) {
                _nonogram.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_QUEENS: {
            QueensDifficulty diff = (r == 0) ? QUEENS_EASY : ((r == 1) ? QUEENS_MEDIUM : QUEENS_HARD);
            Serial.println("[COMPOSER] Generating Queens puzzle...");
            _queens.generate(diff);
            if (!useRaster || !_queens.printRasterToReceipt(printer)) {
                _queens.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_JUMBLE: {
            JumbleDifficulty diff = (r == 0) ? JUMBLE_EASY : ((r == 1) ? JUMBLE_MEDIUM : JUMBLE_HARD);
            Serial.println("[COMPOSER] Generating Daily Jumble...");
            _jumble.generate(diff);
            if (!useRaster || !_jumble.printRasterToReceipt(printer)) {
                _jumble.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_BINARY: {
            BinaryDifficulty diff = (r == 0) ? BINARY_EASY : ((r == 1) ? BINARY_MEDIUM : BINARY_HARD);
            Serial.println("[COMPOSER] Generating Binary...");
            _binary.generate(diff);
            if (!useRaster || !_binary.printRasterToReceipt(printer, diff)) {
                _binary.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_MINES: {
            MinesDifficulty diff = (r == 0) ? MINES_EASY : ((r == 1) ? MINES_MEDIUM : MINES_HARD);
            Serial.println("[COMPOSER] Generating Mines...");
            _mines.generate(diff);
            if (!useRaster || !_mines.printRasterToReceipt(printer, diff)) {
                _mines.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TENTS: {
            TentsDifficulty diff = (r == 0) ? TENTS_EASY : ((r == 1) ? TENTS_MEDIUM : TENTS_HARD);
            Serial.println("[COMPOSER] Generating Tents...");
            _tents.generate(diff);
            if (!useRaster || !_tents.printRasterToReceipt(printer, diff)) {
                _tents.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_BRIDGES: {
            BridgesDifficulty diff = (r == 0) ? BRIDGES_EASY : ((r == 1) ? BRIDGES_MEDIUM : BRIDGES_HARD);
            Serial.println("[COMPOSER] Generating Bridges...");
            _bridges.generate(diff);
            if (!useRaster || !_bridges.printRasterToReceipt(printer, diff)) {
                _bridges.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_TANGO: {
            TangoDifficulty diff = (r == 0) ? TANGO_EASY : ((r == 1) ? TANGO_MEDIUM : TANGO_HARD);
            Serial.println("[COMPOSER] Generating Tango...");
            _tango.generate(diff);
            if (!useRaster || !_tango.printRasterToReceipt(printer, diff)) {
                _tango.printToReceipt(printer, diff);
            }
            break;
        }
        case PUZZLE_WHEEL: {
            WheelDifficulty diff = (r == 0) ? WHEEL_EASY : ((r == 1) ? WHEEL_MEDIUM : WHEEL_HARD);
            Serial.println("[COMPOSER] Generating Wheel...");
            _wheel.generate(diff);
            if (!useRaster || !_wheel.printRasterToReceipt(printer)) {
                _wheel.printToReceipt(printer);
            }
            break;
        }
        case PUZZLE_LIGHTS: {
            LightsDifficulty diff = (r == 0) ? LIGHTS_EASY : ((r == 1) ? LIGHTS_MEDIUM : LIGHTS_HARD);
            Serial.println("[COMPOSER] Generating Lights...");
            _lights.generate(diff);
            if (!useRaster || !_lights.printRasterToReceipt(printer, diff)) {
                _lights.printToReceipt(printer, diff);
            }
            break;
        }
        default:
            break;
    }
}

bool OfflinePuzzleComposer::generateAndPrintReceipt(EscPosPrinter& printer, const String& dateStr, PuzzleGrade grade) {
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
    Serial.println("\n[COMPOSER] Starting 100% offline generation for DAILY 5-PUZZLE MIX...");

    if (!printer.connect()) {
        Serial.println("[COMPOSER] ERROR: Failed to connect to printer.");
        return false;
    }

    printer.init();

    // 1. Receipt Header
    String headerDate = (dateStr.length() > 0) ? dateStr : "Daily On-Demand Edition";
    printer.printHeader("MORNING PUZZLES", headerDate);
    printer.setAlign(ALIGN_CENTER);
    printer.println("DAILY 5-PUZZLE MIX");
    printer.println("");

#if (OFFLINE_PRINT_STYLE == STYLE_HYBRID)
    bool useRaster = true;
#else
    bool useRaster = false;
#endif

    uint8_t count = OFFLINE_PUZZLE_COUNT;
    if (count > (uint8_t)OFFLINE_PUZZLE_TOTAL) count = (uint8_t)OFFLINE_PUZZLE_TOTAL;
    if (count < 1) count = 1;

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
        PUZZLE_LIGHTS
    };

    // Fisher-Yates shuffle
    for (int i = (int)OFFLINE_PUZZLE_TOTAL - 1; i > 0; i--) {
        int j = random(i + 1);
        OfflinePuzzleType temp = allPuzzles[i];
        allPuzzles[i] = allPuzzles[j];
        allPuzzles[j] = temp;
    }

    for (uint8_t i = 0; i < count; i++) {
        printSinglePuzzle(printer, allPuzzles[i], useRaster);
        printer.printHorizontalLine('-');
    }

    // Footer
    printer.printDoubleLine();
    printer.setAlign(ALIGN_CENTER);
    printer.println("Printed on ESP32 80mm Thermal Receipt");
    printer.println("Puzzles generated 100% on-device (Offline)");
    printer.println("Good luck & have a wonderful day!");
    printer.printDoubleLine();

    printer.feed(4);
    printer.cut(false);
    printer.disconnect();

    unsigned long elapsed = millis() - startMs;
    Serial.printf("[COMPOSER] Generation & printing of %d puzzles completed in %lu ms!\n\n", 
                  count, elapsed);
    return true;
}
