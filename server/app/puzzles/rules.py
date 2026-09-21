"""
Morning Puzzles - Game Rules & Guide Module
Loads and provides indexed access to canonical game rules, step-by-step
mechanics, move diagrams, and FAQs from server/data/game_rules.json.
"""

import json
import os
from typing import Dict, Any, Optional, List

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "game_rules.json")
_RULES_DATA: Optional[Dict[str, Any]] = None
_BY_KEY: Dict[str, Dict[str, Any]] = {}
_BY_ID: Dict[int, Dict[str, Any]] = {}


def load_game_rules() -> Dict[str, Any]:
    global _RULES_DATA, _BY_KEY, _BY_ID
    if _RULES_DATA is None:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Canonical rules dataset not found at {DATA_PATH}")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            _RULES_DATA = json.load(f)
        for game in _RULES_DATA.get("games", []):
            _BY_KEY[game["key"].lower()] = game
            _BY_KEY[game["title"].lower()] = game
            _BY_ID[game["id"]] = game
            # Legacy alias mappings
            if game["key"] == "search":
                _BY_KEY["wordsearch"] = game
            elif game["key"] == "stars":
                _BY_KEY["queens"] = game
    return _RULES_DATA


def get_game_rule(identifier: Any) -> Optional[Dict[str, Any]]:
    """Retrieves canonical game rules by ID (int) or key/title (str)."""
    load_game_rules()
    if isinstance(identifier, int):
        return _BY_ID.get(identifier)
    s = str(identifier).strip().lower()
    return _BY_KEY.get(s)


def get_all_game_rules() -> List[Dict[str, Any]]:
    """Returns all 18 canonical game rule specifications."""
    data = load_game_rules()
    return data.get("games", [])
