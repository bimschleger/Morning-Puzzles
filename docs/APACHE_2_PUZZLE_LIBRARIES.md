# Apache 2.0 Open-Source Puzzle Generation Libraries

This document provides a technical survey and implementation reference for the open-source puzzle generators used in **Morning Puzzles**, all licensed under or compatible with the **Apache 2.0** license.

---

## 1. Summary of Libraries

| Puzzle | Recommended Package / Repository | License | Implementation Stack | Difficulty Parameters |
| :--- | :--- | :--- | :--- | :--- |
| **Sudoku** | [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) *(or [jhunters/sudoku](https://github.com/jhunters/sudoku))* | **Apache 2.0** | Python (OR-Tools CP-SAT) / Go | `easy` (~38 clues), `medium` (~30 clues), `hard` (~25 clues). Uniqueness guarantee. |
| **Word Search** | [craigk5n/wordsearch](https://github.com/craigk5n/wordsearch) | **Apache 2.0** | Python | Levels 1–9. Controls allowed directions (forward, diagonal, reverse) and decoy words. |
| **Nonogram** | [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) *(or [141512114/pixle](https://github.com/141512114/pixle))* | **Apache 2.0** | Python (OR-Tools CP-SAT) | `easy` (5x5 / 8x8), `medium` (10x10), `hard` (15x15). Verifies line deduction uniqueness. |
| **Star Battle / Queens** | [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) | **Apache 2.0** | Python (OR-Tools CP-SAT) | 1-Star (Queens style) vs 2-Star (classic Star Battle). Grid sizes 6x6 to 10x10, region shapes. |
| **Jumble** | Native Apache 2.0 Module (`server/app/generators/jumble_gen.py`) | **Apache 2.0** | Python (Standard Library) | `easy` (4–5 letters), `medium` (5–6 letters), `hard` (6–7 letters). Punny riddle solutions. |
| **Binary** | [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) *(Classic #4 / Takuzu)* | **Apache 2.0** | Python / Native C++ | `easy` (6x6), `medium` (8x8), `hard` (8x8). Trio avoidance, line capacity, and line uniqueness guarantees. |
| **Mines** | Simon Tatham Portable Puzzle Collection (`mines.c`) / Native Module | **Apache 2.0 / MIT** | Python / Native C++ | `easy` (8 mines, 28 clues), `medium` (12 mines, 22 clues), `hard` (15 mines, 17 clues). 100% deductive solvability (zero guessing). |
| **Tents** | Simon Tatham Portable Puzzle Collection (`tents.c`) / Native Module | **Apache 2.0 / MIT** | Python / Native C++ | `easy` (6x6, 4–5 trees), `medium` (8x8, 8–9 trees), `hard` (8x8, 10–12 trees). 1:1 tree-tent matching, non-touching, line clues. |
| **Bridges** | Simon Tatham Portable Puzzle Collection (`bridges.c`) / Native Module | **Apache 2.0 / MIT** | Python / Native C++ | `easy` (6x6, 6–8 islands), `medium` (8x8, 10–12 islands), `hard` (8x8, 14–16 islands). Single connected spanning graph, degree saturation. |

---

## 2. Detailed Technical Breakdown

### A. Sudoku (`sudoku_gen.py`)
*   **Upstream Project**: [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) (Apache 2.0)
*   **Algorithmic Approach**: Backtracking solver with constraint propagation and candidate elimination.
*   **Unique Solution Guarantee**: When numbers are randomly removed from the filled board, the solver runs in counting mode (stopping if solutions $\ge 2$). If a removed number results in multiple solutions, the number is restored.
*   **Difficulty Scaling**:
    *   `easy`: 36–40 clues remaining (suitable for quick morning solving).
    *   `medium`: 30–35 clues remaining.
    *   `hard`: 24–29 clues remaining (requires advanced techniques: naked pairs, pointing pairs).

### B. Word Search (`wordsearch_gen.py`)
*   **Upstream Project**: [craigk5n/wordsearch](https://github.com/craigk5n/wordsearch) (Apache 2.0)
*   **Algorithmic Approach**: Bounded vector placement with collision validation against shared letters.
*   **Difficulty Scaling**:
    *   `easy`: Only horizontal left-to-right (`E`) and vertical top-to-bottom (`S`).
    *   `medium`: Horizontal, vertical, and forward diagonals (`E`, `S`, `SE`, `NE`).
    *   `hard`: All 8 directions including backwards horizontal (`W`), upward vertical (`N`), and reverse diagonals (`SW`, `NW`).
*   **Thermal Receipt Layout**: Default grid size is 12x12 (leaving 2 spaces between columns across the 48-character 80mm line) with a 2-column checklist of words below the grid.

### C. Nonogram / Picross (`nonogram_gen.py`)
*   **Upstream Project**: [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) (Apache 2.0)
*   **Algorithmic Approach**: Computes run-length encoded (RLE) blocks across rows and columns.
*   **Difficulty Scaling**:
    *   `easy`: 5x5 grid (fast, highly visual).
    *   `medium`: 10x10 grid (balanced morning challenge).
    *   `hard`: 15x15 grid (fits comfortably across 80mm thermal receipt paper).

### D. Queens / Star Battle (`queens_gen.py`)
*   **Upstream Project**: [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) (Star Battle module) (Apache 2.0)
*   **Rules**:
    *   **1-Star (LinkedIn Queens)**: $N \times N$ grid partitioned into $N$ contiguous color/letter regions. Place exactly 1 Queen per row, column, and region. No two Queens may touch orthogonally or diagonally.
    *   **2-Star (Classic Star Battle)**: Place exactly 2 Stars per row, column, and region. No two Stars may touch orthogonally or diagonally.
*   **Difficulty Scaling**:
    *   `easy`: 6x6 grid, 1-Star (Queens).
    *   `medium`: 8x8 grid, 1-Star (Queens).
    *   `hard`: 9x9 or 10x10 grid, 2-Star.

### E. Jumble / Word Scramble (`jumble_gen.py`)
*   **License**: Apache 2.0 (included directly in `server/app/generators/jumble_gen.py`)
*   **Structure**: 4 scrambled words with designated circled letter positions.
*   **Clue Riddle**: The circled letters form an anagram that answers a punchline riddle printed at the bottom of the section.
*   **Difficulty Scaling**: Controlled by word length (4 letters = easy, 5 letters = medium, 6–7 letters = hard) and letter scramble distance.

### F. Binary / Takuzu (`binary_gen.py` & `BinaryGen.cpp`)
*   **Upstream Project**: [IBM/chuk-puzzles-gym](https://github.com/IBM/chuk-puzzles-gym) Classic Logic Puzzle #4 / Simon Tatham `unruly.c`
*   **Rules**:
    *   Each cell contains `0` or `1`.
    *   No more than two identical numbers may be placed directly adjacent in any row or column (no `000` or `111`).
    *   Each row and column contains an equal count of zeros and ones ($N/2$ zeros, $N/2$ ones).
    *   Each row is unique, and each column is unique (no two rows or columns identical).
*   **Difficulty Scaling**:
    *   `easy`: 6x6 grid (~16 clues, solved via direct trio blocking and row/col capacity).
    *   `medium`: 8x8 grid (~28 clues, solved via 1-step lookahead and line capacity).
    *   `hard`: 8x8 grid (~22 clues, requires Rule 4 row/column uniqueness comparison against completed lines).
*   **Thermal Receipt Layout**: $6\times 6$ ($53\text{px}$ cells) or $8\times 8$ ($40\text{px}$ cells) framed by a Tier 1 perimeter border ($3.5\text{px}$) with centered Space Mono digits and generous handwriting space.

### G. Mines / Solitaire Minesweeper (`mines_gen.py` & `MinesGen.cpp`)
*   **Upstream Reference**: Simon Tatham's Portable Puzzle Collection (`mines.c`) / `puzzle-magazine.com` Analog Paper Minesweeper
*   **Deductive Logic Rules (Zero Guessing Guarantee)**:
    1. **Direct Saturation**: If remaining unrevealed neighbors equal remaining mines needed, all remaining unrevealed cells are mines.
    2. **Direct Clearing**: If a clue's mine requirement is satisfied, all other unrevealed neighbors are guaranteed safe (empty).
    3. **Subset Difference**: If clue $A$'s unknown neighbors form a strict subset of clue $B$'s unknown neighbors, the set difference contains exactly $mines(B) - mines(A)$ mines.
    4. **Global Mine Capacity**: If the total count of discovered mines equals the total grid quota, all remaining unrevealed cells are safe (and vice versa).
*   **Difficulty Scaling**:
    *   `easy`: 8x8 grid, 8 mines, ~28 clues (direct saturation and clearing).
    *   `medium`: 8x8 grid, 12 mines, ~22 clues (2-cell subset overlap difference logic).
    *   `hard`: 8x8 grid, 15 mines, ~17 clues (global capacity counting and multi-clue subset chains).
*   **Thermal Receipt Layout**: $8\times 8$ grid ($40\text{px}$ cells) framed by a Tier 1 perimeter border ($3.5\text{px}$) with centered Space Mono clue digits ($0..8$), total mine count context header (`TOTAL MINES: [COUNT]`), and empty white cells for pencil marking.

### H. Tents / Tents and Trees (`tents_gen.py` & `TentsGen.cpp`)
*   **Upstream Reference**: Simon Tatham's Portable Puzzle Collection (`tents.c`)
*   **Rules**:
    *   Match each pine tree with an orthogonally adjacent tent (1:1 pairing).
    *   No two tents may touch each other, even diagonally.
    *   Numbers along margins specify the exact number of tents in each row and column.
*   **Difficulty Scaling**:
    *   `easy`: 6x6 grid, 4–5 trees/tents (direct line saturation and corner tree matching).
    *   `medium`: 8x8 grid, 8–9 trees/tents (2-cell subset overlap and diagonal exclusion logic).
    *   `hard`: 8x8 grid, 10–12 trees/tents (chain capacity deductions across rows and columns).
*   **Thermal Receipt Layout**: Grid framed by Tier 1 perimeter border ($3.5\text{px}$), 1-bit pine tree icons ($1.8\text{px}$ stroke), and Space Mono clue counts outside the grid.

### I. Bridges / Hashiwokakero (`bridges_gen.py` & `BridgesGen.cpp`)
*   **Upstream Reference**: Simon Tatham's Portable Puzzle Collection (`bridges.c`) / IBM chuk-gym
*   **Rules**:
    *   Connect numbered circular islands with horizontal and vertical bridges.
    *   Up to two bridges may connect any pair of islands.
    *   Bridges may not cross other bridges or islands.
    *   Each island's connected bridge count must match its number ($1..8$).
    *   All islands must form a single connected network (spanning graph).
*   **Difficulty Scaling**:
    *   `easy`: 6x6 grid, 6–8 islands (direct degree saturation and corner degree limits).
    *   `medium`: 8x8 grid, 10–12 islands (cut-node isolation avoidance and 2-step lookahead).
    *   `hard`: 8x8 grid, 14–16 islands (islands up to degree 6–8, complex network spanning constraints).
*   **Thermal Receipt Layout**: Clean grid with $26\text{px}$ circular island badges ($1.8\text{px}$ stroke) and generous unprinted whitespace corridors for pencil line drawings.

---

## 3. Integrating with IBM chuk-puzzles-gym

For advanced users wishing to plug directly into the full IBM benchmarking environment:

```bash
git clone https://github.com/IBM/chuk-puzzles-gym.git
cd chuk-puzzles-gym
pip install -e .
```

The modules in `server/app/generators/` are self-contained drop-in implementations under the Apache 2.0 license that can run standalone with zero mandatory external dependencies.
