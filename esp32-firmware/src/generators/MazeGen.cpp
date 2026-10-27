#include "MazeGen.h"
#include "GeneratorUtils.h"
#include "../printer/EscPosPrinter.h"
#include "../printer/ThermalCanvas.h"

MazeGen::MazeGen() :
    _size(20),
    _cellSize(24),
    _wallThickness(3),
    _solutionMoveCount(0) {
    memset(_wallsH, 0xFF, sizeof(_wallsH));
    memset(_wallsV, 0xFF, sizeof(_wallsV));
}

uint8_t MazeGen::getWallH(uint8_t r, uint8_t c) const {
    if (r >= _size - 1 || c >= _size) return 0;
    uint16_t idx = (uint16_t)r * _size + c;
    return (_wallsH[idx >> 3] >> (idx & 7)) & 1;
}

void MazeGen::setWallH(uint8_t r, uint8_t c, uint8_t val) {
    if (r >= _size - 1 || c >= _size) return;
    uint16_t idx = (uint16_t)r * _size + c;
    if (val) {
        _wallsH[idx >> 3] |= (1 << (idx & 7));
    } else {
        _wallsH[idx >> 3] &= ~(1 << (idx & 7));
    }
}

uint8_t MazeGen::getWallV(uint8_t r, uint8_t c) const {
    if (r >= _size || c >= _size - 1) return 0;
    uint16_t idx = (uint16_t)r * (_size - 1) + c;
    return (_wallsV[idx >> 3] >> (idx & 7)) & 1;
}

void MazeGen::setWallV(uint8_t r, uint8_t c, uint8_t val) {
    if (r >= _size || c >= _size - 1) return;
    uint16_t idx = (uint16_t)r * (_size - 1) + c;
    if (val) {
        _wallsV[idx >> 3] |= (1 << (idx & 7));
    } else {
        _wallsV[idx >> 3] &= ~(1 << (idx & 7));
    }
}

void MazeGen::generate(MazeDifficulty diff, uint32_t seed) {
    if (seed != 0) {
        randomSeed(seed);
    }

    uint8_t branchProbPct = 25;
    if (diff == MAZE_EASY) {
        _size = 10;
        _cellSize = 48;
        _wallThickness = 4;
        branchProbPct = 50;
    } else if (diff == MAZE_HARD) {
        _size = 30;
        _cellSize = 16;
        _wallThickness = 2;
        branchProbPct = 5;
    } else if (diff == MAZE_EXTREME) {
        _size = 40;
        _cellSize = 12;
        _wallThickness = 2;
        branchProbPct = 0;
    } else {
        _size = 20;
        _cellSize = 24;
        _wallThickness = 3;
        branchProbPct = 25;
    }

    // Initialize all walls to 1 (solid)
    memset(_wallsH, 0xFF, sizeof(_wallsH));
    memset(_wallsV, 0xFF, sizeof(_wallsV));

    // Visited bitmask (up to 1600 cells = 200 bytes)
    uint8_t visited[200];
    memset(visited, 0, sizeof(visited));

    auto isVisited = [&](uint8_t r, uint8_t c) -> bool {
        uint16_t idx = (uint16_t)r * _size + c;
        return (visited[idx >> 3] >> (idx & 7)) & 1;
    };

    auto setVisited = [&](uint8_t r, uint8_t c) {
        uint16_t idx = (uint16_t)r * _size + c;
        visited[idx >> 3] |= (1 << (idx & 7));
    };

    // Active stack for growing tree algorithm
    uint16_t active[1600];
    uint16_t activeCount = 0;

    setVisited(0, 0);
    active[activeCount++] = 0;

    struct Neighbor {
        uint8_t r;
        uint8_t c;
        char dir;
    };

    while (activeCount > 0) {
        uint16_t idx = (random(100) < branchProbPct) ? random(activeCount) : (activeCount - 1);
        uint16_t cell = active[idx];
        uint8_t r = (uint8_t)(cell / _size);
        uint8_t c = (uint8_t)(cell % _size);

        Neighbor neighbors[4];
        uint8_t nCount = 0;

        if (r > 0 && !isVisited(r - 1, c)) {
            neighbors[nCount++] = { (uint8_t)(r - 1), c, 'N' };
        }
        if (r < _size - 1 && !isVisited(r + 1, c)) {
            neighbors[nCount++] = { (uint8_t)(r + 1), c, 'S' };
        }
        if (c > 0 && !isVisited(r, c - 1)) {
            neighbors[nCount++] = { r, (uint8_t)(c - 1), 'W' };
        }
        if (c < _size - 1 && !isVisited(r, c + 1)) {
            neighbors[nCount++] = { r, (uint8_t)(c + 1), 'E' };
        }

        if (nCount > 0) {
            uint8_t pick = random(nCount);
            Neighbor chosen = neighbors[pick];
            if (chosen.dir == 'N') {
                setWallH(r - 1, c, 0);
            } else if (chosen.dir == 'S') {
                setWallH(r, c, 0);
            } else if (chosen.dir == 'W') {
                setWallV(r, c - 1, 0);
            } else if (chosen.dir == 'E') {
                setWallV(r, c, 0);
            }

            setVisited(chosen.r, chosen.c);
            active[activeCount++] = (uint16_t)chosen.r * _size + chosen.c;
        } else {
            // Remove cell at idx (swap with back)
            active[idx] = active[activeCount - 1];
            activeCount--;
        }
    }

    solvePath();
}

