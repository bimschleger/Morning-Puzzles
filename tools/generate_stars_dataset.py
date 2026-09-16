#!/usr/bin/env python3
"""
Morning Puzzles - Curated Stars (Queens / Star Battle) Dataset Generator
Generates and verifies 100 unique, opening-anchored puzzles per difficulty tier:
- Easy: 5x5, 1 star, guaranteed size-1 or size-2 anchor
- Medium: 8x8, 1 star, guaranteed size-1 or size-2 anchor
- Hard: 9x9, 2 stars, compact <=5 cell anchor
- Extreme: 10x10, 2 stars, compact <=5 cell anchor
- Master: 10x10, 2 stars

Outputs:
- server/data/stars_dataset.json
- esp32-firmware/src/generators/StarsDataset.h
"""

import json
import os
import random
import sys
import time
from collections import deque
from typing import List, Tuple, Dict, Any, Set, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON_PATH = os.path.join(BASE_DIR, "server", "data", "stars_dataset.json")
CPP_HEADER_PATH = os.path.join(BASE_DIR, "esp32-firmware", "src", "generators", "StarsDataset.h")

TARGET_PER_TIER = 100


# --- Solver & Validator ---
def solve_mrv_1star(regions: List[List[int]], n: int, limit: int = 2) -> int:
    cand = [[True] * n for _ in range(n)]
    row_needed = [1] * n
    col_needed = [1] * n
    reg_needed = [1] * n
    sols = 0

    def search():
        nonlocal sols
        if sols >= limit:
            return
        if all(r == 0 for r in row_needed):
            sols += 1
            return

        min_cands = 999
        best_cells = None

        for r in range(n):
            if row_needed[r] > 0:
                cells = [(r, c) for c in range(n) if cand[r][c]]
                if len(cells) < row_needed[r]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        for c in range(n):
            if col_needed[c] > 0:
                cells = [(r, c) for r in range(n) if cand[r][c]]
                if len(cells) < col_needed[c]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        for reg in range(n):
            if reg_needed[reg] > 0:
                cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == reg and cand[r][c]]
                if len(cells) < reg_needed[reg]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        if not best_cells:
            return

        for r, c in best_cells:
            if not cand[r][c]:
                continue
            elim = set()
            reg = regions[r][c]
            for cc in range(n):
                if cand[r][cc]:
                    elim.add((r, cc))
            for rr in range(n):
                if cand[rr][c]:
                    elim.add((rr, c))
            for rr in range(n):
                for cc in range(n):
                    if regions[rr][cc] == reg and cand[rr][cc]:
                        elim.add((rr, cc))
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and cand[nr][nc]:
                        elim.add((nr, nc))

            for er, ec in elim:
                cand[er][ec] = False
            row_needed[r] -= 1
            col_needed[c] -= 1
            reg_needed[reg] -= 1

            search()

            row_needed[r] += 1
            col_needed[c] += 1
            reg_needed[reg] += 1
            for er, ec in elim:
                cand[er][ec] = True

    search()
    return sols


def count_solutions_2star(regions: List[List[int]], n: int, limit: int = 2) -> int:
    sols = 0

    def solve_row(r, current_stars, col_counts, reg_counts):
        nonlocal sols
        if sols >= limit:
            return
        if r == n:
            if all(c == 2 for c in col_counts) and all(g == 2 for g in reg_counts):
                sols += 1
            return

        for c1 in range(n - 2):
            if col_counts[c1] >= 2:
                continue
            reg1 = regions[r][c1]
            if reg_counts[reg1] >= 2:
                continue
            if any(abs(sr - r) <= 1 and abs(sc - c1) <= 1 for sr, sc in current_stars):
                continue

            for c2 in range(c1 + 2, n):
                if col_counts[c2] >= 2:
                    continue
                reg2 = regions[r][c2]
                if reg2 == reg1 and reg_counts[reg1] >= 1:
                    continue
                if reg2 != reg1 and reg_counts[reg2] >= 2:
                    continue
                if any(abs(sr - r) <= 1 and abs(sc - c2) <= 1 for sr, sc in current_stars):
                    continue

                col_counts[c1] += 1
                col_counts[c2] += 1
                reg_counts[reg1] += 1
                reg_counts[reg2] += 1
                current_stars.append((r, c1))
                current_stars.append((r, c2))

                solve_row(r + 1, current_stars, col_counts, reg_counts)

                current_stars.pop()
                current_stars.pop()
                col_counts[c1] -= 1
                col_counts[c2] -= 1
                reg_counts[reg1] -= 1
                reg_counts[reg2] -= 1

    solve_row(0, [], [0] * n, [0] * n)
    return sols


