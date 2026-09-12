# Candidate Puzzle Library: Evaluation & Implementation Reference

This document provides the architectural survey, evaluation standards, and technical specifications for prospective puzzle candidates to expand the **Morning Puzzles** ecosystem.

---

## 1. Implemented Games (Active Library)

The following 13 puzzles have been implemented and currently comprise the core Morning Puzzles library across the Python backend (`server/app/puzzles/`), ESP32 firmware (`esp32-firmware/src/generators/`), and web simulator (`simulator/receipt_simulator.html`):

| Single-Word Title | Traditional / Common Name | Genre / Category | Implementation Stack | Difficulty Scaling | Solution Key Representation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`--- SUDOKU ---`** | Sudoku | Latin Square / Placement | Python (CP-SAT/Backtracking) + ESP32 C++ | Easy, Medium, Hard (clue count 25–40) | 6-space indented 9×9 ASCII grid |
| **`--- SEARCH ---`** | Word Search | Word / Grid Search | Python + ESP32 C++ | Theme-driven (allowed vector directions) | Coordinates list ($\le 46$ cols) |
| **`--- NONOGRAM ---`** | Picross / Paint by Numbers | Grid Shading / Art | Python (CP-SAT) + ESP32 C++ | Easy (5×5), Medium (10×10), Hard (15×15) | 6-space indented ASCII pixel grid |
| **`--- STARS ---`** | Star Battle / LinkedIn Queens | Object Placement | Python (CP-SAT) + ESP32 C++ | Easy (5×5 1★), Med (8×8 1★), Hard (10×10 2★) | Star coordinate list ($\le 46$ cols) |
| **`--- JUMBLE ---`** | Word Scramble / Daily Jumble | Word / Anagram Riddle | Python + ESP32 C++ | Easy (4–5 letters), Med (5–6), Hard (6–7) | Unscrambled words + punchline |
| **`--- BINARY ---`** | Takuzu / Binairo / Unruly | Parity / Binary Logic | Python (Backtracking) + ESP32 C++ | Easy (6×6), Medium (8×8), Hard (8×8) | 6-space indented 0/1 ASCII grid |
| **`--- MINES ---`** | Solitaire Minesweeper | Minefield Deduction | Python (Deductive solver) + ESP32 C++ | Easy (8 mines), Med (12 mines), Hard (15 mines) | Mine coordinate list ($\le 46$ cols) |
| **`--- TENTS ---`** | Tents and Trees | Bipartite Matching | Python + ESP32 C++ | Easy (6×6, 4–5 tents), Med/Hard (8×8, 8–12 tents) | Tent coordinate list ($\le 46$ cols) |
| **`--- BRIDGES ---`** | Hashiwokakero / Hashi | Graph Spanning Tree | Python + ESP32 C++ | Easy (6×6, 8 islands), Med/Hard (8×8, 10–16) | Inter-island edge list with counts |
| **`--- KILLER ---`** | Killer Sudoku | Latin Square + Arithmetic | Python (CP-SAT / Backtracking) | Easy, Medium, Hard, Extreme | 6-space indented 9×9 ASCII grid |
| **`--- CRYPTOGRAM ---`** | Monoalphabetic Substitution | Cryptographic Deduction | Python (Procedural derangement) | Easy (3 hint letters), Med (1 hint), Hard (0 hints) | Decoded quote and author |
| **`--- TANGO ---`** | LinkedIn Tango | Parity / Edge Relations | Python + ESP32 C++ | Easy (6×6, high clues), Med (6×6), Hard (6×6) | 6-space indented Sun/Moon grid |
| **`--- LADDER ---`** | Word Ladder / Doublets | Word & Pattern | Python (BFS Word Graph) + Dataset | Easy (4-letter, 4–5 words), Med (4-letter, 6–7), Hard (5-letter, 6–8) | Arrow word path ($\le 46$ cols) |

---

## 2. Search & Evaluation Criteria for New Candidates

Every prospective game must satisfy six non-negotiable architectural criteria before admission into the candidate pipeline:

