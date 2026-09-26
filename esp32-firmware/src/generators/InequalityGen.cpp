#include "InequalityGen.h"
#include "InequalityDataset.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

InequalityGen::InequalityGen() : _size(5), _cellSize(88), _height(488) {
    memset(_solution, 0, sizeof(_solution));
    memset(_givens, 0, sizeof(_givens));
    memset(_edges_h, 0, sizeof(_edges_h));
    memset(_edges_v, 0, sizeof(_edges_v));
}

void InequalityGen::applyTransform(uint8_t transform) {
    if (transform == 0) return;

    auto mapCoord = [this, transform](uint8_t r, uint8_t c, uint8_t& nr, uint8_t& nc) {
        if (transform == 1) { nr = c; nc = _size - 1 - r; }                 // rot90
        else if (transform == 2) { nr = _size - 1 - r; nc = _size - 1 - c; } // rot180
        else if (transform == 3) { nr = _size - 1 - c; nc = r; }             // rot270
        else if (transform == 4) { nr = r; nc = _size - 1 - c; }             // flip_h
        else if (transform == 5) { nr = _size - 1 - r; nc = c; }             // flip_v
        else if (transform == 6) { nr = c; nc = r; }                         // transpose
        else if (transform == 7) { nr = _size - 1 - c; nc = _size - 1 - r; } // anti-transpose
        else { nr = r; nc = c; }
    };

    uint8_t newSol[MAX_SIZE][MAX_SIZE];
    uint8_t newGivens[MAX_SIZE][MAX_SIZE];
    memset(newSol, 0, sizeof(newSol));
    memset(newGivens, 0, sizeof(newGivens));

    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t nr, nc;
            mapCoord(r, c, nr, nc);
            newSol[nr][nc] = _solution[r][c];
            newGivens[nr][nc] = _givens[r][c];
        }
    }

    uint8_t newEdgesH[MAX_SIZE][MAX_SIZE - 1];
    uint8_t newEdgesV[MAX_SIZE - 1][MAX_SIZE];
    memset(newEdgesH, 0, sizeof(newEdgesH));
    memset(newEdgesV, 0, sizeof(newEdgesV));

    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size - 1; c++) {
            uint8_t eh = _edges_h[r][c];
            if (eh == 0) continue;

            uint8_t r1 = r, c1 = c;
            uint8_t r2 = r, c2 = c + 1;
            uint8_t nr1, nc1, nr2, nc2;
            mapCoord(r1, c1, nr1, nc1);
            mapCoord(r2, c2, nr2, nc2);

            uint8_t v1 = (eh == 1) ? 1 : 2;
            uint8_t v2 = (eh == 1) ? 2 : 1;

            if (nr1 == nr2) {
                uint8_t r_new = nr1;
                uint8_t c_left = min(nc1, nc2);
                uint8_t val_left = (nc1 < nc2) ? v1 : v2;
                uint8_t val_right = (nc1 < nc2) ? v2 : v1;
                newEdgesH[r_new][c_left] = (val_left < val_right) ? 1 : 2;
            } else {
                uint8_t c_new = nc1;
                uint8_t r_top = min(nr1, nr2);
                uint8_t val_top = (nr1 < nr2) ? v1 : v2;
                uint8_t val_bot = (nr1 < nr2) ? v2 : v1;
                newEdgesV[r_top][c_new] = (val_top < val_bot) ? 1 : 2;
            }
        }
    }

    for (uint8_t r = 0; r < _size - 1; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t ev = _edges_v[r][c];
            if (ev == 0) continue;

            uint8_t r1 = r, c1 = c;
            uint8_t r2 = r + 1, c2 = c;
            uint8_t nr1, nc1, nr2, nc2;
            mapCoord(r1, c1, nr1, nc1);
            mapCoord(r2, c2, nr2, nc2);

            uint8_t v1 = (ev == 1) ? 1 : 2;
            uint8_t v2 = (ev == 1) ? 2 : 1;

            if (nr1 == nr2) {
                uint8_t r_new = nr1;
                uint8_t c_left = min(nc1, nc2);
                uint8_t val_left = (nc1 < nc2) ? v1 : v2;
                uint8_t val_right = (nc1 < nc2) ? v2 : v1;
                newEdgesH[r_new][c_left] = (val_left < val_right) ? 1 : 2;
            } else {
                uint8_t c_new = nc1;
                uint8_t r_top = min(nr1, nr2);
                uint8_t val_top = (nr1 < nr2) ? v1 : v2;
                uint8_t val_bot = (nr1 < nr2) ? v2 : v1;
                newEdgesV[r_top][c_new] = (val_top < val_bot) ? 1 : 2;
            }
        }
    }

    memcpy(_solution, newSol, sizeof(_solution));
    memcpy(_givens, newGivens, sizeof(_givens));
    memcpy(_edges_h, newEdgesH, sizeof(_edges_h));
    memcpy(_edges_v, newEdgesV, sizeof(_edges_v));
}

