#include "BridgesGen.h"
#include "EscPosPrinter.h"
#include "ThermalCanvas.h"
#include <string.h>

static void shuffleInts(uint8_t* arr, uint8_t n) {
    for (int i = n - 1; i > 0; i--) {
        int j = random(0, i + 1);
        uint8_t temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

static bool edgesCrossLocal(uint8_t r1a, uint8_t c1a, uint8_t r1b, uint8_t c1b,
                           uint8_t r2a, uint8_t c2a, uint8_t r2b, uint8_t c2b) {
    bool e1H = (r1a == r1b);
    bool e2H = (r2a == r2b);
    if (e1H == e2H) return false;

    uint8_t hR, hCMin, hCMax, vC, vRMin, vRMax;
    if (e1H) {
        hR = r1a;
        hCMin = (c1a < c1b) ? c1a : c1b;
        hCMax = (c1a > c1b) ? c1a : c1b;
        vC = c2a;
        vRMin = (r2a < r2b) ? r2a : r2b;
        vRMax = (r2a > r2b) ? r2a : r2b;
    } else {
        hR = r2a;
        hCMin = (c2a < c2b) ? c2a : c2b;
        hCMax = (c2a > c2b) ? c2a : c2b;
        vC = c1a;
        vRMin = (r1a < r1b) ? r1a : r1b;
        vRMax = (r1a > r1b) ? r1a : r1b;
    }
    return (vRMin < hR && hR < vRMax) && (hCMin < vC && vC < hCMax);
}

BridgesGen::BridgesGen() : _size(8), _islandCount(10), _bridgeCount(0) {
    memset(_islands, 0, sizeof(_islands));
    memset(_bridges, 0, sizeof(_bridges));
}

void BridgesGen::generate(BridgesDifficulty diff) {
    uint8_t maxDegree = 6;
    if (diff == BRIDGES_EASY) {
        _size = 6;
        _islandCount = 8;
        maxDegree = 4;
    } else if (diff == BRIDGES_HARD) {
        _size = 8;
        _islandCount = 14;
        maxDegree = 8;
    } else {
        _size = 8;
        _islandCount = 10;
        maxDegree = 6;
    }

    uint8_t maxCells = _size * _size;
    uint8_t allCells[64];
    for (uint8_t i = 0; i < maxCells; i++) allCells[i] = i;

    for (uint8_t attempt = 0; attempt < 80; attempt++) {
        shuffleInts(allCells, maxCells);

        for (uint8_t i = 0; i < _islandCount; i++) {
            _islands[i].r = allCells[i] / _size;
            _islands[i].c = allCells[i] % _size;
            _islands[i].count = 0;
        }

        // Find potential edges
        uint8_t potU[64], potV[64];
        uint8_t potCount = 0;

        for (uint8_t i = 0; i < _islandCount; i++) {
            for (uint8_t j = i + 1; j < _islandCount; j++) {
                if (_islands[i].r == _islands[j].r) {
                    uint8_t cMin = (_islands[i].c < _islands[j].c) ? _islands[i].c : _islands[j].c;
                    uint8_t cMax = (_islands[i].c > _islands[j].c) ? _islands[i].c : _islands[j].c;
                    bool blocked = false;
                    for (uint8_t k = 0; k < _islandCount; k++) {
                        if (k != i && k != j && _islands[k].r == _islands[i].r && _islands[k].c > cMin && _islands[k].c < cMax) {
                            blocked = true;
                            break;
                        }
                    }
                    if (!blocked && potCount < 64) {
                        potU[potCount] = i;
                        potV[potCount] = j;
                        potCount++;
                    }
                } else if (_islands[i].c == _islands[j].c) {
                    uint8_t rMin = (_islands[i].r < _islands[j].r) ? _islands[i].r : _islands[j].r;
                    uint8_t rMax = (_islands[i].r > _islands[j].r) ? _islands[i].r : _islands[j].r;
                    bool blocked = false;
                    for (uint8_t k = 0; k < _islandCount; k++) {
                        if (k != i && k != j && _islands[k].c == _islands[i].c && _islands[k].r > rMin && _islands[k].r < rMax) {
                            blocked = true;
                            break;
                        }
                    }
                    if (!blocked && potCount < 64) {
                        potU[potCount] = i;
                        potV[potCount] = j;
                        potCount++;
                    }
                }
            }
        }

        if (potCount < _islandCount - 1) continue;

        // Shuffle potential edges
        uint8_t edgeOrder[64];
        for (uint8_t i = 0; i < potCount; i++) edgeOrder[i] = i;
        shuffleInts(edgeOrder, potCount);

        // Build Spanning Tree with Union-Find
        uint8_t parent[16];
        for (uint8_t i = 0; i < _islandCount; i++) parent[i] = i;

        auto findRoot = [&](uint8_t x) {
            uint8_t root = x;
            while (root != parent[root]) root = parent[root];
            return root;
        };

        _bridgeCount = 0;
        for (uint8_t idx = 0; idx < potCount; idx++) {
            uint8_t e = edgeOrder[idx];
            uint8_t u = potU[e], v = potV[e];

            bool crosses = false;
            for (uint8_t b = 0; b < _bridgeCount; b++) {
                if (edgesCrossLocal(_islands[u].r, _islands[u].c, _islands[v].r, _islands[v].c,
                                    _bridges[b].r1, _bridges[b].c1, _bridges[b].r2, _bridges[b].c2)) {
                    crosses = true;
                    break;
                }
            }

            if (!crosses) {
                uint8_t ru = findRoot(u);
                uint8_t rv = findRoot(v);
                if (ru != rv) {
                    parent[ru] = rv;
                    _bridges[_bridgeCount].r1 = _islands[u].r;
                    _bridges[_bridgeCount].c1 = _islands[u].c;
                    _bridges[_bridgeCount].r2 = _islands[v].r;
                    _bridges[_bridgeCount].c2 = _islands[v].c;
                    _bridges[_bridgeCount].count = 1;
                    _bridgeCount++;
                    _islands[u].count++;
                    _islands[v].count++;
                }
            }
        }

        // Verify connected graph
        uint8_t mainRoot = findRoot(0);
        bool allConnected = true;
        for (uint8_t i = 0; i < _islandCount; i++) {
            if (findRoot(i) != mainRoot) {
                allConnected = false;
                break;
            }
        }

        if (!allConnected) continue;

        // Randomly double some bridge counts
        for (uint8_t b = 0; b < _bridgeCount; b++) {
            uint8_t u = 0, v = 0;
            for (uint8_t i = 0; i < _islandCount; i++) {
                if (_islands[i].r == _bridges[b].r1 && _islands[i].c == _bridges[b].c1) u = i;
                if (_islands[i].r == _bridges[b].r2 && _islands[i].c == _bridges[b].c2) v = i;
            }
            if (_islands[u].count < maxDegree && _islands[v].count < maxDegree) {
                if (random(0, 100) < 35) {
                    _bridges[b].count = 2;
                    _islands[u].count++;
                    _islands[v].count++;
                }
            }
        }

        return; // Success!
    }
}

void BridgesGen::printToReceipt(EscPosPrinter& printer, BridgesDifficulty diff) {
    const char* diffStr = (diff == BRIDGES_EASY) ? "EASY" : ((diff == BRIDGES_HARD) ? "HARD" : "MEDIUM");

    printer.setBold(true);
    printer.println("--- BRIDGES ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Connect all islands into one network using");
    printer.println("1 or 2 lines matching each island's number.");
    printer.println("");

    uint8_t gridH = 2 * _size - 1;
    uint8_t gridW = 2 * _size - 1;
    char charGrid[16][16];
    memset(charGrid, ' ', sizeof(charGrid));

    for (uint8_t i = 0; i < _islandCount; i++) {
        uint8_t r = _islands[i].r * 2;
        uint8_t c = _islands[i].c * 2;
        charGrid[r][c] = '0' + _islands[i].count;
    }

    for (uint8_t r = 0; r < gridH; r++) {
        String line = "      ";
        for (uint8_t c = 0; c < gridW; c++) {
            line += charGrid[r][c];
            line += ' ';
        }
        printer.println(line);
    }
    printer.println("");
}

bool BridgesGen::printRasterToReceipt(EscPosPrinter& printer, BridgesDifficulty diff) {
    const char* diffStr = (diff == BRIDGES_EASY) ? "EASY" : ((diff == BRIDGES_HARD) ? "HARD" : "MEDIUM");

    printer.setAlign(ALIGN_CENTER);
    printer.setBold(true);
    printer.println("--- BRIDGES ---");
    printer.setBold(false);
    printer.println(String("DIFFICULTY: ") + diffStr);
    printer.println("Connect all islands into one network using");
    printer.println("1 or 2 lines matching each island's number.");
    printer.println("");
    printer.setAlign(ALIGN_LEFT);

    const int16_t padding = 32;
    const int16_t boardSize = THERMAL_CANVAS_WIDTH - padding * 2;
    const int16_t step = (_size > 1) ? (boardSize / (_size - 1)) : boardSize;
    const int16_t totalH = padding + boardSize + padding;

    ThermalCanvas canvas;
    if (!canvas.begin(totalH)) {
        return false;
    }

    // Corner framing brackets
    int16_t cornerLen = 16;
    canvas.drawHLine(padding, padding, cornerLen, 2);
    canvas.drawVLine(padding, padding, cornerLen, 2);
    canvas.drawHLine(padding + boardSize - cornerLen, padding, cornerLen, 2);
    canvas.drawVLine(padding + boardSize, padding, cornerLen, 2);
    canvas.drawHLine(padding, padding + boardSize, cornerLen, 2);
    canvas.drawVLine(padding, padding + boardSize - cornerLen, cornerLen, 2);
    canvas.drawHLine(padding + boardSize - cornerLen, padding + boardSize, cornerLen, 2);
    canvas.drawVLine(padding + boardSize, padding + boardSize - cornerLen, cornerLen, 2);

    // Islands
    int16_t islandRadius = max((int16_t)18, min((int16_t)24, (int16_t)(step / 3)));
    for (uint8_t i = 0; i < _islandCount; i++) {
        int16_t cx = padding + _islands[i].c * step;
        int16_t cy = padding + _islands[i].r * step;

        canvas.fillCircle(cx, cy, islandRadius, 0); // clear white interior
        canvas.drawCircle(cx, cy, islandRadius, 2, 1); // circle border
        canvas.drawChar(cx - 5, cy - 7, '0' + _islands[i].count, 2, 1);
    }

    bool ok = canvas.printTo(printer);
    canvas.end();
    return ok;
}