### Criterion 1: Strict Formatting & Standard Compliance
*   **One-Word Title**: Must use a single uppercase English noun enclosed in triple dashes: `--- [TITLE] ---` (e.g. `--- LADDER ---`, `--- CODEWORD ---`, `--- LOOP ---`). Aliases, subtitles, or multi-word titles are strictly forbidden.
*   **Solution Key Subtitle**: Strictly single uppercase word matching the title, without dashes.
*   **Difficulty Placement**: When applicable, placed immediately below the title banner as centered uppercase text prefixed by `DIFFICULTY: ` (`EASY`, `MEDIUM`, `HARD`, `MASTER`, `EXPERT`, `EXTREME`).
*   **Instruction Formula**: Fully interpolated instruction line must never exceed **100 characters** and must follow the canonical formula:
    $$\text{[Imperative Verb]} + \text{[Target with Dynamic Quantity]} + \text{[Context / Clues]} + \text{[Constraint]}$$

### Criterion 2: Thermal Printability & Pen-and-Paper Ergonomics
*   **Physical Canvas Bounds**: 80mm thermal receipt paper provides $576\text{ dots}$ total printable width ($48\text{ font A}$ monospace characters). Graphic canvases are centered with a printable width of $320\text{--}400\text{px}$.
*   **Handwriting Ergonomics**: Any grid cell requiring the solver to write a pencil digit or letter must measure at least **$25\text{--}30\text{px}$** (e.g., $10\times 10$ max for letter writing; $8\times 8$ or $6\times 6$ preferred for rapid morning solving).
*   **Marking Actions**: Allowed pencil interactions are clean writing (digits, letters), single-stroke segment drawing (loops, bridges), circling/crossing out, or light pencil hatching.
*   **Thermal Safety**: Raster graphics must maintain an average duty cycle $\le 35\%$ with no more than 16 consecutive dense black dot rows. Solid black fills are prohibited (use open outlines or stippling).

### Criterion 3: 100% Offline Autonomous Generation & Algorithm Portability
*   **Python-First Standalone Execution**: The primary generator in `server/app/generators/` must run standalone with zero external network access, cloud API calls, or heavy runtime dependencies.
*   **Path to ESP32 C++ Portability**: Algorithms must have a compact memory and computational footprint ($<40\text{KB}$ RAM, $<500\text{ms}$ execution on a microcontroller) to facilitate clean porting to native C++ on the ESP32.
*   **Zero-Trivia Autonomy for Word Games**: Word and language puzzles must rely exclusively on **pure dictionary & pattern algorithms** (graph search, trie lookups, anagram hashing, or cross-matching) operating against compact, embedded open-source word lists (e.g. 4–6 letter word lexicons). Games requiring live internet lookups, external trivia, or large definition dictionaries are disallowed.

### Criterion 4: Mathematical Uniqueness & Deductive Solvability Guarantees
*   **Single Unique Solution**: The generator must mathematically prove that the generated puzzle has strictly **one valid solution**.
*   **Pure Deduction (Zero Guessing)**: Puzzles must be 100% deducible through progressive logical steps. Blind bifurcation, trial-and-error guessing, and 50/50 coin flips are strictly rejected.
*   **Compact Solution Key**: The solution must cleanly format within standard 48-column monospaced lines (grids pre-indented with 6 spaces; coordinate and word lists wrapped to $\le 46$ characters).

### Criterion 5: Open-Source Licensing
*   The reference generator, algorithmic logic, and lexicon sources must be licensed under **Apache 2.0**, **MIT**, or **BSD**. Proprietary, patented, or strictly non-commercial licenses are excluded.

### Criterion 6: Variable Difficulty Scaling
*   Difficulty must be parameterized by structural properties (e.g., grid dimensions, clue density, branching factor, word length, lookahead depth) rather than arbitrary randomization, spanning at least 3 distinct tiers (`easy`, `medium`, `hard`).

---

## 3. Candidate Comparison Matrix

Candidates are organized into five priority tiers. **Tier 1 (Word, Language & Pattern)** is prioritized to rebalance the existing library against the 9 grid-logic games.

