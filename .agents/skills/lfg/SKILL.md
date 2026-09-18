---
name: lfg
description: Grabs the top backlog task from the 'Morning Puzzles' project in Todoist, moves it to 'In Progress', synthesizes the objective, and immediately launches an interactive /grill-me design interview. Trigger whenever the user types /lfg or asks to work on the next backlog task.
---

# LFG: Automated Todoist Backlog Ingestion & /grill-me Launch

This skill automates taking the next prioritised work item from your Todoist "Morning Puzzles" backlog, transitioning it to "In Progress", and immediately launching an interactive `/grill-me` design interview so you can pair-program the solution without manual copy-pasting.

---

## Workflow Steps

When the user types `/lfg` (or requests to pick up the next backlog task), execute this exact sequence:

### 1. Retrieve & Move Top Backlog Task

Check for available Todoist tools or use the local fallback helper:

#### Path A: MCP Server Available
If Todoist MCP tools are present in your environment:
1. Search for project `Morning Puzzles` (or `Morning Games`, case-insensitive).
2. Find the `Backlog` (or `Todo`) section and fetch its tasks, sorted by display order (ascending).
3. If no tasks exist in `Backlog`/`Todo`, report that the backlog is empty and stop.
4. Select the top task (first in list).
5. Locate the `In Progress` (or `Doing`) section (create it under the project if it does not already exist).
6. Move the selected task to the `In Progress`/`Doing` section.

#### Path B: Fallback via Helper Script (Zero-Restart)
If Todoist MCP tools are not registered in the current session, run the project's helper script:
```bash
python3 .agents/skills/lfg/scripts/todoist_helper.py pop-backlog --project "Morning Puzzles"
```

### 2. Handle Execution Responses

- **Missing Credentials**:
  If the script or tool errors with missing credentials:
  - Notify the user that `TODOIST_API_KEY` is not set.
  - Inform them they can set it in their shell (`export TODOIST_API_KEY=...`), add it to `.env.local` in the project root, or add it to `~/.gemini/config/mcp_config.json`.
  - Stop execution.

- **Empty Backlog**:
  If response has `"status": "empty"`:
  - Inform the user: *"The 'Backlog' section in Morning Puzzles has no tasks right now! 🎉"*
  - Stop execution.

- **Success (`status: "popped"`)**:
  Extract the task attributes:
  - **Task Title / Content**: `task["content"]`
  - **Description & Details**: `task["description"]`
  - **Labels / Tags**: `task["labels"]`
  - **Task ID & Link**: `task["url"]`
  - **Moved Destination**: `In Progress`

### 3. Display Task Summary

Print a clean summary card for the user:
```markdown
### 🎯 Active Task: [Task Title]
- **Project**: Morning Puzzles
- **Section**: Moved to `In Progress`
- **Description**: [Task Description or "(No description provided)"]
- **Labels**: [Labels or None]
```

### 4. Synthesize Goal Prompt & Immediately Launch `/grill-me`

1. Synthesize a clear, outcome-focused goal prompt combining the task title, description, and context of the Morning Puzzles codebase:
   `[Outcome Goal]: <Interpolated description of what needs to be built, fixed, or updated>`
2. **Immediate Grilling**: Do **NOT** stop and wait for the user to manually type `/grill-me`. Transition directly into the `/grill-me` interview:
   - Identify the primary architectural/design fork for this task.
   - Formulate the first clarifying question with concrete options and a recommended answer.
   - Immediately invoke the `ask_question` tool to present Question 1 to the user.
