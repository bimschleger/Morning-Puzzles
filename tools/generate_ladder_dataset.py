#!/usr/bin/env python3
"""
Morning Puzzles - Word Ladder Dataset Generator & Curation Tool
Curates authentic, high-quality Lewis Carroll-style Word Ladder puzzles
across 3 difficulty tiers using familiar, everyday English words.

Tiers:
- Easy (50 puzzles): 4 total words (start + 2 intermediate + target), 3 or 4 letters
- Medium (50 puzzles): 5-6 total words (start + 3-4 intermediate + target), 4 letters
- Hard (50 puzzles): 6-7 total words (start + 4-5 intermediate + target), 4 or 5 letters

Outputs:
  server/data/ladder_words.json
  esp32-firmware/src/generators/LadderDataset.h
"""

import json
import os
import ssl
import sys
import urllib.request
from collections import defaultdict, deque
import random
from typing import List, Dict, Any, Tuple, Set

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JSON_PATH = os.path.join(ROOT_DIR, "server", "data", "ladder_words.json")
CPP_HEADER_PATH = os.path.join(ROOT_DIR, "esp32-firmware", "src", "generators", "LadderDataset.h")
ARDUINO_HEADER_PATH = os.path.join(ROOT_DIR, "MorningPuzzles", "LadderDataset.h")

EXCLUDE_WORDS = {
    'AVE', 'LAS', 'LOS', 'SAN', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
    'IRAQ', 'IRAN', 'YORK', 'CHILE', 'ASIA', 'OHIO', 'IOWA', 'UTAH', 'CUBA', 'PERU', 'ROME', 'PARIS',
    'HTTP', 'HTML', 'COM', 'ORG', 'NET', 'GOV', 'EDU', 'WWW', 'URL', 'PDF', 'JPG', 'PNG', 'GIF',
    'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN', 'INC', 'LTD', 'CORP', 'CO',
    'PST', 'EST', 'CST', 'MST', 'GMT', 'UTC', 'AM', 'PM', 'SQL', 'PHP', 'XML', 'CSS',
    'BABE', 'REID', 'ROIN', 'SOIN', 'DORT', 'MORT', 'GIRN', 'FLIK', 'FLIR', 'FLUR', 'HORK',
    'SEX', 'TIT', 'ASS', 'DAMN', 'HELL', 'COCK', 'DICK', 'FUCK', 'SHIT', 'PISS', 'CRAP',
    'POOP', 'FART', 'TURD', 'SLUT', 'WHORE', 'BITCH', 'BASTARD', 'BOOB', 'ANAL'
}

def load_words() -> Dict[str, int]:
    """Loads English words ranked by everyday usage frequency."""
    raw_top: List[str] = []
    try:
        ctx = ssl._create_unverified_context()
        url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt"
        with urllib.request.urlopen(url, context=ctx, timeout=5) as resp:
            raw_top = [line.strip().upper() for line in resp.read().decode("utf-8").splitlines()]
    except Exception as e:
        print(f"[WARN] Could not fetch top words list ({e}), falling back to system dict.")

    dict_words: Set[str] = set()
    dict_path = "/usr/share/dict/words"
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if w.isalpha() and w.islower():
                    dict_words.add(w.upper())

    if not raw_top:
        raw_top = sorted(list(dict_words))

    freq_rank = {}
    for i, w in enumerate(raw_top):
        if w in dict_words and w not in EXCLUDE_WORDS and len(w) in (3, 4, 5):
            freq_rank[w] = i

    return freq_rank

def build_graph(words: List[str], word_len: int) -> Dict[str, List[str]]:
    buckets = defaultdict(list)
    for w in words:
        if len(w) != word_len:
            continue
        for i in range(word_len):
            p = w[:i] + "_" + w[i+1:]
            buckets[p].append(w)
    adj = defaultdict(list)
    for wlist in buckets.values():
        for w1 in wlist:
            for w2 in wlist:
                if w1 != w2:
                    adj[w1].append(w2)
    return adj

def generate_tier_ladders(
    graph: Dict[str, List[str]],
    freq_rank: Dict[str, int],
    word_len: int,
    path_len: int,
    needed: int,
    max_rank_start: int,
    used_pairs: Set[Tuple[str, str]],
    seed: int
) -> List[Dict[str, Any]]:
    random.seed(seed)
    results = []
    starts = [w for w in graph.keys() if len(w) == word_len and freq_rank.get(w, 99999) < max_rank_start]
    random.shuffle(starts)

    for start in starts:
        q = deque([[start]])
        vis = {start}
        while q:
            path = q.popleft()
            L = len(path)
            if L > path_len:
                continue
            curr = path[-1]
            if L == path_len:
                if freq_rank.get(curr, 99999) < max_rank_start:
                    pair = (start, curr)
                    rev = (curr, start)
                    if pair not in used_pairs and rev not in used_pairs:
                        used_pairs.add(pair)
                        used_pairs.add(rev)
                        results.append({
                            "wordLen": word_len,
                            "totalWords": path_len,
                            "start": start,
                            "target": curr,
                            "solution": path,
                            "words": " ".join(path)
                        })
                        if len(results) >= needed:
                            return results
                        break
            for nxt in graph[curr]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(path + [nxt])
        if len(results) >= needed:
            break

    return results

