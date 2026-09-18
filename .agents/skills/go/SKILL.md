---
name: go
description: Inspects the code diff in the active conversation, generates an appropriate commit title and description, and commits and pushes the changes to the main branch on GitHub. Use whenever the user types /go or requests to commit and push code.
---

# Go: Automated Review, Commit & Push to Main

This skill automates the end-of-turn workflow by inspecting active code modifications, crafting meaningful commit metadata (concise title + structured description), committing the changes, and pushing them directly to the `main` branch on GitHub.

---

## Workflow Steps

When the user runs `/go` (or asks to review, commit, and push changes), follow this exact sequence:

### 1. Inspect Active Changes & Code Diff
1. Run `git status -s` to identify all modified, added, deleted, and untracked files.
2. Run `git diff` to view unstaged diffs and `git diff --cached` to inspect any already staged changes.
3. If new untracked files exist, review them to ensure they are intended project files and not temporary scratchpads, IDE artifacts, or sensitive credentials.
4. **Early Exit on Clean State**:
   - If `git status` reports working tree clean (no staged, unstaged, or untracked changes) and no unpushed commits:
     - Inform the user: *"Working tree is clean. There are no changes to commit."*
     - Stop execution.

### 2. Pre-Commit Hygiene & Verification
1. Verify no unintended files are staged (e.g., `.DS_Store`, build artifacts, `.env`, credentials, temporary scratch files).
2. If the repository has active pre-commit hooks, synchronization scripts, or fast test suites, ensure they pass or have been executed.

### 3. Generate Commit Title & Description
Analyze the diffs and conversation context to produce a high-quality commit message:

#### A. Commit Title
- Keep it concise: **$\le 72$ characters** (ideally $\le 50$ characters).
- Use imperative mood with a clear prefix (e.g., `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`) or direct action verb (e.g., `Add ...`, `Update ...`, `Fix ...`).
- Accurately describe the core problem solved or feature delivered.

#### B. Commit Description
- Provide a structured body separated from the title by a blank line.
- Use bullet points summarizing:
  - **What** was changed across key files/modules.
  - **Why** the change was made (the motivation/goal).
  - Any architectural decisions, bug fixes, or behavioral impacts.

### 4. Stage & Commit
1. Stage the relevant modified and untracked files:
   ```bash
   git add <files>
   ```
   *(Or `git add -A` after verifying no accidental scratch files are present).*
2. Execute the commit using the generated title and body:
   ```bash
   git commit -m "<Commit Title>" -m "<Commit Description>"
   ```

### 5. Push to GitHub `main` Branch
1. Determine the current local branch:
   ```bash
   git branch --show-current
   ```
2. Attempt to push to the `main` branch on `origin`:
   - If currently on `main`:
     ```bash
     git push origin main
     ```
   - If currently on another branch:
     - Confirm whether to push the current HEAD to `main` (`git push origin HEAD:main`) or merge into `main`.
3. Handle Push Results:
   - **Success**:
     - Display the commit hash (`git rev-parse --short HEAD`).
     - Display the full commit title and description.
     - Confirm successful push to `origin/main`.
   - **Failure / Conflict**:
     - If rejected because remote has changes:
       - Inform the user that the remote `main` is ahead.
       - Propose running `git pull --rebase origin main` before retrying.
     - If failed due to permissions or branch protection:
       - Report the exact error message from git without force pushing.
