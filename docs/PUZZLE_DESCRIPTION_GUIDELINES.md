# Morning Puzzles: Game Description & Header Authoring Guidelines

This document serves as the permanent reference standard for authoring puzzle titles, difficulty indicators, and one-sentence gameplay descriptions across the **Morning Puzzles** ecosystem (Web Simulator, Python Backend, and ESP32 Firmware).

All existing games—and any new puzzles added in the future—must strictly adhere to these rules.

---

## 1. Core Philosophy & Physical Constraints

Morning Puzzles are designed to print on **80mm thermal receipt printers** running ESC/POS monospace text and 1-bit bitmap graphics:
* **Horizontal Space**: Each physical line has a maximum printable width of **48 monospace characters** (or ~44 characters when styled with safe thermal padding).
* **Vertical Space**: Physical receipt paper is finite. Verbose tutorials, multi-sentence essays, and complex rules crowd out the interactive puzzle board and waste paper.
* **First-Time Solvers**: Players should understand the exact mechanical goal and rules within 3 seconds of reading the description.

---

## 2. The 6 Golden Rules

### Rule 1: Strict Character Limit ($\le 100$ Characters)
* **Maximum String Length**: The fully interpolated description string (including any dynamically inserted counts) must **never exceed 100 characters**.
* **Why**: At 44 characters per line, a 100-character string cleanly wraps into **at most 2 centered lines**. Any description longer than 100 characters spills onto 3 or 4 lines, degrading receipt layout.

### Rule 2: Single Uppercase Title Header
* **Format**: Strictly one uppercase English word enclosed in triple dashes: `--- [TITLE] ---` (e.g., `--- STARS ---`, `--- MINES ---`, `--- KAKURO ---`).
* **Forbidden**: Multi-word titles, subtitles, parenthetical notes, or slash-separated aliases (e.g., *"Star Battle"*, *"Queens / Star Battle"*, *"Word Search"*, *"Daily Jumble"*).

### Rule 3: The Canonical One-Sentence Formula
Every puzzle description must be **exactly one sentence** adhering to this formula:

$$\mathbf{[Imperative\ Verb]} + \mathbf{[Target\ with\ Dynamic\ Quantity]} + \mathbf{[Context\ /\ Clues]} + \mathbf{[Constraint]}$$

* **Imperative Verb**: Start directly with the player's core physical or logical action (*Place, Fill, Deduce, Connect, Pitch, Shade, Unscramble*).
* **Target with Dynamic Quantity**: Specify the exact quantity being placed, solved, or hunted.
* **Context / Clues**: Clarify where or how clues are provided (*"using the adjacent numbered clues"*, *"matching row and column counts"*).
* **Constraint**: State the core prohibitive rule (*"with no stars touching, even diagonally"*, *"with no more than two consecutive of each type"*).

### Rule 4: Dynamic Difficulty-Aware Parameterization
If difficulty alters any quantitative property of the puzzle, the description **must dynamically inject the exact count**:
* **Count Quotas**:
  - Stars: `Place 1 star...` (Easy/Medium) vs. `Place 2 stars...` (Hard/Master)
  - Mines: `Deduce all [8 / 12 / 15] hidden mines...`
  - Tents: `Pitch [4 / 8 / 11] tents...`
  - Word Search: `Find all [N] hidden words listed below.`
* **Dimension / Group Quotas**:
  - Binary: `Fill each row and column with three 0s and three 1s...` (6x6) vs. `four 0s and four 1s...` (8x8)

*Never leave the player guessing about how many targets exist in the grid.*

### Rule 5: Plain English over Geometric & Algorithmic Jargon
Translate formal graph theory and mathematical puzzle jargon into everyday spatial language:

| Technical / Algorithmic Jargon | Forbidden Phrasing | Approved Plain English |
| :--- | :--- | :--- |
| Orthogonal Adjacency | *"orthogonally adjacent"* | **"next to"** or **"horizontally and vertically"** |
| Contiguous Polyomino | *"irregular shaped region"* | **"region"** or **"zone"** |
| 2D Consecutive Identical Symbols | *"in a row"* (causes row/col confusion) | **"consecutive of each type"** |
| Connected Spanning Graph | *"single connected component"* | **"one network"** or **"single loop"** |
| Bipartite Matching | *"pair each tree 1-to-1"* | **"Pitch [N] tents next to trees"** |
| Non-Repeating Permutation | *"without repeating digits"* | **"without repeating"** or **"without repeats"** |

