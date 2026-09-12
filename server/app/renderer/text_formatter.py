"""
80mm Receipt ESC/POS Formatter (Text and Hybrid Raster)
Formats daily puzzle receipts directly into standard ESC/POS command sequences.
Compatible with all commercial 80mm receipt printers (Epson, Star, Munbyn, etc.).
Strictly follows:
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/PUZZLE_HEADER_SPEC.md
  - docs/THERMAL_DRAWING_SPEC.md
"""

from typing import Dict, Any, List, Optional

# ESC/POS Constants
ESC = b"\x1b"
GS  = b"\x1d"
LF  = b"\x0a"

CMD_INIT         = ESC + b"@"
CMD_ALIGN_LEFT   = ESC + b"a\x00"
CMD_ALIGN_CENTER = ESC + b"a\x01"
CMD_ALIGN_RIGHT  = ESC + b"a\x02"
CMD_BOLD_ON      = ESC + b"E\x01"
CMD_BOLD_OFF     = ESC + b"E\x00"
CMD_DOUBLE_SIZE  = GS  + b"!\x11"
CMD_NORMAL_SIZE  = GS  + b"!\x00"
CMD_CUT_PARTIAL  = GS  + b"V\x42\x03"

COLS_80MM = 48  # Standard 80mm Font A characters per line


class EscPosTextReceipt:
    def __init__(self):
        self.buffer = bytearray()
        self.buffer.extend(CMD_INIT)

    def text(self, s: str):
        self.buffer.extend(s.encode("latin-1", errors="replace"))

    def println(self, s: str = ""):
        self.text(s)
        self.buffer.extend(LF)

    def align(self, mode: str):
        if mode == "center":
            self.buffer.extend(CMD_ALIGN_CENTER)
        elif mode == "right":
            self.buffer.extend(CMD_ALIGN_RIGHT)
        else:
            self.buffer.extend(CMD_ALIGN_LEFT)

    def bold(self, enable: bool):
        self.buffer.extend(CMD_BOLD_ON if enable else CMD_BOLD_OFF)

    def double_size(self, enable: bool):
        self.buffer.extend(CMD_DOUBLE_SIZE if enable else CMD_NORMAL_SIZE)

    def horizontal_rule(self, char: str = "-"):
        self.println(char * COLS_80MM)

    def header(self, title: str, date_str: str):
        self.align("center")
        self.horizontal_rule("=")
        self.bold(True)
        self.double_size(True)
        self.println(title)
        self.double_size(False)
        self.bold(False)
        self.println(date_str)
        self.horizontal_rule("=")
        self.align("left")
        self.println()

    def puzzle_header(self, title: str, difficulty: Optional[str] = None, instruction: str = ""):
        """Standardized puzzle header matching docs/PUZZLE_HEADER_SPEC.md"""
        self.align("center")
        self.bold(True)
        self.println(f"--- {title.upper()} ---")
        self.bold(False)
        if difficulty:
            self.println(f"DIFFICULTY: {difficulty.upper()}")
        if instruction:
            self.println(instruction)
        self.println()
        self.align("left")

    def key_value(self, key: str, val: str):
        spaces = max(1, COLS_80MM - len(key) - len(val))
        self.println(key + (" " * spaces) + val)

    def write_raw(self, raw_bytes: bytes):
        self.buffer.extend(raw_bytes)

    def feed(self, lines: int = 4):
        for _ in range(lines):
            self.buffer.extend(LF)

    def cut(self):
        self.buffer.extend(CMD_CUT_PARTIAL)

    def get_bytes(self) -> bytes:
        return bytes(self.buffer)


