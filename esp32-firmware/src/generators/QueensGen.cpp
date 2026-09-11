#include "QueensGen.h"
#include "../printer/EscPosPrinter.h"

QueensGen::QueensGen() : _size(8), _starsPerUnit(1) {
    memset(_regions, -1, sizeof(_regions));
}

bool QueensGen::canPlaceStar(uint8_t r, uint8_t c, uint8_t* colCounts) {
    if (colCounts[c] >= _starsPerUnit) return false;

    // Check all 8 surrounding cells
    for (int dr = -1; dr <= 1; dr++) {
        for (int dc = -1; dc <= 1; dc++) {
            int nr = r + dr;
            int nc = c + dc;
            if (nr >= 0 && nr < _size && nc >= 0 && nc < _size) {
                for (const auto& s : _stars) {
                    if (s.row == nr && s.col == nc) return false;
                }
            }
        }
    }
    return true;
}

bool QueensGen::placeStarsBacktrack(uint8_t row, uint8_t starsPlacedInRow, uint8_t* colCounts) {
    if (row == _size) {
        // Verify all columns have exact star count
        for (uint8_t c = 0; c < _size; c++) {
            if (colCounts[c] != _starsPerUnit) return false;
        }
        return true;
    }

    if (starsPlacedInRow == _starsPerUnit) {
        return placeStarsBacktrack(row + 1, 0, colCounts);
    }

    // Shuffle columns to try
    uint8_t cols[MAX_SIZE];
    for (uint8_t i = 0; i < _size; i++) cols[i] = i;
    for (int i = _size - 1; i > 0; i--) {
        int j = random(i + 1);
        uint8_t temp = cols[i];
        cols[i] = cols[j];
        cols[j] = temp;
    }

    for (uint8_t i = 0; i < _size; i++) {
        uint8_t c = cols[i];
        if (canPlaceStar(row, c, colCounts)) {
            _stars.push_back({row, c});
            colCounts[c]++;

            if (placeStarsBacktrack(row, starsPlacedInRow + 1, colCounts)) {
                return true;
            }

            _stars.pop_back();
            colCounts[c]--;
        }
    }

    return false;
}

void QueensGen::growRegions() {
    memset(_regions, -1, sizeof(_regions));

    // Seed regions from star locations
    for (size_t i = 0; i < _stars.size(); i++) {
        uint8_t regionId = (_starsPerUnit == 1) ? i : (i % _size);
        _regions[_stars[i].row][_stars[i].col] = regionId;
    }

    // Expand regions randomly to fill board
    int unassigned = _size * _size - _stars.size();
    int iterations = 0;
    while (unassigned > 0 && iterations < _size * _size * 6) {
        iterations++;
        uint8_t r = random(_size);
        uint8_t c = random(_size);

        if (_regions[r][c] != -1) {
            int8_t dr[] = {0, 0, 1, -1};
            int8_t dc[] = {1, -1, 0, 0};
            uint8_t dir = random(4);
            int nr = r + dr[dir];
            int nc = c + dc[dir];

            if (nr >= 0 && nr < _size && nc >= 0 && nc < _size && _regions[nr][nc] == -1) {
                _regions[nr][nc] = _regions[r][c];
                unassigned--;
            }
        }
    }

    // Fallback: fill any stranded cells
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            if (_regions[r][c] == -1) _regions[r][c] = 0;
        }
    }
}

void QueensGen::generate(QueensDifficulty difficulty) {
    if (difficulty == QUEENS_EASY) {
        _size = 6;
        _starsPerUnit = 1;
    } else if (difficulty == QUEENS_HARD) {
        _size = 9;
        _starsPerUnit = 2;
    } else {
        _size = 8;
        _starsPerUnit = 1;
    }

    bool solved = false;
    for (int attempts = 0; attempts < 50 && !solved; attempts++) {
        _stars.clear();
        uint8_t colCounts[MAX_SIZE] = {0};
        solved = placeStarsBacktrack(0, 0, colCounts);
    }

    growRegions();
}

void QueensGen::printToReceipt(EscPosPrinter& printer) {
    printer.setBold(true);
    if (_starsPerUnit == 1) {
        printer.println("--- QUEENS PUZZLE ---");
    } else {
        printer.println("--- STAR BATTLE (2-STAR) ---");
    }
    printer.setBold(false);
    printer.println(String("Size: ") + _size + "x" + _size + " | Place " + String(_starsPerUnit) + " per row, col, region");
    printer.println("Rule: No two Queens/Stars may touch diagonally!");
    printer.println("");

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
