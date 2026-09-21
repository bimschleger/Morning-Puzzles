#!/usr/bin/env python3
"""
Morning Puzzles - Unified Curated Datasets Pipeline
Reads canonical JSON datasets in server/data/*.json and:
1. Compiles C++ PROGMEM headers in esp32-firmware/src/generators/
2. Injects / updates datasets in simulator/receipt_simulator.html
3. Synchronizes Arduino IDE sketch (MorningPuzzles/) via scripts/sync_arduino_sketch.sh
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_game_rules

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SERVER_DATA_DIR = ROOT_DIR / "server" / "data"
FW_GEN_DIR = ROOT_DIR / "esp32-firmware" / "src" / "generators"
SIMULATOR_HTML = ROOT_DIR / "simulator" / "receipt_simulator.html"
SYNC_SCRIPT = ROOT_DIR / "scripts" / "sync_arduino_sketch.sh"


# =============================================================================
# 1. STARS DATASET
# =============================================================================
def build_stars_dataset() -> None:
    json_path = SERVER_DATA_DIR / "stars_dataset.json"
    header_path = FW_GEN_DIR / "StarsDataset.h"
    print(f"Building StarsDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    lines = [
        "// Automatically generated from server/data/stars_dataset.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef STARS_DATASET_H",
        "#define STARS_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "static const size_t NUM_STARS_EASY = 100;",
        "static const size_t NUM_STARS_MEDIUM = 100;",
        "static const size_t NUM_STARS_HARD = 100;",
        "static const size_t NUM_STARS_EXTREME = 100;",
        "",
    ]

    tier_specs = [
        ("EASY", 5, 1, len(dataset["easy"])),
        ("MEDIUM", 8, 1, len(dataset["medium"])),
        ("HARD", 9, 2, len(dataset["hard"])),
        ("EXTREME", 10, 2, len(dataset["extreme"])),
    ]

    for tier, size, stars, count in tier_specs:
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
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        sim_res = {}
        for tier in ["easy", "medium", "hard", "extreme"]:
            sim_res[tier] = []
            for p in dataset[tier]:
                r_str = "".join(str(cell) for row in p["regions"] for cell in row)
                s_str = "".join(f"{s[0]}{s[1]}" for s in p["solution"])
                sim_res[tier].append([r_str, s_str])

        js_code = "    const STARS_DATASET = " + json.dumps(sim_res, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const STARS_DATASET = \{.*?\};"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated STARS_DATASET in {SIMULATOR_HTML}")


# =============================================================================
# 2. KILLER SUDOKU DATASET
# =============================================================================
def build_killer_dataset() -> None:
    json_path = SERVER_DATA_DIR / "killer_dataset.json"
    header_path = FW_GEN_DIR / "KillerDataset.h"
    print(f"Building KillerDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    def pack_nibbles(arr: List[int]) -> List[int]:
        out = []
        for i in range(0, len(arr), 2):
            high = arr[i] & 0x0F
            low = (arr[i + 1] & 0x0F) if i + 1 < len(arr) else 0
            out.append((high << 4) | low)
        return out

    lines = [
        "// Automatically generated from server/data/killer_dataset.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef KILLER_DATASET_H",
        "#define KILLER_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "static const size_t NUM_KILLER_EASY = 100;",
        "static const size_t NUM_KILLER_MEDIUM = 100;",
        "static const size_t NUM_KILLER_EXTREME = 100;",
        "",
        "struct Killer4x4Entry {",
        "    uint8_t cage_map[8];",
        "    uint8_t solution[8];",
        "    uint8_t num_cages;",
        "    uint8_t cage_sums[16];",
        "};",
        "",
        "struct Killer6x6Entry {",
        "    uint8_t cage_map[18];",
        "    uint8_t solution[18];",
        "    uint8_t num_cages;",
        "    uint8_t cage_sums[18];",
        "};",
        "",
        "// --- EASY (4x4, Digits 1-4, With Opening Singles) ---",
        "static const Killer4x4Entry KILLER_EASY_DATASET[100] PROGMEM = {",
    ]

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
    lines.append("#endif // KILLER_DATASET_H\n")

    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "    const KILLER_DATASET = " + json.dumps(dataset, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const KILLER_DATASET = \{.*?\};"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated KILLER_DATASET in {SIMULATOR_HTML}")


# =============================================================================
# 3. WORD LADDER DATASET
# =============================================================================
def build_ladder_dataset() -> None:
    json_path = SERVER_DATA_DIR / "ladder_words.json"
    header_path = FW_GEN_DIR / "LadderDataset.h"
    print(f"Building LadderDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    lines = [
        "// Automatically generated from server/data/ladder_words.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef LADDER_DATASET_H",
        "#define LADDER_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "struct LadderDef {",
        "    uint8_t wordLen;",
        "    uint8_t totalWords;",
        "    const char* words;",
        "};",
        "",
        "static const size_t NUM_LADDER_PUZZLES_PER_DIFF = 50;",
        "",
    ]

    for tier, var_name in [("easy", "EASY_LADDERS"), ("medium", "MEDIUM_LADDERS"), ("hard", "HARD_LADDERS")]:
        items = dataset[tier]
        lines.append(f"static const LadderDef {var_name}[NUM_LADDER_PUZZLES_PER_DIFF] PROGMEM = {{")
        for item in items:
            w_len = item.get("wordLen", len(item["solution"][0]))
            total_w = item.get("totalWords", len(item["solution"]))
            words_str = item.get("words", " ".join(item["solution"]))
            lines.append(f'    {{ {w_len}, {total_w}, "{words_str}" }},')
        lines.append("};")
        lines.append("")

    lines.append("#endif // LADDER_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "    const LADDER_DATASET = " + json.dumps(dataset, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const LADDER_DATASET = \{.*?\};"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated LADDER_DATASET in {SIMULATOR_HTML}")


# =============================================================================
# 4. WORD SEARCH DATASET
# =============================================================================
def build_wordsearch_dataset() -> None:
    json_path = SERVER_DATA_DIR / "wordsearch_dataset.json"
    header_path = FW_GEN_DIR / "WordSearchDataset.h"
    print(f"Building WordSearchDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    lines = [
        "// Automatically generated from server/data/wordsearch_dataset.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef WORD_SEARCH_DATASET_H",
        "#define WORD_SEARCH_DATASET_H",
        "",
        "#include <Arduino.h>",
        '#include "WordSearchGen.h"',
        "",
        "struct ThemeDef {",
        "    const char* name;",
        "    const char* words;",
        "};",
        "",
        "static const size_t NUM_WS_THEMES_PER_DIFF = 50;",
        "",
    ]

    for tier, var_name in [("easy", "EASY_THEMES"), ("medium", "MEDIUM_THEMES"), ("hard", "HARD_THEMES")]:
        themes = dataset[tier]
        lines.append(f"static const ThemeDef {var_name}[NUM_WS_THEMES_PER_DIFF] PROGMEM = {{")
        for name, words in themes.items():
            words_str = " ".join(words)
            lines.append("    {")
            lines.append(f'        "{name}",')
            lines.append(f'        "{words_str}"')
            lines.append("    },")
        lines.append("};")
        lines.append("")

    lines.append("inline const ThemeDef* getWordSearchPool(WordSearchDifficulty diff, size_t& outCount) {")
    lines.append("    outCount = NUM_WS_THEMES_PER_DIFF;")
    lines.append("    switch (diff) {")
    lines.append("        case WS_EASY:")
    lines.append("            return EASY_THEMES;")
    lines.append("        case WS_HARD:")
    lines.append("            return HARD_THEMES;")
    lines.append("        case WS_MEDIUM:")
    lines.append("        default:")
    lines.append("            return MEDIUM_THEMES;")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    lines.append("#endif // WORD_SEARCH_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        for tier, var_name in [("easy", "WORD_SEARCH_THEMES_EASY"), ("medium", "WORD_SEARCH_THEMES_MEDIUM"), ("hard", "WORD_SEARCH_THEMES_HARD")]:
            js_code = f"    const {var_name} = " + json.dumps(dataset[tier], separators=(",", ":")) + ";"
            pattern = rf"    const {var_name} = \{{.*?\}};"
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, lambda m, code=js_code: code, content, flags=re.DOTALL)
        SIMULATOR_HTML.write_text(content, encoding="utf-8")
        print(f"  -> Updated WORD_SEARCH_THEMES in {SIMULATOR_HTML}")


# =============================================================================
# 5. CRYPTOGRAM DATASET
# =============================================================================
def build_cryptogram_dataset() -> None:
    json_path = SERVER_DATA_DIR / "cryptograms.json"
    header_path = FW_GEN_DIR / "CryptogramDataset.h"
    print(f"Building CryptogramDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    by_diff = {"easy": [], "medium": [], "hard": []}
    for q in quotes:
        d = q.get("diff", "easy").lower()
        if d in by_diff:
            by_diff[d].append(q)

    lines = [
        "// Automatically generated from server/data/cryptograms.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef CRYPTOGRAM_DATASET_H",
        "#define CRYPTOGRAM_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "struct CryptogramQuote {",
        "    const char* phrase;",
        "    const char* author;",
        "};",
        "",
        "static const size_t NUM_CRYPTOGRAMS_PER_DIFF = 100;",
        f"static const size_t TOTAL_CRYPTOGRAM_PUZZLES = {len(quotes)};",
        "",
    ]

    for tier, var_name in [("easy", "EASY_CRYPTOGRAMS"), ("medium", "MEDIUM_CRYPTOGRAMS"), ("hard", "HARD_CRYPTOGRAMS")]:
        items = by_diff[tier][:100]
        lines.append(f"static const CryptogramQuote {var_name}[NUM_CRYPTOGRAMS_PER_DIFF] PROGMEM = {{")
        for item in items:
            phrase_escaped = item["phrase"].replace('"', '\\"')
            author_escaped = item["author"].replace('"', '\\"')
            lines.append(f'    {{"{phrase_escaped}", "{author_escaped}"}},')
        lines.append("};")
        lines.append("")

    lines.append("#endif // CRYPTOGRAM_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "        this.puzzles = " + json.dumps(quotes, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"        this\.puzzles = \[.*?\];"
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, lambda m, code=js_code: code, content, flags=re.DOTALL)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated CryptogramSimulator.puzzles in {SIMULATOR_HTML}")


# =============================================================================
# 6. JUMBLE DATASET
# =============================================================================
def build_jumble_dataset() -> None:
    json_path = SERVER_DATA_DIR / "jumbles.json"
    header_path = FW_GEN_DIR / "JumbleDataset.h"
    print(f"Building JumbleDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        jumbles = json.load(f)

    lines = [
        "// Automatically generated from server/data/jumbles.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef JUMBLE_DATASET_H",
        "#define JUMBLE_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "struct CompactRiddleSet {",
        "    uint8_t numWords;",
        "    uint8_t circleMasks[6];",
        "    const char* words;",
        "    const char* riddle;",
        "    const char* answer;",
        "};",
        "",
        f"static const size_t TOTAL_JUMBLE_PUZZLES = {len(jumbles)};",
        "static const CompactRiddleSet JUMBLE_DATASET[] PROGMEM = {",
    ]

    for item in jumbles:
        words = item["words"]
        circles = item["circles"]
        riddle = item["riddle"].replace('"', '\\"')
        answer = item["answer"].replace('"', '\\"')

        masks = []
        for c_list in circles:
            mask = 0
            for idx in c_list:
                mask |= (1 << idx)
            masks.append(f"0x{mask:02X}")
        while len(masks) < 6:
            masks.append("0x00")

        words_str = " ".join(words)
        lines.append("    {")
        lines.append(f"        {len(words)},")
        lines.append(f"        {{{', '.join(masks)}}},")
        lines.append(f'        "{words_str}",')
        lines.append(f'        "{riddle}",')
        lines.append(f'        "{answer}"')
        lines.append("    },")

    lines.append("};")
    lines.append("")
    lines.append("#endif // JUMBLE_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "    const JUMBLE_RIDDLES = " + json.dumps(jumbles, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const JUMBLE_RIDDLES = \[.*?\];"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated JUMBLE_RIDDLES in {SIMULATOR_HTML}")


# =============================================================================
# 7. WHEEL DATASET
# =============================================================================
def build_wheel_dataset() -> None:
    json_path = SERVER_DATA_DIR / "wheel_dictionary.json"
    header_path = FW_GEN_DIR / "WheelDataset.h"
    print(f"Building WheelDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    puzzles = data.get("puzzles", [])
    by_diff = {"easy": [], "medium": [], "hard": []}
    for p in puzzles:
        d = p.get("difficulty", "medium").lower()
        if d in by_diff:
            by_diff[d].append(p)

    lines = [
        "// Automatically generated from server/data/wheel_dictionary.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef WHEEL_DATASET_H",
        "#define WHEEL_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "struct WheelPuzzleDef {",
        "    char center;",
        "    char outer[7];",
        "    uint8_t wordCount;",
        "    uint8_t good;",
        "    uint8_t great;",
        "    uint8_t genius;",
        "    uint8_t count4;",
        "    uint8_t count5;",
        "    uint8_t count6;",
        "    uint8_t count7plus;",
        "};",
        "",
        "static const size_t NUM_WHEEL_PUZZLES_PER_DIFF = 20;",
        "",
    ]

    for tier, var_name in [("easy", "EASY_WHEEL_PUZZLES"), ("medium", "MEDIUM_WHEEL_PUZZLES"), ("hard", "HARD_WHEEL_PUZZLES")]:
        items = by_diff[tier][:20]
        lines.append(f"static const WheelPuzzleDef {var_name}[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {{")
        for p in items:
            center = p["center_letter"]
            outer = "".join(p["outer_letters"])
            wc = p["word_count"]
            bm = p.get("benchmarks", {})
            lc = p.get("length_counts", {})
            good = bm.get("good", 15)
            great = bm.get("great", 25)
            genius = bm.get("genius", 35)
            c4 = lc.get("4", 0)
            c5 = lc.get("5", 0)
            c6 = lc.get("6", 0)
            c7 = lc.get("7+", 0)
            lines.append(f"    {{ '{center}', \"{outer}\", {wc}, {good}, {great}, {genius}, {c4}, {c5}, {c6}, {c7} }},")
        lines.append("};")
        lines.append("")

    lines.append("#endif // WHEEL_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        sim_wheel = {"easy": [], "medium": [], "hard": []}
        for tier in ["easy", "medium", "hard"]:
            for p in by_diff[tier][:20]:
                bm = p.get("benchmarks", {})
                lc = p.get("length_counts", {})
                sim_wheel[tier].append({
                    "center": p["center_letter"],
                    "outer": p["outer_letters"],
                    "pangram": p.get("pangrams", [""])[0] if p.get("pangrams") else "",
                    "wordCount": p["word_count"],
                    "good": bm.get("good", 15),
                    "great": bm.get("great", 25),
                    "genius": bm.get("genius", 35),
                    "count4": lc.get("4", 0),
                    "count5": lc.get("5", 0),
                    "count6": lc.get("6", 0),
                    "count7plus": lc.get("7+", 0),
                })
        js_code = "        this.puzzles = " + json.dumps(sim_wheel, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"        this\.puzzles = \{.*?\n        \};"
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, lambda m, code=js_code: code, content, flags=re.DOTALL)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated WheelSimulator.puzzles in {SIMULATOR_HTML}")


# =============================================================================
# 8. TOWERS DATASET
# =============================================================================
def build_towers_dataset() -> None:
    json_path = SERVER_DATA_DIR / "towers_dataset.json"
    header_path = FW_GEN_DIR / "TowersDataset.h"
    print(f"Building TowersDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    def pack_nibbles(arr: List[int]) -> List[int]:
        out = []
        for i in range(0, len(arr), 2):
            high = arr[i] & 0x0F
            low = (arr[i + 1] & 0x0F) if i + 1 < len(arr) else 0
            out.append((high << 4) | low)
        return out

    lines = [
        "// Automatically generated from server/data/towers_dataset.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef TOWERS_DATASET_H",
        "#define TOWERS_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "static const size_t NUM_TOWERS_EASY = 100;",
        "static const size_t NUM_TOWERS_MEDIUM = 100;",
        "static const size_t NUM_TOWERS_HARD = 100;",
        "static const size_t NUM_TOWERS_EXTREME = 100;",
        "",
        "struct Towers4x4Entry {",
        "    uint8_t solution[8]; // 16 cells packed as nibbles",
        "    uint8_t clues[8];    // 16 clues: top(4), bottom(4), left(4), right(4)",
        "};",
        "",
        "struct Towers5x5Entry {",
        "    uint8_t solution[13]; // 25 cells packed as nibbles (last byte low nibble 0)",
        "    uint8_t clues[10];    // 20 clues: top(5), bottom(5), left(5), right(5)",
        "};",
        "",
        "struct Towers6x6Entry {",
        "    uint8_t solution[18]; // 36 cells packed as nibbles",
        "    uint8_t clues[12];    // 24 clues: top(6), bottom(6), left(6), right(6)",
        "};",
        "",
    ]

    # EASY (4x4)
    lines.append("// --- EASY (4x4, Heights 1-4) ---")
    lines.append("static const Towers4x4Entry TOWERS_EASY_DATASET[100] PROGMEM = {")
    for p in dataset["easy"]:
        size = 4
        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)
        clues_flat = p["clues"]["top"] + p["clues"]["bottom"] + p["clues"]["left"] + p["clues"]["right"]
        clues_packed = pack_nibbles(clues_flat)
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        c_str = "{" + ", ".join(str(x) for x in clues_packed) + "}"
        lines.append(f"    {{{s_str}, {c_str}}},")
    lines.append("};\n")

    # MEDIUM (5x5)
    lines.append("// --- MEDIUM (5x5, Heights 1-5) ---")
    lines.append("static const Towers5x5Entry TOWERS_MEDIUM_DATASET[100] PROGMEM = {")
    for p in dataset["medium"]:
        size = 5
        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)
        clues_flat = p["clues"]["top"] + p["clues"]["bottom"] + p["clues"]["left"] + p["clues"]["right"]
        clues_packed = pack_nibbles(clues_flat)
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        c_str = "{" + ", ".join(str(x) for x in clues_packed) + "}"
        lines.append(f"    {{{s_str}, {c_str}}},")
    lines.append("};\n")

    # HARD (6x6)
    lines.append("// --- HARD (6x6, Heights 1-6) ---")
    lines.append("static const Towers6x6Entry TOWERS_HARD_DATASET[100] PROGMEM = {")
    for p in dataset["hard"]:
        size = 6
        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)
        clues_flat = p["clues"]["top"] + p["clues"]["bottom"] + p["clues"]["left"] + p["clues"]["right"]
        clues_packed = pack_nibbles(clues_flat)
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        c_str = "{" + ", ".join(str(x) for x in clues_packed) + "}"
        lines.append(f"    {{{s_str}, {c_str}}},")
    lines.append("};\n")

    # EXTREME (6x6)
    lines.append("// --- EXTREME (6x6, Heights 1-6, Sparse Clues) ---")
    lines.append("static const Towers6x6Entry TOWERS_EXTREME_DATASET[100] PROGMEM = {")
    for p in dataset["extreme"]:
        size = 6
        sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
        sol_packed = pack_nibbles(sol_flat)
        clues_flat = p["clues"]["top"] + p["clues"]["bottom"] + p["clues"]["left"] + p["clues"]["right"]
        clues_packed = pack_nibbles(clues_flat)
        s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
        c_str = "{" + ", ".join(str(x) for x in clues_packed) + "}"
        lines.append(f"    {{{s_str}, {c_str}}},")
    lines.append("};\n")

    lines.append("#endif // TOWERS_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "    const TOWERS_DATASET = " + json.dumps(dataset, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const TOWERS_DATASET = \{.*?\};"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated TOWERS_DATASET in {SIMULATOR_HTML}")
        else:
            stars_pattern = r"(const STARS_DATASET = \{.*?\};)"
            if re.search(stars_pattern, content):
                content = re.sub(stars_pattern, r"\1\n" + js_code, content, count=1)
                SIMULATOR_HTML.write_text(content, encoding="utf-8")
                print(f"  -> Injected TOWERS_DATASET into {SIMULATOR_HTML}")



# =============================================================================
# 9. FUTOSHIKI DATASET
# =============================================================================
def build_futoshiki_dataset() -> None:
    json_path = SERVER_DATA_DIR / "futoshiki_dataset.json"
    header_path = FW_GEN_DIR / "FutoshikiDataset.h"
    print(f"Building FutoshikiDataset from {json_path}...")

    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    def pack_nibbles(arr: List[int]) -> List[int]:
        out = []
        for i in range(0, len(arr), 2):
            high = arr[i] & 0x0F
            low = (arr[i + 1] & 0x0F) if i + 1 < len(arr) else 0
            out.append((high << 4) | low)
        return out

    lines = [
        "// Automatically generated from server/data/futoshiki_dataset.json by tools/datasets/build_all_datasets.py",
        "// Do not edit directly!",
        "#ifndef FUTOSHIKI_DATASET_H",
        "#define FUTOSHIKI_DATASET_H",
        "",
        "#include <Arduino.h>",
        "",
        "static const size_t NUM_FUTOSHIKI_EASY = 100;",
        "static const size_t NUM_FUTOSHIKI_MEDIUM = 100;",
        "static const size_t NUM_FUTOSHIKI_HARD = 100;",
        "",
        "struct Futoshiki4x4Entry {",
        "    uint8_t solution[8]; // 16 cells packed nibbles",
        "    uint8_t givens[8];   // 16 cells packed nibbles (0=empty, 1..4=given)",
        "    uint8_t edges_h[12]; // 4 rows x 3 cols",
        "    uint8_t edges_v[12]; // 3 rows x 4 cols",
        "};",
        "",
        "struct Futoshiki5x5Entry {",
        "    uint8_t solution[13]; // 25 cells packed nibbles (last low nibble 0)",
        "    uint8_t givens[13];   // 25 cells packed nibbles",
        "    uint8_t edges_h[20];  // 5 rows x 4 cols",
        "    uint8_t edges_v[20];  // 4 rows x 5 cols",
        "};",
        "",
        "struct Futoshiki6x6Entry {",
        "    uint8_t solution[18]; // 36 cells packed nibbles",
        "    uint8_t givens[18];   // 36 cells packed nibbles",
        "    uint8_t edges_h[30];  // 6 rows x 5 cols",
        "    uint8_t edges_v[30];  // 5 rows x 6 cols",
        "};",
        "",
    ]

    tier_specs = [
        ("EASY", 4),
        ("MEDIUM", 5),
        ("HARD", 6),
    ]

    for tier, size in tier_specs:
        puzzles = dataset[tier.lower()]
        entry_type = f"Futoshiki{size}x{size}Entry"
        lines.append(f"// --- {tier} ({size}x{size}, Digits 1-{size}) ---")
        lines.append(f"static const {entry_type} FUTOSHIKI_{tier}_DATASET[100] PROGMEM = {{")
        for p in puzzles:
            sol_flat = [p["solution"][r][c] for r in range(size) for c in range(size)]
            sol_packed = pack_nibbles(sol_flat)

            givens_grid = [0] * (size * size)
            for r, c, val in p["givens"]:
                givens_grid[r * size + c] = val
            givens_packed = pack_nibbles(givens_grid)

            eh_flat = [p["edges_h"][r][c] for r in range(size) for c in range(size - 1)]
            ev_flat = [p["edges_v"][r][c] for r in range(size - 1) for c in range(size)]

            s_str = "{" + ", ".join(str(x) for x in sol_packed) + "}"
            g_str = "{" + ", ".join(str(x) for x in givens_packed) + "}"
            eh_str = "{" + ", ".join(str(x) for x in eh_flat) + "}"
            ev_str = "{" + ", ".join(str(x) for x in ev_flat) + "}"

            lines.append(f"    {{{s_str}, {g_str}, {eh_str}, {ev_str}}},")
        lines.append("};\n")

    lines.append("#endif // FUTOSHIKI_DATASET_H\n")
    header_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Wrote {header_path}")

    # Update simulator
    if SIMULATOR_HTML.exists():
        js_code = "    const FUTOSHIKI_DATASET = " + json.dumps(dataset, separators=(",", ":")) + ";"
        content = SIMULATOR_HTML.read_text(encoding="utf-8")
        pattern = r"    const FUTOSHIKI_DATASET = \{.*?\};"
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: js_code, content)
            SIMULATOR_HTML.write_text(content, encoding="utf-8")
            print(f"  -> Updated FUTOSHIKI_DATASET in {SIMULATOR_HTML}")
        else:
            towers_pattern = r"(const TOWERS_DATASET = \{.*?\};)"
            if re.search(towers_pattern, content):
                content = re.sub(towers_pattern, r"\1\n" + js_code, content, count=1)
                SIMULATOR_HTML.write_text(content, encoding="utf-8")
                print(f"  -> Injected FUTOSHIKI_DATASET into {SIMULATOR_HTML}")


def main() -> None:
    print("==================================================================")
    print("STARTING UNIFIED CURATED DATASETS COMPILATION PIPELINE")
    print("==================================================================")
    build_stars_dataset()
    build_killer_dataset()
    build_ladder_dataset()
    build_wordsearch_dataset()
    build_cryptogram_dataset()
    build_jumble_dataset()
    build_wheel_dataset()
    build_towers_dataset()
    build_futoshiki_dataset()
    build_game_rules.main()

    print("\nSynchronizing Arduino IDE sketch target...")
    subprocess.check_call([str(SYNC_SCRIPT)])

    print("==================================================================")
    print("ALL CURATED DATASETS SUCCESSFULLY COMPILED & SYNCHRONIZED!")
    print("==================================================================")


if __name__ == "__main__":
    main()