### Rule 6: Generator Ground Truth
Only describe what the generation engine guarantees:
* Do **not** claim a puzzle *"reveals a hidden pixel picture"* or *"draws an illustration"* if the puzzle generator outputs procedural or abstract patterns.
* Explicitly describe the sequence, block lengths, and spacing mechanics (e.g., for Nonograms: *"Shade blocks of cells matching each clue in order, separated by at least one empty cell."*).

---

## 3. Canonical Registry Matrix (Existing 9 Games)

| Puzzle | Difficulty / Variant | Canonical One-Sentence Gameplay Instruction | Chars |
| :--- | :--- | :--- | :---: |
| **STARS** | Easy / Med (1★)<br>Hard / Master (2★) | **1★**: `"Place 1 star in each row, column, and region with no stars touching, even diagonally."`<br>**2★**: `"Place 2 stars in each row, column, and region with no stars touching, even diagonally."` | **84**<br>**85** |
| **SUDOKU** | All | `"Fill every row, column, and 3x3 box with digits 1-9 without repeating."` | **71** |
| **SEARCH** | Dynamic Count | `"Find all [N] hidden words listed below."`<br>*(Fallback: `"Find all listed words hidden across the grid."`)* | **40**<br>*(46)* |
| **NONOGRAM** | All | `"Shade blocks of cells matching each clue in order, separated by at least one empty cell."` | **89** |
| **JUMBLE** | All | `"Unscramble each word, then use the circled letters to solve the riddle."` | **71** |
| **BINARY** | Easy (6x6)<br>Med / Hard (8x8) | **Easy**: `"Fill each row and column with three 0s and three 1s, with no more than two consecutive of each type."`<br>**Med/Hard**: `"Fill each row and column with four 0s and four 1s, with no more than two consecutive of each type."` | **99**<br>**98** |
| **MINES** | Easy (8)<br>Med (12)<br>Hard (15) | `"Deduce all [8 / 12 / 15] hidden mines using the adjacent numbered clues."` | **60–61** |
| **TENTS** | Easy (4)<br>Med (8)<br>Hard (11) | `"Pitch [4 / 8 / 11] tents next to trees without tents touching, matching row and column counts."` | **84–85** |
| **BRIDGES** | All | `"Connect all islands into one network using 1 or 2 lines matching each island's number."` | **88** |
| **KILLER** | Easy / Med (4x4)<br>Extreme (6x6) | `"Fill every row, column, and box with digits [1-4 / 1-6], matching cage sums without repeats."` | **84** |

---

## 4. Reference Implementations for Future Games

Use these pre-tested reference examples when expanding Morning Puzzles with new puzzle types:

| Puzzle | Proposed Header | Canonical Description Example | Length |
| :--- | :--- | :--- | :---: |
| **Battleships** | `--- BATTLESHIPS ---` | `"Place [N] ships matching row and column counts with no ships touching, even diagonally."` | 89 chars |
| **Kakuro** | `--- KAKURO ---` | `"Fill white runs with digits 1-9 without repeats so each group sums to its clue."` | 81 chars |
| **Slitherlink** | `--- SLITHERLINK ---` | `"Draw a single loop without branches, surrounding each number with that many lines."` | 84 chars |
| **Nurikabe** | `--- NURIKABE ---` | `"Shade cells to form numbered white islands matching their values surrounded by water."` | 86 chars |
| **Hitori** | `--- HITORI ---` | `"Shade duplicate numbers so no shaded cells touch and unshaded cells remain connected."` | 87 chars |
| **Masyu** | `--- MASYU ---` | `"Draw a single loop turning at black circles and passing straight through white circles."` | 88 chars |
| **Akari (Light Up)**| `--- AKARI ---` | `"Place light bulbs to illuminate all corridors without any two bulbs shining on each other."` | 92 chars |

---

## 5. Authoring Checklist for New Puzzles

Before submitting or committing a new puzzle description, verify:
- [ ] Title is strictly a single uppercase word enclosed by `--- [TITLE] ---`.
- [ ] Instruction starts immediately with an imperative verb (*Place, Fill, Draw, Shade, Connect, Deduce*).
- [ ] Total string length is strictly **$\le 100$ characters** for all difficulty configurations.
- [ ] Quantitative targets (target counts, dimensions, numbers) are parameterized dynamically.
- [ ] The sentence contains zero algorithmic jargon (*no "orthogonally adjacent", "polyomino", etc.*).
- [ ] Wraps into $\le 2$ lines on a 48-column thermal receipt without splitting words.
- [ ] Accurately represents what the generator actually creates without making false aesthetic promises.
