import json
import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from update_history import load_history, save_history, update_history_entry


class TestLoadHistory:
    def test_load_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            data = {"history": [{"version": "1.0"}]}
            with open(file_path, "w") as f:
                json.dump(data, f)
            result = load_history(file_path)
            assert result == data

    def test_load_non_existent_file(self):
        result = load_history(Path("/nonexistent/path.json"))
        assert result == {"history": []}

    def test_load_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.json"
            with open(file_path, "w") as f:
                f.write("{}")
            result = load_history(file_path)
            assert result == {}


class TestSaveHistory:
    def test_save_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "nested" / "test.json"
            data = {"history": [{"version": "1.0"}]}
            save_history(file_path, data)
            assert file_path.exists()
            with open(file_path) as f:
                assert json.load(f) == data

    def test_save_overwrites_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            with open(file_path, "w") as f:
                json.dump({"old": "data"}, f)
            data = {"history": [{"version": "2.0"}]}
            save_history(file_path, data)
            with open(file_path) as f:
                assert json.load(f) == data


class TestUpdateHistoryEntry:
    def test_add_new_version_as_current(self):
        history = {"history": []}
        added_new = update_history_entry(history, "14.0.0.800", 0, 3, 1, is_historical=False)
        assert added_new is True
        assert len(history["history"]) == 1
        entry = history["history"][0]
        assert entry["version"] == "14.0.0.800"
        assert entry["arb"] == 0
        assert entry["major"] == 3
        assert entry["minor"] == 1
        assert entry["status"] == "current"
        assert "first_seen" in entry
        assert "last_checked" in entry

    def test_add_new_version_with_md5(self):
        history = {"history": []}
        update_history_entry(history, "14.0.0.800", 0, 3, 1, md5="abc123")
        assert history["history"][0]["md5"] == "abc123"

    def test_add_existing_version_returns_false(self):
        history = {"history": [{"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current", "md5": "oldmd5"}]}
        result = update_history_entry(history, "14.0.0.800", 0, 3, 1)
        assert result is False

    def test_add_existing_updates_last_checked(self):
        history = {"history": [{"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current"}]}
        update_history_entry(history, "14.0.0.800", 0, 3, 1)
        assert history["history"][0]["last_checked"] != "2024-01-01"

    def test_new_current_archives_old(self):
        history = {"history": [{"version": "14.0.0.700", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current"}]}
        update_history_entry(history, "14.0.0.800", 0, 3, 1)
        statuses = {e["version"]: e["status"] for e in history["history"]}
        assert statuses["14.0.0.800"] == "current"
        assert statuses["14.0.0.700"] == "archived"

    def test_historical_entry_does_not_archive(self):
        history = {"history": [{"version": "14.0.0.700", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current"}]}
        update_history_entry(history, "13.0.0.500", 1, 2, 1, is_historical=True)
        assert history["history"][0]["status"] == "current"

    def test_warning_on_md5_change(self, capsys):
        history = {"history": [{"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current", "md5": "oldmd5"}]}
        update_history_entry(history, "14.0.0.800", 0, 3, 1, md5="newmd5")
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "MD5 changed" in captured.out

    def test_no_warning_on_first_md5(self, capsys):
        history = {"history": [{"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                                "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                                "status": "current"}]}
        update_history_entry(history, "14.0.0.800", 0, 3, 1, md5="firstmd5")
        captured = capsys.readouterr()
        assert "WARNING" not in captured.out

    def test_sort_current_first(self):
        history = {"history": [
            {"version": "14.0.0.700", "arb": 0, "major": 3, "minor": 1,
             "first_seen": "2024-02-01", "last_checked": "2024-02-01", "status": "archived"},
        ]}
        update_history_entry(history, "14.0.0.800", 0, 3, 1)
        assert history["history"][0]["status"] == "current"
        assert history["history"][0]["version"] == "14.0.0.800"

    def test_historical_entry_appended_not_inserted(self):
        history = {"history": [
            {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
             "first_seen": "2024-01-01", "last_checked": "2024-01-01", "status": "current"},
        ]}
        update_history_entry(history, "13.0.0.500", 1, 2, 0, is_historical=True)
        assert history["history"][-1]["version"] == "13.0.0.500"
