#!/usr/bin/env python3
"""
Generates canonical server/data/towers_dataset.json containing 100 verified
puzzles each for easy (4x4), medium (5x5), and hard (6x6).

Uses a compiled C++ backtracking solver to ensure:
- 100% mathematical uniqueness (count_solutions == 1)
- Deductive opening anchor presence (clue of 1 or N)
- Pure exterior clues only
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_JSON = ROOT_DIR / "server" / "data" / "towers_dataset.json"

CPP_SOURCE = r"""#include <iostream>
#include <vector>
#include <array>
#include <numeric>
#include <algorithm>
#include <random>
#include <chrono>
#include <sstream>

using namespace std;

struct Clues {
    vector<int> top;
    vector<int> bottom;
    vector<int> left;
    vector<int> right;
};

int count_vis(const int* arr, int n) {
    int m = 0, c = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > m) { c++; m = arr[i]; }
    }
    return c;
}

int count_vis_rev(const int* arr, int n) {
    int m = 0, c = 0;
    for (int i = n - 1; i >= 0; i--) {
        if (arr[i] > m) { c++; m = arr[i]; }
    }
    return c;
}

int solutions = 0;
int grid[6][6];
bool col_used[6][7];

void solve(int r, int N, const Clues& clues, const vector<vector<int>>& perms, const vector<vector<int>>& row_cands) {
    if (solutions >= 2) return;
    if (r == N) {
        for (int c = 0; c < N; c++) {
            if (clues.top[c] > 0) {
                int col_arr[6];
                for (int i = 0; i < N; i++) col_arr[i] = grid[i][c];
                if (count_vis(col_arr, N) != clues.top[c]) return;
            }
            if (clues.bottom[c] > 0) {
                int col_arr[6];
                for (int i = 0; i < N; i++) col_arr[i] = grid[N - 1 - i][c];
                if (count_vis(col_arr, N) != clues.bottom[c]) return;
            }
        }
        solutions++;
        return;
    }

    for (int pid : row_cands[r]) {
        const auto& p = perms[pid];
        bool ok = true;
        for (int c = 0; c < N; c++) {
            if (col_used[c][p[c]]) { ok = false; break; }
        }
        if (!ok) continue;

        for (int c = 0; c < N; c++) {
            if (clues.top[c] > 0) {
                int prefix[6];
                int max_val = 0;
                int v = 0;
                for (int i = 0; i < r; i++) {
                    prefix[i] = grid[i][c];
                    if (prefix[i] > max_val) { v++; max_val = prefix[i]; }
                }
                if (p[c] > max_val) { v++; max_val = p[c]; }
                if (v > clues.top[c]) { ok = false; break; }
                // Max additional visible can only be (N - max_val)
                int max_possible = v + (N - max_val);
                if (max_possible < clues.top[c]) { ok = false; break; }
            }
        }
        if (!ok) continue;

        for (int c = 0; c < N; c++) {
            grid[r][c] = p[c];
            col_used[c][p[c]] = true;
        }

        solve(r + 1, N, clues, perms, row_cands);

        for (int c = 0; c < N; c++) {
            col_used[c][p[c]] = false;
        }
    }
}

int count_solutions(int N, const Clues& clues, const vector<vector<int>>& perms) {
    vector<vector<int>> row_cands(N);
    for (int r = 0; r < N; r++) {
        for (size_t i = 0; i < perms.size(); i++) {
            const auto& p = perms[i];
            if (clues.left[r] > 0 && count_vis(p.data(), N) != clues.left[r]) continue;
            if (clues.right[r] > 0 && count_vis_rev(p.data(), N) != clues.right[r]) continue;
            row_cands[r].push_back(i);
        }
    }
    solutions = 0;
    for (int c = 0; c < N; c++)
        for (int v = 0; v <= N; v++) col_used[c][v] = false;
    solve(0, N, clues, perms, row_cands);
    return solutions;
}

bool has_anchor(int N, const Clues& clues) {
    for (int v : clues.top) if (v == 1 || v == N) return true;
    for (int v : clues.bottom) if (v == 1 || v == N) return true;
    for (int v : clues.left) if (v == 1 || v == N) return true;
    for (int v : clues.right) if (v == 1 || v == N) return true;
    return false;
}

