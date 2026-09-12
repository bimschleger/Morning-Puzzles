"""
Cryptogram / Letter Substitution Cipher Generator
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
import string
from typing import List, Dict, Any, Optional, Tuple

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cryptograms.json")


class CryptogramGenerator:
    """
    Generates monoalphabetic substitution cryptograms with procedural derangement ciphers,
    dynamic letter clues, and layout formatted for comfortable pencil solving on 80mm receipts.
    """

    def __init__(self, seed: Optional[int] = None, data_path: Optional[str] = None):
        if seed is not None:
            random.seed(seed)

        path = data_path or DATA_PATH
        self.puzzles: List[Dict[str, Any]] = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.puzzles = json.load(f)
            except Exception as e:
                print(f"[CryptogramGenerator] Warning: Could not load {path}: {e}")

        if not self.puzzles:
            # Fallback quotes if dataset is missing
            self.puzzles = [
                {
                    "id": "easy_fallback",
                    "diff": "easy",
                    "phrase": "A JOURNEY OF A THOUSAND MILES BEGINS WITH A SINGLE STEP.",
                    "author": "LAO TZU",
                    "category": "Wisdom"
                },
                {
                    "id": "medium_fallback",
                    "diff": "medium",
                    "phrase": "THE FUTURE BELONGS TO THOSE WHO BELIEVE IN THE BEAUTY OF THEIR DREAMS.",
                    "author": "ELEANOR ROOSEVELT",
                    "category": "Inspiration"
                },
                {
                    "id": "hard_fallback",
                    "diff": "hard",
                    "phrase": "I USED TO THINK I WAS INDECISIVE, BUT NOW I AM NOT SO SURE.",
                    "author": "TOMMY COOPER",
                    "category": "Wit"
                }
            ]

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        candidates = [p for p in self.puzzles if p.get("diff", "").lower() == difficulty]
        if not candidates:
            candidates = self.puzzles

        selected = random.choice(candidates)
        phrase = selected["phrase"].upper()
        author = selected.get("author", "ANONYMOUS").upper()
        category = selected.get("category", "General")

        # Procedural derangement substitution cipher: no letter maps to itself
        plain_to_cipher, cipher_to_plain = self._generate_derangement_key()

        # Encrypt phrase (preserve spaces and punctuation)
        ciphertext = "".join(plain_to_cipher.get(ch, ch) for ch in phrase)

        # Extract clues based on difficulty
        # Easy: 3 clues, Medium: 2 clues, Hard: 1 clue
        clue_count = 3 if difficulty == "easy" else (1 if difficulty == "hard" else 2)
        clues = self._select_clues(phrase, plain_to_cipher, clue_count)

        if len(clues) == 1:
            clue_str = f"CLUE: {clues[0]['cipher']} = {clues[0]['plain']}"
        else:
            clue_str = "CLUES: " + ", ".join(f"{c['cipher']} = {c['plain']}" for c in clues)

        formatted_text = self.format_ascii_text(ciphertext, author)

        return {
            "type": "cryptogram",
            "id": selected.get("id", ""),
            "difficulty": difficulty,
            "phrase": phrase,
            "author": author,
            "category": category,
            "ciphertext": ciphertext,
            "plain_to_cipher": plain_to_cipher,
            "cipher_to_plain": cipher_to_plain,
            "clues": clues,
            "clue_str": clue_str,
            "clue_count": len(clues),
            "text": formatted_text,
            "solution": phrase,
        }

    def _generate_derangement_key(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Generates a random permutation where no letter maps to itself."""
        letters = list(string.ascii_uppercase)
        shuffled = letters.copy()
        for _ in range(100):
            random.shuffle(shuffled)
            if all(a != b for a, b in zip(letters, shuffled)):
                break
        else:
            # Deterministic cyclic shift if derangement loop exhausted
            shuffled = letters[1:] + letters[:1]

        p2c = dict(zip(letters, shuffled))
        c2p = dict(zip(shuffled, letters))
        return p2c, c2p

    def _select_clues(self, phrase: str, p2c: Dict[str, str], count: int) -> List[Dict[str, str]]:
        """Selects distinct letter clues from letters actually appearing in the phrase."""
        distinct_letters = list(set(ch for ch in phrase if ch in string.ascii_uppercase))
        if not distinct_letters:
            distinct_letters = list(string.ascii_uppercase[:count])

        # Prioritize frequent vowels or common letters for helpful hints
        common_order = ["E", "T", "A", "O", "I", "N", "S", "H", "R", "D", "L", "C", "U", "M", "W", "F", "G", "Y", "P", "B", "V", "K", "J", "X", "Q", "Z"]
        sorted_in_phrase = [ch for ch in common_order if ch in distinct_letters] + [ch for ch in distinct_letters if ch not in common_order]

        count = min(count, len(distinct_letters))
        chosen_plain = random.sample(sorted_in_phrase[:max(count * 2, count)], count)

        clues = []
        for p in chosen_plain:
            c = p2c[p]
            clues.append({"cipher": c, "plain": p})

        # Sort alphabetically by cipher letter for clean display
        clues.sort(key=lambda x: x["cipher"])
        return clues

    @staticmethod
    def format_ascii_text(ciphertext: str, author: str = "") -> str:
        """
        Formats the cryptogram into dual-row ASCII layout with handwriting guess slots
        directly above each ciphertext letter, word-wrapped to <= 44 columns, followed by
        an alphabet tracker and 4-5 handwriting scratchpad lines.
        """
        words = ciphertext.split(" ")
        lines_of_words: List[List[str]] = []
        current_line: List[str] = []
        current_len = 0

        # In spaced representation: a word of length L takes (2L - 1) chars.
        # Between words: 2 spaces.
        for word in words:
            word_spaced_len = len(word) * 2 - 1 if word else 0
            needed = word_spaced_len + (2 if current_line else 0)
            if current_line and (current_len + needed > 42):
                lines_of_words.append(current_line)
                current_line = [word]
                current_len = word_spaced_len
            else:
                current_line.append(word)
                current_len += needed

        if current_line:
            lines_of_words.append(current_line)

        output_lines: List[str] = []

        for line_words in lines_of_words:
            # Row 1 (Handwriting slot row directly above ciphertext)
            slot_parts = []
            cipher_parts = []
            for word in line_words:
                s_chars = []
                c_chars = []
                for ch in word:
                    if ch in string.ascii_uppercase:
                        s_chars.append("_")
                    else:
                        s_chars.append(" ")
                    c_chars.append(ch)
                slot_parts.append(" ".join(s_chars))
                cipher_parts.append(" ".join(c_chars))

            # 2 spaces between words
            slot_row = "  ".join(slot_parts)
            cipher_row = "  ".join(cipher_parts)

            # Left indent 3 spaces for safe thermal margin
            output_lines.append("   " + slot_row)
            output_lines.append("   " + cipher_row)
            output_lines.append("")  # Generous blank line between wrapped rows

        if author:
            output_lines.append(f"   -- {author}")
            output_lines.append("")

        # Dashed tear divider separating puzzle from letter tracking scratchpad
        output_lines.append("  - - - - - - - - - - - - - - - - - - - - - - - -")
        output_lines.append("  ALPHABET TRACKER:")
        output_lines.append("  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
        output_lines.append("  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
        output_lines.append("")
        output_lines.append("  SCRATCHPAD:")
        for _ in range(4):
            output_lines.append("  ______________________________________________")
            output_lines.append("")

        return "\n".join(output_lines)
