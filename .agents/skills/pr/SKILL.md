---
name: pr
description: Inspects active code changes, runs pre-flight tests & Arduino sketch synchronization, creates/manages a feature branch, commits changes, pushes to GitHub origin, and opens a Pull Request targeting main. Use whenever the user types /pr or asks to create a pull request.
---

# PR: Automated Review, Test, Commit, Push & Pull Request Creation

This skill automates the complete pull request workflow for **Pen and Paper Puzzles**:
1. Inspecting active code modifications and diffs.
2. Managing branch isolation (automatically branching if on `main`).
3. Running local pre-flight tests (`test_puzzle_standards.py`) and Arduino sketch mirroring (`sync_arduino_sketch.sh`).
4. Generating conventional commit titles and structured descriptions.
5. Pushing the feature branch to `origin`.
6. Creating a Pull Request against `main` using GitHub CLI (`gh pr create`) with a web URL fallback.

---

## Workflow Steps

When the user runs `/pr` (or asks to create a pull request), execute this exact sequence:

### 1. Inspect Active Changes & Code Diff
1. Run `git status -s` to identify all modified, added, deleted, and untracked files.
2. Run `git diff` to view unstaged diffs and `git diff --cached` to inspect any already staged changes.
3. Review untracked files to ensure they are intended project files and not temporary scratchpads, IDE artifacts (`.DS_Store`), or credentials.
4. **Early Exit on Clean State**:
   - If `git status` reports working tree clean (no staged, unstaged, or untracked changes) and no unpushed commits:
     - Inform the user: *"Working tree is clean. There are no changes to commit."*
     - Stop execution.

---

## 2. Branch & Worktree Management
1. Check current branch:
   ```bash
   git branch --show-current
   ```
2. **If currently on `main`**:
   - Formulate a concise, kebab-case branch name reflecting the changes (e.g., `feature/add-daily-pr-workflow`, `fix/jumble-circle-alignment`, `refactor/tango-raster`).
   - Create and switch to the new feature branch:
     ```bash
     git checkout -b <branch-name>
     ```
   - Inform the user: *"Created and switched to feature branch `<branch-name>` to keep `main` clean."*
3. **If already on a feature branch or worktree**:
   - Stay on the current branch.

---

### 3. Pre-Flight Verification & Hygiene (Rule Enforcement)
Before committing, ensure repository integrity:
1. **Arduino Sketch Synchronization (Rule 7)**:
   ```bash
   chmod +x ./scripts/sync_arduino_sketch.sh
   ./scripts/sync_arduino_sketch.sh
   ```
   If `PenAndPaperPuzzles/` files were updated by the sync script, ensure they are staged.
2. **Puzzle Presentation Standards (Rule 1–4, 6)**:
   ```bash
   python3 server/test_puzzle_standards.py
   ```
   If any standard test fails, halt and fix the issue before proceeding.
3. **Game Onboarding, Setup Portal & Parity Standards (Rule 18)**:
   ```bash
   python3 server/test_game_onboarding.py
   python3 server/test_game_rules.py
   ```
   If any onboarding or game rule verification fails, halt and resolve it before proceeding.

---

### 4. Generate Commit & PR Title and Description
Analyze the diffs and conversation context to produce high-quality metadata:

#### A. Title
- Concise: **$\le 72$ characters** (ideally $\le 50$ characters).
- Conventional Commit prefix: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Imperative mood (e.g., `feat: implement github actions ci and pr workflow`).

#### B. Description / PR Body
- Separated from the title by a blank line.
- Provide a clear, bulleted summary:
  - **Summary**: What was added, changed, or fixed.
  - **Motivation**: Why the change was made.
  - **Testing**: What local tests passed (e.g., standards suite, visual consistency, sketch sync).

---

### 5. Stage & Commit
1. Stage the relevant modified and untracked files:
   ```bash
   git add <files>
   ```
2. Execute the commit:
   ```bash
   git commit -m "<Commit Title>" -m "<Commit Description>"
   ```

---

### 6. Push to Remote Feature Branch
Push the branch to `origin`:
```bash
git push -u origin <branch-name>
```

---

### 7. Open Pull Request on GitHub
1. Check GitHub CLI authentication status:
   ```bash
   gh auth status
   ```
2. **If authenticated**:
   - Create the PR targeting `main`:
     ```bash
     gh pr create --base main --head <branch-name> --title "<Commit Title>" --body "<Commit Description>"
     ```
   - Capture and display the resulting PR URL to the user.
3. **If `gh` is unauthenticated or encounters an error**:
   - Display a direct GitHub web URL for one-click creation:
     ```text
     https://github.com/bimschleger/pen-and-paper-puzzles/compare/main...<branch-name>?expand=1
     ```
   - Remind the user:
     ```text
     Tip: Run `gh auth login` once in your terminal to enable zero-click automatic PR creation in future runs.
     ```

---

### 8. Final Report
Present a clean summary to the user:
- Branch: `<branch-name>`
- Commit: `<hash>` (`<title>`)
- PR URL: Link to the GitHub Pull Request
- Status: GitHub Actions CI checks are now running on the PR.