def is_4connected(regions: List[List[int]], n: int) -> bool:
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for reg_id in range(n):
        cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == reg_id]
        if not cells:
            return False
        visited = set()
        q = [cells[0]]
        visited.add(cells[0])
        while q:
            cr, cc = q.pop(0)
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                if (nr, nc) in cells and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
        if len(visited) != len(cells):
            return False
    return True


# --- Generation Functions ---
def generate_1star_puzzle(n: int) -> Optional[Dict[str, Any]]:
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    stars: List[Tuple[int, int]] = []
    cols = [False] * n

    def place_stars(r: int) -> bool:
        if r == n:
            return True
        cands = list(range(n))
        random.shuffle(cands)
        for c in cands:
            if cols[c]:
                continue
            if any(abs(sr - r) <= 1 and abs(sc - c) <= 1 for sr, sc in stars):
                continue
            cols[c] = True
            stars.append((r, c))
            if place_stars(r + 1):
                return True
            stars.pop()
            cols[c] = False
        return False

    if not place_stars(0):
        return None

    star_order = list(range(n))
    random.shuffle(star_order)
    anchor_idx = star_order[0]
    small_idx = star_order[1]
    small_idx2 = star_order[2] if n > 5 else -1

    grid = [[-1] * n for _ in range(n)]
    frontiers: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    cur_sizes = [1] * n
    target_sizes = [random.randint(max(4, n - 2), n + 3) for _ in range(n)]
    target_sizes[anchor_idx] = 1 if n <= 5 or random.random() < 0.5 else 2
    target_sizes[small_idx] = random.choice([2, 3])
    if small_idx2 != -1:
        target_sizes[small_idx2] = random.choice([2, 3, 4])

    protected = {anchor_idx, small_idx}
    if small_idx2 != -1:
        protected.add(small_idx2)

    for idx in range(n):
        r, c = stars[idx]
        grid[r][c] = idx
        if cur_sizes[idx] < target_sizes[idx]:
            frontiers[idx].append((r, c))

    unassigned = n * n - n
    active = [i for i in range(n) if cur_sizes[i] < target_sizes[i]]

    while unassigned > 0 and active:
        reg = random.choice(active)
        cands = []
        for fr, fc in frontiers[reg]:
            for dr, dc in dirs:
                nr, nc = fr + dr, fc + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1 and (nr, nc) not in stars:
                    cands.append((nr, nc))
        if not cands:
            active.remove(reg)
            continue
        chosen = random.choice(cands)
        grid[chosen[0]][chosen[1]] = reg
        frontiers[reg].append(chosen)
        cur_sizes[reg] += 1
        unassigned -= 1
        if cur_sizes[reg] >= target_sizes[reg]:
            active.remove(reg)

    # Fill remaining unassigned cells without expanding protected anchors
    while unassigned > 0:
        prog = False
        for r in range(n):
            for c in range(n):
                if grid[r][c] == -1:
                    adj = [
                        grid[r + dr][c + dc]
                        for dr, dc in dirs
                        if 0 <= r + dr < n and 0 <= c + dc < n and grid[r + dr][c + dc] != -1 and grid[r + dr][c + dc] not in protected
                    ]
                    if not adj:
                        adj = [
                            grid[r + dr][c + dc]
                            for dr, dc in dirs
                            if 0 <= r + dr < n and 0 <= c + dc < n and grid[r + dr][c + dc] != -1
                        ]
                    if adj:
                        grid[r][c] = random.choice(adj)
                        unassigned -= 1
                        prog = True
        if not prog:
            break

    if unassigned > 0 or not is_4connected(grid, n):
        return None

    reg_sizes = [sum(row.count(reg) for row in grid) for reg in range(n)]
    if min(reg_sizes) > 2:
        return None

    if solve_mrv_1star(grid, n, limit=2) == 1:
        return {
            "size": n,
            "stars_per_unit": 1,
            "regions": grid,
            "solution": sorted([[r, c] for r, c in stars]),
        }
    return None


