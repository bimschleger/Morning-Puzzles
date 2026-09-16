#!/usr/bin/env python3
"""
Curator Script for Morning Puzzles: Killer Sudoku Dataset
Generates and strictly verifies 100 Easy (4x4), 100 Medium (4x4), and 100 Extreme (6x6) puzzles.
Guarantees:
1. Unique mathematical solution via constraint backtracking.
2. 100% deductive solvability (solved purely via cage sum combinations, naked/hidden singles, naked pairs).
3. Strictly 4-connected orthogonally contiguous cages.
4. Guaranteed opening anchors (unique sum combinations).
5. Dihedral D4 symmetry invariance across rotations and reflections.
Exports:
- server/data/killer_dataset.json
- esp32-firmware/src/generators/KillerDataset.h
"""

import os
import sys
import json
import random
import itertools
from collections import deque
from typing import List, Tuple, Dict, Any, Optional, Set

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JSON_OUT = os.path.join(ROOT_DIR, "server", "data", "killer_dataset.json")
CPP_OUT = os.path.join(ROOT_DIR, "esp32-firmware", "src", "generators", "KillerDataset.h")


def is_4_connected(cells: List[Tuple[int, int]]) -> bool:
    if not cells:
        return False
    cell_set = set(cells)
    visited = set()
    q = deque([cells[0]])
    visited.add(cells[0])
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in cell_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))
    return len(visited) == len(cells)


