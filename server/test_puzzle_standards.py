#!/usr/bin/env python3
"""
Automated Test Suite: Morning Puzzles Presentation & Authoring Standards
Strictly validates:
  - docs/PUZZLE_HEADER_SPEC.md (Single-word titles, difficulty rules, header hierarchy)
  - docs/PUZZLE_DESCRIPTION_GUIDELINES.md (<= 100 chars, imperative formula, plain English)
  - docs/PUZZLE_SOLUTION_KEY_SPEC.md (48-column monospaced solution layout, indentation, separators)
  - simulator/receipt_simulator.html consistency with Python backend & specifications
"""

import os
import re
import sys

# Add server directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import generate_daily_bundle
from app.renderer.text_formatter import build_daily_receipt_bytes, EscPosTextReceipt
from app.puzzles.base import BasePuzzle, BasePuzzleResult
from app.puzzles.registry import DEFAULT_REGISTRY

APPROVED_TITLES = [
    "SUDOKU",
    "SEARCH",
    "NONOGRAM",
    "STARS",
    "JUMBLE",
    "BINARY",
    "MINES",
    "TENTS",
    "BRIDGES",
    "KILLER",
    "CRYPTOGRAM",
    "TANGO",
    "LADDER",
    "WHEEL",
    "LIGHTS",
    "LOOP",
]

FORBIDDEN_TITLE_PATTERNS = [
    r"Word\s+Search",
    r"Daily\s+Jumble",
    r"Queens\s*/\s*Star\s*Battle",
    r"Nonogram\s*/\s*Picross",
    r"Tents\s*(?:and|&)\s*Trees",
    r"Hashiwokakero",
    r"Picross",
    r"Star\s*Battle",
    r"Akari",
    r"Light\s*Up",
    r"Slitherlink",
    r"Fences",
]

FORBIDDEN_JARGON_TERMS = [
    "orthogonally adjacent",
    "orthogonal",
    "in a row",
    "polyomino",
    "connected component",
    "spanning tree",
    "bipartite",
    "permutation",
]

APPROVED_IMPERATIVE_VERBS = [
    "Place",
    "Fill",
    "Find",
    "Shade",
    "Unscramble",
    "Deduce",
    "Pitch",
    "Connect",
    "Draw",
]


def test_titles_and_forbidden_terms():
    print("Test 1: Verifying Strict One-Word Titles & Zero Forbidden Aliases...")
    bundle = generate_daily_bundle(difficulty="medium")
    receipt_bytes = build_daily_receipt_bytes(bundle)
    receipt_text = receipt_bytes.decode("latin-1")

    # 1. Verify all approved one-word titles exist in the receipt
    for title in APPROVED_TITLES:
        expected_header = f"--- {title} ---"
        assert expected_header in receipt_text, f"Missing canonical header '{expected_header}' in receipt output"
        # Must be strictly one word
        assert len(title.split()) == 1, f"Title '{title}' is not a single word"
        assert title.isupper(), f"Title '{title}' must be uppercase"

    # 2. Verify no forbidden aliases appear anywhere in the output
    for pattern in FORBIDDEN_TITLE_PATTERNS:
        match = re.search(pattern, receipt_text, re.IGNORECASE)
        assert not match, f"Forbidden title alias matching '{pattern}' found in receipt: '{match.group(0) if match else ''}'"

    print(f"  -> Passed! All {len(APPROVED_TITLES)} puzzle headers use strictly one-word uppercase titles with zero forbidden aliases.\n")


def test_difficulty_presentation_and_theme_rules():
    print("Test 2: Verifying Difficulty Representation & Theme Rules...")
    bundle = generate_daily_bundle(difficulty="medium")
    receipt_bytes = build_daily_receipt_bytes(bundle)
    receipt_text = receipt_bytes.decode("latin-1")

    # 1. SEARCH must NEVER display a difficulty line
    lines = receipt_text.split("\n")
    for i, line in enumerate(lines):
        if "--- SEARCH ---" in line:
            # Check the next 3 lines
            surrounding = "\n".join(lines[i : i + 4])
            assert "DIFFICULTY:" not in surrounding, (
                f"SEARCH header must omit difficulty line! Found:\n{surrounding}"
            )

    # 2. Puzzles with difficulty must have DIFFICULTY: [LEVEL] directly below title
    difficulty_puzzles = ["SUDOKU", "NONOGRAM", "STARS", "JUMBLE", "BINARY", "MINES", "TENTS", "BRIDGES", "KILLER", "CRYPTOGRAM", "TANGO", "LADDER", "WHEEL"]
    for title in difficulty_puzzles:
        header_str = f"--- {title} ---"
        assert header_str in receipt_text, f"Missing header {header_str}"
        for i, line in enumerate(lines):
            if header_str in line:
                diff_line = lines[i + 1] if i + 1 < len(lines) else ""
                assert "DIFFICULTY:" in diff_line, (
                    f"{title}: Expected 'DIFFICULTY: [LEVEL]' immediately beneath title line. Got: '{diff_line}'"
                )

    print(f"  -> Passed! Difficulty rules verified: SEARCH omits difficulty, other {len(difficulty_puzzles)} puzzles correctly display DIFFICULTY: [LEVEL].\n")


