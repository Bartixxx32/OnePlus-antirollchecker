import json
import os
import pytest
import tempfile
from json import JSONDecodeError
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from generate_database import generate_database, load_history


class TestLoadHistory:
    def test_load_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            data = {"device": "OnePlus 12", "history": [{"version": "14.0.0.800"}]}
            with open(file_path, "w") as f:
                json.dump(data, f)
            result = load_history(file_path)
            assert result == data

    def test_load_missing_file(self):
        result = load_history(Path("/nonexistent/file.json"))
        assert result == {}

    def test_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad.json"
            with open(file_path, "w") as f:
                f.write("not json")
            with pytest.raises(json.JSONDecodeError):
                load_history(file_path)


class TestGenerateDatabase:
    @pytest.fixture
    def history_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            os.chdir(tmpdir)
            os.makedirs("data/history")
            yield Path(tmpdir)
            os.chdir(orig_cwd)

    def write_history(self, filename, data):
        path = Path("data/history") / filename
        with open(path, "w") as f:
            json.dump(data, f)

    def test_generates_single_model(self, history_dir):
        self.write_history("12_GLO.json", {
            "device": "OnePlus 12",
            "device_id": "12",
            "model": "CPH2581",
            "region": "GLO",
            "history": [
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "md5": "abc123", "first_seen": "2024-01-01",
                 "last_checked": "2024-01-15", "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert "CPH2581" in db
        assert db["CPH2581"]["device_name"] == "OnePlus 12"
        assert "14.0.0.800" in db["CPH2581"]["versions"]
        assert db["CPH2581"]["versions"]["14.0.0.800"]["arb"] == 0

    def test_multiple_regions_same_version(self, history_dir):
        self.write_history("12_GLO.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "GLO",
            "history": [
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "md5": "abc", "first_seen": "2024-01-01",
                 "last_checked": "2024-01-15", "status": "current"}
            ]
        })
        self.write_history("12_EU.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "EU",
            "history": [
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "md5": "def", "first_seen": "2024-01-01",
                 "last_checked": "2024-01-15", "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        version = db["CPH2581"]["versions"]["14.0.0.800"]
        assert sorted(version["regions"]) == ["EU", "GLO"]

    def test_different_md5_per_region(self, history_dir):
        self.write_history("12_GLO.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "GLO",
            "history": [
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "md5": "abc", "first_seen": "2024-01-01",
                 "last_checked": "2024-01-15", "status": "current"}
            ]
        })
        self.write_history("12_EU.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "EU",
            "history": [
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "md5": "def", "first_seen": "2024-01-01",
                 "last_checked": "2024-01-15", "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        md5_field = db["CPH2581"]["versions"]["14.0.0.800"]["md5"]
        assert isinstance(md5_field, dict)
        assert md5_field["GLO"] == "abc"
        assert md5_field["EU"] == "def"

    def test_unknown_device_order_to_999(self, history_dir):
        self.write_history("UnknownX_GLO.json", {
            "device": "Unknown", "device_id": "UnknownX", "model": "XXXXX",
            "region": "GLO",
            "history": [
                {"version": "1.0", "arb": 0, "major": 1, "minor": 0,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert db["XXXXX"]["device_order"] == 999

    def test_skips_model_without_model_number(self, history_dir):
        self.write_history("no_model.json", {
            "device": "Unknown", "device_id": "unknown", "region": "GLO",
            "history": []
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert db == {}

    def test_hardware_features_included(self, history_dir):
        self.write_history("15_GLO.json", {
            "device": "OnePlus 15", "device_id": "15", "model": "CPH2747",
            "region": "GLO",
            "history": [
                {"version": "16.0.0.100", "arb": 1, "major": 4, "minor": 0,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        meta = db["CPH2747"]
        assert "expect_esim" in meta
        assert "expect_barometer" in meta
        assert isinstance(meta["expect_esim"], bool)
        assert isinstance(meta["expect_barometer"], bool)

    def test_versions_sorted_descending(self, history_dir):
        self.write_history("12_GLO.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "GLO",
            "history": [
                {"version": "14.0.0.700", "arb": 0, "major": 3, "minor": 1,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "archived"},
                {"version": "14.0.0.900", "arb": 0, "major": 3, "minor": 1,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "current"},
                {"version": "14.0.0.800", "arb": 0, "major": 3, "minor": 1,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "archived"},
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        versions = list(db["CPH2581"]["versions"].keys())
        assert versions == ["14.0.0.900", "14.0.0.800", "14.0.0.700"]

    def test_no_history_directory(self, history_dir):
        os.rmdir("data/history")
        generate_database()
        assert not Path("data/database.json").exists()

    def test_empty_history_directory(self, history_dir):
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert db == {}

    def test_history_entry_without_version_skipped(self, history_dir):
        self.write_history("12_GLO.json", {
            "device": "OnePlus 12", "device_id": "12", "model": "CPH2581",
            "region": "GLO",
            "history": [
                {"arb": 0, "major": 3, "minor": 1}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert len(db["CPH2581"]["versions"]) == 0

    def test_is_hardcoded_flag_in_output(self, history_dir):
        self.write_history("Nord_CE_3_Lite_GLO.json", {
            "device": "OnePlus Nord CE 3 Lite",
            "device_id": "Nord CE 3 Lite",
            "model": "CPH2467",
            "region": "GLO",
            "history": [
                {"version": "CPH2467_11.0.0.1700(EX01)", "arb": 1, "major": 3, "minor": 0,
                 "first_seen": "2024-01-01", "last_checked": "2024-01-01",
                 "status": "current"}
            ]
        })
        generate_database()
        with open("data/database.json") as f:
            db = json.load(f)
        assert db["CPH2467"]["versions"]["CPH2467_11.0.0.1700(EX01)"]["is_hardcoded"] is True
