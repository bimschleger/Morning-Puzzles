#!/usr/bin/env python3
"""
Todoist Helper for Morning Puzzles (/lfg Skill)

Provides robust zero-dependency integration with Todoist REST API v2 and Sync API v9.
Supports:
  - status: Validates credentials and inspects 'Morning Puzzles' project & sections.
  - pop-backlog: Finds 'Morning Puzzles', grabs the top task in 'Backlog',
                 ensures 'In Progress' section exists, moves the task to 'In Progress',
                 and outputs structured task JSON for /grill-me.
  - peek-backlog: Previews the top task in 'Backlog' without moving it.
"""

from __future__ import annotations

import os
import sys
import json
import uuid
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Optional, Union, List, Dict, Any


def load_api_token() -> str:
    """Finds and returns the Todoist API token from env, .env.local, or .env."""
    token = os.environ.get("TODOIST_API_KEY") or os.environ.get("TODOIST_API_TOKEN")
    if token and token.strip():
        return token.strip()

    # Check .env.local and .env in current and parent directories
    candidate_dirs = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parents[3],  # repo root if in .agents/skills/lfg/scripts/
    ]

    for directory in candidate_dirs:
        for filename in [".env.local", ".env"]:
            file_path = directory / filename
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("#") or not line:
                                continue
                            if "=" in line:
                                key, val = line.split("=", 1)
                                key = key.strip()
                                val = val.strip().strip("'\"")
                                if key in ("TODOIST_API_KEY", "TODOIST_API_TOKEN") and val:
                                    return val
                except Exception:
                    pass

    return ""