def test_description_length_and_canonical_formula():
    print("Test 3: Verifying Description Length (<= 100 chars) & Canonical Formula across all difficulties...")
    # Test descriptions across multiple difficulties
    difficulties = ["easy", "medium", "hard", "extreme"]

    for diff in difficulties:
        bundle = generate_daily_bundle(difficulty=diff)

        descriptions = []

        # 1. Sudoku
        descriptions.append(("Sudoku", "Fill every row, column, and 3x3 box with digits 1-9 without repeating."))

        # 2. Search
        ws = bundle.get("wordsearch", {})
        words_count = len(ws.get("placed_words", [])) or len(ws.get("words", []))
        search_desc = f"Find all {words_count} hidden words listed below." if words_count else "Find all listed words hidden across the grid."
        descriptions.append(("Search", search_desc))

        # 3. Nonogram
        descriptions.append(("Nonogram", "Shade blocks of cells matching each clue in order, separated by at least one empty cell."))

        # 4. Stars
        q = bundle.get("queens", {})
        q_diff = str(q.get("difficulty", diff))
        stars_num = 2 if q_diff.lower() in ("hard", "master", "extreme") or q.get("stars_per_unit", 1) > 1 else 1
        star_str = "2 stars" if stars_num > 1 else "1 star"
        descriptions.append(("Stars", f"Place {star_str} in each row, column, and region with no stars touching, even diagonally."))

        # 5. Jumble
        descriptions.append(("Jumble", "Unscramble each word, then use the circled letters to solve the riddle."))

        # 6. Binary
        b = bundle.get("binary", {})
        b_size = b.get("size", 8)
        if b_size == 6 or diff == "easy":
            b_desc = "Fill each row and column with three 0s and three 1s, with no more than two consecutive of each type."
        else:
            b_desc = "Fill each row and column with four 0s and four 1s, with no more than two consecutive of each type."
        descriptions.append(("Binary", b_desc))

        # 7. Mines
        m = bundle.get("mines", {})
        m_diff = str(m.get("difficulty", diff))
        total_mines = m.get("total_mines", 8 if m_diff.lower() == "easy" else (15 if m_diff.lower() == "hard" else 12))
        descriptions.append(("Mines", f"Deduce all {total_mines} hidden mines using the adjacent numbered clues."))

        # 8. Tents
        t = bundle.get("tents", {})
        t_diff = str(t.get("difficulty", diff))
        t_count = t.get("tree_count", 4 if t_diff.lower() == "easy" else (11 if t_diff.lower() == "hard" else 8))
        descriptions.append(("Tents", f"Pitch {t_count} tents next to trees without tents touching, matching row and column counts."))

        # 9. Bridges
        descriptions.append(("Bridges", "Connect all islands into one network using 1 or 2 lines matching each island's number."))

        # 10. Killer
        k = bundle.get("killer", {})
        k_size = k.get("size", 4)
        k_range = "1-4" if k_size == 4 else "1-6"
        descriptions.append(("Killer", f"Fill every row, column, and box with digits {k_range}, matching cage sums without repeats."))

        # 11. Cryptogram
        c = bundle.get("cryptogram", {})
        c_cnt = c.get("clue_count", 3 if diff == "easy" else (1 if diff == "hard" else 2))
        c_clue_word = "1 letter clue" if c_cnt == 1 else f"{c_cnt} letter clues"
        descriptions.append(("Cryptogram", f"Deduce the hidden phrase using the {c_clue_word} and substitution logic."))

        # 12. Tango
        tg = bundle.get("tango", {})
        tg_diff = str(tg.get("difficulty", diff))
        tg_size = tg.get("size", 6)
        if tg_size == 6 or tg_diff.lower() in ("easy", "medium"):
            tg_desc = "Fill each line with three 0s and three 1s without trios; = means same, x means opposite."
        else:
            tg_desc = "Fill each line with four 0s and four 1s without trios; = means same, x means opposite."
        # Validate each description from the bundle and from DEFAULT_REGISTRY
        for plugin in DEFAULT_REGISTRY.get_all():
            data = bundle[plugin.puzzle_id]
            desc = plugin.get_instruction(data)
            descriptions.append((plugin.title, desc))

        for name, desc in descriptions:
            # Rule 1: <= 100 characters
            assert len(desc) <= 100, (
                f"{name} description exceeds 100 characters ({len(desc)} chars) in '{diff}':\n  '{desc}'"
            )

            # Rule 2: Exactly 1 sentence (ends with single period, exactly one period total)
            assert desc.endswith("."), f"{name} description must end with a period: '{desc}'"
            assert desc.count(".") == 1, f"{name} description must be exactly one sentence. Found {desc.count('.')} periods: '{desc}'"

            # Rule 3: Starts with approved imperative verb
            first_word = desc.split()[0]
            assert first_word in APPROVED_IMPERATIVE_VERBS, (
                f"{name} description must start with approved imperative verb {APPROVED_IMPERATIVE_VERBS}, got '{first_word}'"
            )

            # Rule 4: Zero forbidden jargon
            for jargon in FORBIDDEN_JARGON_TERMS:
                assert jargon not in desc.lower(), (
                    f"{name} description contains forbidden jargon term '{jargon}': '{desc}'"
                )

    print("  -> Passed! All descriptions across all difficulties are <= 100 chars, follow the canonical 1-sentence formula, and contain zero jargon.\n")


