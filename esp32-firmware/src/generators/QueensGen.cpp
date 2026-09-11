#include "QueensGen.h"
#include "../printer/EscPosPrinter.h"
#include <queue>
#include <algorithm>
#include <cmath>

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
    std::vector<StarPos> frontiers[MAX_SIZE];
    const int8_t dr[] = {0, 0, 1, -1};
    const int8_t dc[] = {1, -1, 0, 0};

    if (_starsPerUnit == 1) {
        for (size_t i = 0; i < _stars.size(); i++) {
            _regions[_stars[i].row][_stars[i].col] = (int8_t)i;
            frontiers[i].push_back(_stars[i]);
        }
    } else {
        // 2-Star mode: pair the 2*_size stars into _size pairs
        bool pairedSuccess = false;
        int8_t tempGrid[MAX_SIZE][MAX_SIZE];

        for (int attempt = 0; attempt < 50 && !pairedSuccess; attempt++) {
            memset(tempGrid, -1, sizeof(tempGrid));
            std::vector<StarPos> unpaired = _stars;
            // Shuffle unpaired stars
            for (int i = (int)unpaired.size() - 1; i > 0; i--) {
                int j = random(i + 1);
                std::swap(unpaired[i], unpaired[j]);
            }

            int pairsCount = 0;
            bool allPaired = true;

            while (!unpaired.empty()) {
                StarPos s1 = unpaired.front();
                unpaired.erase(unpaired.begin());

                // Sort candidates by Manhattan distance
                std::sort(unpaired.begin(), unpaired.end(), [s1](const StarPos& a, const StarPos& b) {
                    return (abs((int)a.row - (int)s1.row) + abs((int)a.col - (int)s1.col)) <
                           (abs((int)b.row - (int)s1.row) + abs((int)b.col - (int)s1.col));
                });

                int foundIdx = -1;
                std::vector<StarPos> foundPath;

                for (size_t ci = 0; ci < unpaired.size(); ci++) {
                    StarPos s2 = unpaired[ci];
                    // BFS corridor from s1 to s2
                    std::queue<std::pair<StarPos, std::vector<StarPos>>> q;
                    bool visited[MAX_SIZE][MAX_SIZE] = {false};
                    q.push({s1, {s1}});
                    visited[s1.row][s1.col] = true;

                    while (!q.empty()) {
                        auto curr = q.front();
                        q.pop();
                        StarPos cp = curr.first;
                        if (cp.row == s2.row && cp.col == s2.col) {
                            foundPath = curr.second;
                            break;
                        }
                        for (int d = 0; d < 4; d++) {
                            int nr = cp.row + dr[d];
                            int nc = cp.col + dc[d];
                            if (nr >= 0 && nr < _size && nc >= 0 && nc < _size && !visited[nr][nc]) {
                                bool isStar = false;
                                for (const auto& st : _stars) {
                                    if (st.row == nr && st.col == nc) { isStar = true; break; }
                                }
                                if ((nr == s2.row && nc == s2.col) || (!isStar && tempGrid[nr][nc] == -1)) {
                                    visited[nr][nc] = true;
                                    std::vector<StarPos> np = curr.second;
                                    np.push_back({(uint8_t)nr, (uint8_t)nc});
                                    q.push({{(uint8_t)nr, (uint8_t)nc}, np});
                                }
                            }
                        }
                    }

                    if (!foundPath.empty()) {
                        foundIdx = (int)ci;
                        break;
                    }
                }

                if (foundIdx != -1) {
                    unpaired.erase(unpaired.begin() + foundIdx);
                    int8_t regId = (int8_t)pairsCount++;
                    for (const auto& p : foundPath) {
                        tempGrid[p.row][p.col] = regId;
                    }
                } else {
                    allPaired = false;
                    break;
                }
            }

            if (allPaired && pairsCount == _size) {
                pairedSuccess = true;
                for (uint8_t r = 0; r < _size; r++) {
                    for (uint8_t c = 0; c < _size; c++) {
                        _regions[r][c] = tempGrid[r][c];
                        if (_regions[r][c] != -1) {
                            frontiers[_regions[r][c]].push_back({r, c});
                        }
                    }
                }
            }
        }

        if (!pairedSuccess) {
            for (size_t i = 0; i < _stars.size(); i++) {
                int8_t reg = (int8_t)(i % _size);
                _regions[_stars[i].row][_stars[i].col] = reg;
                frontiers[reg].push_back(_stars[i]);
            }
        }
    }

    // Multi-source BFS growth
    int unassigned = 0;
    for (uint8_t r = 0; r < _size; r++) {
        for (uint8_t c = 0; c < _size; c++) {
            if (_regions[r][c] == -1) unassigned++;
        }
    }

    std::vector<uint8_t> activeRegions(_size);
    for (uint8_t i = 0; i < _size; i++) activeRegions[i] = i;

    while (unassigned > 0 && !activeRegions.empty()) {
        int randIdx = random(activeRegions.size());
        uint8_t reg = activeRegions[randIdx];

        std::vector<StarPos> candidates;
        for (const auto& cell : frontiers[reg]) {
            for (int d = 0; d < 4; d++) {
                int nr = cell.row + dr[d];
                int nc = cell.col + dc[d];
                if (nr >= 0 && nr < _size && nc >= 0 && nc < _size && _regions[nr][nc] == -1) {
                    candidates.push_back({(uint8_t)nr, (uint8_t)nc});
                }
            }
        }

        if (candidates.empty()) {
            activeRegions.erase(activeRegions.begin() + randIdx);
            continue;
        }

        StarPos chosen = candidates[random(candidates.size())];
        _regions[chosen.row][chosen.col] = (int8_t)reg;
        frontiers[reg].push_back(chosen);
        unassigned--;
    }

    // Strict connectivity safety fallback: attach to adjacent region
    if (unassigned > 0) {
        bool progress = true;
        while (unassigned > 0 && progress) {
            progress = false;
            for (uint8_t r = 0; r < _size; r++) {
                for (uint8_t c = 0; c < _size; c++) {
                    if (_regions[r][c] == -1) {
                        for (int d = 0; d < 4; d++) {
                            int nr = r + dr[d];
                            int nc = c + dc[d];
                            if (nr >= 0 && nr < _size && nc >= 0 && nc < _size && _regions[nr][nc] != -1) {
                                _regions[r][c] = _regions[nr][nc];
                                unassigned--;
                                progress = true;
                                break;
                            }
                        }
                    }
                }
            }
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
    } else if (difficulty == QUEENS_MASTER) {
        _size = 10;
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
