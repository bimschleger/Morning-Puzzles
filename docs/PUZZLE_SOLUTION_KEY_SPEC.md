# Morning Puzzles: ASCII Solution Key & Answer Presentation Specification

This specification defines the structural rules, monospaced layout geometry, character column limits, glyph vocabulary, and presentation standards for rendering the optional **Solution Key** across the **Morning Puzzles** ecosystem (Web Simulator, Python Backend, and ESP32 Firmware).

---

## 1. Physical & Font Constraints

* **Standard Character Pitch**: 48 columns per line (ESC/POS Font A, $12 \times 24\text{ dots}$ on 80mm paper at 203 DPI, $48 \times 12 = 576\text{ dots}$).
* **Line Width Restriction**: **No line may exceed 48 characters**. Any line exceeding 48 characters will cause undesirable line wrapping on thermal receipt hardware, destroying grid alignment.
* **Safe Left Indent**: For centered or visually balanced ASCII grids, use a fixed left margin (typically 6 spaces: `'      '`) so the puzzle grid sits comfortably within the 48-column thermal receipt.
* **Blank Line Separation**: Exactly **one blank line** must follow each game's solution block before the next game title.

---

## 2. Master Solution Key Header Structure

When the solution key is enabled, it is appended to the bottom of the receipt directly above the receipt footer, framed by dashed dividers:

```text
------------------------------------------------  <-- 48 dashes
                [ SOLUTION KEY ]                  <-- Centered title
------------------------------------------------  <-- 48 dashes

[GAME 1 SUBTITLE]
[Game 1 Solution Content]

[GAME 2 SUBTITLE]
[Game 2 Solution Content]
...
```

* **Section Delimiter**: A 48-character dashed rule (`-` repeated 48 times).
* **Section Header**: `[ SOLUTION KEY ]` centered in 48 columns.
* **Game Subtitle**: Strictly single-word uppercase matching [`docs/PUZZLE_HEADER_SPEC.md`](PUZZLE_HEADER_SPEC.md) (e.g. `SUDOKU`, `SEARCH`, `NONOGRAM`, `STARS`, `JUMBLE`, `BINARY`, `MINES`, `TENTS`, `BRIDGES`).

---

## 3. Standard Per-Game ASCII Formatting Rules

### A. SUDOKU (`SUDOKU`)
* **Format**: 9 rows of 9 digits separated by single spaces.
* **Indentation**: 6 spaces left padding (total width: $6 + 9 \times 2 - 1 = 23\text{ chars} \le 48$).
* **Example**:
  ```text
  SUDOKU
        5 3 4 6 7 8 9 1 2
        6 7 2 1 9 5 3 4 8
        1 9 8 3 4 2 5 6 7
        8 5 9 7 6 1 4 2 3
        4 2 6 8 5 3 7 9 1
        7 1 3 9 2 4 8 5 6
        9 6 1 5 3 7 2 8 4
        2 8 7 4 1 9 6 3 5
        3 4 5 2 8 6 1 7 9

  ```

### B. SEARCH (`SEARCH`)
* **Format**:
  * Line 1: `Theme: [THEME NAME]` (if theme metadata exists).
  * Line 2+: `Words: [WORD1], [WORD2], ...` word-wrapped to $\le 46$ characters per line.
* **Example**:
  ```text
  SEARCH
  Theme: MORNING
  Words: COFFEE, SUNRISE, TOAST, BREEZE,
  ALARM, CEREAL, NEWSPAPER, SHOWER

  ```

### C. NONOGRAM (`NONOGRAM`)
* **Format**: $N \times N$ character grid where each cell is separated by a space.
* **Glyphs**:
  * `* `: Shaded filled cell (unified boolean-placement glyph).
  * `. `: Unshaded empty cell.
* **Indentation**: 6 spaces left padding.
* **Example** (8x8):
  ```text
  NONOGRAM
        * . . * * * . *
        * * . * . * * .
        . . . * * . . .
        * . * . . * * .
        . * * . * . . *
        * . * * . * . .
        . * . * * . * .
        * * . . . * * *

  ```

### D. STARS (`STARS`)
* **Format**: $N \times N$ grid displaying `* ` for stars and `. ` for non-star squares.
* **Indentation**: 6 spaces left padding.
* **Example** (8x8):
  ```text
  STARS
        . . * . . . . .
        . . . . . . * .
        * . . . . . . .
        . . . . * . . .
        . . . . . . . *
        . * . . . . . .
        . . . . . * . .
        . . . * . . . .

  ```

### E. JUMBLE (`JUMBLE`)
* **Format**:
  * Line 1: Unscrambled clue words prefixed with `Words:  `.
  * Line 2: Punny riddle punchline prefixed with `Answer: `.
  * Word-wrapped to $\le 46$ characters.
* **Example**:
  ```text
  JUMBLE
  Words:  FROST, GLAND, BREEZE, SHADOW
  Answer: A BREATH OF FRESH AIR

  ```

### F. BINARY (`BINARY`)
* **Format**: $N \times N$ ($6\times 6$ or $8\times 8$) grid of `0` and `1` digits separated by a space.
* **Indentation**: 6 spaces left padding.
* **Example** (6x6):
  ```text
  BINARY
        0 1 0 1 1 0
        1 0 1 0 0 1
        0 1 0 1 0 1
        1 0 1 0 1 0
        0 0 1 1 0 1
        1 1 0 0 1 0

  ```

