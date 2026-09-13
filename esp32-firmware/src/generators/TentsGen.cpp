#include "TentsGen.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"
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
    printer.println(String("Pitch ") + _treeCount + " tents next to trees without tents");
    printer.println("touching, matching row and column counts.");
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

bool TentsGen::printRasterToReceipt(EscPosPrinter& printer, TentsDifficulty diff) {
    const char* diffStr = (diff == TENTS_EASY) ? "EASY" : ((diff == TENTS_HARD) ? "HARD" : "MEDIUM");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- TENTS ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println(String("Pitch ") + _treeCount + " tents next to trees without tents");
    printer.println("touching, matching row and column counts.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t padding = 24;
    const int16_t innerWidth = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t marginW = 48;
    const int16_t boardSize = innerWidth - marginW;
    const int16_t cellSize = boardSize / _size;
    const int16_t gridW = cellSize * _size;
    const int16_t gridX = padding + marginW;
    const int16_t gridY = padding + marginW;
    const int16_t totalH = gridY + gridW + padding;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Outer grid border
    canvas.drawRect(gridX, gridY, gridW, gridW, 4);

    // Inner grid lines
    for (uint8_t i = 1; i < _size; i++) {
        canvas.drawHLine(gridX, gridY + i * cellSize, gridW, 1);
        canvas.drawVLine(gridX + i * cellSize, gridY, gridW, 1);
    }

    // Column clues
    for (uint8_t c = 0; c < _size; c++) {
        char buf[4];
        snprintf(buf, sizeof(buf), "%d", _colClues[c]);
        int16_t cx = gridX + c * cellSize + (cellSize - 12) / 2;
        canvas.drawText(cx, gridY - 24, buf, 2);
    }

    // Row clues
    for (uint8_t r = 0; r < _size; r++) {
        char buf[4];
        snprintf(buf, sizeof(buf), "%d", _rowClues[r]);
        int16_t cy = gridY + r * cellSize + (cellSize - 14) / 2;
        canvas.drawText(padding + 16, cy, buf, 2);
    }

    // Trees ('T') or center dots
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            if (_puzzle[r][c] == 1) {
                int16_t tx = gridX + c * cellSize + (cellSize - 18) / 2;
                int16_t ty = gridY + r * cellSize + (cellSize - 21) / 2;
                canvas.drawChar(tx, ty, 'T', 3);
            } else {
                int16_t dotX = gridX + c * cellSize + cellSize / 2;
                int16_t dotY = gridY + r * cellSize + cellSize / 2;
                canvas.fillCircle(dotX, dotY, 2);
            }
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

