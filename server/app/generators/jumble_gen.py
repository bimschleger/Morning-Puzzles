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

import random
from typing import List, Tuple, Dict, Any, Optional

JUMBLE_PAIRS = [
    {
        "difficulty": "easy",
        "words": ["ROAST", "PLANT", "LIGHT", "CROWN"],
        "clue": "Why did the coffee file a police report?",
        "answer": "IT GOT MUGGED",
        "circle_indices": [[0, 2], [1], [0, 4], [2]] # extracts letters to form answer
    },
    {
        "difficulty": "medium",
        "words": ["GLANCE", "SPHERE", "BREEZE", "SUMMIT"],
        "clue": "What do you call a sleeping dinosaur?",
        "answer": "A DINO SNORE",
        "circle_indices": [[1, 3], [0, 4], [2, 5], [1]]
    },
    {
        "difficulty": "hard",
        "words": ["JOURNEY", "WHISPER", "LANTERN", "THUNDER"],
        "clue": "Why couldn't the bicycle stand up by itself?",
        "answer": "IT WAS TWO TIRED",
        "circle_indices": [[0, 4], [2, 5], [1, 3], [0, 3]]
    },
    {
        "difficulty": "easy",
        "words": ["BREAD", "SPOON", "CLOCK", "TABLE"],
        "clue": "What did the ocean say to the sailboat?",
        "answer": "NOTHING IT JUST WAVED",
        "circle_indices": [[0, 1], [2], [0, 4], [1, 3]]
    },
    {
        "difficulty": "medium",
        "words": ["SHADOW", "FLAVOR", "CASTLE", "GUITAR"],
        "clue": "Why did the scarecrow win an award?",
        "answer": "OUTSTANDING IN HIS FIELD",
        "circle_indices": [[0, 3], [1, 4], [0, 2], [1, 5]]
    }
]

class JumbleGenerator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        candidates = [p for p in JUMBLE_PAIRS if p["difficulty"] == difficulty]
        if not candidates:
            candidates = JUMBLE_PAIRS

        selected = random.choice(candidates)
        words_data = []

        for idx, word in enumerate(selected["words"]):
            scrambled = self._scramble(word)
            circles = selected["circle_indices"][idx]
            words_data.append({
                "original": word,
                "scrambled": scrambled,
                "length": len(word),
                "circle_indices": circles
            })

        return {
            "type": "jumble",
            "difficulty": difficulty,
            "words": words_data,
            "clue": selected["clue"],
            "answer": selected["answer"],
            "text": self.format_text(words_data, selected["clue"])
        }

    def _scramble(self, word: str) -> str:
        chars = list(word)
        # Shuffle until it doesn't match original
        for _ in range(20):
            random.shuffle(chars)
            candidate = "".join(chars)
            if candidate != word:
                return candidate
        return "".join(chars)

    @staticmethod
    def format_text(words_data: List[Dict[str, Any]], clue: str) -> str:
        lines = []
        lines.append("Unscramble these four Jumbles, one letter to each square:")
        for item in words_data:
            scrambled = item["scrambled"]
            circles = item["circle_indices"]
            # Mark circled positions with parentheses
            slot_repr = []
            for i, ch in enumerate(scrambled):
                if i in circles:
                    slot_repr.append(f"({ch})")
                else:
                    slot_repr.append(f"[{ch}]")
            lines.append(f"  {scrambled:<10} -> {' '.join(slot_repr)}")

        lines.append("")
        lines.append(f"Now arrange the circled letters to answer the riddle:")
        lines.append(f"Q: \"{clue}\"")
        lines.append("A: _____________________________________")
        return "\n".join(lines)


if __name__ == "__main__":
    gen = JumbleGenerator()
    res = gen.generate(difficulty="medium")
    print(f"Jumble ({res['difficulty']}):")
    print(res["text"])