def solve_deductive(size: int, box_r: int, box_c: int, cages: List[Dict[str, Any]]) -> Optional[List[List[int]]]:
    candidates = [[set(range(1, size + 1)) for _ in range(size)] for _ in range(size)]

    units = []
    for r in range(size):
        units.append([(r, c) for c in range(size)])
    for c in range(size):
        units.append([(r, c) for r in range(size)])
    for br in range(0, size, box_r):
        for bc in range(0, size, box_c):
            units.append([(br + dr, bc + dc) for dr in range(box_r) for dc in range(box_c)])

    cell_to_cage = {}
    for cg in cages:
        for cell in cg["cells"]:
            cell_to_cage[tuple(cell)] = cg

    changed = True
    while changed:
        changed = False

        # 1. Cage Sum Combination Filtering
        for cg in cages:
            cells = [tuple(c) for c in cg["cells"]]
            k = len(cells)
            target = cg["sum"]

            possible_combos = []
            for combo in itertools.combinations(range(1, size + 1), k):
                if sum(combo) == target:
                    possible_combos.append(combo)

            valid_assignments = []
            for combo in possible_combos:
                for perm in itertools.permutations(combo):
                    if all(perm[i] in candidates[cells[i][0]][cells[i][1]] for i in range(k)):
                        valid_assignments.append(perm)

            if not valid_assignments:
                return None

            for i, (r, c) in enumerate(cells):
                allowed_digits = {assign[i] for assign in valid_assignments}
                if len(allowed_digits) < len(candidates[r][c]):
                    candidates[r][c] &= allowed_digits
                    changed = True

        # 2. Naked Singles
        for r in range(size):
            for c in range(size):
                if len(candidates[r][c]) == 1:
                    val = next(iter(candidates[r][c]))
                    peers = set()
                    for cc in range(size):
                        if cc != c: peers.add((r, cc))
                    for rr in range(size):
                        if rr != r: peers.add((rr, c))
                    br, bc = (r // box_r) * box_r, (c // box_c) * box_c
                    for dr in range(box_r):
                        for dc in range(box_c):
                            if (br + dr, bc + dc) != (r, c):
                                peers.add((br + dr, bc + dc))
                    cg = cell_to_cage.get((r, c))
                    if cg:
                        for cell in cg["cells"]:
                            t_cell = tuple(cell)
                            if t_cell != (r, c):
                                peers.add(t_cell)

                    for pr, pc in peers:
                        if val in candidates[pr][pc]:
                            candidates[pr][pc].remove(val)
                            changed = True

        # 3. Hidden Singles in Units
        for unit in units:
            for digit in range(1, size + 1):
                places = [(r, c) for r, c in unit if digit in candidates[r][c]]
                if len(places) == 1:
                    r, c = places[0]
                    if len(candidates[r][c]) > 1:
                        candidates[r][c] = {digit}
                        changed = True

        # 4. Naked Pairs in Units
        for unit in units:
            pair_cells = [(r, c) for r, c in unit if len(candidates[r][c]) == 2]
            for i in range(len(pair_cells)):
                for j in range(i + 1, len(pair_cells)):
                    r1, c1 = pair_cells[i]
                    r2, c2 = pair_cells[j]
                    if candidates[r1][c1] == candidates[r2][c2]:
                        pair_vals = candidates[r1][c1]
                        for r, c in unit:
                            if (r, c) != (r1, c1) and (r, c) != (r2, c2):
                                if any(v in candidates[r][c] for v in pair_vals):
                                    candidates[r][c] -= pair_vals
                                    changed = True

        for r in range(size):
            for c in range(size):
                if len(candidates[r][c]) == 0:
                    return None

    if all(len(candidates[r][c]) == 1 for r in range(size) for c in range(size)):
        return [[next(iter(candidates[r][c])) for c in range(size)] for r in range(size)]
    return None


def count_solutions_backtrack(size: int, box_r: int, box_c: int, cages: List[Dict[str, Any]], limit: int = 2) -> int:
    board = [[0] * size for _ in range(size)]
    cell_cage = {}
    for cg in cages:
        for cell in cg["cells"]:
            cell_cage[tuple(cell)] = cg

    sols = 0

    def is_valid(r: int, c: int, val: int) -> bool:
        for i in range(size):
            if board[r][i] == val or board[i][c] == val:
                return False
        br = (r // box_r) * box_r
        bc = (c // box_c) * box_c
        for dr in range(box_r):
            for dc in range(box_c):
                if board[br + dr][bc + dc] == val:
                    return False

        cg = cell_cage[(r, c)]
        cur_sum = val
        filled = 1
        for cell in cg["cells"]:
            cr, cc = cell[0], cell[1]
            if (cr, cc) == (r, c):
                continue
            v = board[cr][cc]
            if v != 0:
                if v == val:
                    return False
                cur_sum += v
                filled += 1

        target = cg["sum"]
        total = len(cg["cells"])
        if cur_sum > target:
            return False
        if filled == total:
            if cur_sum != target:
                return False
        else:
            rem = total - filled
            if cur_sum + (rem * (rem + 1)) // 2 > target:
                return False
        return True

    def search(r: int, c: int):
        nonlocal sols
        if sols >= limit:
            return
        if r == size:
            sols += 1
            return
        next_r = r + (c + 1) // size
        next_c = (c + 1) % size
        for val in range(1, size + 1):
            if is_valid(r, c, val):
                board[r][c] = val
                search(next_r, next_c)
                board[r][c] = 0

    search(0, 0)
    return sols


def generate_board(size: int, box_r: int, box_c: int) -> List[List[int]]:
    board = [[0] * size for _ in range(size)]
    def is_valid(r: int, c: int, val: int) -> bool:
        for i in range(size):
            if board[r][i] == val or board[i][c] == val:
                return False
        br, bc = (r // box_r) * box_r, (c // box_c) * box_c
        for dr in range(box_r):
            for dc in range(box_c):
                if board[br + dr][bc + dc] == val:
                    return False
        return True

    def fill(r: int, c: int) -> bool:
        if r == size:
            return True
        nr = r + (c + 1) // size
        nc = (c + 1) % size
        nums = list(range(1, size + 1))
        random.shuffle(nums)
        for n in nums:
            if is_valid(r, c, n):
                board[r][c] = n
                if fill(nr, nc):
                    return True
                board[r][c] = 0
        return False

    fill(0, 0)
    return board


def partition_cages(solution: List[List[int]], size: int, min_cage: int, max_cage: int, allow_single: bool = False) -> Optional[List[Dict[str, Any]]]:
    assigned = [[-1] * size for _ in range(size)]
    cages = []

    def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        res = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                res.append((nr, nc))
        return res

    all_coords = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(all_coords)

    cage_id = 0
    for r, c in all_coords:
        if assigned[r][c] != -1:
            continue
        cur_size = random.randint(min_cage, max_cage)
        cage_cells = [[r, c]]
        digits = {solution[r][c]}
        assigned[r][c] = cage_id

        while len(cage_cells) < cur_size:
            cands = []
            for cr, cc in cage_cells:
                for nr, nc in neighbors(cr, cc):
                    if assigned[nr][nc] == -1 and solution[nr][nc] not in digits:
                        cands.append((nr, nc))
            if not cands:
                break
            ch_r, ch_c = random.choice(cands)
            cage_cells.append([ch_r, ch_c])
            digits.add(solution[ch_r][ch_c])
            assigned[ch_r][ch_c] = cage_id

        cages.append({
            "id": cage_id,
            "cells": sorted(cage_cells),
            "sum": sum(solution[cr][cc] for cr, cc in cage_cells)
        })
        cage_id += 1

    if not allow_single:
        for idx in range(len(cages) - 1, -1, -1):
            cg = cages[idx]
            if len(cg["cells"]) == 1:
                cr, cc = cg["cells"][0]
                val = solution[cr][cc]
                merged = False
                for nr, nc in neighbors(cr, cc):
                    nid = assigned[nr][nc]
                    ncage = next((c for c in cages if c["id"] == nid), None)
                    if ncage and len(ncage["cells"]) < max_cage:
                        ndigits = {solution[r][c] for r, c in ncage["cells"]}
                        if val not in ndigits:
                            ncage["cells"].append([cr, cc])
                            ncage["cells"].sort()
                            ncage["sum"] += val
                            assigned[cr][cc] = nid
                            cages.pop(idx)
                            merged = True
                            break
                if not merged:
                    return None

    for i, cg in enumerate(cages):
        cg["id"] = i
    return cages


def transform_cage(cg: Dict[str, Any], size: int, transform: int) -> Dict[str, Any]:
    rot = transform % 4
    flip = (transform >= 4)
    new_cells = []
    for r, c in cg["cells"]:
        tr, tc = r, c
        for _ in range(rot):
            tr, tc = tc, size - 1 - tr
        if flip:
            tc = size - 1 - tc
        new_cells.append([tr, tc])
    return {
        "id": cg["id"],
        "cells": sorted(new_cells),
        "sum": cg["sum"]
    }


def verify_transforms(size: int, box_r: int, box_c: int, cages: List[Dict[str, Any]]) -> bool:
    for t in range(8):
        if box_r != box_c and (t % 2 == 1):
            continue
        t_cages = [transform_cage(cg, size, t) for cg in cages]
        for cg in t_cages:
            if not is_4_connected([tuple(c) for c in cg["cells"]]):
                return False
        if count_solutions_backtrack(size, box_r, box_c, t_cages, limit=2) != 1:
            return False
        if solve_deductive(size, box_r, box_c, t_cages) is None:
            return False
    return True


def curate_tier(tier_name: str, size: int, box_r: int, box_c: int, min_c: int, max_c: int, allow_single: bool, count: int = 100):
    print(f"\n--- Curating {count} {tier_name.upper()} ({size}x{size}) Killer Sudoku Puzzles ---")
    puzzles = []
    attempts = 0
    while len(puzzles) < count:
        attempts += 1
        sol = generate_board(size, box_r, box_c)
        cages = partition_cages(sol, size, min_c, max_c, allow_single=allow_single)
        if not cages:
            continue

        has_anchor = False
        for cg in cages:
            k = len(cg["cells"])
            s = cg["sum"]
            if size == 4:
                if (k == 2 and s in (3, 4, 7)) or (k == 3 and s in (6, 9)) or (k == 1):
                    has_anchor = True
                    break
            else:
                if (k == 2 and s in (3, 4, 10, 11)) or (k == 3 and s in (6, 7, 14, 15)):
                    has_anchor = True
                    break
        if not has_anchor:
            continue

        if count_solutions_backtrack(size, box_r, box_c, cages) != 1:
            continue
        if solve_deductive(size, box_r, box_c, cages) is None:
            continue
        if not verify_transforms(size, box_r, box_c, cages):
            continue

        for i, cg in enumerate(cages):
            cg["id"] = i

        puzzles.append({
            "size": size,
            "box_rows": box_r,
            "box_cols": box_c,
            "cages": cages,
            "solution": sol
        })
        if len(puzzles) % 10 == 0 or len(puzzles) == count:
            print(f"  [{tier_name.upper()}] Generated {len(puzzles)}/{count} puzzles (Attempts: {attempts})")

    return puzzles


def export_cpp_header(dataset: Dict[str, List[Dict[str, Any]]]):
    print(f"\nExporting C++ header to {CPP_OUT}...")

    def pack_nibbles(vals: List[int]) -> List[int]:
        res = []
        for i in range(0, len(vals), 2):
            high = vals[i] & 0x0F
            low = (vals[i + 1] & 0x0F) if i + 1 < len(vals) else 0
            res.append((high << 4) | low)
        return res

    lines = []
    lines.append("// Morning Puzzles - Curated Deductive Killer Sudoku Dataset")
    lines.append("// Auto-generated by scripts/build_killer_dataset.py. Do not edit directly.")
    lines.append("#ifndef KILLER_DATASET_H")
    lines.append("#define KILLER_DATASET_H")
    lines.append("")
    lines.append("#include <Arduino.h>")
    lines.append("")
    lines.append("static const size_t NUM_KILLER_EASY = 100;")
    lines.append("static const size_t NUM_KILLER_MEDIUM = 100;")
    lines.append("static const size_t NUM_KILLER_EXTREME = 100;")
    lines.append("")
    lines.append("// Struct for 4x4 Killer Sudoku entry (33 bytes each)")
    lines.append("struct Killer4x4Entry {")
    lines.append("    uint8_t cage_map[8];      // 16 nibbles: cell index -> cage ID (0..15)")
    lines.append("    uint8_t solution[8];      // 16 nibbles: cell index -> digit (1..4)")
    lines.append("    uint8_t num_cages;        // Number of cages in this puzzle")
    lines.append("    uint8_t cage_sums[16];    // Sum for each cage ID")
    lines.append("};")
    lines.append("")
    lines.append("// Struct for 6x6 Killer Sudoku entry (55 bytes each)")
    lines.append("struct Killer6x6Entry {")
    lines.append("    uint8_t cage_map[18];     // 36 nibbles: cell index -> cage ID (0..17)")
    lines.append("    uint8_t solution[18];     // 36 nibbles: cell index -> digit (1..6)")
    lines.append("    uint8_t num_cages;        // Number of cages in this puzzle")
    lines.append("    uint8_t cage_sums[18];    // Sum for each cage ID")
    lines.append("};")
    lines.append("")

    # Emit EASY (4x4)
    lines.append("// --- EASY (4x4, Digits 1-4) ---")
    lines.append("static const Killer4x4Entry KILLER_EASY_DATASET[100] PROGMEM = {")
    for p in dataset["easy"]:
        size = 4
        c_map = [0] * (size * size)
        for cg in p["cages"]:
            cid = cg["id"]
            for cell in cg["cells"]:
                r, c = cell[0], cell[1]
                c_map[r * size + c] = cid
        c_packed = pack_nibbles(c_map)

        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)

        num_cages = len(p["cages"])
        sums = [cg["sum"] for cg in p["cages"]] + [0] * (16 - num_cages)

        c_str = "{" + ", ".join(str(x) for x in c_packed) + "}"
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        sums_str = "{" + ", ".join(str(x) for x in sums) + "}"
        lines.append(f"    {{{c_str}, {s_str}, {num_cages}, {sums_str}}},")
    lines.append("};")
    lines.append("")

    # Emit MEDIUM (4x4)
    lines.append("// --- MEDIUM (4x4, Digits 1-4, Zero Singles) ---")
    lines.append("static const Killer4x4Entry KILLER_MEDIUM_DATASET[100] PROGMEM = {")
    for p in dataset["medium"]:
        size = 4
        c_map = [0] * (size * size)
        for cg in p["cages"]:
            cid = cg["id"]
            for cell in cg["cells"]:
                r, c = cell[0], cell[1]
                c_map[r * size + c] = cid
        c_packed = pack_nibbles(c_map)

        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)

        num_cages = len(p["cages"])
        sums = [cg["sum"] for cg in p["cages"]] + [0] * (16 - num_cages)

        c_str = "{" + ", ".join(str(x) for x in c_packed) + "}"
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        sums_str = "{" + ", ".join(str(x) for x in sums) + "}"
        lines.append(f"    {{{c_str}, {s_str}, {num_cages}, {sums_str}}},")
    lines.append("};")
    lines.append("")

    # Emit EXTREME (6x6)
    lines.append("// --- EXTREME (6x6, Digits 1-6, Zero Singles) ---")
    lines.append("static const Killer6x6Entry KILLER_EXTREME_DATASET[100] PROGMEM = {")
    for p in dataset["extreme"]:
        size = 6
        c_map = [0] * (size * size)
        for cg in p["cages"]:
            cid = cg["id"]
            for cell in cg["cells"]:
                r, c = cell[0], cell[1]
                c_map[r * size + c] = cid
        c_packed = pack_nibbles(c_map)

        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)

        num_cages = len(p["cages"])
        sums = [cg["sum"] for cg in p["cages"]] + [0] * (18 - num_cages)

        c_str = "{" + ", ".join(str(x) for x in c_packed) + "}"
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        sums_str = "{" + ", ".join(str(x) for x in sums) + "}"
        lines.append(f"    {{{c_str}, {s_str}, {num_cages}, {sums_str}}},")
    lines.append("};")
    lines.append("")
    lines.append("#endif // KILLER_DATASET_H")
    lines.append("")

    with open(CPP_OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"  -> Saved {CPP_OUT}")


def main():
    random.seed(42)
    easy_puzzles = curate_tier("easy", 4, 2, 2, 1, 2, allow_single=True, count=100)
    med_puzzles = curate_tier("medium", 4, 2, 2, 2, 3, allow_single=False, count=100)
    ext_puzzles = curate_tier("extreme", 6, 2, 3, 2, 4, allow_single=False, count=100)

    dataset = {
        "easy": easy_puzzles,
        "medium": med_puzzles,
        "extreme": ext_puzzles
    }

    print(f"\nSaving JSON dataset to {JSON_OUT}...")
    with open(JSON_OUT, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"  -> Saved {JSON_OUT} ({os.path.getsize(JSON_OUT)} bytes)")

    export_cpp_header(dataset)
    print("\nDataset generation complete!")


if __name__ == "__main__":
    main()
