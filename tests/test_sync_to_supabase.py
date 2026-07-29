import importlib
import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


ENV = {"SUPABASE_URL": "https://test.supabase.co", "SUPABASE_SERVICE_KEY": "test-key"}


def reload_sync_module():
    import sync_to_supabase as _mod
    return importlib.reload(_mod)


class TestSyncToSupabase:
    @pytest.fixture(autouse=True)
    def setup_env(self):
        with patch.dict(os.environ, ENV, clear=True):
            mod = reload_sync_module()
            yield mod

    @pytest.fixture
    def mock_requests(self, setup_env):
        sync_module = setup_env
        with patch.object(sync_module, "requests") as mock_req:
            self._mock_get = MagicMock()
            self._mock_get.json.return_value = []
            self._mock_get.status_code = 200
            self._mock_post = MagicMock()
            self._mock_post.status_code = 201
            self._mock_delete = MagicMock()
            self._mock_delete.status_code = 204
            mock_req.request.side_effect = lambda method, *a, **kw: {
                "GET": self._mock_get,
                "DELETE": self._mock_delete,
            }.get(method, MagicMock())
            mock_req.post.return_value = self._mock_post
            yield mock_req, sync_module

    def write_db(self, data):
        with open("data/database.json", "w") as f:
            json.dump(data, f)

    def test_sync_with_empty_db(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self.write_db({})
        sync_module.sync()
        calls = mock_req.request.call_args_list
        get_calls = [c for c in calls if c[0][0] == "GET"]
        assert len(get_calls) >= 2

    def test_sync_with_models(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self.write_db({
            "CPH2581": {
                "device_name": "OnePlus 12", "device_order": 3,
                "expect_esim": True, "expect_barometer": False, "versions": {}
            }
        })
        sync_module.sync()
        post_call = mock_req.post.call_args
        assert post_call is not None
        url = post_call[0][0]
        assert "models" in url
        sent_json = post_call[1]["json"]
        assert any(m["model_id"] == "CPH2581" for m in sent_json)

    def test_sync_deletes_missing_models(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self._mock_get.json.side_effect = [
            [{"model_id": "CPH2581"}, {"model_id": "OLD_MODEL"}],
            []
        ]
        self.write_db({"CPH2581": {
            "device_name": "OnePlus 12", "device_order": 3,
            "expect_esim": True, "expect_barometer": False, "versions": {}
        }})
        sync_module.sync()
        delete_calls = [
            c for c in mock_req.request.call_args_list
            if c[0][0] == "DELETE"
        ]
        deleted_params = [c[1]["params"] for c in delete_calls]
        assert any(p.get("model_id") == "eq.OLD_MODEL" for p in deleted_params)

    def test_sync_deletes_orphaned_versions(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self._mock_get.json.side_effect = [
            [{"model_id": "CPH2581"}],
            [{"model_id": "CPH2581", "version_name": "OLD_VER"},
             {"model_id": "CPH2581", "version_name": "14.0.0.800"}]
        ]
        self.write_db({"CPH2581": {
            "device_name": "OnePlus 12", "device_order": 3,
            "expect_esim": True, "expect_barometer": False,
            "versions": {"14.0.0.800": {"arb": 0, "major": 3, "minor": 1,
                                          "first_seen": "2024-01", "last_checked": "2024-01",
                                          "status": "current", "is_hardcoded": False, "regions": ["GLO"]}}
        }})
        sync_module.sync()
        delete_calls = [
            c for c in mock_req.request.call_args_list
            if c[0][0] == "DELETE"
        ]
        version_deletes = [c for c in delete_calls if "version_name" in c[1].get("params", {})]
        assert any(c[1]["params"].get("version_name") == "eq.OLD_VER" for c in version_deletes)

    def test_sync_raises_on_missing_env(self):
        with patch.dict(os.environ, {}, clear=True):
            sync_module = reload_sync_module()
            sync_module.SUPABASE_URL = None
            sync_module.SUPABASE_SERVICE_KEY = None
            with pytest.raises(SystemExit):
                sync_module.sync()

    def test_sync_raises_on_missing_database(self, setup_env):
        sync_module = setup_env
        if Path("data/database.json").exists():
            os.remove("data/database.json")
        with pytest.raises(SystemExit):
            sync_module.sync()

    def test_sync_uses_correct_headers(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self.write_db({})
        sync_module.sync()
        for call_args in mock_req.request.call_args_list:
            headers = call_args[1]["headers"]
            assert headers["Accept-Profile"] == "arb_checker"
            assert headers["Content-Profile"] == "arb_checker"
            assert headers["apikey"] == "test-key"
            assert headers["Authorization"] == "Bearer test-key"

    def test_sync_upserts_versions(self, mock_requests):
        mock_req, sync_module = mock_requests
        os.makedirs("data", exist_ok=True)
        self.write_db({"CPH2581": {
            "device_name": "OnePlus 12", "device_order": 3,
            "expect_esim": True, "expect_barometer": False,
            "versions": {"14.0.0.800": {"arb": 0, "major": 3, "minor": 1,
                                          "md5": "abc123",
                                          "first_seen": "2024-01-01",
                                          "last_checked": "2024-01-15",
                                          "status": "current",
                                          "is_hardcoded": False,
                                          "regions": ["GLO"]}}
        }})
        sync_module.sync()
        post_calls = mock_req.post.call_args_list
        versions_post = None
        for c in post_calls:
            if "versions" in c[0][0]:
                versions_post = c
                break
        assert versions_post is not None
        sent = versions_post[1]["json"]
        assert len(sent) == 1
        assert sent[0]["model_id"] == "CPH2581"
        assert sent[0]["version_name"] == "14.0.0.800"
        assert sent[0]["arb"] == 0
        assert sent[0]["md5"] == "abc123"
        assert sent[0]["regions"] == ["GLO"]