void InequalityGen::generate(InequalityDifficulty difficulty, uint32_t seed) {
    if (seed == 0) {
        seed = (uint32_t)random(800);
    }
    uint16_t puzzleIdx = (seed / 8) % 100;
    uint8_t transform = seed % 8;

    memset(_solution, 0, sizeof(_solution));
    memset(_givens, 0, sizeof(_givens));
    memset(_edges_h, 0, sizeof(_edges_h));
    memset(_edges_v, 0, sizeof(_edges_v));

    _cellSize = 88;

    if (difficulty == INEQUALITY_EASY || difficulty == INEQUALITY_MEDIUM) {
        _size = 4;
        _height = 400;
        const Inequality4x4Entry* p = (difficulty == INEQUALITY_EASY) ? &INEQUALITY_EASY_DATASET[puzzleIdx] : &INEQUALITY_MEDIUM_DATASET[puzzleIdx];
        for (uint8_t r = 0; r < 4; r++) {
            for (uint8_t c = 0; c < 4; c++) {
                uint8_t idx = r * 4 + c;
                uint8_t bSol = pgm_read_byte(&p->solution[idx >> 1]);
                _solution[r][c] = (idx & 1) ? (bSol & 0x0F) : (bSol >> 4);

                uint8_t bGiv = pgm_read_byte(&p->givens[idx >> 1]);
                _givens[r][c] = (idx & 1) ? (bGiv & 0x0F) : (bGiv >> 4);
            }
        }
        for (uint8_t r = 0; r < 4; r++) {
            for (uint8_t c = 0; c < 3; c++) {
                _edges_h[r][c] = pgm_read_byte(&p->edges_h[r * 3 + c]);
            }
        }
        for (uint8_t r = 0; r < 3; r++) {
            for (uint8_t c = 0; c < 4; c++) {
                _edges_v[r][c] = pgm_read_byte(&p->edges_v[r * 4 + c]);
            }
        }
    } else { // INEQUALITY_HARD or INEQUALITY_EXTREME (5x5)
        _size = 5;
        _height = 488;
        const Inequality5x5Entry* p = (difficulty == INEQUALITY_HARD) ? &INEQUALITY_HARD_DATASET[puzzleIdx] : &INEQUALITY_EXTREME_DATASET[puzzleIdx];
        for (uint8_t r = 0; r < 5; r++) {
            for (uint8_t c = 0; c < 5; c++) {
                uint8_t idx = r * 5 + c;
                uint8_t bSol = pgm_read_byte(&p->solution[idx >> 1]);
                _solution[r][c] = (idx & 1) ? (bSol & 0x0F) : (bSol >> 4);

                uint8_t bGiv = pgm_read_byte(&p->givens[idx >> 1]);
                _givens[r][c] = (idx & 1) ? (bGiv & 0x0F) : (bGiv >> 4);
            }
        }
        for (uint8_t r = 0; r < 5; r++) {
            for (uint8_t c = 0; c < 4; c++) {
                _edges_h[r][c] = pgm_read_byte(&p->edges_h[r * 4 + c]);
            }
        }
        for (uint8_t r = 0; r < 4; r++) {
            for (uint8_t c = 0; c < 5; c++) {
                _edges_v[r][c] = pgm_read_byte(&p->edges_v[r * 5 + c]);
            }
        }
    }

    applyTransform(transform);
}

