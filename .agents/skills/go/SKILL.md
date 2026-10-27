---
name: go
description: Inspects code diff, commits changes, and opens a Pull Request to main by delegating to the /pr skill. Use whenever the user types /go or asks to commit and push code.
---

# Go (Redirect to /pr)

The `/go` skill has been upgraded to enforce the project's **Pull Request & CI Workflow**. 

When `/go` is invoked, execute the exact workflow defined in [`/pr`](file:///Users/brian.bimschleger/Documents/GitHub/MOrning%20Puzzles/.agents/skills/pr/SKILL.md):
1. Inspect code changes and clean up unintended files.
2. Ensure work is on a dedicated feature branch (branching automatically if on `main`).
3. Run pre-commit checks (`sync_arduino_sketch.sh` and `test_puzzle_standards.py`).
4. Stage and commit changes with a structured title and description.
5. Push the branch to `origin`.
6. Open a GitHub Pull Request targeting `main`.
