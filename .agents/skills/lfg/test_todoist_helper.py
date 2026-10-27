"""
Unit tests for todoist_helper.py
"""

import json
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add script directory to sys.path
script_dir = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(script_dir))

import todoist_helper


class TestTodoistHelper(unittest.TestCase):

    def setUp(self):
        self.client = todoist_helper.TodoistClient(api_token="test_token")

    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_find_project_case_insensitive(self, mock_get):
        mock_get.return_value = [
            {"id": "111", "name": "Work"},
            {"id": "222", "name": "Morning Puzzles"},
            {"id": "333", "name": "Personal"},
        ]
        p = self.client.find_project("morning puzzles")
        self.assertEqual(p["id"], "222")
        self.assertEqual(p["name"], "Morning Puzzles")

    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_find_project_not_found(self, mock_get):
        mock_get.return_value = [{"id": "111", "name": "Work"}]
        with self.assertRaises(ValueError):
            self.client.find_project("Morning Puzzles")

    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_get_tasks_sorted_by_order(self, mock_get):
        mock_get.return_value = [
            {"id": "task3", "content": "Third", "order": 3},
            {"id": "task1", "content": "First", "order": 1},
            {"id": "task2", "content": "Second", "order": 2},
        ]
        tasks = self.client.get_tasks("222", "sec_backlog")
        self.assertEqual([t["id"] for t in tasks], ["task1", "task2", "task3"])

    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_pop_backlog_empty(self, mock_get):
        # mock projects, sections, tasks
        def side_effect(endpoint, params=None):
            if endpoint == "projects":
                return [{"id": "222", "name": "Morning Puzzles"}]
            if endpoint == "sections":
                return [{"id": "s_backlog", "name": "Backlog"}]
            if endpoint == "tasks":
                return []
            return []
        mock_get.side_effect = side_effect

        res = self.client.pop_backlog("Morning Puzzles", move_to_in_progress=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "empty")

    @patch.object(todoist_helper.TodoistClient, "move_task_to_section")
    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_pop_backlog_success(self, mock_get, mock_move):
        mock_move.return_value = True

        def side_effect(endpoint, params=None):
            if endpoint == "projects":
                return [{"id": "222", "name": "Morning Puzzles"}]
            if endpoint == "sections":
                return [
                    {"id": "s_backlog", "name": "Backlog"},
                    {"id": "s_progress", "name": "In Progress"},
                ]
            if endpoint == "tasks":
                return [
                    {"id": "t1", "content": "Add Slitherlink puzzle", "description": "Implement 8x8 Slitherlink", "order": 1},
                    {"id": "t2", "content": "Add Sudoku generator", "description": "Daily Sudoku", "order": 2},
                ]
            return []
        mock_get.side_effect = side_effect

        res = self.client.pop_backlog("Morning Puzzles", move_to_in_progress=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "popped")
        self.assertEqual(res["task"]["id"], "t1")
        self.assertEqual(res["task"]["content"], "Add Slitherlink puzzle")
        self.assertEqual(res["moved_to_section"], "In Progress")
        mock_move.assert_called_once_with("t1", "s_progress")

    @patch.object(todoist_helper.TodoistClient, "move_task_to_section")
    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_pop_backlog_immediate_move_to_doing(self, mock_get, mock_move):
        mock_move.return_value = True

        def side_effect(endpoint, params=None):
            if endpoint == "projects":
                return [{"id": "222", "name": "Morning Puzzles"}]
            if endpoint == "sections":
                return [
                    {"id": "s_todo", "name": "To Do"},
                    {"id": "s_doing", "name": "Doing"},
                ]
            if endpoint == "tasks":
                return [
                    {"id": "t10", "content": "Fix Sudoku solver", "description": "Fix edge case", "order": 1},
                ]
            return []
        mock_get.side_effect = side_effect

        res = self.client.pop_backlog("Morning Puzzles", move_to_doing=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "popped")
        self.assertEqual(res["task"]["id"], "t10")
        self.assertEqual(res["moved_to_section"], "Doing")
        mock_move.assert_called_once_with("t10", "s_doing")

    @patch.object(todoist_helper.TodoistClient, "complete_task")
    @patch.object(todoist_helper.TodoistClient, "move_task_to_section")
    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_finish_task(self, mock_get, mock_move, mock_complete):
        mock_move.return_value = True
        mock_complete.return_value = True

        def side_effect(endpoint, params=None):
            if endpoint == "projects":
                return [{"id": "222", "name": "Morning Puzzles"}]
            if endpoint == "sections":
                return [
                    {"id": "s_doing", "name": "Doing"},
                    {"id": "s_done", "name": "Done"},
                ]
            return []
        mock_get.side_effect = side_effect

        res = self.client.finish_task(task_id="t10", project_name="Morning Puzzles")
        self.assertTrue(res["success"])
        self.assertEqual(res["status"], "completed")
        self.assertEqual(res["task_id"], "t10")
        self.assertEqual(res["moved_to_section"], "Done")
        mock_move.assert_called_once_with("t10", "s_done")
        mock_complete.assert_called_once_with("t10")

    @patch("urllib.request.urlopen")
    def test_complete_task_sync_api(self, mock_urlopen):
        # Mock Sync API returning ok
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"sync_status": {"test-uuid": "ok"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        with patch("uuid.uuid4", return_value="test-uuid"):
            res = self.client.complete_task("t10")
            self.assertTrue(res)

    @patch.object(todoist_helper.TodoistClient, "_http_get")
    def test_section_aliases(self, mock_get):
        mock_get.return_value = [
            {"id": "s1", "name": "To Do"},
            {"id": "s2", "name": "Doing"},
            {"id": "s3", "name": "Done"},
        ]
        s_todo = self.client.get_or_create_section("222", "backlog")
        self.assertEqual(s_todo["id"], "s1")

        s_doing = self.client.get_or_create_section("222", "in progress")
        self.assertEqual(s_doing["id"], "s2")

        s_done = self.client.get_or_create_section("222", "completed")
        self.assertEqual(s_done["id"], "s3")


if __name__ == "__main__":
    unittest.main()