def generate_2star_puzzle(n: int) -> Optional[Dict[str, Any]]:
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    col_counts = [0] * n
    stars: List[Tuple[int, int]] = []

    def place_stars(r: int, in_row: int) -> bool:
        if r == n:
            return all(c == 2 for c in col_counts)
        if in_row == 2:
            return place_stars(r + 1, 0)
        cands = list(range(n))
        random.shuffle(cands)
        for c in cands:
            if col_counts[c] >= 2:
                continue
            if any(abs(sr - r) <= 1 and abs(sc - c) <= 1 for sr, sc in stars):
                continue
            stars.append((r, c))
            col_counts[c] += 1
            if place_stars(r, in_row + 1):
                return True
            stars.pop()
            col_counts[c] -= 1
        return False

    if not place_stars(0, 0):
        return None

    star_set = set(stars)
    temp_grid = [[-1] * n for _ in range(n)]
    unpaired = list(stars)
    random.shuffle(unpaired)
    pairs: List[int] = []

    while unpaired:
        s1 = unpaired.pop(0)
        unpaired.sort(key=lambda s: abs(s[0] - s1[0]) + abs(s[1] - s1[1]))
        found_corridor = None
        target_idx = -1
        for idx, s2 in enumerate(unpaired):
            q = deque([(s1[0], s1[1], [(s1[0], s1[1])])])
            visited = {s1}
            while q:
                cr, cc, path = q.popleft()
                if (cr, cc) == s2:
                    found_corridor = path
                    break
                for dr, dc in dirs:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                        if (nr, nc) == s2 or ((nr, nc) not in star_set and temp_grid[nr][nc] == -1):
                            visited.add((nr, nc))
                            q.append((nr, nc, path + [(nr, nc)]))
            if found_corridor:
                target_idx = idx
                break
        if found_corridor:
            s2 = unpaired.pop(target_idx)
            reg_id = len(pairs)
            for pr, pc in found_corridor:
                temp_grid[pr][pc] = reg_id
            pairs.append(reg_id)
        else:
            break

    if len(pairs) != n:
        return None

    # Fill remaining unassigned cells
    unassigned = sum(row.count(-1) for row in temp_grid)
    while unassigned > 0:
        prog = False
        for r in range(n):
            for c in range(n):
                if temp_grid[r][c] == -1:
                    adj = []
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and temp_grid[nr][nc] != -1:
                            adj.append(temp_grid[nr][nc])
                    if adj:
                        temp_grid[r][c] = random.choice(adj)
                        unassigned -= 1
                        prog = True
        if not prog:
            break

    if unassigned > 0 or not is_4connected(temp_grid, n):
        return None

    reg_sizes = [sum(row.count(reg) for row in temp_grid) for reg in range(n)]
    if min(reg_sizes) > 5:
        return None

    if count_solutions_2star(temp_grid, n, limit=2) == 1:
        return {
            "size": n,
            "stars_per_unit": 2,
            "regions": temp_grid,
            "solution": sorted([[r, c] for r, c in stars]),
        }
    return None


def generate_tier(diff_name: str, size: int, stars: int, target_count: int) -> List[Dict[str, Any]]:
    print(f"Generating {target_count} {diff_name.upper()} puzzles ({size}x{size}, {stars} stars)...", flush=True)
    puzzles = []
    attempts = 0
    t0 = time.time()

    while len(puzzles) < target_count:
        attempts += 1
        if stars == 1:
            p = generate_1star_puzzle(size)
        else:
            p = generate_2star_puzzle(size)

        if p is not None:
            puzzles.append(p)
            if len(puzzles) % 10 == 0 or len(puzzles) == target_count:
                dt = time.time() - t0
                print(f"  [{len(puzzles)}/{target_count}] found in {dt:.1f}s ({attempts} attempts)", flush=True)

    return puzzles