void MazeGen::solvePath() {
    uint16_t totalCells = (uint16_t)_size * _size;
    uint16_t parent[1600];
    for (uint16_t i = 0; i < totalCells; i++) parent[i] = 0xFFFF;

    uint8_t seen[200] = {0};
    auto isSeen = [&](uint8_t r, uint8_t c) -> bool {
        uint16_t idx = (uint16_t)r * _size + c;
        return (seen[idx >> 3] >> (idx & 7)) & 1;
    };
    auto setSeen = [&](uint8_t r, uint8_t c) {
        uint16_t idx = (uint16_t)r * _size + c;
        seen[idx >> 3] |= (1 << (idx & 7));
    };

    uint16_t queue[1600];
    uint16_t head = 0;
    uint16_t tail = 0;

    queue[tail++] = 0;
    setSeen(0, 0);

    uint16_t targetCell = totalCells - 1;
    while (head < tail) {
        uint16_t cell = queue[head++];
        if (cell == targetCell) break;

        uint8_t r = (uint8_t)(cell / _size);
        uint8_t c = (uint8_t)(cell % _size);

        // North
        if (r > 0 && getWallH(r - 1, c) == 0 && !isSeen(r - 1, c)) {
            setSeen(r - 1, c);
            parent[(uint16_t)(r - 1) * _size + c] = cell;
            queue[tail++] = (uint16_t)(r - 1) * _size + c;
        }
        // South
        if (r < _size - 1 && getWallH(r, c) == 0 && !isSeen(r + 1, c)) {
            setSeen(r + 1, c);
            parent[(uint16_t)(r + 1) * _size + c] = cell;
            queue[tail++] = (uint16_t)(r + 1) * _size + c;
        }
        // West
        if (c > 0 && getWallV(r, c - 1) == 0 && !isSeen(r, c - 1)) {
            setSeen(r, c - 1);
            parent[(uint16_t)r * _size + (c - 1)] = cell;
            queue[tail++] = (uint16_t)r * _size + (c - 1);
        }
        // East
        if (c < _size - 1 && getWallV(r, c) == 0 && !isSeen(r, c + 1)) {
            setSeen(r, c + 1);
            parent[(uint16_t)r * _size + (c + 1)] = cell;
            queue[tail++] = (uint16_t)r * _size + (c + 1);
        }
    }

    // Trace back path from target to 0
    uint16_t pathCells[1600];
    uint16_t pathLen = 0;
    uint16_t cur = targetCell;
    while (cur != 0xFFFF) {
        pathCells[pathLen++] = cur;
        if (cur == 0) break;
        cur = parent[cur];
    }

    // Reverse path so it goes from start to end
    for (uint16_t i = 0; i < pathLen / 2; i++) {
        uint16_t tmp = pathCells[i];
        pathCells[i] = pathCells[pathLen - 1 - i];
        pathCells[pathLen - 1 - i] = tmp;
    }

    // Convert into aggregated cardinal direction steps
    _solutionMoveCount = 0;
    for (uint16_t i = 0; i < pathLen - 1; i++) {
        uint8_t r1 = (uint8_t)(pathCells[i] / _size);
        uint8_t c1 = (uint8_t)(pathCells[i] % _size);
        uint8_t r2 = (uint8_t)(pathCells[i + 1] / _size);
        uint8_t c2 = (uint8_t)(pathCells[i + 1] % _size);

        char d;
        if (r2 == r1 + 1) d = 'S';
        else if (r2 == r1 - 1) d = 'N';
        else if (c2 == c1 + 1) d = 'E';
        else d = 'W';

        if (_solutionMoveCount > 0 && _solutionMoves[_solutionMoveCount - 1].dir == d) {
            _solutionMoves[_solutionMoveCount - 1].steps++;
        } else if (_solutionMoveCount < 300) {
            _solutionMoves[_solutionMoveCount++] = { d, 1 };
        }
    }
}

