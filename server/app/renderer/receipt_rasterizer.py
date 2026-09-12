"""
Morning Puzzles - ESC/POS 80mm Raster Image Renderer (Facade)
Maintains 100% backwards compatibility with legacy callers and existing test suites
by delegating to the unified Puzzle Plugin architecture and ThermalCanvas engine.
"""

from typing import Dict, Any, Optional
from .canvas import (
    THERMAL_WIDTH_DOTS,
    THERMAL_WIDTH_BYTES,
    HAS_PILLOW,
    image_to_escpos_raster,
    calculate_duty_cycle,
    pil_to_escpos,
    ThermalBitmap,
    FONT_5X7,
)
from ..puzzles.registry import DEFAULT_REGISTRY


def render_sudoku_raster(sudoku_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("sudoku").render_raster(sudoku_data, target_width=target_width)


def render_wordsearch_raster(wordsearch_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("wordsearch").render_raster(wordsearch_data, target_width=target_width)


def render_nonogram_raster(nonogram_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS, show_solution: bool = False) -> bytes:
    return DEFAULT_REGISTRY.get("nonogram").render_raster(nonogram_data, target_width=target_width)


def render_queens_dithered_raster(queens_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("queens").render_raster(queens_data, target_width=target_width)


def render_jumble_raster(jumble_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("jumble").render_raster(jumble_data, target_width=target_width)


def render_binary_raster(binary_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("binary").render_raster(binary_data, target_width=target_width)


def render_mines_raster(mines_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("mines").render_raster(mines_data, target_width=target_width)


def render_tents_raster(tents_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("tents").render_raster(tents_data, target_width=target_width)


def render_bridges_raster(bridges_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("bridges").render_raster(bridges_data, target_width=target_width)


def render_killer_raster(killer_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("killer").render_raster(killer_data, target_width=target_width)


def render_cryptogram_raster(cryptogram_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("cryptogram").render_raster(cryptogram_data, target_width=target_width)


def render_tango_raster(tango_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    return DEFAULT_REGISTRY.get("tango").render_raster(tango_data, target_width=target_width)
