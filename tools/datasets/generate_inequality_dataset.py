#!/usr/bin/env python3
"""
Generates canonical server/data/inequality_dataset.json containing 100 verified
puzzles each for easy (4x4), medium (4x4), hard (5x5), and extreme (5x5).

Uses a compiled C++ backtracking solver and generator to guarantee:
- 100% mathematical uniqueness (count_solutions == 1)
- Balanced givens and inequality edges
- Opening deductive anchors
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_JSON = ROOT_DIR / "server" / "data" / "inequality_dataset.json"

CPP_SOURCE = r"""#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <random>
#include <chrono>
#include <sstream>

using namespace std;

int N;
int grid[6][6];
int solutions = 0;

bool is_valid(int r, int c, int val, const vector<vector<int>>& edges_h, const vector<vector<int>>& edges_v) {
    for (int i = 0; i < N; i++) {
        if (grid[r][i] == val || grid[i][c] == val) return false;
    }
    if (c > 0 && grid[r][c - 1] > 0) {
        int op = edges_h[r][c - 1];
        if (op == 1 && !(grid[r][c - 1] < val)) return false;
        if (op == 2 && !(grid[r][c - 1] > val)) return false;
    }
    if (c + 1 < N && grid[r][c + 1] > 0) {
        int op = edges_h[r][c];
        if (op == 1 && !(val < grid[r][c + 1])) return false;
        if (op == 2 && !(val > grid[r][c + 1])) return false;
    }
    if (r > 0 && grid[r - 1][c] > 0) {
        int op = edges_v[r - 1][c];
        if (op == 1 && !(grid[r - 1][c] < val)) return false;
        if (op == 2 && !(grid[r - 1][c] > val)) return false;
    }
    if (r + 1 < N && grid[r + 1][c] > 0) {
        int op = edges_v[r][c];
        if (op == 1 && !(val < grid[r + 1][c])) return false;
        if (op == 2 && !(val > grid[r + 1][c])) return false;
    }
    return true;
}

void solve(const vector<vector<int>>& edges_h, const vector<vector<int>>& edges_v) {
    if (solutions >= 2) return;
    int best_r = -1, best_c = -1;
    int min_cands = N + 1;
    int best_mask = 0;

    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            if (grid[r][c] == 0) {
                int mask = 0;
                int count = 0;
                for (int v = 1; v <= N; v++) {
                    if (is_valid(r, c, v, edges_h, edges_v)) {
                        mask |= (1 << v);
                        count++;
                    }
                }
                if (count == 0) return;
                if (count < min_cands) {
                    min_cands = count;
                    best_mask = mask;
                    best_r = r;
                    best_c = c;
                    if (count == 1) goto found_best;
                }
            }
        }
    }
found_best:
    if (best_r == -1) {
        solutions++;
        return;
    }
    for (int v = 1; v <= N; v++) {
        if (best_mask & (1 << v)) {
            grid[best_r][best_c] = v;
            solve(edges_h, edges_v);
            grid[best_r][best_c] = 0;
            if (solutions >= 2) return;
        }
    }
}

int count_solutions(const vector<vector<int>>& edges_h, const vector<vector<int>>& edges_v) {
    solutions = 0;
    solve(edges_h, edges_v);
    return solutions;
}

bool fill_latin(int r, int c, mt19937& rng) {
    if (r == N) return true;
    int nr = (c + 1 == N) ? r + 1 : r;
    int nc = (c + 1 == N) ? 0 : c + 1;
    vector<int> nums(N);
    iota(nums.begin(), nums.end(), 1);
    shuffle(nums.begin(), nums.end(), rng);
    for (int v : nums) {
        bool ok = true;
        for (int i = 0; i < N; i++) {
            if (grid[r][i] == v || grid[i][c] == v) { ok = false; break; }
        }
        if (ok) {
            grid[r][c] = v;
            if (fill_latin(nr, nc, rng)) return true;
            grid[r][c] = 0;
        }
    }
    return false;
}

struct Edge { char type; int r, c; };