void MazeGen::printToReceipt(EscPosPrinter& printer, MazeDifficulty diff) {
    const char* indent = "      ";

    if (_size <= 12) {
        printer.print(indent);
        printer.print("+   ");
        for (uint8_t c = 1; c < _size; c++) printer.print("+---");
        printer.println("+");

        for (uint8_t r = 0; r < _size; r++) {
            printer.print(indent);
            printer.print("|");
            for (uint8_t c = 0; c < _size; c++) {
                printer.print("   ");
                if (c < _size - 1) {
                    printer.print(getWallV(r, c) ? "|" : " ");
                } else {
                    printer.print("|");
                }
            }
            printer.println("");

            printer.print(indent);
            if (r < _size - 1) {
                printer.print("+");
                for (uint8_t c = 0; c < _size; c++) {
                    printer.print(getWallH(r, c) ? "---" : "   ");
                    printer.print("+");
                }
                printer.println("");
            } else {
                for (uint8_t c = 0; c < _size - 1; c++) printer.print("+---");
                printer.print("+   ");
                printer.println("+");
            }
        }
    } else {
        printer.print(indent);
        printer.print("+ ");
        for (uint8_t c = 1; c < _size; c++) printer.print("+-");
        printer.println("+");

        for (uint8_t r = 0; r < _size; r++) {
            printer.print(indent);
            printer.print("|");
            for (uint8_t c = 0; c < _size; c++) {
                printer.print(" ");
                if (c < _size - 1) {
                    printer.print(getWallV(r, c) ? "|" : " ");
                } else {
                    printer.print("|");
                }
            }
            printer.println("");

            printer.print(indent);
            if (r < _size - 1) {
                printer.print("+");
                for (uint8_t c = 0; c < _size; c++) {
                    printer.print(getWallH(r, c) ? "-" : " ");
                    printer.print("+");
                }
                printer.println("");
            } else {
                for (uint8_t c = 0; c < _size - 1; c++) printer.print("+-");
                printer.print("+ ");
                printer.println("+");
            }
        }
    }
}

bool MazeGen::printRasterToReceipt(EscPosPrinter& printer, MazeDifficulty diff) {
    ThermalCanvas canvas;
    if (!canvas.begin(576)) {
        return false;
    }
    canvas.clear(0);

    const int16_t boardSize = 480;
    const int16_t leftMargin = (canvas.getWidth() - boardSize) / 2; // 48
    const int16_t topMargin = (576 - boardSize) / 2;               // 48
    const uint8_t outerT = 4;
    const uint8_t wallT = _wallThickness;
    const uint8_t halfT = wallT / 2;

    // 1. Inner Walls (strictly clamped to board boundaries to prevent frame protrusion)
    // Horizontal walls between row r and r+1
    for (uint8_t r = 0; r < _size - 1; r++) {
        int16_t wy = topMargin + (r + 1) * _cellSize - halfT;
        for (uint8_t c = 0; c < _size; c++) {
            if (getWallH(r, c)) {
                int16_t wxStart = max(leftMargin, (int16_t)(leftMargin + c * _cellSize - halfT));
                int16_t wxEnd = min((int16_t)(leftMargin + boardSize), (int16_t)(leftMargin + (c + 1) * _cellSize + halfT + (_wallThickness % 2)));
                canvas.drawHLine(wxStart, wy, wxEnd - wxStart, wallT, 1);
            }
        }
    }

    // Vertical walls between col c and c+1
    for (uint8_t r = 0; r < _size; r++) {
        int16_t wyStart = max(topMargin, (int16_t)(topMargin + r * _cellSize - halfT));
        int16_t wyEnd = min((int16_t)(topMargin + boardSize), (int16_t)(topMargin + (r + 1) * _cellSize + halfT + (_wallThickness % 2)));
        for (uint8_t c = 0; c < _size - 1; c++) {
            if (getWallV(r, c)) {
                int16_t wx = leftMargin + (c + 1) * _cellSize - halfT;
                canvas.drawVLine(wx, wyStart, wyEnd - wyStart, wallT, 1);
            }
        }
    }

    // 2. Outer Frame (thickness 4, rendered over inner walls for clean single-frame boundaries)
    // Top wall: open at cell 0
    canvas.drawHLine(leftMargin + _cellSize, topMargin, boardSize - _cellSize, outerT, 1);
    // Left wall: solid
    canvas.drawVLine(leftMargin, topMargin, boardSize, outerT, 1);
    // Right wall: solid
    canvas.drawVLine(leftMargin + boardSize - outerT, topMargin, boardSize, outerT, 1);
    // Bottom wall: open at cell n-1
    canvas.drawHLine(leftMargin, topMargin + boardSize - outerT, boardSize - _cellSize, outerT, 1);

    // 3. Badges "IN" and "OUT"
    int16_t inCx = leftMargin + _cellSize / 2;
    int16_t inTx = inCx - 11;
    int16_t inTy = 24;
    canvas.drawText(inTx, inTy, "IN", 2, 1);

    int16_t outCx = leftMargin + boardSize - _cellSize / 2;
    int16_t outTx = outCx - 17;
    int16_t outTy = topMargin + boardSize + 10;
    canvas.drawText(outTx, outTy, "OUT", 2, 1);

    bool res = canvas.printTo(printer);
    canvas.end();
    return res;
}