# ==============================================================================
# Pure ASCII Text Mode Receipt Builder
# ==============================================================================
def build_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """Combines generated puzzles into an 80mm ESC/POS text-only byte stream."""
    r = EscPosTextReceipt()

    # Header
    title = daily_data.get("title", "MORNING PUZZLES")
    date_str = daily_data.get("date", "Daily Edition")
    r.header(title, date_str)

    # 1. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        r.puzzle_header(
            "SUDOKU",
            s.get("difficulty", "Medium"),
            "Fill the grid so that every row, column, and 3x3 box contains digits 1 through 9 without repeating."
        )
        for line in s.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 2. Word Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        r.puzzle_header(
            "SEARCH",
            None,
            "Find and circle all of the listed words hidden horizontally, vertically, or diagonally within the letter grid."
        )
        for line in ws.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 3. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        r.puzzle_header(
            "NONOGRAM",
            n.get("difficulty", "Easy"),
            "Use the number clues outside the grid to shade the correct cells and reveal the hidden pixel picture."
        )
        for line in n.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 4. Queens / Star Battle
    if "queens" in daily_data:
        q = daily_data["queens"]
        q_diff = str(q.get("difficulty", "Medium"))
        stars_num = 2 if q_diff.lower() in ("hard", "master", "extreme") or q.get("stars_per_unit", 1) > 1 else 1
        star_str = f"{stars_num} stars" if stars_num > 1 else "1 star"
        r.puzzle_header(
            "STARS",
            q_diff,
            f"Place stars so each row, column, and shaped region contains {star_str} with no two stars touching, even diagonally."
        )
        for line in q.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 5. Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        r.puzzle_header(
            "JUMBLE",
            j.get("difficulty", "Medium"),
            "Unscramble the clue words, then arrange the circled letters to solve the punchline riddle."
        )
        for line in j.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 6. Binary
    if "binary" in daily_data:
        b = daily_data["binary"]
        r.puzzle_header(
            "BINARY",
            b.get("difficulty", "Medium"),
            "Fill the grid with 0s and 1s so no more than two identical numbers touch and each row and column has equal counts."
        )
        for line in b.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 7. Mines
    if "mines" in daily_data:
        m = daily_data["mines"]
        m_diff = str(m.get("difficulty", "Medium"))
        total_mines = m.get("total_mines", 8 if m_diff.lower() == "easy" else (15 if m_diff.lower() == "hard" else 12))
        r.puzzle_header(
            "MINES",
            m_diff,
            f"Use the numbered clues showing adjacent mine counts to deduce each of the {total_mines} hidden mines across the grid."
        )
        r.println(f"TOTAL MINES: {total_mines}")
        r.println()
        for line in m.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()

    # 8. Tents
    if "tents" in daily_data:
        r.horizontal_rule("-")
        t = daily_data["tents"]
        r.puzzle_header(
            "TENTS",
            t.get("difficulty", "Medium"),
            "Pair each tree with an orthogonally adjacent tent such that tents never touch, even diagonally, matching the row and column counts."
        )
        for line in t.get("text", "").split("\n"):
            r.println(line)
        r.println()

    # 9. Bridges
    if "bridges" in daily_data:
        r.horizontal_rule("-")
        b = daily_data["bridges"]
        r.puzzle_header(
            "BRIDGES",
            b.get("difficulty", "Medium"),
            "Connect the numbered islands with single or double lines horizontally and vertically so all islands form a single network matching each island's bridge count."
        )
        for line in b.get("text", "").split("\n"):
            r.println(line)
        r.println()

    # Optional Solution Key
    if daily_data.get("show_solutions"):
        _append_solution_key(r, daily_data)

    # Footer
    r.align("center")
    r.horizontal_rule("=")
    r.println("Good luck! Solutions tomorrow morning.")
    r.println("Printed on ESP32 80mm Commercial Thermal Receipt")
    r.horizontal_rule("=")
    r.feed(4)
    r.cut()

    return r.get_bytes()