def test_solution_key_spec():
    print("Test 4: Verifying Solution Key Monospaced Layout, Indentation & Width Limits...")
    bundle = generate_daily_bundle(difficulty="medium")
    bundle["show_solutions"] = True
    receipt_bytes = build_daily_receipt_bytes(bundle)
    receipt_text = receipt_bytes.decode("latin-1")

    # 1. Check master header
    assert "------------------------------------------------" in receipt_text
    assert "[ SOLUTION KEY ]" in receipt_text

    # Extract solution key text
    key_start = receipt_text.find("[ SOLUTION KEY ]")
    assert key_start != -1
    key_text = receipt_text[key_start:]

    # Strip ESC and GS hardware control sequences to get clean printable text
    clean_key_text = re.sub(r'\x1b[a-zA-Z@!][\x00-\xff]?|\x1d[a-zA-Z@!][\x00-\xff]?', '', key_text)

    # 2. Check each game subtitle matches strictly one-word uppercase
    for title in APPROVED_TITLES:
        # Title must appear as a standalone subtitle line
        pattern = rf"(?:^|\n){re.escape(title)}\n"
        assert re.search(pattern, clean_key_text), f"Missing solution subtitle for '{title}' in Solution Key"

    # 3. Check line width restriction (<= 48 characters for every line)
    lines = clean_key_text.split("\n")
    for line in lines:
        clean = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', line)
        assert len(clean) <= 48, (
            f"Solution key line exceeds 48 characters ({len(clean)} chars): '{clean}'"
        )

    # 4. Check safe indent (6 spaces) for grid and stacked solutions
    for grid_title in ["SUDOKU", "NONOGRAM", "BINARY", "MINES", "KILLER", "TANGO", "STARS", "LADDER", "BRIDGES", "TENTS", "LIGHTS", "LOOP"]:
        idx = clean_key_text.find(f"\n{grid_title}\n")
        assert idx != -1
        grid_section = clean_key_text[idx + len(grid_title) + 2 : idx + len(grid_title) + 200]
        first_grid_line = grid_section.split("\n")[0]
        assert first_grid_line.startswith("      "), (
            f"{grid_title} grid line does not have 6 spaces left padding: '{first_grid_line}'"
        )

    print("  -> Passed! Solution Key adheres strictly to 48-column ESC/POS constraints, 6-space indentation, and single-word subtitles.\n")


