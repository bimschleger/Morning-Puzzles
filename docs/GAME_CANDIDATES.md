# Candidate Logic Games: Evaluation & Implementation Reference

This document provides the definitive architectural survey, ranking, and technical specification for potential new logic and deduction games to expand the **Morning Puzzles** ecosystem (featuring **Sudoku**, **Search**, **Nonogram**, **Stars**, **Jumble**, **Binary**, **Mines**, **Tents**, **Bridges**, **Killer**, and **Cryptogram**).

Every candidate has been evaluated against three non-negotiable criteria:
1. **Thermal Printability**: Feasibility of clean rendering on 80mm thermal receipt paper ($576\text{ dots}$ printable width, $321\text{px}$ inner canvas, 1-bit monochrome, comfortable pencil-solving space).
2. **Open-Source Procedural Generation**: Availability of mature open-source engines (MIT, Apache 2.0, or BSD) capable of generating novel, randomized puzzles on demand without reliance on static databases.
3. **Allowable Output & Solvability Guarantees**: Mathematical proof of a single unique solution and 100% human-deducible logic with **zero guessing** required.

---

## 1. Candidate Comparison Matrix

| Rank | Single-Word Title | Traditional Name | Status | Open-Source Engine | License | Implementation Stack | Thermal Print Fit | Generation Maturity | Allowable Output Guarantee |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **1** | **BRIDGES** | Hashiwokakero | **Included** | Simon Tatham (`bridges.c`) / IBM chuk-gym | **MIT** / **Apache 2.0** | Pure ANSI C / Python | **10 / 10** | High (Spanning tree + solver) | Guaranteed unique; fully connected graph |
| **2** | **BINARY** | Takuzu / Binairo | **Included** | Simon Tatham (`unruly.c`) / IBM chuk-gym #4 | **MIT** / **Apache 2.0** | Pure ANSI C / Python | **10 / 10** | High (Backtracking + CP-SAT) | Guaranteed unique; no trios, equal 0/1, unique lines |
| **3** | **MINES** | Solitaire Minesweeper | **Included** | Simon Tatham (`mines.c`) / CP-SAT generator | **MIT** / **Apache 2.0** | Pure ANSI C / Python | **9.7 / 10** | High (Deductive no-guess solver) | Guaranteed unique; 100% solvable without guessing |
| **4** | **HITORI** | Hitori (Nikoli) | Candidate | Simon Tatham (`hitori.c`) | **MIT** | Pure ANSI C | **9.6 / 10** | High (Backtracking pruner) | Guaranteed unique; 100% connected white cells |
| **5** | **LOOP** | Slitherlink | Candidate | Simon Tatham (`loopy.c`) | **MIT** | Pure ANSI C | **9.5 / 10** | Very High (Deductive loop solver) | Guaranteed unique; 1 closed loop, no branches |
| **6** | **TENTS** | Tents & Trees | **Included** | Simon Tatham (`tents.c`) | **MIT** / **Apache 2.0** | Pure ANSI C / Python | **9.3 / 10** | High (Matching engine + pruner) | Guaranteed unique; 1:1 tree-tent pairing |
| **7** | **CALCU** | Calcudoku / KenKen | Candidate | Simon Tatham (`keen.c`) | **MIT** | Pure ANSI C | **9.0 / 10** | High (Latin square + cage solver) | Guaranteed unique; valid integer arithmetic |
| **8** | **FUTOSHIKI** | Futoshiki / Unequal | Candidate | Simon Tatham (`unequal.c`) | **MIT** | Pure ANSI C | **9.0 / 10** | High (Latin square + poset solver) | Guaranteed unique; no cyclical inequalities |
| **9** | **KAKURO** | Cross Sums | Candidate | Simon Tatham (`kakuro.c`) | **MIT** | Pure ANSI C | **8.7 / 10** | High (Crossword fill + partition solver)| Guaranteed unique; no duplicate digits per run |
| **10**| **FLEET** | Battleships / Bimaru | Candidate | Simon Tatham (`pearl.c` variant) / Solitaire Battleship | **MIT** / **Apache 2.0** | C / Python (CP-SAT) | **8.5 / 10** | Medium-High (Fleet placer + SAT solver)| Guaranteed unique; non-touching ship bounds |

---

## 2. Detailed Game Profiles