# ==============================================================================
# Hybrid Mode Receipt Builder (ESC/POS Text Headers + 1-Bit GS v 0 Raster Graphics)
# ==============================================================================
def build_hybrid_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """
    Combines standardized ESC/POS text headers with crisp 576-dot 1-bit raster bitmaps.
    Strictly conforms to:
      - docs/PUZZLE_HEADER_SPEC.md (standardized text headers/instructions)
      - docs/THERMAL_80MM_PRINT_GUIDE.md (576 dots width, 4-line feed before cut)
      - docs/THERMAL_DRAWING_SPEC.md (geometric hatching and stroke hierarchy)
    Falls back gracefully to text mode if Pillow is not available.
    """
    try:
        from .receipt_rasterizer import (
            render_sudoku_raster,
            render_wordsearch_raster,
            render_nonogram_raster,
            render_queens_dithered_raster,
            render_jumble_raster,
            render_binary_raster,
            render_mines_raster,
            render_tents_raster,
            render_bridges_raster,
        )
        has_pillow = True
    except (ImportError, RuntimeError):
        has_pillow = False

    if not has_pillow:
        return build_daily_receipt_bytes(daily_data)

    r = EscPosTextReceipt()

    # 1. Master Receipt Header
    title = daily_data.get("title", "MORNING PUZZLES")
    date_str = daily_data.get("date", "Daily Edition")
    r.header(title, date_str)

    # 2. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        r.puzzle_header(
            "SUDOKU",
            s.get("difficulty", "Medium"),
            "Fill the grid so that every row, column, and 3x3 box contains digits 1 through 9 without repeating."
        )
        try:
            raster = render_sudoku_raster(s)
            r.write_raw(raster)
        except Exception:
            for line in s.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 3. Word Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        r.puzzle_header(
            "SEARCH",
            None,
            "Find and circle all of the listed words hidden horizontally, vertically, or diagonally within the letter grid."
        )
        try:
            raster = render_wordsearch_raster(ws)
            r.write_raw(raster)
        except Exception:
            for line in ws.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 4. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        r.puzzle_header(
            "NONOGRAM",
            n.get("difficulty", "Easy"),
            "Use the number clues outside the grid to shade the correct cells and reveal the hidden pixel picture."
        )
        try:
            raster = render_nonogram_raster(n)
            r.write_raw(raster)
        except Exception:
            for line in n.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 5. Stars / Queens
    if "queens" in daily_data:
        q = daily_data["queens"]
        q_diff = str(q.get("difficulty", "Medium"))
        stars_num = 2 if q_diff.lower() in ("hard", "master", "extreme") or q.get("stars_per_unit", 1) > 1 else 1
        star_str = f"{stars_num} stars" if stars_num > 1 else "1 star"
        r.puzzle_header(
            "STARS",
            q_diff,
            f"Place stars so each row, column, and shaped region contains {star_str} with no two stars touching, even diagonally."
        )
        try:
            raster = render_queens_dithered_raster(q)
            r.write_raw(raster)
        except Exception:
            for line in q.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 6. Daily Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        r.puzzle_header(
            "JUMBLE",
            j.get("difficulty", "Medium"),
            "Unscramble the clue words, then arrange the circled letters to solve the punchline riddle."
        )
        try:
            raster = render_jumble_raster(j)
            r.write_raw(raster)
        except Exception:
            for line in j.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 7. Binary
    if "binary" in daily_data:
        b = daily_data["binary"]
        r.puzzle_header(
            "BINARY",
            b.get("difficulty", "Medium"),
            "Fill the grid with 0s and 1s so no more than two identical numbers touch and each row and column has equal counts."
        )
        try:
            raster = render_binary_raster(b)
            r.write_raw(raster)
        except Exception:
            for line in b.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 8. Mines
    if "mines" in daily_data:
        m = daily_data["mines"]
        m_diff = str(m.get("difficulty", "Medium"))
        total_mines = m.get("total_mines", 8 if m_diff.lower() == "easy" else (15 if m_diff.lower() == "hard" else 12))
        r.puzzle_header(
            "MINES",
            m_diff,
            f"Use the numbered clues showing adjacent mine counts to deduce each of the {total_mines} hidden mines across the grid."
        )
        try:
            raster = render_mines_raster(m)
            r.write_raw(raster)
        except Exception:
            r.println(f"TOTAL MINES: {total_mines}")
            r.println()
            for line in m.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()

    # 9. Tents
    if "tents" in daily_data:
        r.horizontal_rule("-")
        t = daily_data["tents"]
        r.puzzle_header(
            "TENTS",
            t.get("difficulty", "Medium"),
            "Pair each tree with an orthogonally adjacent tent such that tents never touch, even diagonally, matching the row and column counts."
        )
        try:
            raster = render_tents_raster(t)
            r.write_raw(raster)
        except Exception:
            for line in t.get("text", "").split("\n"):
                r.println(line)
        r.println()

    # 10. Bridges
    if "bridges" in daily_data:
        r.horizontal_rule("-")
        b = daily_data["bridges"]
        r.puzzle_header(
            "BRIDGES",
            b.get("difficulty", "Medium"),
            "Connect the numbered islands with single or double lines horizontally and vertically so all islands form a single network matching each island's bridge count."
        )
        try:
            raster = render_bridges_raster(b)
            r.write_raw(raster)
        except Exception:
            for line in b.get("text", "").split("\n"):
                r.println(line)
        r.println()

    # Optional Solution Key
    if daily_data.get("show_solutions"):
        _append_solution_key(r, daily_data)

    # Master Footer
    r.align("center")
    r.horizontal_rule("=")
    r.println("Good luck! Solutions tomorrow morning.")
    r.println("Printed on ESP32 80mm Commercial Thermal Receipt")
    r.horizontal_rule("=")

    # Mandatory 4-line feed before cutter offset
    r.feed(4)
    r.cut()

    return r.get_bytes()


