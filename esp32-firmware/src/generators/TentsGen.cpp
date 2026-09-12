#include "TentsGen.h"
#include "../printer/EscPosPrinter.h"
#include <string.h>

static void shuffleIndices(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

TentsGen::TentsGen() : _size(8), _treeCount(8) {
    memset(_rowClues, 0, sizeof(_rowClues));
    memset(_colClues, 0, sizeof(_colClues));
    memset(_puzzle, 0, sizeof(_puzzle));
    memset(_solution, 0, sizeof(_solution));
}

void TentsGen::generate(TentsDifficulty diff) {
    if (diff == TENTS_EASY) {
        _size = 6;
        _treeCount = 4;
    } else if (diff == TENTS_HARD) {
        _size = 8;
        _treeCount = 11;
    } else {
        _size = 8;
        _treeCount = 8;
    }

    uint8_t maxCells = _size * _size;
    uint8_t allCells[64];
    for (uint8_t i = 0; i < maxCells; i++) allCells[i] = i;

    for (uint8_t attempt = 0; attempt < 100; attempt++) {
        shuffleIndices(allCells, maxCells);

        uint8_t tentR[16], tentC[16];
        uint8_t placedTents = 0;
        bool occupied[8][8];
        memset(occupied, 0, sizeof(occupied));

        for (uint8_t idx = 0; idx < maxCells; idx++) {
            if (placedTents >= _treeCount) break;
            uint8_t r = allCells[idx] / _size;
            uint8_t c = allCells[idx] % _size;
            if (!occupied[r][c]) {
                tentR[placedTents] = r;
                tentC[placedTents] = c;
                placedTents++;

                // Mark cell and all 8 neighbors as occupied
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        int nr = r + dr;
                        int nc = c + dc;
                        if (nr >= 0 && nr < _size && nc >= 0 && nc < _size) {
                            occupied[nr][nc] = true;
                        }
                    }
                }
            }
        }

        if (placedTents < _treeCount) continue;

        // Place tree for each tent
        bool treeOccupied[8][8];
        memset(treeOccupied, 0, sizeof(treeOccupied));
        for (uint8_t i = 0; i < placedTents; i++) {
            treeOccupied[tentR[i]][tentC[i]] = true;
        }

        uint8_t treeR[16], treeC[16];
        bool success = true;

        for (uint8_t i = 0; i < placedTents; i++) {
            uint8_t tr = tentR[i], tc = tentC[i];
            uint8_t candR[4], candC[4];
            uint8_t candCount = 0;

            const int drs[4] = {-1, 1, 0, 0};
            const int dcs[4] = {0, 0, -1, 1};
            for (uint8_t d = 0; d < 4; d++) {
                int nr = tr + drs[d];
                int nc = tc + dcs[d];
                if (nr >= 0 && nr < _size && nc >= 0 && nc < _size) {
                    if (!treeOccupied[nr][nc]) {
                        candR[candCount] = nr;
                        candC[candCount] = nc;
                        candCount++;
                    }
                }
            }

            if (candCount == 0) {
                success = false;
                break;
            }

            uint8_t pick = random(0, candCount);
            treeR[i] = candR[pick];
            treeC[i] = candC[pick];
            treeOccupied[candR[pick]][candC[pick]] = true;
        }

        if (!success) continue;

        // Compute row and column clues
        memset(_rowClues, 0, sizeof(_rowClues));
        memset(_colClues, 0, sizeof(_colClues));
        memset(_puzzle, 0, sizeof(_puzzle));
        memset(_solution, 0, sizeof(_solution));

        for (uint8_t i = 0; i < placedTents; i++) {
            _rowClues[tentR[i]]++;
            _colClues[tentC[i]]++;
            _puzzle[treeR[i]][treeC[i]] = 1;     // 1 = tree
            _solution[treeR[i]][treeC[i]] = 1;   // 1 = tree
            _solution[tentR[i]][tentC[i]] = 2;   // 2 = tent
        }

        return; // Success!
    }
}

void TentsGen::printToReceipt(EscPosPrinter& printer, TentsDifficulty diff) {
    const char* diffStr = (diff == TENTS_EASY) ? "EASY" : ((diff == TENTS_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- TENTS ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Pair each tree with an orthogonally adjacent tent");
    printer.println("such that tents never touch, even diagonally,");
    printer.println("matching the row and column counts.");
    printer.println("");

    // Col clues header
    String colHeader = "       ";
    for (uint8_t c = 0; c < _size; c++) {
        colHeader += String(_colClues[c]) + " ";
    }
    printer.println(colHeader);

    String sep = "     +";
    for (uint8_t c = 0; c < _size; c++) sep += "--";
    sep += "+";
    printer.println(sep);

    for (uint8_t r = 0; r < _size; r++) {
        String line = String("   ") + _rowClues[r] + " |";
        for (uint8_t c = 0; c < _size; c++) {
            if (_puzzle[r][c] == 1) {
                line += " T";
            } else {
                line += " .";
            }
        }
        line += " |";
        printer.println(line);
    }
    printer.println(sep);
    printer.println("");
}
