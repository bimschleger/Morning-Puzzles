"""
Morning Puzzles - Puzzle Registry
Central registry providing O(1) puzzle lookup by ID and maintaining
the canonical daily sequence for receipt printing and bundle composition.
"""

import datetime
import random
from typing import Dict, List, Optional, Any
from .base import BasePuzzle, BasePuzzleResult
from .sudoku import SudokuPuzzle
from .wordsearch import WordSearchPuzzle
from .nonogram import NonogramPuzzle
from .stars import StarsPuzzle
from .jumble import JumblePuzzle
from .binary import BinaryPuzzle
from .mines import MinesPuzzle
from .tents import TentsPuzzle
from .bridges import BridgesPuzzle
from .killer import KillerPuzzle
from .cryptogram import CryptogramPuzzle
from .tango import TangoPuzzle
from .ladder import LadderPuzzle
from .wheel import WheelPuzzle
from .lights import LightsPuzzle
from .loop import LoopPuzzle


class PuzzleRegistry:
    """
    Registry for Morning Puzzles plugins.
    Guarantees deterministic print order and dynamic ID dispatch.
    """

    def __init__(self, plugins: Optional[List[BasePuzzle]] = None):
        self._order: List[str] = []
        self._by_id: Dict[str, BasePuzzle] = {}
        if plugins:
            for p in plugins:
                self.register(p)

    def register(self, puzzle: BasePuzzle):
        """Registers a puzzle plugin instance."""
        p_id = puzzle.puzzle_id.lower()
        if p_id not in self._by_id:
            self._order.append(p_id)
        self._by_id[p_id] = puzzle

    def get(self, puzzle_id: str) -> Optional[BasePuzzle]:
        """Retrieves a puzzle plugin by its ID."""
        return self._by_id.get(puzzle_id.lower())

    def get_all(self) -> List[BasePuzzle]:
        """Returns all registered puzzle plugins in canonical order."""
        return [self._by_id[p_id] for p_id in self._order]

    def generate_bundle(self, difficulty: str = "medium") -> Dict[str, Any]:
        """
        Generates the standard daily bundle containing all 12 puzzles.
        Preserves legacy dictionary keys and difficulty mappings.
        """
        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        bundle: Dict[str, Any] = {
            "title": "DAILY MORNING PUZZLES",
            "date": today_str,
            "difficulty": difficulty,
        }

        diff_lower = difficulty.lower()

        for plugin in self.get_all():
            if diff_lower == "random":
                p_diff = random.choice(plugin.supported_difficulties)
            else:
                p_diff = diff_lower
                # Special difficulty adjustments matching legacy bundle generation
                if plugin.puzzle_id == "killer" and diff_lower == "hard":
                    p_diff = "extreme"
                elif plugin.puzzle_id == "nonogram":
                    p_diff = "easy" if diff_lower == "easy" else "medium"

            result = plugin.generate(difficulty=p_diff)
            bundle[plugin.puzzle_id] = result.to_dict()

        return bundle


# Canonical ordered registry instance
DEFAULT_REGISTRY = PuzzleRegistry([
    SudokuPuzzle(),
    WordSearchPuzzle(),
    NonogramPuzzle(),
    StarsPuzzle(),
    JumblePuzzle(),
    BinaryPuzzle(),
    MinesPuzzle(),
    TentsPuzzle(),
    BridgesPuzzle(),
    KillerPuzzle(),
    CryptogramPuzzle(),
    TangoPuzzle(),
    LadderPuzzle(),
    WheelPuzzle(),
    LightsPuzzle(),
    LoopPuzzle(),
])