def _append_solution_key(r: EscPosTextReceipt, daily_data: Dict[str, Any]):
    """
    Appends an ASCII Solution Key strictly conforming to docs/PUZZLE_SOLUTION_KEY_SPEC.md.
    Enforces <= 48 character lines, standard 6-space indent for grids, and blank line separation.
    """
    import textwrap

    r.horizontal_rule("-")
    r.align("center")
    r.bold(True)
    r.println("[ SOLUTION KEY ]")
    r.bold(False)
    r.horizontal_rule("-")
    r.align("left")
    r.println()

    # 1. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        sol = s.get("solution", [])
        if sol:
            r.bold(True)
            r.println("SUDOKU")
            r.bold(False)
            for row in sol:
                r.println("      " + " ".join(str(x) for x in row))
            r.println()

    # 2. Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        words = ws.get("words", [])
        theme = ws.get("theme", "")
        r.bold(True)
        r.println("SEARCH")
        r.bold(False)
        if theme:
            r.println(f"Theme: {theme}")
        words_str = "Words: " + ", ".join(words)
        for line in textwrap.wrap(words_str, 46):
            r.println(line)
        r.println()

    # 3. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        sol = n.get("solution", [])
        if sol:
            r.bold(True)
            r.println("NONOGRAM")
            r.bold(False)
            for row in sol:
                r.println("      " + " ".join("# " if c == 1 else ". " for c in row))
            r.println()

    # 4. Stars
    if "queens" in daily_data:
        q = daily_data["queens"]
        stars = q.get("queens", [])
        if stars:
            r.bold(True)
            r.println("STARS")
            r.bold(False)
            stars_str = "Stars at: " + "  ".join(f"({sr+1},{sc+1})" for sr, sc in sorted(stars))
            for line in textwrap.wrap(stars_str, 46):
                r.println(line)
            r.println()

    # 5. Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        raw_words = j.get("words", [])
        words = [w.get("original", str(w)) if isinstance(w, dict) else str(w) for w in raw_words]
        ans = j.get("answer", "")
        r.bold(True)
        r.println("JUMBLE")
        r.bold(False)
        if words:
            for line in textwrap.wrap("Words:  " + ", ".join(words), 46):
                r.println(line)
        if ans:
            for line in textwrap.wrap(f"Answer: {ans}", 46):
                r.println(line)
        r.println()

    # 6. Binary
    if "binary" in daily_data:
        b = daily_data["binary"]
        sol = b.get("solution", [])
        if sol:
            r.bold(True)
            r.println("BINARY")
            r.bold(False)
            for row in sol:
                r.println("      " + " ".join(str(c) for c in row))
            r.println()

    # 7. Mines
    if "mines" in daily_data:
        m = daily_data["mines"]
        sol = m.get("solution", [])
        puzzle = m.get("puzzle", [])
        if sol:
            r.bold(True)
            r.println("MINES")
            r.bold(False)
            for row_idx in range(len(sol)):
                row_str = "      "
                for col_idx in range(len(sol[row_idx])):
                    if puzzle and puzzle[row_idx][col_idx] >= 0:
                        row_str += f"{puzzle[row_idx][col_idx]} "
                    elif sol[row_idx][col_idx] == 1:
                        row_str += "* "
                    else:
                        row_str += ". "
                r.println(row_str)
            r.println()

    # 8. Tents
    if "tents" in daily_data:
        t = daily_data["tents"]
        sol = t.get("solution", [])
        tents = t.get("tents", [])
        r.bold(True)
        r.println("TENTS")
        r.bold(False)
        if sol:
            for row in sol:
                row_str = "      "
                for cell in row:
                    if cell == 1:
                        row_str += "T "
                    elif cell == 2:
                        row_str += "^ "
                    else:
                        row_str += ". "
                r.println(row_str)
        if tents:
            tents_str = "Tents at: " + "  ".join(f"({tr+1},{tc+1})" for tr, tc in sorted(tents))
            for line in textwrap.wrap(tents_str, 46):
                r.println(line)
        r.println()

    # 9. Bridges
    if "bridges" in daily_data:
        b = daily_data["bridges"]
        sol_text = b.get("solution_text", "")
        bridges = b.get("solution_bridges", [])
        r.bold(True)
        r.println("BRIDGES")
        r.bold(False)
        if sol_text:
            for line in sol_text.split("\n"):
                r.println(line)
        if bridges:
            b_str = "Bridges: " + ", ".join(f"({x['r1']+1},{x['c1']+1})-({x['r2']+1},{x['c2']+1})[{x['count']}]" for x in bridges)
            for line in textwrap.wrap(b_str, 46):
                r.println(line)
        r.println()

