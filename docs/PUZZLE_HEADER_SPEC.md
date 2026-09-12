# Morning Puzzles: Header & Presentation Specification

This document establishes the official visual and structural standard for representing game titles, difficulty ratings, and puzzle layouts across the **Morning Puzzles** ecosystem (Web Simulator, Python Backend, and ESP32 Firmware).

All existing games—and any future games added to Morning Puzzles—must strictly conform to this specification.

---

## 1. Core Design Principles

1. **Strict One-Word Titles**: Every puzzle must have a single-word uppercase title (e.g. `STARS`, `SUDOKU`, `SEARCH`, `NONOGRAM`, `JUMBLE`, `BINARY`, `MINES`). Multi-word names, compound descriptors, subtitles, and slash-delineated variants (such as *"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, or *"Nonogram / Picross"*) are **strictly prohibited**.
2. **Uniform Visual Hierarchy**: Every puzzle begins with the same standardized header format regardless of whether it is rendered as a high-contrast thermal canvas graphic or a plain-text monospaced ASCII fallback.
3. **Mandatory One-Sentence Gameplay Instruction**: Underneath the title header and underneath the difficulty (or directly beneath the title if no difficulty exists), every puzzle must feature **exactly one clear, concise sentence** explaining the goal or how to play the game so that new players can immediately understand the objective.
4. **Difficulty Rating Placement**: For puzzles that feature a difficulty tier, the rating must be placed **immediately underneath the game title and immediately above the one-sentence gameplay instruction**.
5. **Contextual Metadata Placement**: Metadata specific to solving mechanics (such as Search themes, Jumble cartoon punchlines, or Nonogram row/column clue numbers, or Mines total count) belongs in or directly adjacent to the interactive solving area—never in the top title header.
6. **No Grid Dimension Leaks**: Headers must never display grid dimensions (e.g. `8x8 Grid`, `5x5 Picross`, `Size: 10x10`).

---

## 2. Standard Header Hierarchy

```
[Section Separator / Spacing]
      --- [ONE-WORD TITLE] ---      <-- Line 1: Centered Single-Word Title
       DIFFICULTY: [LEVEL]          <-- Line 2: Centered Difficulty (if applicable)
  [One-sentence instruction line]   <-- Line 3: 1-Sentence Goal / How-to-Play Description
[Spacing / Context Metadata (e.g. TOTAL MINES: N)]
┌────────────────────────────────┐
│                                │
│   DRAWING OF THE GAME ITSELF   │  <-- Line 4: Grid / Interactive Puzzle Canvas
│                                │
└────────────────────────────────┘
[Solving Checklist / Clues]         <-- Line 5: Word Checklist, Riddle Punchline, etc.
```

### Formatting Details (48-Column Thermal Monospace / ESC/POS)
* **Title Format**: Centered, strictly one word, uppercase, enclosed by triple dashes:
  ```text
  --- STARS ---
  --- SUDOKU ---
  --- SEARCH ---
  --- NONOGRAM ---
  --- JUMBLE ---
  --- BINARY ---
  --- MINES ---
  ```
* **Difficulty Format**: Centered, uppercase, prefixed by `DIFFICULTY: `:
  ```text
  DIFFICULTY: EASY
  DIFFICULTY: MEDIUM
  DIFFICULTY: HARD
  DIFFICULTY: MASTER
  DIFFICULTY: EXPERT
  ```
* **One-Sentence Instruction Format**: Centered or wrapped across 48-column thermal monospace, italicized in simulator UI, concise single sentence.

---

## 3. Official Game Registry & Matrix

| Puzzle Name | Exact Title Header | Has Difficulty? | Standard Difficulty Values | Canonical One-Sentence Gameplay Instruction | Notes / Placement Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stars** | `--- STARS ---` | **Yes** | `EASY` (5x5), `MEDIUM` (8x8), `HARD` (9x9 2★), `MASTER` (10x10 2★) | *Place [1 star / 2 stars] in each row, column, and region with no stars touching, even diagonally.* | Dynamic star count (1★ for Easy/Medium, 2★ for Hard/Master). Replaces legacy "Queens" / "Star Battle". |
| **Sudoku** | `--- SUDOKU ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | *Fill every row, column, and 3x3 box with digits 1-9 without repeating.* | Direct and concise. Pure 9x9 grid follows instruction. |
| **Search** | `--- SEARCH ---` | **No** *(Theme)* | *None* | *Find all [N] hidden words listed below.* *(Fallback: Find all listed words hidden across the grid.)* | Dynamic word count [N]. `★ THEME: [NAME]` placed with checklist words below grid. |
| **Nonogram** | `--- NONOGRAM ---` | **Yes** | `EASY` (5x5), `MEDIUM` (8x8), `HARD` (10x10), `EXPERT` (15x15) | *Shade blocks of cells matching each clue in order, separated by at least one empty cell.* | Explains multiple ordered block sequences and separating empty cells without referencing pictures. |
| **Jumble** | `--- JUMBLE ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | *Unscramble each word, then use the circled letters to solve the riddle.* | Clean 2-step prompt without jargon. |
| **Binary** | `--- BINARY ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Fill each row and column with [three 0s and three 1s / four 0s and four 1s], with no more than two consecutive of each type.* | Dynamic counts: three 0s/1s for 6x6 (Easy), four 0s/1s for 8x8 (Medium/Hard). Avoids "in a row" ambiguity. |
| **Mines** | `--- MINES ---` | **Yes** | `EASY` (8 Mines), `MEDIUM` (12 Mines), `HARD` (15 Mines) | *Deduce all [8 / 12 / 15] hidden mines using the adjacent numbered clues.* | Dynamic mine count [N]. `TOTAL MINES: [N]` placed between instruction and drawing. Zero guessing. |
| **Tents** | `--- TENTS ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Pitch [4 / 8 / 11] tents next to trees without tents touching, matching row and column counts.* | Dynamic tent count (4 for Easy, 8 for Medium, 11 for Hard). Replaces "orthogonally adjacent" with "next to trees". |
| **Bridges** | `--- BRIDGES ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Connect all islands into one network using 1 or 2 lines matching each island's number.* | 45% reduction. Explains single network, 1 or 2 lines, and island matching numbers. |

---

## 4. Prohibited Elements Checklist

Before committing any puzzle renderer or generator update, verify that **NONE** of the following elements appear in the header or drawing:

- [x] **NO multi-word titles or slash-separated names** (*"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, *"Nonogram / Picross"*, *"Tents and Trees"*, *"Hashiwokakero"*). Titles must be strictly a single word.
- [x] **NO multi-sentence rule essays or multi-paragraph tutorials** (gameplay instructions must be strictly one concise, clear sentence).
- [x] **NO missing or omitted gameplay instructions** (every game must include its canonical one-sentence goal between difficulty and drawing).
- [x] **NO grid dimension metadata in titles** (*"8x10 Grid"*, *"Size: 5x5"*).
- [x] **NO duplicate in-canvas titles** (e.g., drawing `S E A R C H` or `J U M B L E` inside the canvas when the standardized header is already present above it).
- [x] **NO simulator-only debug labels** on physical receipts (*"Thermal 203 DPI"*, *"Shaded by 1-Bit Dithering"*).

---

## 5. Specification for Adding New Games

When adding a new puzzle type to Morning Puzzles:

1. **Select Strict One-Word Title**: Choose a single uppercase English word (e.g., `--- CROSSWORD ---`, `--- TANGLE ---`, `--- KAKURO ---`, `--- BATTLESHIPS ---`, `--- NURIKABE ---`). Multi-word, hyphenated, or slash-separated names are strictly forbidden.
2. **Define One-Sentence Instruction**: Author exactly one clear, concise sentence explaining the objective so new players understand how to play immediately. The instruction must strictly adhere to the $\le 100$-character limit, canonical formula, and dynamic parameterization rules detailed in [`docs/PUZZLE_DESCRIPTION_GUIDELINES.md`](PUZZLE_DESCRIPTION_GUIDELINES.md).
3. **Determine Difficulty Applicability**:
   - If the game has discrete difficulty levels, map them to standard keywords (`EASY`, `MEDIUM`, `HARD`, `EXPERT`, `MASTER`) and display via `DIFFICULTY: [LEVEL]`.
   - If the game is driven by theme or topic rather than difficulty, omit the difficulty line and place the one-sentence instruction directly below the title.
4. **Canvas Drawing**: Start the canvas directly with the visual puzzle component (borders, cells, or game clues). Do not draw a banner title inside the canvas.
5. **Checklist & Clues**: Place any answer verification or pencil-tracking tools (checkboxes `[ ]`, scratch lines) underneath the puzzle grid separated by a dashed tear-line.
6. **Solution Key Formatting**: Ensure the game's solution format strictly follows the monospaced ASCII requirements in [`docs/PUZZLE_SOLUTION_KEY_SPEC.md`](PUZZLE_SOLUTION_KEY_SPEC.md).