class TodoistClient:
    REST_BASE_URL = "https://api.todoist.com/rest/v2"
    SYNC_BASE_URL = "https://api.todoist.com/sync/v9/sync"

    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError(
                "Todoist API token not found. Please set TODOIST_API_KEY in your environment "
                "or add TODOIST_API_KEY=your_token to .env.local in the workspace."
            )
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "MorningPuzzles-LFG-Skill/1.0"
        }

    def _http_get(self, endpoint: str, params: dict = None) -> list | dict:
        url = f"{self.REST_BASE_URL}/{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=self.headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Todoist API GET {endpoint} failed (HTTP {e.code}): {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to Todoist API: {e.reason}")

    def _http_post(self, endpoint: str, data: dict) -> list | dict:
        url = f"{self.REST_BASE_URL}/{endpoint}"
        body_bytes = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body_bytes, headers=self.headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Todoist API POST {endpoint} failed (HTTP {e.code}): {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to Todoist API: {e.reason}")

    PROJECT_ALIASES = ["morning puzzles", "morning games"]
    BACKLOG_ALIASES = ["backlog", "todo", "to do"]
    IN_PROGRESS_ALIASES = ["in progress", "doing"]

    def find_project(self, project_name: str = "Morning Puzzles") -> dict:
        projects = self._http_get("projects")
        target = project_name.strip().lower()
        candidates = [target]
        if target in self.PROJECT_ALIASES:
            candidates = self.PROJECT_ALIASES

        for p in projects:
            p_name = p.get("name", "").strip().lower()
            if p_name in candidates:
                return p
        available = [p.get("name", "") for p in projects]
        raise ValueError(
            f"Project '{project_name}' not found in Todoist. Available projects: {available}"
        )

    def get_sections(self, project_id: str) -> list[dict]:
        return self._http_get("sections", {"project_id": project_id})

    def get_or_create_section(self, project_id: str, section_name: str) -> dict:
        sections = self.get_sections(project_id)
        target = section_name.strip().lower()
        candidates = [target]
        if target in self.IN_PROGRESS_ALIASES:
            candidates = self.IN_PROGRESS_ALIASES

        for s in sections:
            s_name = s.get("name", "").strip().lower()
            if s_name in candidates:
                return s
        # Create the section if missing
        new_sec = self._http_post("sections", {"project_id": project_id, "name": section_name})
        return new_sec

    def get_tasks(self, project_id: str, section_id: str = None) -> list[dict]:
        params = {"project_id": project_id}
        if section_id:
            params["section_id"] = section_id
        tasks = self._http_get("tasks", params)
        # Sort by display order (order ascending)
        tasks.sort(key=lambda t: t.get("order", 0))
        return tasks

    def move_task_to_section(self, task_id: str, section_id: str) -> bool:
        """Moves a task to a different section using the Todoist Sync API v9 item_move command."""
        cmd_uuid = str(uuid.uuid4())
        commands = [
            {
                "type": "item_move",
                "uuid": cmd_uuid,
                "args": {
                    "id": task_id,
                    "section_id": section_id
                }
            }
        ]
        post_data = urllib.parse.urlencode({"commands": json.dumps(commands)}).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MorningPuzzles-LFG-Skill/1.0"
        }
        req = urllib.request.Request(self.SYNC_BASE_URL, data=post_data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                sync_status = resp_json.get("sync_status", {})
                status = sync_status.get(cmd_uuid)
                if status == "ok":
                    return True
                if isinstance(status, dict) and "error" in status:
                    raise RuntimeError(f"Sync API error moving task: {status}")
                return True
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else ""
            raise RuntimeError(f"Sync API item_move failed (HTTP {e.code}): {err_body}")

    def get_comments(self, task_id: str) -> list[dict]:
        """Fetches comments for a given task ID."""
        try:
            return self._http_get("comments", {"task_id": task_id})
        except Exception:
            return []

    def pop_backlog(self, project_name: str = "Morning Puzzles", move_to_in_progress: bool = True) -> dict:
        project = self.find_project(project_name)
        project_id = project["id"]

        sections = self.get_sections(project_id)
        backlog_sec = None
        for s in sections:
            s_name = s.get("name", "").strip().lower()
            if s_name in self.BACKLOG_ALIASES:
                backlog_sec = s
                break

        if not backlog_sec:
            available_secs = [s.get("name", "") for s in sections]
            return {
                "success": False,
                "error": f"Section 'Backlog' (or 'Todo') not found in project '{project_name}'. Found sections: {available_secs}"
            }

        tasks = self.get_tasks(project_id, backlog_sec["id"])
        if not tasks:
            return {
                "success": True,
                "status": "empty",
                "project_name": project["name"],
                "section_name": backlog_sec["name"],
                "message": f"Backlog in '{project_name}' is empty. No tasks to pick up!"
            }

        top_task = tasks[0]

        # Fetch comments and attachments
        comments = self.get_comments(top_task["id"])
        attachments = []
        for c in comments:
            att = c.get("attachment") or c.get("fileAttachment")
            if att:
                attachments.append({
                    "file_name": att.get("file_name") or att.get("fileName", ""),
                    "file_type": att.get("file_type") or att.get("fileType", ""),
                    "file_url": att.get("file_url") or att.get("fileUrl", ""),
                    "resource_type": att.get("resource_type") or att.get("resourceType", ""),
                })

        if move_to_in_progress:
            in_progress_sec = self.get_or_create_section(project_id, "In Progress")
            self.move_task_to_section(top_task["id"], in_progress_sec["id"])
            moved_to = in_progress_sec["name"]
            moved_section_id = in_progress_sec["id"]
        else:
            moved_to = None
            moved_section_id = None

        return {
            "success": True,
            "status": "popped",
            "project_name": project["name"],
            "project_id": project_id,
            "moved_to_section": moved_to,
            "task": {
                "id": top_task.get("id"),
                "content": top_task.get("content", ""),
                "description": top_task.get("description", ""),
                "priority": top_task.get("priority", 1),
                "labels": top_task.get("labels", []),
                "url": top_task.get("url", ""),
                "due": top_task.get("due"),
                "order": top_task.get("order", 0),
                "comments": [{"id": c.get("id"), "content": c.get("content", ""), "posted_at": c.get("posted_at")} for c in comments],
                "attachments": attachments,
            }
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Todoist Helper for /lfg")
    parser.add_argument("command", choices=["status", "pop-backlog", "peek-backlog"], help="Command to run")
    parser.add_argument("--project", default="Morning Puzzles", help="Project name (default: 'Morning Puzzles')")
    parser.add_argument("--token", default="", help="Todoist API token (optional override)")
    args = parser.parse_args()

    token = args.token or load_api_token()
    if not token:
        print(json.dumps({
            "success": False,
            "error": "No Todoist API token found. Please set TODOIST_API_KEY environment variable or add to .env.local."
        }, indent=2))
        sys.exit(1)

    client = TodoistClient(token)

    try:
        if args.command == "status":
            project = client.find_project(args.project)
            sections = client.get_sections(project["id"])
            sec_summary = []
            for s in sections:
                tasks = client.get_tasks(project["id"], s["id"])
                sec_summary.append({
                    "id": s["id"],
                    "name": s["name"],
                    "task_count": len(tasks),
                    "tasks": [{"id": t["id"], "content": t["content"], "order": t.get("order", 0)} for t in tasks]
                })
            print(json.dumps({
                "success": True,
                "project": {"id": project["id"], "name": project["name"]},
                "sections": sec_summary
            }, indent=2))

        elif args.command == "pop-backlog":
            result = client.pop_backlog(args.project, move_to_in_progress=True)
            print(json.dumps(result, indent=2))

        elif args.command == "peek-backlog":
            result = client.pop_backlog(args.project, move_to_in_progress=False)
            print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