def test_simulator_consistency():
    print("Test 5: Verifying Simulator Template & Header Call Consistency...")
    sim_path = os.path.join(os.path.dirname(__file__), "..", "simulator", "receipt_simulator.html")
    assert os.path.exists(sim_path), f"Simulator file not found at {sim_path}"

    with open(sim_path, "r", encoding="utf-8") as f:
        sim_content = f.read()

    # 1. Search header call must NOT pass difficulty in simulator
    # Correct: addStandardPuzzleHeader(items, 'SEARCH', null, searchDesc) or without wsDiff
    search_call_match = re.search(r"addStandardPuzzleHeader\s*\(\s*items\s*,\s*['\"]SEARCH['\"]\s*,\s*([^,)]+)", sim_content)
    assert search_call_match, "Could not find addStandardPuzzleHeader call for SEARCH in simulator"
    diff_arg = search_call_match.group(1).strip()
    assert diff_arg in ("null", "undefined", "None", "false"), (
        f"Simulator must NOT pass difficulty to SEARCH header! Found '{diff_arg}'. SEARCH is theme-driven."
    )

    # 2. Check PUZZLE_INSTRUCTIONS table lengths
    instr_block_match = re.search(r"const\s+PUZZLE_INSTRUCTIONS\s*=\s*\{([^}]+)\};", sim_content)
    assert instr_block_match, "Could not find PUZZLE_INSTRUCTIONS in simulator"
    instr_block = instr_block_match.group(1)

    for line in instr_block.split("\n"):
        line = line.strip()
        if not line or not line.startswith("'"):
            continue
        m = re.match(r"'([A-Z]+)'\s*:\s*'([^']+)'", line)
        if m:
            game_name, text = m.group(1), m.group(2)
            assert len(text) <= 100, f"Simulator PUZZLE_INSTRUCTIONS for {game_name} exceeds 100 chars ({len(text)}): '{text}'"
            assert game_name in APPROVED_TITLES, f"Unknown game {game_name} in simulator PUZZLE_INSTRUCTIONS"

    print("  -> Passed! Simulator templates and header calls strictly match canonical specification.\n")


def test_plugin_contract_compliance():
    print("Test 6: Verifying BasePuzzle Contract & Auto-Discovery on DEFAULT_REGISTRY...")
    plugins = DEFAULT_REGISTRY.get_all()
    assert len(plugins) == len(APPROVED_TITLES), f"Expected {len(APPROVED_TITLES)} registered plugins, found {len(plugins)}"

    for p in plugins:
        # 1. Type validation
        assert isinstance(p, BasePuzzle), f"{p} must inherit from BasePuzzle"

        # 2. Identifier validation
        assert p.puzzle_id and p.puzzle_id.islower(), f"Invalid puzzle_id: '{p.puzzle_id}'"
        assert p.title and p.title.isupper() and len(p.title.split()) == 1, f"Invalid title: '{p.title}'"
        assert p.title in APPROVED_TITLES, f"Title '{p.title}' not in APPROVED_TITLES"

        # 3. Test generation & contract methods
        res = p.generate(difficulty="medium")
        assert isinstance(res, BasePuzzleResult), f"{p.title} generate() must return BasePuzzleResult"
        assert isinstance(res.to_dict(), dict), f"{p.title} to_dict() must return a dict"

        # 4. Instruction verification
        instr = p.get_instruction(res)
        assert len(instr) <= 100, f"{p.title} instruction exceeds 100 chars: '{instr}'"
        assert instr.endswith("."), f"{p.title} instruction must end with period: '{instr}'"
        assert instr.split()[0] in APPROVED_IMPERATIVE_VERBS, f"{p.title} instruction verb invalid: '{instr}'"

        # 5. ASCII puzzle formatting
        ascii_art = p.format_ascii_puzzle(res)
        assert isinstance(ascii_art, str) and len(ascii_art) > 0, f"{p.title} ASCII formatting empty"

        # 6. Solution key formatting
        sol_lines = p.format_solution_key(res)
        assert isinstance(sol_lines, list) and len(sol_lines) > 0, f"{p.title} solution lines empty"
        for line in sol_lines:
            assert len(line) <= 48, f"{p.title} solution line exceeds 48 chars: '{line}'"

        # 7. Raster rendering
        raster = p.render_raster(res)
        assert isinstance(raster, (bytes, bytearray)) and len(raster) >= 8, f"{p.title} raster invalid"
        assert raster[0:4] == bytes([0x1D, 0x76, 0x30, 0x00]), f"{p.title} raster missing GS v 0 header"

    print(f"  -> Passed! All {len(plugins)} plugins strictly comply with BasePuzzle contracts and standards.\n")