void InequalityGen::printToReceipt(EscPosPrinter& printer) {
    for (uint8_t r = 0; r < _size; r++) {
        String rowStr = "      ";
        for (uint8_t c = 0; c < _size; c++) {
            if (_givens[r][c] > 0) {
                rowStr += String(_givens[r][c]);
            } else {
                rowStr += ".";
            }
            if (c < _size - 1) {
                uint8_t eh = _edges_h[r][c];
                if (eh == 1) rowStr += " < ";
                else if (eh == 2) rowStr += " > ";
                else rowStr += "   ";
            }
        }
        printer.println(rowStr);

        if (r < _size - 1) {
            String vStr = "      ";
            for (uint8_t c = 0; c < _size; c++) {
                uint8_t ev = _edges_v[r][c];
                if (ev == 1) vStr += "^";
                else if (ev == 2) vStr += "v";
                else vStr += " ";
                if (c < _size - 1) {
                    vStr += "   ";
                }
            }
            printer.println(vStr);
        }
    }
}

bool InequalityGen::printRasterToReceipt(EscPosPrinter& printer) {
    ThermalCanvas canvas;
    if (!canvas.begin(_height)) {
        return false;
    }
    canvas.clear();

    uint16_t grid_w = _size * _cellSize;
    uint16_t grid_x = (576 - grid_w) / 2;
    uint16_t grid_y = (_height - grid_w) / 2;

    // Outer grid border (4px)
    canvas.drawRect(grid_x, grid_y, grid_w, grid_w, 4);

    // Inner cell dividers (1px)
    for (uint8_t i = 1; i < _size; i++) {
        canvas.drawHLine(grid_x, grid_y + i * _cellSize, grid_w, 1);
        canvas.drawVLine(grid_x + i * _cellSize, grid_y, grid_w, 1);
    }

    // Horizontal inequality operators
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size - 1; c++) {
            uint8_t eh = _edges_h[r][c];
            if (eh == 1 || eh == 2) {
                uint16_t cx = grid_x + (c + 1) * _cellSize;
                uint16_t cy = grid_y + r * _cellSize + _cellSize / 2;
                canvas.fillRect(cx - 12, cy - 12, 25, 25, 0);
                if (eh == 1) { // <
                    for (int8_t d = 0; d < 8; d++) {
                        canvas.setPixel(cx - 4 + d, cy - d, 1);
                        canvas.setPixel(cx - 4 + d, cy - d + 1, 1);
                        canvas.setPixel(cx - 4 + d, cy + d, 1);
                        canvas.setPixel(cx - 4 + d, cy + d - 1, 1);
                    }
                } else if (eh == 2) { // >
                    for (int8_t d = 0; d < 8; d++) {
                        canvas.setPixel(cx + 3 - d, cy - d, 1);
                        canvas.setPixel(cx + 3 - d, cy - d + 1, 1);
                        canvas.setPixel(cx + 3 - d, cy + d, 1);
                        canvas.setPixel(cx + 3 - d, cy + d - 1, 1);
                    }
                }
            }
        }
    }

    // Vertical inequality operators
    for (uint8_t r = 0; r < _size - 1; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            uint8_t ev = _edges_v[r][c];
            if (ev == 1 || ev == 2) {
                uint16_t cx = grid_x + c * _cellSize + _cellSize / 2;
                uint16_t cy = grid_y + (r + 1) * _cellSize;
                canvas.fillRect(cx - 12, cy - 12, 25, 25, 0);
                if (ev == 1) { // ^
                    for (int8_t d = 0; d < 8; d++) {
                        canvas.setPixel(cx - d, cy - 4 + d, 1);
                        canvas.setPixel(cx - d + 1, cy - 4 + d, 1);
                        canvas.setPixel(cx + d, cy - 4 + d, 1);
                        canvas.setPixel(cx + d - 1, cy - 4 + d, 1);
                    }
                } else if (ev == 2) { // v
                    for (int8_t d = 0; d < 8; d++) {
                        canvas.setPixel(cx - d, cy + 3 - d, 1);
                        canvas.setPixel(cx - d + 1, cy + 3 - d, 1);
                        canvas.setPixel(cx + d, cy + 3 - d, 1);
                        canvas.setPixel(cx + d - 1, cy + 3 - d, 1);
                    }
                }
            }
        }
    }

    // Given numbers inside cells (scale 3: 15x21 glyph, 18px width)
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            if (_givens[r][c] > 0) {
                uint16_t tx = grid_x + c * _cellSize + (_cellSize - 18) / 2;
                uint16_t ty = grid_y + r * _cellSize + (_cellSize - 21) / 2;
                char str[2] = { (char)('0' + _givens[r][c]), '\0' };
                canvas.drawText(tx, ty, str, 3);
            }
        }
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}
