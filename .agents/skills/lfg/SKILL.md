---
name: lfg
description: Grabs the top task from the to-do column in Todoist ('Pen and Paper Puzzles' or 'Morning Puzzles'), immediately moves it to the doing column, generates an implementation plan from the task details, comments, and attachments, executes and verifies the work, and upon successful completion moves the task to the done column and marks it complete. Trigger whenever the user types /lfg or asks to work on the next backlog task.
---

# LFG: Automated Todoist Task Ingestion, Planning & Lifecycle Execution

This skill manages the complete end-to-end task lifecycle for the **Pen and Paper Puzzles** (formerly **Morning Puzzles**) project in Todoist:
1. Identifying the top task in the **To-Do** column.
2. **Immediately moving** that task over to the **Doing** column upon identification.
3. Generating a comprehensive **implementation plan** utilizing all task context (title, short description, comments, and attachments).
4. Executing and verifying the code changes across all targets.
5. **Moving the task to the Done column** and **marking it complete** once work is successfully finished.

---

## Workflow Steps

When the user types `/lfg` (or requests to pick up the next task), execute this exact sequence:

### 1. Identify & Immediately Move Top Task from To-Do to Doing

Check for available Todoist tools or use the local fallback helper:

#### Path A: MCP Server Available
If Todoist MCP tools are present in your environment:
1. Search for project `Morning Puzzles` (or `Morning Games`, case-insensitive) using `find-projects`.
2. Find the `To-Do` column using `find-sections` (matching aliases: `To Do`, `Todo`, `to-do`, or `Backlog`).
3. Fetch tasks in the `To-Do` section using `find-tasks`, sorted by display order (ascending).
4. If no tasks exist in `To-Do`, inform the user that the To-Do column is empty and stop.
5. Select the top task (first in list).
6. **Immediately Move to the Doing Column**:
   - Locate the `Doing` column using `find-sections` (matching aliases: `Doing`, `In Progress`, or `in-progress`). If it does not exist, create it with `add-sections`.
   - Call `update-tasks` with `tasks: [{"id": taskId, "sectionId": doingSectionId}]` to move the task to `Doing` right away.
7. **Inspect Comments & Attachments**:
   - Call `find-comments` with `taskId`.
   - If any comment has a `fileAttachment` or `attachment`:
     - Extract `fileUrl` and call `view-attachment` with `fileUrl`.
     - For images or visual references, inspect them to understand visual specs, mockups, or bug reports.
     - Note all additional requirements and context from comment text.

#### Path B: Fallback via Helper Script (Zero-Restart)
If Todoist MCP tools are not registered in the current session, run the project's helper script:
```bash
python3 .agents/skills/lfg/scripts/todoist_helper.py pop-backlog --project "Morning Puzzles"
```
The script automatically:
- Finds the top task in `To-Do` / `Backlog`.
- Immediately moves it to `Doing` / `In Progress`.
- Retrieves all comments and attached file metadata into `task["attachments"]` and `task["comments"]`.

---

### 2. Handle Execution Responses

- **Missing Credentials**:
  If the script or tool errors with missing credentials:
  - Notify the user that `TODOIST_API_KEY` is not set.
  - Inform them they can set it in their shell (`export TODOIST_API_KEY=...`), add it to `.env.local` in the project root, or add it to `~/.gemini/config/mcp_config.json`.
  - Stop execution.

- **Empty To-Do Column**:
  If response has `"status": "empty"`:
  - Inform the user: *"The 'To-Do' column in Morning Puzzles has no tasks right now! 🎉"*
  - Stop execution.

- **Success (`status: "popped"`)**:
  Extract the task attributes:
  - **Task Title / Content**: `task["content"]`
  - **Description & Details**: `task["description"]`
  - **Attachments**: `task.get("attachments", [])` (or comments with attachments)
  - **Comments**: `task.get("comments", [])`
  - **Labels / Tags**: `task.get("labels", [])`
  - **Task ID & Link**: `task.get("id")`, `task.get("url")`
  - **Moved Destination**: `Doing` (or `In Progress`)

---

### 3. Display Task Summary Card

Print a clean summary card for the user:
```markdown
### 🎯 Active Task: [Task Title]
- **Project**: Morning Puzzles
- **Status**: Moved to `Doing`
- **Description**: [Task Description or "(No description provided)"]
- **Comments**: [Count of comments and highlights, or "(None)"]
- **Attachments**: [List filenames/types, or "(None)"]
- **Labels**: [Labels or None]
```

---

### 4. Generate the Implementation Plan

Synthesize all details from the task:
- **Task Title & Short Description**: Core objective and user intent.
- **Comments**: Implementation clarifications, design decisions, or constraints.
- **Attachments**: Inspect visual assets (reference mockups, thermal print scans, alignment guides, diagrams).
- **Codebase Context**: Check project architecture standards (`.agents/rules/puzzle_standards.md` Rules 1–17).

Generate a structured plan covering:
1. **User Goal & Problem Formulation**: Exact scope derived from the task title, description, comments, and attachments.
2. **Tri-Target Architecture & Parity Requirements**:
   - Python backend plugin (`server/app/puzzles/<game>.py`)
   - ESP32 firmware generator (`esp32-firmware/src/generators/<Game>Gen.cpp`)
   - Web Simulator emulation (`simulator/receipt_simulator.html`)
   - Arduino sketch sync (`./scripts/sync_arduino_sketch.sh`)
3. **Step-by-Step Implementation Tasks**: Specific file modifications and additions.
4. **Verification & Testing Plan**: Automated test suites to run (`test_puzzle_standards.py`, `test_thermal_format.py`, `test_visual_consistency.py`, etc.).

Present the plan to the user (as a plan artifact or structured walkthrough) before or during implementation.

---

### 5. Execute & Verify Work

1. Carry out the planned modifications cleanly.
2. Run automated validation suites:
   ```bash
   python3 server/test_puzzle_standards.py
   python3 server/test_thermal_format.py
   python3 server/test_visual_consistency.py
   ```
3. Run the Arduino IDE synchronization script if firmware was updated:
   ```bash
   ./scripts/sync_arduino_sketch.sh
   ```
4. Verify that all changes comply with Morning Puzzles Rules 1–17 and pass with zero warnings/errors.

---

### 6. Move Task to Done & Mark Complete

Once the work is **successfully complete and verified**, transition and complete the task in Todoist:

#### Path A: MCP Server Available
1. Find or create the `Done` column:
   - Use `find-sections` to locate the `Done` section (matching aliases `Done`, `Completed`).
   - If not found, create it using `add-sections` with `{"projectId": projectId, "name": "Done"}`.
2. Move the task from `Doing` to `Done`:
   - Call `update-tasks` with `tasks: [{"id": taskId, "sectionId": doneSectionId}]`.
3. Mark the task complete:
   - Call `complete-tasks` with `ids: [taskId]`.

#### Path B: Fallback via Helper Script
Run the helper script's `finish-task` command:
```bash
python3 .agents/skills/lfg/scripts/todoist_helper.py finish-task --task-id <TASK_ID> --project "Morning Puzzles"
```
The script will:
- Locate or create the `Done` section.
- Move the task into `Done`.
- Mark the task as completed in Todoist.

Finally, inform the user:
```markdown
### ✅ Task Completed: [Task Title]
- **Status**: Moved to `Done` and marked complete in Todoist.
- **Verification**: All test suites passed successfully.
```