| Priority | Single-Word Title | Traditional Name | Category | Primary Engine / Reference | License | Print Fit | Generation Complexity | Portability to C++ |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **P1** | **`CODEWORD`** | Coded Crossword / Cipher Grid | Word & Pattern | Compact Crossword Filler + Substitution | Apache 2.0 / MIT | **9.5 / 10** | Medium (Backtracking fill + letter cipher) | **Medium-High** |
| **P1** | **`WHEEL`** | Word Wheel / Target Anagram | Word & Pattern | Anagram Index / 9-Letter Subsets | Apache 2.0 / MIT | **10 / 10** | Low (Dictionary pre-indexing) | **Very High** (Flash lookup table) |
| **P1** | **`SQUARE`** | Word Square / Sator Grid | Word & Pattern | Symmetric Backtracking Word Fill | Apache 2.0 / MIT | **9.8 / 10** | Low-Medium (Trie-based symmetric fill) | **High** (Trie on PROGMEM) |
| **P2** | **`LOOP`** | Slitherlink / Fences | Loop & Circuit | Simon Tatham (`loopy.c`) / Nikoli Solver | MIT | **9.5 / 10** | Medium-High (Deductive loop solver) | **Very High** (Direct C port) |
| **P2** | **`MASYU`** | Masyu / Pearl Loop | Loop & Circuit | Nikoli Solver / Simon Tatham (`pearl.c`) | MIT | **9.4 / 10** | Medium (Local pearl rules + loop closure)| **High** |
| **P3** | **`HITORI`** | Hitori | Shading & Region | Simon Tatham (`hitori.c`) / Nikoli Solver | MIT | **9.6 / 10** | Medium (Backtracking pruner + connectivity)| **Very High** (Direct C port) |
| **P3** | **`SHIKAKU`** | Shikaku / Rectangles | Shading & Region | Simon Tatham (`rect.c`) / Exact Cover | MIT | **9.4 / 10** | Medium (Disjoint rectangle partitioning) | **High** |
| **P3** | **`NURIKABE`** | Nurikabe / Islands | Shading & Region | Nikoli Solver / CP-SAT Solver | MIT / Apache 2.0 | **9.2 / 10** | High (White island sizing + black sea 2x2)| **Medium** |
| **P4** | **`CALCU`** | Calcudoku / KenKen | Arithmetic Latin Sq | Simon Tatham (`keen.c`) / Latin Solver | MIT | **9.0 / 10** | Medium (Latin square + polyomino cages) | **Very High** (Direct C port) |
| **P4** | **`FUTOSHIKI`** | Futoshiki / Unequal | Arithmetic Latin Sq | Simon Tatham (`unequal.c`) / Latin Solver | MIT | **9.0 / 10** | Medium (Latin square + inequality poset) | **Very High** (Direct C port) |
| **P4** | **`KAKURO`** | Kakuro / Cross Sums | Arithmetic Latin Sq | Simon Tatham (`kakuro.c`) / Partition | MIT | **8.7 / 10** | High (Crossword geometry + sum partition) | **High** |
| **P4** | **`SKYSCRAPERS`**| Skyscrapers / Towers | Arithmetic Latin Sq | Simon Tatham (`towers.c`) / Latin Solver | MIT | **9.1 / 10** | Medium-High (Latin square + exterior sight)| **Very High** (Direct C port) |
| **P5** | **`FLEET`** | Battleships / Bimaru | Placement & Sight | Simon Tatham (`pearl.c` variant) / CP-SAT | MIT / Apache 2.0 | **8.8 / 10** | Medium-High (Fleet placer + SAT pruner) | **High** |
| **P5** | **`AKARI`** | Light Up / Akari | Placement & Sight | Simon Tatham (`lightup.c`) / Ray caster | MIT | **9.3 / 10** | Medium (Ray line-of-sight + bulb counts) | **Very High** (Direct C port) |

---

## 4. Detailed Candidate Profiles

---

### Priority Tier 1: Word, Language & Pattern Puzzles

#### 1. LADDER (`--- LADDER ---`)
*   **Traditional Names**: Word Ladder, Doublets (invented by Lewis Carroll in 1877).
*   **Canonical Instruction**: `Change 1 letter per step to turn [START] into [TARGET] using [N] valid English words.` ($\le 85$ chars)
*   **Core Rules**:
    1. The player is given a start word and a target word of equal length (e.g., `COLD` $\to$ `WARM`).
    2. At each intermediate step, change exactly one letter to form another valid English word.
    3. The number of rungs/steps is fixed based on the shortest path.
