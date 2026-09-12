---
description: Standards for Morning Puzzles game naming, difficulty representation, description authoring, and solution key layout
trigger: always_on
---

# Morning Puzzles: Game Naming, Description, Difficulty & Solution Key Standards

All agents and contributors working on Morning Puzzles must strictly follow these non-negotiable presentation and formatting standards across the Python backend, ESP32 firmware, and Web Simulator:

## 1. Game Titles & Naming
- **Strict One-Word Uppercase Title**: Every puzzle must have a single uppercase English word enclosed in triple dashes: `--- [TITLE] ---` (e.g., `--- STARS ---`, `--- SUDOKU ---`, `--- SEARCH ---`, `--- NONOGRAM ---`, `--- JUMBLE ---`, `--- BINARY ---`, `--- MINES ---`, `--- TENTS ---`, `--- BRIDGES ---`, `--- KILLER ---`).
- **Forbidden Titles**: Multi-word titles, subtitles, or slash-separated aliases (*"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, *"Nonogram / Picross"*, *"Tents and Trees"*, *"Hashiwokakero"*) are strictly prohibited.
- **Subtitles in Solution Key**: Strictly single uppercase word matching the title, without dashes (e.g. `SUDOKU`, `SEARCH`, `NONOGRAM`, `STARS`, `JUMBLE`, `BINARY`, `MINES`, `TENTS`, `BRIDGES`, `KILLER`).
- **No Duplicate In-Canvas Titles**: Canvas graphics and ASCII renderers must not draw duplicate banner titles inside the puzzle board.

## 2. Difficulty Representation & Placement
- **Vertical Hierarchy**: When applicable, placed **immediately below the title header and immediately above the one-sentence gameplay instruction**:
  ```text
  --- [TITLE] ---
  DIFFICULTY: [LEVEL]
  [One-sentence instruction line]
  ```
- **Format**: Centered, uppercase, prefixed by `DIFFICULTY: ` (`DIFFICULTY: EASY`, `DIFFICULTY: MEDIUM`, `DIFFICULTY: HARD`, `DIFFICULTY: MASTER`, `DIFFICULTY: EXPERT`, `DIFFICULTY: EXTREME`).
- **Theme-Driven Exception**: Puzzles driven by theme rather than difficulty (`SEARCH`) **must completely omit** the difficulty line.

## 3. Gameplay Descriptions
- **Strict Character Limit ($\le 100$ Characters)**: The fully interpolated description string (including any dynamically inserted quantities) must **never exceed 100 characters** to guarantee clean $\le 2$-line wrapping at 44 printable columns on 80mm thermal receipt paper.
- **Canonical One-Sentence Formula**:
  `[Imperative Verb] + [Target with Dynamic Quantity] + [Context / Clues] + [Constraint]`
- **Approved Imperative Verbs**: Must begin directly with an action verb (*Place, Fill, Deduce, Connect, Pitch, Shade, Unscramble, Find*).
- **Dynamic Parameterization**: If difficulty alters any quantitative property, dynamically inject the exact count (e.g., `Place 1 star...` vs `Place 2 stars...`, `Deduce all [8 / 12 / 15] hidden mines...`, `Pitch [4 / 8 / 11] tents...`, `Find all [N] hidden words...`, digits `1-4` vs `1-6`).
- **Plain English Over Jargon**: Avoid algorithmic/geometric jargon (*no "orthogonally adjacent", "in a row", "polyomino", "connected component", "bipartite matching"*).
- **Generator Ground Truth**: Only state what the generation algorithm actually creates (do not claim procedural nonograms reveal a pixel picture).

## 4. Solution Key Layout & Presentation
- **Master Header**: Delimited by 48 dashes, centered `[ SOLUTION KEY ]`, followed by 48 dashes.
- **Column Restriction**: Standard ESC/POS Font A 48-column line limit. No line may exceed 48 characters. Coordinate lists and word lists must wrap to $\le 46$ characters.
- **Indentation**: 6 spaces left padding (`'      '`) for 2D ASCII grids to ensure visual centering.
- **Blank Line Separation**: Exactly one blank line must separate each puzzle's solution block.

## 5. Automated Verification
All changes must pass the automated validation suite:
```bash
python3 server/test_puzzle_standards.py
python3 server/test_thermal_format.py
```
