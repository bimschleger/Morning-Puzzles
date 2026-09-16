#include "KillerGen.h"
#include "KillerDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

KillerGen::KillerGen() : _size(4), _boxRows(2), _boxCols(2), _numCages(0) {
    memset(_cageMap, 0, sizeof(_cageMap));
    memset(_solution, 0, sizeof(_solution));
    memset(_cageSums, 0, sizeof(_cageSums));
}

void KillerGen::applyTransform(uint8_t transform) {
    uint8_t rot = transform % 4;
    bool flip = (transform >= 4);

    for (uint8_t k = 0; k < rot; k++) {
        uint8_t tempMap[MAX_SIZE][MAX_SIZE];
        uint8_t tempSol[MAX_SIZE][MAX_SIZE];
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                tempMap[j][_size - 1 - i] = _cageMap[i][j];
                tempSol[j][_size - 1 - i] = _solution[i][j];
            }
        }
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                _cageMap[i][j] = tempMap[i][j];
                _solution[i][j] = tempSol[i][j];
            }
        }
    }

    if (flip) {
        uint8_t tempMap[MAX_SIZE][MAX_SIZE];
        uint8_t tempSol[MAX_SIZE][MAX_SIZE];
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                tempMap[i][_size - 1 - j] = _cageMap[i][j];
                tempSol[i][_size - 1 - j] = _solution[i][j];
            }
        }
        for (uint8_t i = 0; i < _size; i++) {
            for (uint8_t j = 0; j < _size; j++) {
                _cageMap[i][j] = tempMap[i][j];
                _solution[i][j] = tempSol[i][j];
            }
        }
    }
}

void KillerGen::generate(KillerDifficulty difficulty, uint32_t seed) {
    if (seed == 0) {
        seed = (uint32_t)random(800);
    }
    uint16_t puzzleIdx = (seed / 8) % 100;

    if (difficulty == KILLER_EASY) {
        _size = 4;
        _boxRows = 2;
        _boxCols = 2;
        uint8_t transform = seed % 8;

        const Killer4x4Entry* entry = &KILLER_EASY_DATASET[puzzleIdx];
        _numCages = pgm_read_byte(&entry->num_cages);
        for (uint8_t i = 0; i < 16; i++) {
            uint8_t mapByte = pgm_read_byte(&entry->cage_map[i / 2]);
            _cageMap[i / 4][i % 4] = (i % 2 == 0) ? (mapByte >> 4) : (mapByte & 0x0F);

            uint8_t solByte = pgm_read_byte(&entry->solution[i / 2]);
            _solution[i / 4][i % 4] = (i % 2 == 0) ? (solByte >> 4) : (solByte & 0x0F);
        }
        for (uint8_t c = 0; c < _numCages && c < MAX_CAGES; c++) {
            _cageSums[c] = pgm_read_byte(&entry->cage_sums[c]);
        }
        applyTransform(transform);
    } else if (difficulty == KILLER_EXTREME) {
        _size = 6;
        _boxRows = 2;
        _boxCols = 3;
        // Box-preserving symmetries: 0 (identity), 2 (180 rot), 4 (h-flip), 6 (v-flip)
        uint8_t transform = (seed % 4) * 2;

        const Killer6x6Entry* entry = &KILLER_EXTREME_DATASET[puzzleIdx];
        _numCages = pgm_read_byte(&entry->num_cages);
        for (uint8_t i = 0; i < 36; i++) {
            uint8_t mapByte = pgm_read_byte(&entry->cage_map[i / 2]);
            _cageMap[i / 6][i % 6] = (i % 2 == 0) ? (mapByte >> 4) : (mapByte & 0x0F);

            uint8_t solByte = pgm_read_byte(&entry->solution[i / 2]);
            _solution[i / 6][i % 6] = (i % 2 == 0) ? (solByte >> 4) : (solByte & 0x0F);
        }
        for (uint8_t c = 0; c < _numCages && c < MAX_CAGES; c++) {
            _cageSums[c] = pgm_read_byte(&entry->cage_sums[c]);
        }
        applyTransform(transform);
    } else { // KILLER_MEDIUM
        _size = 4;
        _boxRows = 2;
        _boxCols = 2;
        uint8_t transform = seed % 8;

        const Killer4x4Entry* entry = &KILLER_MEDIUM_DATASET[puzzleIdx];
        _numCages = pgm_read_byte(&entry->num_cages);
        for (uint8_t i = 0; i < 16; i++) {
            uint8_t mapByte = pgm_read_byte(&entry->cage_map[i / 2]);
            _cageMap[i / 4][i % 4] = (i % 2 == 0) ? (mapByte >> 4) : (mapByte & 0x0F);

            uint8_t solByte = pgm_read_byte(&entry->solution[i / 2]);
            _solution[i / 4][i % 4] = (i % 2 == 0) ? (solByte >> 4) : (solByte & 0x0F);
        }
        for (uint8_t c = 0; c < _numCages && c < MAX_CAGES; c++) {
            _cageSums[c] = pgm_read_byte(&entry->cage_sums[c]);
        }
        applyTransform(transform);
    }
}