def write_cpp_header(dataset: Dict[str, List[Dict[str, Any]]], output_path: str):
    lines = [
        "#ifndef STARS_DATASET_H",
        "#define STARS_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        f"static const size_t NUM_STARS_EASY = {len(dataset['easy'])};",
        f"static const size_t NUM_STARS_MEDIUM = {len(dataset['medium'])};",
        f"static const size_t NUM_STARS_HARD = {len(dataset['hard'])};",
        f"static const size_t NUM_STARS_EXTREME = {len(dataset['extreme'])};",
        "",
    ]

    for tier, size, stars, count in [
        ("EASY", 5, 1, len(dataset["easy"])),
        ("MEDIUM", 8, 1, len(dataset["medium"])),
        ("HARD", 9, 2, len(dataset["hard"])),
        ("EXTREME", 10, 2, len(dataset["extreme"])),
    ]:
        puzzles = dataset[tier.lower()]
        total_cells = size * size
        total_stars = size * stars
        packed_region_bytes = (total_cells + 1) // 2

        lines.append(f"// --- {tier} ({size}x{size}, {stars}-Star) ---")
        lines.append(f"static const uint8_t STARS_{tier}_REGIONS[{count}][{packed_region_bytes}] PROGMEM = {{")
        for p in puzzles:
            flat = [p["regions"][r][c] for r in range(size) for c in range(size)]
            packed_regions = []
            for i in range(0, total_cells, 2):
                high = flat[i] & 0x0F
                low = (flat[i + 1] & 0x0F) if i + 1 < total_cells else 0
                packed_regions.append((high << 4) | low)
            lines.append("    {" + ", ".join(map(str, packed_regions)) + "},")
        lines.append("};")
        lines.append("")

        lines.append(f"static const uint8_t STARS_{tier}_SOLUTIONS[{count}][{total_stars}] PROGMEM = {{")
        for p in puzzles:
            packed_solutions = [f"0x{(s[0] << 4) | (s[1] & 0x0F):02X}" for s in p["solution"]]
            lines.append(f"    {{{', '.join(packed_solutions)}}},")
        lines.append("};")
        lines.append("")

    lines.append("#endif // STARS_DATASET_H\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote C++ header to: {output_path}")


def update_simulator_html(dataset: Dict[str, List[Dict[str, Any]]], simulator_path: str):
    if not os.path.exists(simulator_path):
        return
    res = {}
    for tier in ["easy", "medium", "hard", "extreme"]:
        res[tier] = []
        for p in dataset[tier]:
            r_str = "".join(str(cell) for row in p["regions"] for cell in row)
            s_str = "".join(f"{s[0]}{s[1]}" for s in p["solution"])
            res[tier].append([r_str, s_str])

    js_code = "    const STARS_DATASET = " + json.dumps(res, separators=(",", ":")) + ";"
    with open(simulator_path, "r") as f:
        content = f.read()

    import re
    pattern = r"    const STARS_DATASET = \{.*?\};"
    if re.search(pattern, content):
        content = re.sub(pattern, js_code, content)
        with open(simulator_path, "w") as f:
            f.write(content)
        print(f"Updated JS dataset in: {simulator_path}")


def main():
    random.seed(20240915)
    os.makedirs(os.path.dirname(DATA_JSON_PATH), exist_ok=True)

    existing = {}
    if os.path.exists(DATA_JSON_PATH):
        try:
            with open(DATA_JSON_PATH, "r") as f:
                existing = json.load(f)
        except Exception:
            pass

    dataset: Dict[str, List[Dict[str, Any]]] = {}
    for tier, size, stars in [("easy", 5, 1), ("medium", 8, 1), ("hard", 9, 2), ("extreme", 10, 2)]:
        if tier in existing and len(existing[tier]) == TARGET_PER_TIER:
            print(f"Reusing {len(existing[tier])} verified {tier.upper()} puzzles from existing dataset.")
            dataset[tier] = existing[tier]
        else:
            dataset[tier] = generate_tier(tier, size, stars, TARGET_PER_TIER)

    dataset["master"] = dataset["extreme"]

    with open(DATA_JSON_PATH, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Wrote JSON dataset to: {DATA_JSON_PATH}")

    write_cpp_header(dataset, CPP_HEADER_PATH)
    update_simulator_html(dataset, os.path.join(BASE_DIR, "simulator", "receipt_simulator.html"))
    print("Dataset generation complete!")


if __name__ == "__main__":
    main()
