#include "NonogramGen.h"
#include "EscPosPrinter.h"
#include "ThermalCanvas.h"

NonogramGen::NonogramGen() : _size(5) {
    memset(_grid, 0, sizeof(_grid));
}

void NonogramGen::calculateClues() {
    for (uint8_t i = 0; i < _size; i++) {
        _rowClues[i].clear();
        _colClues[i].clear();
    }

    // Row clues
    for (uint8_t r = 0; r < _size; r++) {
        uint8_t count = 0;
        for (uint8_t c = 0; c < _size; c++) {
            if (_grid[r][c] == 1) {
                count++;
            } else if (count > 0) {
                _rowClues[r].push_back(count);
                count = 0;
            }
        }
        if (count > 0) _rowClues[r].push_back(count);
        if (_rowClues[r].empty()) _rowClues[r].push_back(0);
    }

    // Column clues
    for (uint8_t c = 0; c < _size; c++) {
        uint8_t count = 0;
        for (uint8_t r = 0; r < _size; r++) {
            if (_grid[r][c] == 1) {
                count++;
            } else if (count > 0) {
                _colClues[c].push_back(count);
                count = 0;
            }
        }
        if (count > 0) _colClues[c].push_back(count);
        if (_colClues[c].empty()) _colClues[c].push_back(0);
    }
}

void NonogramGen::generate(NonogramDifficulty difficulty) {
    if (difficulty == NONO_EASY) _size = 5;
    else if (difficulty == NONO_HARD) _size = 10;
    else _size = 8;

    // Generate balanced random pattern (~50-60% fill)
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            _grid[r][c] = (random(100) < 55) ? 1 : 0;
        }
    }

    calculateClues();
}

void NonogramGen::printToReceipt(EscPosPrinter& printer) {
    const char* diffStr = (_size <= 5) ? "EASY" : ((_size <= 8) ? "MEDIUM" : "HARD");

    printer.setBold(true);
    printer.println("--- NONOGRAM ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Shade blocks of cells matching each clue in");
    printer.println("order, separated by at least one empty cell.");
    printer.println("");

    // Find maximum depth of column clues
    size_t maxColClues = 1;
    for (uint8_t c = 0; c < _size; c++) {
        if (_colClues[c].size() > maxColClues) {
            maxColClues = _colClues[c].size();
        }
    }

    // Print column clues header
    for (size_t clueIdx = 0; clueIdx < maxColClues; clueIdx++) {
        String line = "        "; // Offset for row clues
        for (uint8_t c = 0; c < _size; c++) {
            size_t numClues = _colClues[c].size();
            size_t pad = maxColClues - numClues;
            if (clueIdx >= pad) {
                uint8_t val = _colClues[c][clueIdx - pad];
                if (val < 10) line += " ";
                line += String(val) + " ";
            } else {
                line += "   ";
            }
        }
        printer.println(line);
    }

    // Divider line
    String sep = "       +";
    for (uint8_t c = 0; c < _size; c++) sep += "---";
    printer.println(sep);

    // Print each row with its clues and empty dot slots
    for (uint8_t r = 0; r < _size; r++) {
        String clueStr = "";
        for (size_t i = 0; i < _rowClues[r].size(); i++) {
            clueStr += String(_rowClues[r][i]) + " ";
        }
        // Pad clue string to 6 characters
        while (clueStr.length() < 6) clueStr = " " + clueStr;

        String line = clueStr + " | ";
        for (uint8_t c = 0; c < _size; c++) {
            line += "   ";
        }
        printer.println(line);
    }
    printer.println("");
}

bool NonogramGen::printRasterToReceipt(EscPosPrinter& printer) {
    const char* diffStr = (_size == 5) ? "EASY" : ((_size == 8) ? "MEDIUM" : "HARD");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- NONOGRAM ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Shade blocks of cells matching each clue in");
    printer.println("order, separated by at least one empty cell.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t padding = 24;
    const int16_t innerWidth = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t cellSize = (_size <= 5) ? 76 : ((_size <= 8) ? 50 : 40);
    const uint8_t majorInterval = (_size == 8) ? 4 : 5;
    const int16_t gridSize = cellSize * _size;
    const int16_t rowClueWidth = innerWidth - gridSize;

    size_t maxColClues = 1;
    for (uint8_t c = 0; c < _size; c++) {
        if (_colClues[c].size() > maxColClues) maxColClues = _colClues[c].size();
    }
    const int16_t colClueItemH = max((int16_t)24, (int16_t)(cellSize * 0.55));
    const int16_t colClueHeight = max((int16_t)50, (int16_t)(maxColClues * colClueItemH + 16));
    const int16_t totalH = 12 + colClueHeight + gridSize + 12;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    int16_t gridX = padding + rowClueWidth;
    int16_t gridY = 12 + colClueHeight;

    canvas.drawRect(padding, 12, rowClueWidth, colClueHeight, 3);
    canvas.drawRect(gridX, 12, gridSize, colClueHeight, 3);
    canvas.drawRect(padding, gridY, rowClueWidth, gridSize, 3);
    canvas.drawRect(gridX, gridY, gridSize, gridSize, 4);

    // Column clues
    for (uint8_t c = 0; c < _size; c++) {
        int16_t colCx = gridX + c * cellSize + cellSize / 2 - 6;
        size_t numClues = _colClues[c].size();
        for (size_t k = 0; k < numClues; k++) {
            int16_t dist = (numClues - 1 - k) * colClueItemH;
            char buf[4];
            snprintf(buf, sizeof(buf), "%d", _colClues[c][k]);
            canvas.drawText(colCx, gridY - 18 - dist, buf, 2);
        }
        if (c > 0) {
            bool isMajor = (c % majorInterval == 0);
            canvas.drawVLine(gridX + c * cellSize, 12, colClueHeight, isMajor ? 3 : 1);
        }
    }

    // Row clues
    for (uint8_t r = 0; r < _size; r++) {
        int16_t rowCy = gridY + r * cellSize + cellSize / 2 - 7;
        size_t numClues = _rowClues[r].size();
        for (size_t k = 0; k < numClues; k++) {
            int16_t dist = (numClues - 1 - k) * 20;
            char buf[4];
            snprintf(buf, sizeof(buf), "%d", _rowClues[r][k]);
            canvas.drawText(gridX - 16 - dist, rowCy, buf, 2);
        }
        if (r > 0) {
            bool isMajor = (r % majorInterval == 0);
            canvas.drawHLine(padding, gridY + r * cellSize, rowClueWidth, isMajor ? 3 : 1);
        }
    }

    // Major/minor grid lines
    for (uint8_t i = 1; i < _size; i++) {
        bool isMajor = (i % majorInterval == 0);
        uint8_t thickness = isMajor ? 4 : 1;
        canvas.drawHLine(gridX, gridY + i * cellSize, gridSize, thickness);
        canvas.drawVLine(gridX + i * cellSize, gridY, gridSize, thickness);
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