### 1. BRIDGES (`--- BRIDGES ---`)
* **Traditional Names**: Hashiwokakero, Hashi, Bridges.
* **Core Rules**:
  1. The grid contains circular "islands" with numbers $1..8$.
  2. The player draws horizontal and vertical lines ("bridges") connecting adjacent islands.
  3. Up to two bridges may connect any pair of islands.
  4. Bridges may not cross other bridges or islands.
  5. The number of bridges attached to an island must exactly match its number.
  6. All islands must form a single connected network (spanning graph).
* **Thermal Print Layout**:
  * Grid: $7\times 7$ ($45\text{px}$ cells), $8\times 8$ ($40\text{px}$ cells), or $9\times 9$ ($35\text{px}$ cells).
  * Islands: $26\text{px}$ diameter circles (Tier 3 outline $1.8\text{px}$) with bold centered digit.
  * Inter-island space: Clean white paper, providing comfortable room for pencil tracks.
* **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`bridges.c`, MIT License).
* **Allowable Output Validation**:
  * Generates random spanning tree to ensure full connectedness, then adds edges up to degree 8.
  * Deductive solver simulates human techniques (island saturation, cut-node isolation avoidance).
  * Discards boards if guessing is required or $>1$ solution exists.

---

### 2. BINARY (`--- BINARY ---`)
* **Traditional Names**: Takuzu, Binairo, Binary Puzzle (IBM chuk-gym #4, binarypuzzle.com).
* **Core Rules**:
  1. Each cell must contain either a `0` or a `1`.
  2. No more than two identical numbers may be placed directly adjacent horizontally or vertically (neither `000` nor `111` may appear anywhere).
  3. Each row and column must contain an equal number of zeros and ones ($N/2$ zeros, $N/2$ ones).
  4. Each row is unique, and each column is unique (no two rows or two columns can be identical).
* **Difficulty Tiers**:
  * **Easy** ($6\times 6$): Direct trio blocking (`0 0 _` $\implies 1$; `1 _ 1` $\implies 0$) and row/col capacity counting.
  * **Medium** ($8\times 8$): 1-step lookahead combining trio blocking with line capacity limits.
  * **Hard** ($8\times 8$ or $10\times 10$): Rule 4 row/column uniqueness comparison against completed lines.
* **Thermal Print Layout**:
  * Geometry: $6\times 6$ ($53\text{px}$ cells) or $8\times 8$ ($40\text{px}$ cells).
  * Outer border: Tier 1 ($3.5\text{px}$ solid black).
  * Gridlines: Tier 4 ($1.0\text{px}$).
  * Clues: Centered bold `"Space Mono"` characters (`0` and `1`).
  * Empty cells: White square space for pencil entries.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`unruly.c`, MIT License) and IBM `chuk-puzzles-gym` Classic Logic Puzzle #4 (`takuzu.py`, Apache 2.0).
* **Allowable Output Validation**:
  * Verifies that the completed grid satisfies all 4 rules.
  * Iterative clue pruning checks that remaining clues admit strictly one unique solution solvable without bifurcation/guessing.

---

### 3. MINES (`--- MINES ---`)
* **Traditional Names**: Solitaire Minesweeper, Paper Minesweeper (puzzle-magazine.com).
* **Core Rules**:
  1. A rectangular grid (e.g. $8\times 8$ or $8\times 10$).
  2. Numbered clue cells ($0..8$) indicate how many of the 8 surrounding cells contain a mine.
  3. Numbered cells are safe (cannot contain a mine).
  4. Unrevealed cells are either a **Mine** or **Empty/Safe**.
  5. The total number of mines in the puzzle is given in the header (e.g. `12 MINES`).
* **Difficulty Tiers**:
  * **Easy**: Direct neighbor saturation and zero-clearing.
  * **Medium**: 2-cell subset difference logic (e.g. 1-2-1 and 1-2-2-1 patterns).
  * **Hard**: Global mine count capacity constraints combined with disjoint boundary analysis.
* **Pure Deduction Guarantee**:
  * Unlike computer Minesweeper, every puzzle is guaranteed **100% solvable by logic alone without guessing** (no 50/50 guesses).
* **Thermal Print Layout**:
  * $8\times 8$ ($40\text{px}$ cells) or $8\times 10$ ($40\text{px}$ cells).
  * Clue cells feature bold numbers.
  * Header displays difficulty and total mine count: `DIFFICULTY: MEDIUM (14 MINES)`.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`mines.c`, MIT License) with deductive solver, or CP-SAT exact-cover generator.