*   **Thermal Receipt Layout & Pen Ergonomics**:
    *   Vertical ladder display: each rung printed with boxed letter frames ($30\text{px}\times 30\text{px}$ per letter), leaving empty intermediate rungs for handwriting.
    *   Horizontal width: 4–5 letter boxes centered ($\sim 150\text{px}$), extremely legible and comfortable for pencil writing.
*   **Open-Source Generation Engine**:
    *   Graph breadth-first search (BFS) over an unweighted graph where vertices are words and edges connect words with Hamming distance 1.
    *   Lexicon: Scrabble ENABLE or SOWPODS 4-letter and 5-letter word lists (Public Domain / MIT).
*   **Difficulty Scaling**:
    *   `easy`: 4-letter words, 3–4 intermediate steps, high-degree gateway words (e.g. `HEAD` $\to$ `TEAL`).
    *   `medium`: 4-letter words, 5–6 intermediate steps, bottleneck words with lower branching factors.
    *   `hard`: 5-letter words, 6–8 intermediate steps (e.g. `BLACK` $\to$ `WHITE`).
*   **Solution Key Format**:
    *   Header: `LADDER`
    *   Content: Complete sequence of valid words separated by arrows (`COLD -> CORD -> CARD -> WARD -> WARM`), wrapped to $\le 46$ characters.

---

#### 2. CODEWORD (`--- CODEWORD ---`)
*   **Traditional Names**: Coded Crosswords, Cipher Crosswords, Codewords.
*   **Canonical Instruction**: `Decipher the alphabet grid where numbers 1-26 replace letters using [3 / 2 / 1] starter hints.` ($\le 95$ chars)
*   **Core Rules**:
    1. A compact interlocking crossword grid (e.g. $7\times 7$ or $9\times 9$) where every white cell contains a number from $1$ to $26$.
    2. Each number represents one unique letter of the English alphabet throughout the entire grid.
    3. There are no definition clues: solving is driven purely by letter patterns, vowel placements, word lengths, and cross-intersections.
    4. A starter letter key gives 1 to 3 initial letter-number assignments.
*   **Thermal Receipt Layout & Pen Ergonomics**:
    *   $7\times 7$ grid: $44\text{px}$ cells; $9\times 9$ grid: $34\text{px}$ cells.
    *   Top corner of each cell contains small number ($1..26$); lower portion has spacious white area for handwritten letter.
    *   Alphabet checklist ($A..Z$) printed directly below the grid for crossing off cracked letters.
*   **Open-Source Generation Engine**:
    *   Procedural crossword symmetry filler paired with bijective random permutation $\pi: \{1..26\} \leftrightarrow \{A..Z\}$.
    *   Backtracking exact solver verifies that the remaining number assignments can be uniquely deduced without ambiguity.
*   **Difficulty Scaling**:
    *   `easy`: $7\times 7$ grid, 3 starter letters provided (including common vowels `E` or `A`).
    *   `medium`: $9\times 9$ grid, 2 starter letters provided (1 vowel, 1 consonant).
    *   `hard`: $9\times 9$ grid, 1 starter letter provided (a rare consonant like `K` or `W`).
*   **Solution Key Format**:
    *   Header: `CODEWORD`
    *   Content: Monospaced 2-row table mapping numbers $1..26$ to their decrypted letters (`1=C 2=A 3=T ...`).

---

#### 3. WHEEL (`--- WHEEL ---`)
*   **Traditional Names**: Word Wheel, Target, Polygon, Anagram Wheel.
*   **Canonical Instruction**: `Find [N] words of 4+ letters containing central letter [X], including the 9-letter anagram.` ($\le 95$ chars)
*   **Core Rules**:
    1. An outer ring of 8 letters surrounds a single compulsory central letter (9 total letters).
    2. Solvers find all valid English words of 4 or more letters that can be constructed from the wheel.
    3. Every valid word must contain the central letter.
    4. Each letter in the wheel may be used at most once per word.
    5. Exactly one 9-letter anagram is guaranteed to exist.
*   **Thermal Receipt Layout & Pen Ergonomics**:
    *   $3\times 3$ octagonal rosette or grid: central cell highlighted with double-thick border; 8 outer cells contain bold Space Mono letters.
    *   Below the wheel: Target benchmark scores (`Good: 12, Excellent: 18, Genius: 25+`) and empty lined columns for writing found words.