void KillerGen::printToReceipt(EscPosPrinter& printer) {
    const char letters[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    String sepBorder = "      +";
    for (uint8_t c = 0; c < _size; c++) sepBorder += "---+";
    printer.println(sepBorder);

    for (uint8_t r = 0; r < _size; r++) {
        String rowStr = "      |";
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t cid = _cageMap[r][c];
            char label = letters[cid % 26];
            rowStr += " ";
            rowStr += label;
            rowStr += " |";
        }
        printer.println(rowStr);
        printer.println(sepBorder);
    }
    printer.println("");

    // Cage sums legend wrapped to <= 44 columns
    String curLine = "CAGES: ";
    for (uint8_t c = 0; c < _numCages; c++) {
        String item = String(letters[c % 26]) + "=" + String((int)_cageSums[c]);
        if (c + 1 < _numCages) item += ", ";
        if (curLine.length() + item.length() > 44) {
            printer.println(curLine);
            curLine = "       " + item;
        } else {
            curLine += item;
        }
    }
    if (curLine.length() > 7) {
        printer.println(curLine);
    }
    printer.println("");
}

bool KillerGen::printRasterToReceipt(EscPosPrinter& printer) {
    const int16_t padding = 24;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t cellSize = boardSize / _size;
    const int16_t actualBoard = cellSize * _size;
    const int16_t totalH = padding + actualBoard + padding;
    const int16_t inset = (_size == 4) ? 10 : 8;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // 1. Outer Frame
    canvas.drawRect(padding, padding, actualBoard, actualBoard, 4);

    // 2. Grid lines
    for (uint8_t r = 1; r < _size; r++) {
        int16_t y = padding + r * cellSize;
        uint8_t thick = (r % _boxRows == 0) ? 4 : 2;
        canvas.drawHLine(padding, y, actualBoard, thick);
    }
    for (uint8_t c = 1; c < _size; c++) {
        int16_t x = padding + c * cellSize;
        uint8_t thick = (c % _boxCols == 0) ? 4 : 2;
        canvas.drawVLine(x, padding, actualBoard, thick);
    }

    // 3. Inset Dashed Cage Outlines
    const int16_t dashLen = 8;
    const int16_t gapLen = 6;
    const int16_t step = dashLen + gapLen;

    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t cid = _cageMap[r][c];
            int16_t x0 = padding + c * cellSize + inset;
            int16_t y0 = padding + r * cellSize + inset;
            int16_t x1 = padding + (c + 1) * cellSize - inset;
            int16_t y1 = padding + (r + 1) * cellSize - inset;

            // Top edge
            if (r == 0 || _cageMap[r - 1][c] != cid) {
                for (int16_t x = x0; x < x1; x += step) {
                    int16_t seg = ((x + dashLen) > x1) ? (x1 - x) : dashLen;
                    canvas.drawHLine(x, y0, seg, 2);
                }
            }
            // Bottom edge
            if (r == _size - 1 || _cageMap[r + 1][c] != cid) {
                for (int16_t x = x0; x < x1; x += step) {
                    int16_t seg = ((x + dashLen) > x1) ? (x1 - x) : dashLen;
                    canvas.drawHLine(x, y1, seg, 2);
                }
            }
            // Left edge
            if (c == 0 || _cageMap[r][c - 1] != cid) {
                for (int16_t y = y0; y < y1; y += step) {
                    int16_t seg = ((y + dashLen) > y1) ? (y1 - y) : dashLen;
                    canvas.drawVLine(x0, y, seg, 2);
                }
            }
            // Right edge
            if (c == _size - 1 || _cageMap[r][c + 1] != cid) {
                for (int16_t y = y0; y < y1; y += step) {
                    int16_t seg = ((y + dashLen) > y1) ? (y1 - y) : dashLen;
                    canvas.drawVLine(x1, y, seg, 2);
                }
            }
        }
    }

    // 4. Clue Sum Numerals (drawn at top-left cell of each cage)
    for (uint8_t cid = 0; cid < _numCages; cid++) {
        int8_t minR = -1;
        int8_t minC = -1;
        for (uint8_t r = 0; r < _size; r++) {
            for (uint8_t c = 0; c < _size; c++) {
                if (_cageMap[r][c] == cid) {
                    if (minR == -1) {
                        minR = r;
                        minC = c;
                    }
                }
            }
        }
        if (minR != -1) {
            int16_t tx = padding + minC * cellSize + inset + 3;
            int16_t ty = padding + minR * cellSize + inset + 3;
            char sumStr[8];
            snprintf(sumStr, sizeof(sumStr), "%d", (int)_cageSums[cid]);
            canvas.drawText(tx, ty, sumStr, 2);
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}