---

### 4. HITORI (`--- HITORI ---`)
* **Traditional Names**: Hitori (Nikoli).
* **Core Rules**:
  1. An $N \times N$ grid is completely filled with numbers.
  2. The player shades out duplicate numbers so that no number appears more than once in any row or column.
  3. Shaded cells never touch orthogonally (no two black cells share an edge).
  4. All unshaded cells form a single connected orthogonal group.
* **Thermal Print Layout**:
  * Identical geometry to Sudoku: $8\times 8$ ($40\text{px}$) or $9\times 9$ ($35\text{px}$).
  * High-contrast numbers in every cell; solvers cross out or shade cells with pencil.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`hitori.c`, MIT License).

---

### 5. LOOP (`--- LOOP ---`)
* **Traditional Names**: Slitherlink, Fences, Takegaki.
* **Core Rules**:
  1. A grid of dot intersections with clue numbers $0..3$ in some cells.
  2. Draw line segments between adjacent dots to form a single continuous closed loop without branches or self-intersections.
  3. Each number specifies how many of its 4 edges belong to the loop.
* **Thermal Print Layout**:
  * $8\times 8$ ($40\text{px}$) or $10\times 10$ ($32\text{px}$) dot grid.
  * Prominent dot vertices ($4\text{px}$ circles) and centered numbers.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`loopy.c`, MIT License).

---

### 6. TENTS (`--- TENTS ---`)
* **Traditional Names**: Tents and Trees, Camping.
* **Core Rules**:
  1. Match each tree with an orthogonally adjacent tent (1:1 relationship).
  2. No two tents may touch each other, even diagonally.
  3. Row and column clue numbers specify the total tents in each line.
* **Thermal Print Layout**:
  * $8\times 8$ ($35\text{px}$ cells + margin) with 1-bit thermal pine tree icons and margin counts.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`tents.c`, MIT License).

---

### 7. CALCU (`--- CALCU ---`)
* **Traditional Names**: Calcudoku, KenKen, Mathdoku.
* **Core Rules**:
  1. $N \times N$ Latin square (digits $1..N$ once per row and column).
  2. Irregular polyomino cages display an arithmetic clue (e.g. `12+`, `3-`, `8x`, `2/`).
  3. Digits in each cage must calculate to the clue value using the operator.
* **Thermal Print Layout**:
  * $5\times 5$ ($64\text{px}$) or $6\times 6$ ($53\text{px}$).
  * Tier 2 heavy cage outlines ($2.5\text{px}$); operator clue in upper-left corner of cage.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`keen.c`, MIT License).

---

### 8. FUTOSHIKI (`--- FUTOSHIKI ---`)
* **Traditional Names**: Futoshiki, Unequal.
* **Core Rules**:
  1. Digits $1..N$ in each row and column without repeating.
  2. Inequality signs (`<`, `>`) between adjacent cells must be satisfied.
* **Thermal Print Layout**:
  * $5\times 5$ ($55\text{px}$) or $6\times 6$ ($46\text{px}$).
  * Minimalist grid with inequality symbols centered on cell borders.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`unequal.c`, MIT License).

---

### 9. KAKURO (`--- KAKURO ---`)
* **Traditional Names**: Kakuro, Cross Sums.
* **Core Rules**:
  1. Number crossword puzzle with black clue cells and white entry cells.
  2. White cells are filled with digits $1..9$.
  3. Digits in a continuous run must sum to the clue number and cannot repeat.
* **Thermal Print Layout**:
  * $8\times 8$ or $9\times 9$ grid with diagonal slashes dividing across and down sums.
* **Open-Source Engine**: Simon Tatham's PSTR Puzzles (`kakuro.c`, MIT License).

---

### 10. FLEET (`--- FLEET ---`)
* **Traditional Names**: Battleships, Solitaire Battleships, Bimaru.
* **Core Rules**:
  1. $10\times 10$ grid containing 10 hidden ships (1x4, 2x3, 3x2, 4x1).
  2. Ships cannot touch each other, even diagonally.
  3. Numbers along top and left margins specify total ship segments per row/column.
* **Thermal Print Layout**:
  * $10\times 10$ grid ($30\text{px}$ cells + margins) using 1-bit ship glyphs.
* **Open-Source Engine**: `solitaire-battleship` / Simon Tatham variant / CP-SAT.
