"""
Morning Puzzles - Word Ladder Generator
Procedurally generates Lewis Carroll-style Word Ladder puzzles
using BFS shortest path search over compact English word graphs.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import json
import random
from collections import deque, defaultdict
from typing import List, Dict, Any, Optional, Tuple

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ladder_words.json")

FALLBACK_LADDERS: Dict[str, List[Dict[str, Any]]] = {
    "easy": [
        {
            "start": "COLD",
            "target": "WARM",
            "steps": 4,
            "solution": ["COLD", "WOLD", "WORD", "WARD", "WARM"]
        },
        {
            "start": "LOVE",
            "target": "HATE",
            "steps": 3,
            "solution": ["LOVE", "HOVE", "HAVE", "HATE"]
        },
        {
            "start": "LEAD",
            "target": "GOLD",
            "steps": 3,
            "solution": ["LEAD", "LOAD", "GOAD", "GOLD"]
        },
        {
            "start": "EAST",
            "target": "WEST",
            "steps": 2,
            "solution": ["EAST", "WAST", "WEST"]
        }
    ],
    "medium": [
        {
            "start": "LAKE",
            "target": "POND",
            "steps": 4,
            "solution": ["LAKE", "LANE", "PANE", "PAND", "POND"]
        },
        {
            "start": "CAMP",
            "target": "TENT",
            "steps": 5,
            "solution": ["CAMP", "CARP", "CART", "CANT", "CENT", "TENT"]
        },
        {
            "start": "BOOK",
            "target": "READ",
            "steps": 4,
            "solution": ["BOOK", "BOOD", "ROOD", "ROAD", "READ"]
        },
        {
            "start": "WHEAT",
            "target": "BREAD",
            "steps": 4,
            "solution": ["WHEAT", "THEAT", "TREAT", "TREAD", "BREAD"]
        }
    ],
    "hard": [
        {
            "start": "SLEEP",
            "target": "DREAM",
            "steps": 6,
            "solution": ["SLEEP", "BLEEP", "BLEED", "BREED", "BREAD", "DREAD", "DREAM"]
        },
        {
            "start": "FOUR",
            "target": "FIVE",
            "steps": 5,
            "solution": ["FOUR", "FOUD", "FOLD", "FOLE", "FILE", "FIVE"]
        }
    ]
}


class LadderGenerator:
    """
    Procedural generator for Word Ladder (Doublets) puzzles.
    Uses breadth-first search (BFS) over unweighted Hamming distance graphs.
    """

    def __init__(self, seed: Optional[int] = None, data_path: Optional[str] = None):
        if seed is not None:
            random.seed(seed)

        path = data_path or DATA_PATH
        self.words4: List[str] = []
        self.words5: List[str] = []
        self.curated: Dict[str, List[Dict[str, Any]]] = FALLBACK_LADDERS

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.words4 = data.get("words4", [])
                    self.words5 = data.get("words5", [])
                    if "curated" in data:
                        self.curated = data["curated"]
            except Exception as e:
                print(f"[LadderGenerator] Warning: Could not load {path}: {e}")

        # Lazy graphs
        self._graph4: Optional[Dict[str, List[str]]] = None
        self._graph5: Optional[Dict[str, List[str]]] = None

    def _build_graph(self, word_len: int) -> Dict[str, List[str]]:
        words = self.words4 if word_len == 4 else self.words5
        buckets = defaultdict(list)
        for w in words:
            for i in range(word_len):
                p = w[:i] + "_" + w[i + 1:]
                buckets[p].append(w)

        adj = defaultdict(list)
        for p, wlist in buckets.items():
            for w1 in wlist:
                for w2 in wlist:
                    if w1 != w2:
                        adj[w1].append(w2)
        return adj

    def find_shortest_path(self, start: str, target: str) -> Optional[List[str]]:
        """Finds shortest path between start and target words via BFS."""
        if len(start) != len(target):
            return None
        if start == target:
            return [start]

        word_len = len(start)
        if word_len == 4:
            if self._graph4 is None:
                self._graph4 = self._build_graph(4)
            graph = self._graph4
        elif word_len == 5:
            if self._graph5 is None:
                self._graph5 = self._build_graph(5)
            graph = self._graph5
        else:
            return None

        if start not in graph or target not in graph:
            return None

        q = deque([[start]])
        seen = {start}
        while q:
            path = q.popleft()
            curr = path[-1]
            for nxt in graph[curr]:
                if nxt == target:
                    return path + [nxt]
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(path + [nxt])
        return None

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generates a Word Ladder puzzle for the specified difficulty.
        Draws from curated high-quality daily ladders with verified family-friendly vocabulary.
        """
        if seed is not None:
            random.seed(seed)

        diff = difficulty.lower()
        pool = self.curated.get(diff, self.curated.get("medium", []))
        if not pool:
            pool = FALLBACK_LADDERS.get(diff, FALLBACK_LADDERS["medium"])

        selected = random.choice(pool)
        solution = list(selected["solution"])
        start_word = solution[0]
        target_word = solution[-1]
        word_len = len(start_word)
        intermediate_count = len(solution) - 2

        puzzle_id = f"ladder_{start_word.lower()}_{target_word.lower()}"

        return {
            "id": puzzle_id,
            "type": "ladder",
            "difficulty": diff,
            "start_word": start_word,
            "target_word": target_word,
            "word_len": word_len,
            "intermediate_count": intermediate_count,
            "total_words": len(solution),
            "solution": solution,
        }