def verify_dataset(dataset: Dict[str, List[Dict[str, Any]]]):
    for tier in ["easy", "medium", "hard"]:
        ladders = dataset[tier]
        assert len(ladders) == 50, f"Tier {tier} must contain exactly 50 puzzles, found {len(ladders)}"
        for idx, item in enumerate(ladders):
            sol = item["solution"]
            w_len = item["wordLen"]
            total_words = item["totalWords"]
            assert len(sol) == total_words, f"Tier {tier} puzzle {idx} length mismatch: {len(sol)} vs {total_words}"
            assert sol[0] == item["start"], f"Tier {tier} puzzle {idx} start mismatch"
            assert sol[-1] == item["target"], f"Tier {tier} puzzle {idx} target mismatch"
            assert len(set(sol)) == len(sol), f"Tier {tier} puzzle {idx} has duplicates: {sol}"
            for i in range(len(sol) - 1):
                w1, w2 = sol[i], sol[i+1]
                assert len(w1) == w_len, f"Word {w1} length mismatch"
                diffs = sum(c1 != c2 for c1, c2 in zip(w1, w2))
                assert diffs == 1, f"Invalid step {w1} -> {w2} (diffs={diffs})"

def write_cpp_header(dataset: Dict[str, List[Dict[str, Any]]], filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    lines = [
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
        ""
    ]

    for tier_name, arr_name in [("easy", "EASY_LADDERS"), ("medium", "MEDIUM_LADDERS"), ("hard", "HARD_LADDERS")]:
        lines.append(f"static const LadderDef {arr_name}[NUM_LADDER_PUZZLES_PER_DIFF] PROGMEM = {{")
        for item in dataset[tier_name]:
            w_len = item["wordLen"]
            total_w = item["totalWords"]
            words_str = item["words"]
            lines.append(f'    {{ {w_len}, {total_w}, "{words_str}" }},')
        lines.append("};")
        lines.append("")

    lines.append("#endif // LADDER_DATASET_H")
    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {filepath}")

def main():
    print("Loading English word frequency corpus...")
    freq_rank = load_words()
    print(f"Loaded {len(freq_rank)} clean 3-5 letter words.")

    words3 = [w for w, r in freq_rank.items() if len(w) == 3 and r < 3500]
    words4 = [w for w, r in freq_rank.items() if len(w) == 4 and r < 4500]
    words5 = [w for w, r in freq_rank.items() if len(w) == 5 and r < 7500]

    g3 = build_graph(words3, 3)
    g4 = build_graph(words4, 4)
    g5 = build_graph(words5, 5)

    used_pairs: Set[Tuple[str, str]] = set()

    print("Generating Easy Tier (20 3-letter 4-word, 30 4-letter 4-word)...")
    easy = generate_tier_ladders(g3, freq_rank, word_len=3, path_len=4, needed=20, max_rank_start=2500, used_pairs=used_pairs, seed=101) + \
           generate_tier_ladders(g4, freq_rank, word_len=4, path_len=4, needed=30, max_rank_start=2500, used_pairs=used_pairs, seed=102)

    print("Generating Medium Tier (30 4-letter 5-word, 20 4-letter 6-word)...")
    med = generate_tier_ladders(g4, freq_rank, word_len=4, path_len=5, needed=30, max_rank_start=3000, used_pairs=used_pairs, seed=103) + \
          generate_tier_ladders(g4, freq_rank, word_len=4, path_len=6, needed=20, max_rank_start=3000, used_pairs=used_pairs, seed=104)

    print("Generating Hard Tier (25 4-letter 7-word, 15 5-letter 6-word, 10 5-letter 7-word)...")
    hard = generate_tier_ladders(g4, freq_rank, word_len=4, path_len=7, needed=25, max_rank_start=3000, used_pairs=used_pairs, seed=105) + \
           generate_tier_ladders(g5, freq_rank, word_len=5, path_len=6, needed=15, max_rank_start=4500, used_pairs=used_pairs, seed=106) + \
           generate_tier_ladders(g5, freq_rank, word_len=5, path_len=7, needed=10, max_rank_start=5500, used_pairs=used_pairs, seed=107)

    dataset = {
        "easy": easy,
        "medium": med,
        "hard": hard
    }

    print("Verifying full dataset...")
    verify_dataset(dataset)
    print("Verification passed! (150/150 valid minimal ladders)")

    # Save JSON
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Wrote {JSON_PATH}")

    # Save C++ Header
    write_cpp_header(dataset, CPP_HEADER_PATH)
    if os.path.exists(os.path.dirname(ARDUINO_HEADER_PATH)):
        write_cpp_header(dataset, ARDUINO_HEADER_PATH)

if __name__ == "__main__":
    main()