*   **Open-Source Generation Engine**:
    *   Selects a 9-letter word with rich sub-anagram density from a curated 9-letter root dataset.
    *   Offline evaluation: pre-computed letter-frequency bitmask checks dictionary words in $<5\text{ms}$.
*   **Difficulty Scaling**:
    *   `easy`: Highly accessible central letter (`E`, `A`, `R`), 25+ valid sub-words, common 9-letter root.
    *   `medium`: Moderate central letter (`T`, `L`, `O`), 15–24 valid sub-words.
    *   `hard`: Restrictive central letter (`U`, `G`, `B`), 10–15 valid sub-words.
*   **Solution Key Format**:
    *   Header: `WHEEL`
    *   Content: The 9-letter anagram solution, total valid word count, and list of all valid words wrapped to $\le 46$ characters.

---

#### 4. SQUARE (`--- SQUARE ---`)
*   **Traditional Names**: Word Square, Sator Square, Symmetric Cross.
*   **Canonical Instruction**: `Fill the [4x4 / 5x5] grid with words that read identically across and down using [N] clues.` ($\le 95$ chars)
*   **Core Rules**:
    1. A square grid of letters ($4\times 4$ or $5\times 5$) where row $k$ and column $k$ form the exact same word for all $k$.
    2. Several initial letters are provided as fixed clues.
    3. The solver deduces the remaining letters so that every row and column forms a valid English word.
*   **Thermal Receipt Layout & Pen Ergonomics**:
    *   $4\times 4$ ($65\text{px}$ cells) or $5\times 5$ ($52\text{px}$ cells) grid.
    *   Ultra-spacious white cells with centered clue letters; ample room for pencil solving.
*   **Open-Source Generation Engine**:
    *   Trie-based backtracking search on symmetric prefix lookups over a curated 4-letter and 5-letter dictionary.
    *   Solver validates that the remaining clues admit exactly one valid symmetric word square.
*   **Difficulty Scaling**:
    *   `easy`: $4\times 4$ grid with 6–7 starting letter clues.
    *   `medium`: $4\times 4$ grid with 4 starting letter clues.
    *   `hard`: $5\times 5$ grid with 5–6 starting letter clues.
*   **Solution Key Format**:
    *   Header: `SQUARE`
    *   Content: 6-space indented ASCII word square grid.

---

### Priority Tier 2: Loop & Circuit Drawing Puzzles

#### 5. LOOP (`--- LOOP ---`)
*   **Traditional Names**: Slitherlink, Fences, Takegaki (Nikoli).
*   **Canonical Instruction**: `Draw a single continuous closed loop connecting dots so each number matches its edge count.` ($\le 95$ chars)
*   **Core Rules**:
    1. A grid of dots where some cells contain numbers $0..3$.
    2. Connect adjacent dots horizontally and vertically to form a single continuous closed loop without branches or crossings.
    3. Numbered cells must have exactly that many edges occupied by the loop; empty cells can have any number of edges.
*   **Thermal Print Layout**:
    *   $7\times 7$ ($45\text{px}$) or $8\times 8$ ($38\text{px}$) dot grid.
    *   Vertices drawn as distinct $4\text{px}$ filled circles; numbers centered cleanly inside cells.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`loopy.c`, MIT License).
*   **Difficulty Scaling**:
    *   `easy`: $6\times 6$ grid, direct corner $0$/$3$ clues, adjacent $3\text{-}3$ patterns.
    *   `medium`: $8\times 8$ grid, corner avoidance and loop closure lookahead.
    *   `hard`: $10\times 10$ grid, non-local parity and Jordan curve interior/exterior theorems.

---

#### 6. MASYU (`--- MASYU ---`)
*   **Traditional Names**: Masyu, Pearl Puzzle, Shiroshinju Kuroshinju (Nikoli).
*   **Canonical Instruction**: `Draw a single closed loop passing through all pearls following white and black corner rules.` ($\le 96$ chars)
*   **Core Rules**:
    1. Draw a single non-intersecting loop passing through all white and black circles ("pearls").
    2. White pearls: loop must pass straight through, and must turn in at least one immediately adjacent cell.
    3. Black pearls: loop must turn $90^\circ$ on the black pearl, and must continue straight for at least two cells in both directions.
