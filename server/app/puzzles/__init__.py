"""
Morning Puzzles - Puzzles Package
Unified puzzle plugin architecture.
"""

from .base import BasePuzzle, BasePuzzleResult
from .registry import PuzzleRegistry, DEFAULT_REGISTRY

__all__ = [
    "BasePuzzle",
    "BasePuzzleResult",
    "PuzzleRegistry",
    "DEFAULT_REGISTRY",
]