int main() {
    mt19937 rng(42);
    cout << "{" << endl;

    vector<pair<string, int>> tiers = {{"easy", 4}, {"medium", 5}, {"hard", 6}};
    for (size_t t_idx = 0; t_idx < tiers.size(); t_idx++) {
        string tier_name = tiers[t_idx].first;
        int N = tiers[t_idx].second;
        int target_clues = (N == 4) ? 9 : (N == 5 ? 12 : 15);

        vector<int> base(N);
        iota(base.begin(), base.end(), 1);
        vector<vector<int>> perms;
        do {
            perms.push_back(base);
        } while (next_permutation(base.begin(), base.end()));

        cout << "  \"" << tier_name << "\": [" << endl;

        int generated_count = 0;
        while (generated_count < 100) {
            vector<vector<int>> sol(N);
            while (true) {
                vector<int> p_order(perms.size());
                iota(p_order.begin(), p_order.end(), 0);
                shuffle(p_order.begin(), p_order.end(), rng);
                bool used[6][7] = {false};
                bool possible = true;
                for (int r = 0; r < N; r++) {
                    bool found = false;
                    for (int pid : p_order) {
                        const auto& p = perms[pid];
                        bool ok = true;
                        for (int c = 0; c < N; c++) {
                            if (used[c][p[c]]) { ok = false; break; }
                        }
                        if (ok) {
                            sol[r] = p;
                            for (int c = 0; c < N; c++) used[c][p[c]] = true;
                            found = true;
                            break;
                        }
                    }
                    if (!found) { possible = false; break; }
                }
                if (possible) break;
            }

            Clues clues;
            clues.top.resize(N);
            clues.bottom.resize(N);
            clues.left.resize(N);
            clues.right.resize(N);

            for (int c = 0; c < N; c++) {
                int col_arr[6];
                for (int r = 0; r < N; r++) col_arr[r] = sol[r][c];
                clues.top[c] = count_vis(col_arr, N);
                clues.bottom[c] = count_vis_rev(col_arr, N);
            }
            for (int r = 0; r < N; r++) {
                clues.left[r] = count_vis(sol[r].data(), N);
                clues.right[r] = count_vis_rev(sol[r].data(), N);
            }

            // Verify full clues give unique solution
            if (count_solutions(N, clues, perms) != 1) continue;

            struct Pos { int side, idx; };
            vector<Pos> positions;
            for (int i = 0; i < N; i++) {
                positions.push_back({0, i});
                positions.push_back({1, i});
                positions.push_back({2, i});
                positions.push_back({3, i});
            }
            shuffle(positions.begin(), positions.end(), rng);

            int current_clues = 4 * N;
            for (const auto& pos : positions) {
                int* val_ptr = nullptr;
                if (pos.side == 0) val_ptr = &clues.top[pos.idx];
                else if (pos.side == 1) val_ptr = &clues.bottom[pos.idx];
                else if (pos.side == 2) val_ptr = &clues.left[pos.idx];
                else val_ptr = &clues.right[pos.idx];

                int old_val = *val_ptr;
                *val_ptr = 0;

                if (!has_anchor(N, clues)) {
                    *val_ptr = old_val;
                    continue;
                }

                if (count_solutions(N, clues, perms) != 1) {
                    *val_ptr = old_val;
                    continue;
                }

                current_clues--;
                if (current_clues <= target_clues) break;
            }

            // Final safety check: must be strictly uniquely solvable with anchor
            if (count_solutions(N, clues, perms) != 1 || !has_anchor(N, clues)) continue;

            // Output JSON object
            cout << "    {" << endl;
            cout << "      \"size\": " << N << "," << endl;
            cout << "      \"clues\": {" << endl;
            cout << "        \"top\": [";
            for (int i = 0; i < N; i++) cout << clues.top[i] << (i + 1 < N ? ", " : "");
            cout << "]," << endl;
            cout << "        \"bottom\": [";
            for (int i = 0; i < N; i++) cout << clues.bottom[i] << (i + 1 < N ? ", " : "");
            cout << "]," << endl;
            cout << "        \"left\": [";
            for (int i = 0; i < N; i++) cout << clues.left[i] << (i + 1 < N ? ", " : "");
            cout << "]," << endl;
            cout << "        \"right\": [";
            for (int i = 0; i < N; i++) cout << clues.right[i] << (i + 1 < N ? ", " : "");
            cout << "]" << endl;
            cout << "      }," << endl;
            cout << "      \"solution\": [" << endl;
            for (int r = 0; r < N; r++) {
                cout << "        [";
                for (int c = 0; c < N; c++) cout << sol[r][c] << (c + 1 < N ? ", " : "");
                cout << "]" << (r + 1 < N ? "," : "") << endl;
            }
            cout << "      ]" << endl;
            cout << "    }" << (generated_count + 1 < 100 ? "," : "") << endl;
            generated_count++;
        }

        cout << "  ]" << (t_idx + 1 < tiers.size() ? "," : "") << endl;
    }
    cout << "}" << endl;
    return 0;
}
"""

def main():
    print("Compiling Towers dataset generator in C++...")
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = Path(tmpdir) / "gen.cpp"
        bin_path = Path(tmpdir) / "gen"
        src_path.write_text(CPP_SOURCE, encoding="utf-8")

        subprocess.check_call([
            "clang++", "-O3", "-std=c++17", str(src_path), "-o", str(bin_path)
        ])

        print(f"Generating 300 base puzzles (Easy 4x4, Medium 5x5, Hard 6x6)...")
        res = subprocess.check_output([str(bin_path)], text=True)

        # Validate JSON parses correctly
        data = json.loads(res)
        assert len(data["easy"]) == 100
        assert len(data["medium"]) == 100
        assert len(data["hard"]) == 100

        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            f.write(res)

        print(f"Wrote canonical dataset to {OUTPUT_JSON} (total {len(data['easy']) + len(data['medium']) + len(data['hard'])} puzzles).")

if __name__ == "__main__":
    main()