*   **Thermal Print Layout**:
    *   $8\times 8$ ($38\text{px}$) or $10\times 10$ ($30\text{px}$) grid.
    *   White pearls rendered as hollow circles ($1.8\text{px}$ stroke); black pearls rendered as filled circles.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`pearl.c`, MIT License) / Nikoli solver.

---

### Priority Tier 3: Shading & Region Partitioning Puzzles

#### 7. HITORI (`--- HITORI ---`)
*   **Traditional Names**: Hitori (Nikoli).
*   **Canonical Instruction**: `Shade duplicate numbers so no duplicates share a line, black cells do not touch, and white cells connect.` ($\le 100$ chars)
*   **Core Rules**:
    1. The grid is completely filled with numbers.
    2. Shade out cells so that no duplicate number appears in any row or column among white cells.
    3. Shaded (black) cells cannot touch each other horizontally or vertically.
    4. All remaining unshaded (white) cells must form a single orthogonally connected network.
*   **Thermal Print Layout**:
    *   $8\times 8$ ($40\text{px}$ cells) or $9\times 9$ ($35\text{px}$ cells).
    *   Identical cell footprint to Sudoku; numbers printed with high contrast.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`hitori.c`, MIT License).

---

#### 8. SHIKAKU (`--- SHIKAKU ---`)
*   **Traditional Names**: Shikaku, Rectangles, Divide by Squares (Nikoli).
*   **Canonical Instruction**: `Divide the grid into non-overlapping rectangles so each rectangle contains exactly 1 number equal to its area.` ($\le 100$ chars)
*   **Core Rules**:
    1. Some cells contain numbers.
    2. Divide the entire grid into rectangular and square regions along grid lines.
    3. Each rectangle must contain exactly one number, which equals the cell area of that rectangle.
*   **Thermal Print Layout**:
    *   $8\times 8$ ($40\text{px}$) or $10\times 10$ ($32\text{px}$) grid.
    *   Numbers centered in cells; light grid lines provide clear pencil tracking for drawing outlines.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`rect.c`, MIT License).

---

#### 9. NURIKABE (`--- NURIKABE ---`)
*   **Traditional Names**: Nurikabe, Islands in the Stream (Nikoli).
*   **Canonical Instruction**: `Shade cells to form a continuous sea with no 2x2 pools, leaving numbered islands matching cell areas.` ($\le 100$ chars)
*   **Core Rules**:
    1. Numbered cells represent "islands"; unnumbered cells can be island (white) or sea (black).
    2. Each island contains exactly one number and must be an orthogonally connected group of white cells of that size.
    3. All sea cells form a single connected orthogonal network.
    4. No $2\times 2$ square of sea cells is allowed anywhere in the grid.
    5. Islands cannot touch each other orthogonally.
*   **Thermal Print Layout**:
    *   $8\times 8$ ($40\text{px}$) or $9\times 9$ ($35\text{px}$) grid.
*   **Open-Source Engine**: Nikoli Nurikabe solver / IBM chuk-puzzles-gym / CP-SAT.

---

### Priority Tier 4: Arithmetic & Latin Square Puzzles

#### 10. CALCU (`--- CALCU ---`)
*   **Traditional Names**: Calcudoku, KenKen, Mathdoku, Keen.
*   **Canonical Instruction**: `Fill digits 1-[N] per line so cage values equal their arithmetic clue (+, -, x, /).` ($\le 85$ chars)
*   **Core Rules**:
    1. $N \times N$ Latin square: digits $1..N$ appear exactly once in each row and column.
    2. Heavy-bordered cages display a target number and arithmetic operator (e.g. `12+`, `3-`, `8x`, `2/`).
    3. Digits within a cage must yield the target using the specified operation. Digits may repeat within a cage if not in the same row/col.
*   **Thermal Print Layout**:
    *   $5\times 5$ ($64\text{px}$) or $6\times 6$ ($53\text{px}$) grid with Tier 2 ($2.5\text{px}$) cage outlines.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`keen.c`, MIT License).

---