def test_master_receipt_header_and_footer():
    print("Test 7: Verifying Master Receipt Header & Footer Offline Standards across Targets...")
    base_dir = os.path.join(os.path.dirname(__file__), "..")

    # 1. Python DailyReceiptComposer output
    bundle = generate_daily_bundle(difficulty="medium")
    receipt_bytes = build_daily_receipt_bytes(bundle)
    receipt_text = receipt_bytes.decode("latin-1")
    assert "MORNING PUZZLES" in receipt_text, "Python receipt missing MORNING PUZZLES header"
    assert "Enjoy your morning puzzles" in receipt_text, "Python receipt missing offline header tagline"
    assert "Enjoy your day!" in receipt_text, "Python receipt missing 'Enjoy your day!' footer"
    assert "diagnostics" not in receipt_text.lower(), "Python receipt contains forbidden diagnostics"

    # 2. ESP32 Firmware OfflinePuzzleComposer.cpp
    fw_composer = os.path.join(base_dir, "esp32-firmware", "src", "generators", "OfflinePuzzleComposer.cpp")
    with open(fw_composer, "r") as f:
        fw_src = f.read()
    assert '"MORNING PUZZLES"' in fw_src, "Firmware missing MORNING PUZZLES"
    assert '"Enjoy your morning puzzles"' in fw_src, "Firmware missing 'Enjoy your morning puzzles'"
    assert '"Enjoy your day!"' in fw_src, "Firmware missing 'Enjoy your day!'"
    assert "diagnostics" not in fw_src.lower(), "Firmware composer contains diagnostics"

    # 3. Arduino IDE Sketch OfflinePuzzleComposer.cpp
    ino_composer = os.path.join(base_dir, "MorningPuzzles", "OfflinePuzzleComposer.cpp")
    with open(ino_composer, "r") as f:
        ino_src = f.read()
    assert '"MORNING PUZZLES"' in ino_src, "Arduino sketch missing MORNING PUZZLES"
    assert '"Enjoy your morning puzzles"' in ino_src, "Arduino sketch missing 'Enjoy your morning puzzles'"
    assert '"Enjoy your day!"' in ino_src, "Arduino sketch missing 'Enjoy your day!'"

    # 4. Web Simulator receipt_simulator.html
    sim_path = os.path.join(base_dir, "simulator", "receipt_simulator.html")
    with open(sim_path, "r") as f:
        sim_src = f.read()
    assert "'MORNING PUZZLES'" in sim_src or '"MORNING PUZZLES"' in sim_src, "Simulator missing MORNING PUZZLES"
    assert "Enjoy your morning puzzles" in sim_src, "Simulator missing 'Enjoy your morning puzzles'"
    assert "Enjoy your day!" in sim_src, "Simulator missing 'Enjoy your day!'"

    print("  -> Passed! Master receipt header and footer strictly adhere to offline standards across all 4 targets.\n")


def test_playable_cells_cleanliness():
    print("Test 8: Verifying Clean Playable Cells Standard (No Center Dots / Guide Marks)...")
    base_dir = os.path.join(os.path.dirname(__file__), "..")

    # In Mines, Nonogram, and Tents generators, empty/playable cells must not have center dots
    files_to_check = [
        os.path.join(base_dir, "esp32-firmware", "src", "generators", "MinesGen.cpp"),
        os.path.join(base_dir, "esp32-firmware", "src", "generators", "NonogramGen.cpp"),
        os.path.join(base_dir, "esp32-firmware", "src", "generators", "TentsGen.cpp"),
        os.path.join(base_dir, "MorningPuzzles", "MinesGen.cpp"),
        os.path.join(base_dir, "MorningPuzzles", "NonogramGen.cpp"),
        os.path.join(base_dir, "MorningPuzzles", "TentsGen.cpp"),
        os.path.join(base_dir, "server", "app", "puzzles", "mines.py"),
        os.path.join(base_dir, "server", "app", "puzzles", "nonogram.py"),
    ]

    for fpath in files_to_check:
        with open(fpath, "r") as f:
            src = f.read()
        assert "dotX" not in src, f"{os.path.basename(fpath)} still contains phantom dot rendering (dotX)"
        assert "dotY" not in src, f"{os.path.basename(fpath)} still contains phantom dot rendering (dotY)"

    print("  -> Passed! Empty playable cells remain clean across all targets with zero phantom dots.\n")


if __name__ == "__main__":
    print("==================================================================")
    print("RUNNING MORNING PUZZLES PRESENTATION & AUTHORING STANDARDS TESTS")
    print("==================================================================\n")

    test_titles_and_forbidden_terms()
    test_difficulty_presentation_and_theme_rules()
    test_description_length_and_canonical_formula()
    test_solution_key_spec()
    test_simulator_consistency()
    test_plugin_contract_compliance()
    test_master_receipt_header_and_footer()
    test_playable_cells_cleanliness()

    print("==================================================================")
    print("ALL PRESENTATION & AUTHORING STANDARDS TESTS PASSED (8/8)!")
    print("==================================================================")

