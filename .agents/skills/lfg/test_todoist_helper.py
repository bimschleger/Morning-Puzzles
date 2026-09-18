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


if __name__ == "__main__":
    unittest.main()
