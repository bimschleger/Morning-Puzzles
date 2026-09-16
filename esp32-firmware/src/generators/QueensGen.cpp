#include "QueensGen.h"
#include "StarsDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

QueensGen::QueensGen() : _size(8), _starsPerUnit(1), _numStars(0) {
    memset(_regions, -1, sizeof(_regions));
}

void QueensGen::applyTransform(uint8_t transform) {
    uint8_t rot = transform % 4;
    bool flip = (transform >= 4);

    for (uint8_t r = 0; r < rot; r++) {
        int8_t temp[MAX_SIZE][MAX_SIZE];
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                temp[j][_size - 1 - i] = _regions[i][j];
            }
        }
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                _regions[i][j] = temp[i][j];
            }
        }
        for (uint8_t s = 0; s < _numStars; s++) {
            uint8_t oldR = _stars[s].row;
            uint8_t oldC = _stars[s].col;
            _stars[s].row = oldC;
            _stars[s].col = _size - 1 - oldR;
        }
    }

    if (flip) {
        int8_t temp[MAX_SIZE][MAX_SIZE];
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                temp[i][_size - 1 - j] = _regions[i][j];
            }
        }
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                _regions[i][j] = temp[i][j];
            }
        }
        for (uint8_t s = 0; s < _numStars; s++) {
            _stars[s].col = _size - 1 - _stars[s].col;
        }
    }
}

void QueensGen::generate(QueensDifficulty difficulty, uint32_t seed) {
    if (seed == 0) {
        seed = (uint32_t)random(800);
    }
    uint16_t puzzleIdx = (seed / 8) % 100;
    uint8_t transform = seed % 8;

    const uint8_t* regionsData = nullptr;
    const uint8_t* solutionsData = nullptr;

    if (difficulty == QUEENS_EASY) {
        _size = 5;
        _starsPerUnit = 1;
        regionsData = &STARS_EASY_REGIONS[puzzleIdx][0];
        solutionsData = &STARS_EASY_SOLUTIONS[puzzleIdx][0];
    } else if (difficulty == QUEENS_HARD) {
        _size = 9;
        _starsPerUnit = 2;
        regionsData = &STARS_HARD_REGIONS[puzzleIdx][0];
        solutionsData = &STARS_HARD_SOLUTIONS[puzzleIdx][0];
    } else if (difficulty == QUEENS_MASTER) {
        _size = 10;
        _starsPerUnit = 2;
        regionsData = &STARS_EXTREME_REGIONS[puzzleIdx][0];
        solutionsData = &STARS_EXTREME_SOLUTIONS[puzzleIdx][0];
    } else { // QUEENS_MEDIUM
        _size = 8;
        _starsPerUnit = 1;
        regionsData = &STARS_MEDIUM_REGIONS[puzzleIdx][0];
        solutionsData = &STARS_MEDIUM_SOLUTIONS[puzzleIdx][0];
    }

    _numStars = _size * _starsPerUnit;

    // Unpack 4-bit nibble regions (2 cells per byte)
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t idx = r * _size + c;
            uint8_t byteVal = pgm_read_byte(regionsData + (idx >> 1));
            _regions[r][c] = (idx & 1) ? (byteVal & 0x0F) : (byteVal >> 4);
        }
    }

    // Unpack packed star coordinates: (row << 4) | col
    for (uint8_t i = 0; i < _numStars; i++) {
        uint8_t packed = pgm_read_byte(solutionsData + i);
        _stars[i].row = packed >> 4;
        _stars[i].col = packed & 0x0F;
    }

    applyTransform(transform);
}

void QueensGen::printToReceipt(EscPosPrinter& printer) {
    // Column numbers header
    String header = "     ";
    for (uint8_t c = 0; c < _size; c++) {
        header += String(c + 1) + " ";
    }
    printer.println(header);

    String divLine = "    +";
    for (uint8_t c = 0; c < _size; c++) divLine += "--";
    printer.println(divLine);

    // Grid rows with region letters
    const char letters[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (uint8_t r = 0; r < _size; r++) {
        String line = "  " + String(r + 1) + " |";
        for (uint8_t c = 0; c < _size; c++) {
            int8_t reg = _regions[r][c];
            char label = letters[reg % 26];
            line += " ";
            line += label;
        }
        printer.println(line);
    }
    printer.println("");
}

bool QueensGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t padding = 24;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t cellSize = boardSize / _size;
    const int16_t totalH = padding + cellSize * _size + padding;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Shading per region
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            int8_t reg = _regions[r][c];
            if (reg >= 0) {
                int16_t x0 = padding + c * cellSize;
                int16_t y0 = padding + r * cellSize;
                canvas.fillHatch(x0, y0, cellSize, cellSize, reg);
            }
        }
    }

    // Region boundaries and grid lines
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            int8_t reg = _regions[r][c];
            int16_t x0 = padding + c * cellSize;
            int16_t y0 = padding + r * cellSize;
            bool isBottom = (r == _size - 1) || (r + 1 < _size && _regions[r + 1][c] != reg);
            canvas.drawHLine(x0, y0 + cellSize, cellSize, isBottom ? 4 : 1);

            bool isRight = (c == _size - 1) || (c + 1 < _size && _regions[r][c + 1] != reg);
            canvas.drawVLine(x0 + cellSize, y0, cellSize, isRight ? 4 : 1);
        }
    }

    canvas.drawRect(padding, padding, cellSize * _size, cellSize * _size, 5);

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}
