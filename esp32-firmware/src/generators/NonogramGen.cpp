#include "NonogramGen.h"
#include "../printer/EscPosPrinter.h"

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
    printer.println("Use the number clues outside the grid to shade");
    printer.println("the correct cells and reveal the pixel picture.");
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
            line += " . ";
        }
        printer.println(line);
    }
    printer.println("");
}