int main() {
    mt19937 rng(1337);
    cout << "{" << endl;

    struct TierSpec {
        string name;
        int N;
        int min_givens;
        int max_givens;
        int min_edges;
        int max_edges;
    };
    vector<TierSpec> tiers = {
        {"easy", 4, 5, 7, 6, 8},
        {"medium", 4, 3, 4, 5, 7},
        {"hard", 5, 4, 6, 8, 11},
        {"extreme", 5, 2, 3, 6, 9}
    };
    for (size_t t_idx = 0; t_idx < tiers.size(); t_idx++) {
        const auto& spec = tiers[t_idx];
        string tier_name = spec.name;
        N = spec.N;

        int min_givens = spec.min_givens;
        int max_givens = spec.max_givens;
        int min_edges = spec.min_edges;
        int max_edges = spec.max_edges;

        cerr << "Generating tier: " << tier_name << " (" << N << "x" << N << ")..." << endl;
        cout << "  \"" << tier_name << "\": [" << endl;

        int count = 0;
        while (count < 100) {
            for (int r = 0; r < N; r++) for (int c = 0; c < N; c++) grid[r][c] = 0;
            fill_latin(0, 0, rng);
            int sol[6][6];
            for (int r = 0; r < N; r++) for (int c = 0; c < N; c++) sol[r][c] = grid[r][c];

            vector<vector<int>> edges_h(N, vector<int>(N - 1, 0));
            vector<vector<int>> edges_v(N - 1, vector<int>(N, 0));
            vector<Edge> all_edges;

            for (int r = 0; r < N; r++) {
                for (int c = 0; c < N - 1; c++) {
                    edges_h[r][c] = (sol[r][c] < sol[r][c + 1]) ? 1 : 2;
                    all_edges.push_back({'h', r, c});
                }
            }
            for (int r = 0; r < N - 1; r++) {
                for (int c = 0; c < N; c++) {
                    edges_v[r][c] = (sol[r][c] < sol[r + 1][c]) ? 1 : 2;
                    all_edges.push_back({'v', r, c});
                }
            }

            shuffle(all_edges.begin(), all_edges.end(), rng);
            int target_edges = min_edges + (rng() % (max_edges - min_edges + 1));
            for (int r = 0; r < N; r++) for (int c = 0; c < N - 1; c++) edges_h[r][c] = 0;
            for (int r = 0; r < N - 1; r++) for (int c = 0; c < N; c++) edges_v[r][c] = 0;

            for (int i = 0; i < target_edges; i++) {
                const auto& e = all_edges[i];
                if (e.type == 'h') edges_h[e.r][e.c] = (sol[e.r][e.c] < sol[e.r][e.c + 1]) ? 1 : 2;
                else edges_v[e.r][e.c] = (sol[e.r][e.c] < sol[e.r + 1][e.c]) ? 1 : 2;
            }

            // Prune givens down
            vector<pair<int, int>> cells;
            for (int r = 0; r < N; r++) for (int c = 0; c < N; c++) cells.push_back({r, c});
            shuffle(cells.begin(), cells.end(), rng);

            int target_givens = min_givens + (rng() % (max_givens - min_givens + 1));
            int curr_givens = N * N;

            for (auto& cell : cells) {
                if (curr_givens <= target_givens) break;
                int r = cell.first, c = cell.second;
                grid[r][c] = 0;
                if (count_solutions(edges_h, edges_v) == 1) {
                    curr_givens--;
                } else {
                    grid[r][c] = sol[r][c];
                }
            }

            if (curr_givens >= min_givens && curr_givens <= max_givens && count_solutions(edges_h, edges_v) == 1) {
                cout << "    {" << endl;
                cout << "      \"size\": " << N << "," << endl;
                cout << "      \"givens\": [";
                bool first_g = true;
                for (int r = 0; r < N; r++) {
                    for (int c = 0; c < N; c++) {
                        if (grid[r][c] > 0) {
                            if (!first_g) cout << ", ";
                            cout << "[" << r << ", " << c << ", " << grid[r][c] << "]";
                            first_g = false;
                        }
                    }
                }
                cout << "]," << endl;

                cout << "      \"edges_h\": [" << endl;
                for (int r = 0; r < N; r++) {
                    cout << "        [";
                    for (int c = 0; c < N - 1; c++) {
                        cout << edges_h[r][c] << (c + 1 < N - 1 ? ", " : "");
                    }
                    cout << "]" << (r + 1 < N ? "," : "") << endl;
                }
                cout << "      ]," << endl;

                cout << "      \"edges_v\": [" << endl;
                for (int r = 0; r < N - 1; r++) {
                    cout << "        [";
                    for (int c = 0; c < N; c++) {
                        cout << edges_v[r][c] << (c + 1 < N ? ", " : "");
                    }
                    cout << "]" << (r + 1 < N - 1 ? "," : "") << endl;
                }
                cout << "      ]," << endl;

                cout << "      \"solution\": [" << endl;
                for (int r = 0; r < N; r++) {
                    cout << "        [";
                    for (int c = 0; c < N; c++) {
                        cout << sol[r][c] << (c + 1 < N ? ", " : "");
                    }
                    cout << "]" << (r + 1 < N ? "," : "") << endl;
                }
                cout << "      ]" << endl;

                cout << "    }" << (count + 1 < 100 ? "," : "") << endl;
                count++;
            }
        }
        cout << "  ]" << (t_idx + 1 < tiers.size() ? "," : "") << endl;
    }
    cout << "}" << endl;
    return 0;
}
"""

def main():
    print("Compiling Inequality dataset generator in C++...")
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "generate_inequality.cpp")
        bin_path = os.path.join(tmpdir, "generate_inequality")

        with open(src_path, "w") as f:
            f.write(CPP_SOURCE)

        cmd_compile = ["g++", "-O3", "-std=c++17", src_path, "-o", bin_path]
        subprocess.check_call(cmd_compile)

        print("Executing generator (producing 400 unique Inequality puzzles across 4 tiers)...")
        raw_output = subprocess.check_output([bin_path], encoding="utf-8")

        data = json.loads(raw_output)
        print(f"Loaded generated JSON: {len(data['easy'])} easy, {len(data['medium'])} medium, {len(data['hard'])} hard, {len(data['extreme'])} extreme.")

        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"Successfully generated and wrote {OUTPUT_JSON}!")

if __name__ == "__main__":
    main()
