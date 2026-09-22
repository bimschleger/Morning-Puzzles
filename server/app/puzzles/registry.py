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
from .towers import TowersPuzzle
from .inequality import InequalityPuzzle


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

    @staticmethod
    def get_tier_for_slot(index: int, total_count: int) -> str:
        if total_count <= 1:
            return "medium"
        p = index / (total_count - 1)
        if p < 0.25:
            return "easy"
        if p < 0.65:
            return "medium"
        if p < 0.85:
            return "hard"
        return "extreme"

    def generate_bundle(self, difficulty: str = "medium", count: Optional[int] = None) -> Dict[str, Any]:
        """
        Generates the standard daily bundle or a random N-puzzle mix.
        Supports staggered progressive difficulty scaling across arbitrary puzzle counts.
        """
        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        bundle: Dict[str, Any] = {
            "title": "MORNING PUZZLES",
            "header_tagline": "Enjoy your morning puzzles",
            "date": today_str,
            "difficulty": difficulty,
        }

        diff_lower = difficulty.lower()
        all_plugins = self.get_all()

        if count is None and diff_lower in ("staggered", "progressive"):
            count = 5

        if count is not None:
            n = max(1, min(count, len(all_plugins)))
            selected_plugins = random.sample(all_plugins, n)
            is_progressive = diff_lower in ("random", "staggered", "progressive")
            bundle["subtitle"] = f"DAILY {n}-PUZZLE MIX"
            bundle["puzzle_order"] = [p.puzzle_id for p in selected_plugins]

            for i, plugin in enumerate(selected_plugins):
                if is_progressive:
                    target_tier = self.get_tier_for_slot(i, n)
                    if target_tier == "extreme":
                        if "extreme" in plugin.supported_difficulties:
                            p_diff = "extreme"
                        elif "master" in plugin.supported_difficulties:
                            p_diff = "master"
                        else:
                            p_diff = "hard"
                    else:
                        p_diff = target_tier
                else:
                    p_diff = diff_lower
                    if plugin.puzzle_id == "killer" and diff_lower == "hard":
                        p_diff = "extreme"
                    elif plugin.puzzle_id == "nonogram":
                        p_diff = "easy" if diff_lower == "easy" else "medium"

                result = plugin.generate(difficulty=p_diff)
                bundle[plugin.puzzle_id] = result.to_dict()

            return bundle

        for plugin in all_plugins:
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
    TowersPuzzle(),
    InequalityPuzzle(),
])