#### 11. FUTOSHIKI (`--- FUTOSHIKI ---`)
*   **Traditional Names**: Futoshiki, Unequal.
*   **Canonical Instruction**: `Fill digits 1-[N] in every line while satisfying all inequality signs between adjacent cells.` ($\le 95$ chars)
*   **Core Rules**:
    1. $N \times N$ Latin square: digits $1..N$ appear once in each row and column.
    2. Inequality signs (`<`, `>`) between adjacent cells must be strictly satisfied.
*   **Thermal Print Layout**:
    *   $5\times 5$ ($55\text{px}$) or $6\times 6$ ($46\text{px}$) grid with centered inequality glyphs on cell borders.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`unequal.c`, MIT License).

---

#### 12. KAKURO (`--- KAKURO ---`)
*   **Traditional Names**: Kakuro, Cross Sums.
*   **Canonical Instruction**: `Fill white runs with digits 1-9 without duplicates so each run sums to its clue value.` ($\le 90$ chars)
*   **Core Rules**:
    1. Crossword-style layout with black clue cells and white answer cells.
    2. White cells contain digits $1..9$.
    3. Each horizontal and vertical continuous run of white cells must sum to the clue number above or to the left, with no repeating digits in a run.
*   **Thermal Print Layout**:
    *   $8\times 8$ grid; clue cells diagonally split with across sum in upper-right and down sum in lower-left.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`kakuro.c`, MIT License).

---

#### 13. SKYSCRAPERS (`--- SKYSCRAPERS ---`)
*   **Traditional Names**: Skyscrapers, Towers.
*   **Canonical Instruction**: `Place heights 1-[N] per line so exterior numbers match the count of visible taller buildings.` ($\le 95$ chars)
*   **Core Rules**:
    1. $N \times N$ grid representing skyscrapers of heights $1..N$ (each height appears once per row and column).
    2. Exterior clue numbers indicate how many skyscrapers are visible from that vantage point (taller buildings obscure shorter ones behind them).
*   **Thermal Print Layout**:
    *   $5\times 5$ ($52\text{px}$) or $6\times 6$ ($44\text{px}$) grid with exterior clue margins.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`towers.c`, MIT License).

---

### Priority Tier 5: Object Placement & Line-of-Sight Puzzles

#### 14. FLEET (`--- FLEET ---`)
*   **Traditional Names**: Battleships, Bimaru, Solitaire Battleships.
*   **Canonical Instruction**: `Locate the hidden fleet of 10 non-touching ships matching row and column segment tallies.` ($\le 92$ chars)
*   **Core Rules**:
    1. $10\times 10$ grid hiding a standard naval fleet: 1 battleship ($4\text{ cells}$), 2 cruisers ($3\text{ cells}$), 3 destroyers ($2\text{ cells}$), and 4 submarines ($1\text{ cell}$).
    2. Ships cannot touch each other, even diagonally.
    3. Numbers along top and left margins specify total ship segments in each row/column. Initial water and ship clues may be given.
*   **Thermal Print Layout**:
    *   $10\times 10$ grid ($30\text{px}$ cells + exterior margin tallies).
*   **Open-Source Engine**: Simon Tatham variant / CP-SAT Solitaire Battleship generator (MIT / Apache 2.0).

---

#### 15. AKARI (`--- AKARI ---`)
*   **Traditional Names**: Light Up, Akari (Nikoli).
*   **Canonical Instruction**: `Place light bulbs to illuminate all corridors without any two bulbs shining on each other.` ($\le 92$ chars)
*   **Core Rules**:
    1. Place light bulbs in white cells. Bulbs project light horizontally and vertically until blocked by black barrier cells.
    2. All white cells must be illuminated.
    3. No two light bulbs may illuminate each other (no line of sight between bulbs).
    4. Some black cells contain numbers $0..4$, specifying exactly how many bulbs must be placed orthogonally adjacent to that cell.
*   **Thermal Print Layout**:
    *   $8\times 8$ ($40\text{px}$) or $10\times 10$ ($32\text{px}$) grid.
    *   Light bulbs marked as circles with radial rays; numbered black cells rendered with white text on black background.
*   **Open-Source Engine**: Simon Tatham's Portable Puzzle Collection (`lightup.c`, MIT License).
