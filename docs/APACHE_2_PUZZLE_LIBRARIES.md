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

---

## 3. Integrating with IBM chuk-puzzles-gym

For advanced users wishing to plug directly into the full IBM benchmarking environment:

```bash
git clone https://github.com/IBM/chuk-puzzles-gym.git
cd chuk-puzzles-gym
pip install -e .
```

The modules in `server/app/generators/` are self-contained drop-in implementations under the Apache 2.0 license that can run standalone with zero mandatory external dependencies.
