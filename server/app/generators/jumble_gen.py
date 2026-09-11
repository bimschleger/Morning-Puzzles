"""
Jumble / Word Scramble Puzzle Generator
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
from typing import List, Tuple, Dict, Any, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "jumbles.json")

class JumbleGenerator:
    def __init__(self, seed: Optional[int] = None, data_path: Optional[str] = None):
        if seed is not None:
            random.seed(seed)

        path = data_path or DATA_PATH
        self.puzzles = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.puzzles = json.load(f)
            except Exception as e:
                print(f"[JumbleGenerator] Warning: Could not load {path}: {e}")

        # Fallback if file not found
        if not self.puzzles:
            self.puzzles = [
                {
                    "id": "fallback_001",
                    "diff": "easy",
                    "words": ["ROAST", "PLANT", "LIGHT", "CROWN"],
                    "circles": [[0, 2], [1], [0, 4], [2]],
                    "riddle": "Why did the coffee file a police report?",
                    "answer": "IT GOT MUGGED"
                }
            ]

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        candidates = [p for p in self.puzzles if p.get("diff", "").lower() == difficulty]
        if not candidates:
            candidates = self.puzzles

        selected = random.choice(candidates)
        words_data = []

        for idx, word in enumerate(selected["words"]):
            scrambled = self._scramble(word)
            circles = selected["circles"][idx]
            words_data.append({
                "original": word,
                "scrambled": scrambled,
                "length": len(word),
                "circle_indices": circles
            })

        riddle_text = selected.get("riddle") or selected.get("clue", "")
        answer_text = selected["answer"]

        return {
            "type": "jumble",
            "id": selected.get("id", ""),
            "difficulty": difficulty,
            "words": words_data,
            "clue": riddle_text,
            "riddle": riddle_text,
            "answer": answer_text,
            "text": self.format_text(words_data, riddle_text)
        }

    def _scramble(self, word: str) -> str:
        chars = list(word)
        for _ in range(25):
            random.shuffle(chars)
            candidate = "".join(chars)
            if candidate != word:
                return candidate
        return "".join(chars)

    @staticmethod
    def format_text(words_data: List[Dict[str, Any]], clue: str) -> str:
        count = len(words_data)
        lines = []
        lines.append(f"Unscramble these {count} Jumbles, one letter to each square:")
        for item in words_data:
            scrambled = item["scrambled"]
            circles = item["circle_indices"]
            slot_repr = []
            for i, ch in enumerate(scrambled):
                if i in circles:
                    slot_repr.append(f"({ch})")
                else:
                    slot_repr.append(f"[{ch}]")
            lines.append(f"  {scrambled:<10} -> {' '.join(slot_repr)}")

        lines.append("")
        lines.append("Now arrange the circled letters to answer the riddle:")
        lines.append(f"Q: \"{clue}\"")
        lines.append("A: _____________________________________")
        return "\n".join(lines)


if __name__ == "__main__":
    gen = JumbleGenerator()
    print(f"Loaded {len(gen.puzzles)} Jumble puzzles.")
    for diff in ["easy", "medium", "hard"]:
        res = gen.generate(difficulty=diff)
        print(f"\nJumble [{res['difficulty'].upper()} - {res['id']}] ({len(res['words'])} words):")
        print(f"Riddle: {res['riddle']}")
        print(f"Answer: {res['answer']}")
        for w in res["words"]:
            print(f"  {w['scrambled']} -> {w['original']} (circles: {w['circle_indices']})")