### G. MINES (`MINES`)
* **Format**: $8 \times 8$ grid displaying revealed clue numbers $0..8$, `* ` for mines, and `. ` for safe non-clue cells.
* **Indentation**: 6 spaces left padding.
* **Example**:
  ```text
  MINES
        . 1 * 1 . . 1 *
        1 2 2 1 . 1 2 2
        * 1 . . . 1 * 1
        1 1 . . . 1 1 1
        . . 1 1 1 . . .
        . . 1 * 1 . 1 1
        1 1 2 2 2 1 2 *
        1 * 1 1 * 1 2 *

  ```

### H. TENTS (`TENTS`)
* **Format**: $N \times N$ ($6\times 6$ or $8\times 8$) grid showing tree, tent, and grass positions.
* **Glyphs**:
  * `T `: Tree (fixed given)
  * `* `: Tent (player-placed — unified boolean-placement glyph)
  * `. `: Empty grass
* **Indentation**: 6 spaces left padding.
* **Example** (6x6):
  ```text
  TENTS
        T * . T * .
        . . . . . .
        * T . . * T
        . . . . . .
        T * . T * .
        . . . . . .

  ```

### I. BRIDGES (`BRIDGES`)
* **Format**: Monospaced grid showing island numbers and orthogonal bridge lines connecting them.
* **Glyphs**:
  * Number in cell (e.g. `2`, `3`, `4`) representing the island.
  * `- `: Single horizontal bridge
  * `= `: Double horizontal bridge
  * `| `: Single vertical bridge
  * `" ` (or `||`): Double vertical bridge
  * `  `: Empty water
* **Indentation**: 6 spaces left padding for grid.
* **Example** (6x6):
  ```text
  BRIDGES
        2 = = 4 - - 2
        |     |     |
        |     |     |
        2 - - 3 - - 1

  ```

### J. KILLER (`KILLER`)
* **Format**: Pure solved numeric grid (4 rows of 4 digits for 4x4, or 6 rows of 6 digits for 6x6) with digits separated by single spaces.
* **Indentation**: 6 spaces left padding (safe thermal indent).
* **Example** (4x4):
  ```text
  KILLER
        1 4 2 3
        3 2 4 1
        4 1 3 2
        2 3 1 4

  ```
* **Example** (6x6):
  ```text
  KILLER
        1 4 2 3 5 6
        3 5 6 1 4 2
        2 1 3 4 6 5
        6 2 4 5 1 3
        4 6 5 2 3 1
        5 3 1 6 2 4

  ```

### K. CRYPTOGRAM (`CRYPTOGRAM`)
* **Format**:
  * Line 1+: `Answer: [DECRYPTED PHRASE]` word-wrapped to $\le 46$ characters per line.
  * Last line: `-- [AUTHOR NAME]` (if author attribution is present) — matching the in-puzzle attribution style.
* **Example**:
  ```text
  CRYPTOGRAM
  Answer: THE FUTURE BELONGS TO THOSE WHO
  BELIEVE IN THE BEAUTY OF THEIR DREAMS.
  -- ELEANOR ROOSEVELT


### L. TANGO (`TANGO`)
* **Format**: $N \times N$ ($6\times 6$ or $8\times 8$) grid of `0` and `1` digits separated by a space (edge clues are omitted from the solution key).
* **Indentation**: 6 spaces left padding.
* **Example** (6x6):
  ```text
  TANGO
        0 1 0 1 1 0
        1 0 1 0 0 1
        0 1 0 1 0 1
        1 0 1 0 1 0
        0 0 1 1 0 1
        1 1 0 0 1 0

  ```

### M. LADDER (`LADDER`)
* **Format**: Vertically stacked sequence of words, with each word on its own line.
* **Indentation**: 6 spaces left padding.
* **Example**:
  ```text
  LADDER
        COLD
        CORD
        CARD
        WARD
        WARM

  ```

---


## 4. Prohibited Elements Checklist in Solution Keys

- [x] **NO lines longer than 48 characters** (wrapping breaks receipt layout).
- [x] **NO missing game solutions** (if game was selected in receipt, its solution MUST appear in the key).
- [x] **NO missing blank line after an entry** (must separate each puzzle's solution block).
- [x] **NO multi-word subtitles** (must use strictly single-word uppercase matching [`docs/PUZZLE_HEADER_SPEC.md`](PUZZLE_HEADER_SPEC.md)).
- [x] **NO ambiguous glyphs** (must strictly follow the glyph definitions in Section 3).

---

## 5. Automated Verification Pipeline

All solution keys, indentation offsets, maximum line widths, and per-puzzle subtitles are continuously and automatically validated by:

```bash
python3 server/test_puzzle_standards.py
python3 server/test_thermal_format.py
```

This test programmatically validates:
1. Every solution key line strictly adheres to the 48-character thermal printing column width ($\le 48$ characters).
2. All 2D ASCII grid outputs use a safe left margin of 6 spaces (`'      '`).
3. Every puzzle subtitle is strictly a single uppercase word matching the master title.
4. Each game entry is followed by exactly one blank line separator.

