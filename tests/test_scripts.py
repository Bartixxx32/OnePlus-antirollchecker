import unittest
from unittest.mock import patch, MagicMock
import json
from pathlib import Path
import tempfile
import shutil
import os

# Import modules to test
import parse_ini
import generate_readme
import update_history
import fetch_firmware

class TestParseIni(unittest.TestCase):
    def test_parse_ini_section(self):
        ini_content = """
[OP 15 GLO]
url=https://example.com/fw1.zip
version=15.0.0.1
url=https://example.com/fw2.zip
version=15.0.0.2
        """
        results = parse_ini.parse_ini_section(ini_content, "[OP 15 GLO]")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['version'], "15.0.0.1")
        self.assertEqual(results[0]['url'], "https://example.com/fw1.zip")
        self.assertEqual(results[1]['version'], "15.0.0.2")
        self.assertEqual(results[1]['url'], "https://example.com/fw2.zip")

    def test_get_section_name(self):
        # Assuming config.py is correctly set up
        section = parse_ini.get_section_name("15", "GLO")
        self.assertEqual(section, "[OP 15 GLO]")
        section = parse_ini.get_section_name("INVALID", "GLO")
        self.assertIsNone(section)

class TestGenerateReadme(unittest.TestCase):
    def test_get_region_name(self):
        self.assertEqual(generate_readme.get_region_name("GLO"), "Global")
        self.assertEqual(generate_readme.get_region_name("CN"), "China")
        self.assertEqual(generate_readme.get_region_name("Unknown"), "Unknown")

    def test_generate_device_section(self):
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [
                    {
                        "version": "15.0.0.1",
                        "arb": 1,
                        "major": 15,
                        "minor": 0,
                        "first_seen": "2024-01-01",
                        "last_checked": "2024-01-02",
                        "status": "current"
                    }
                ]
            }
        }
        lines = generate_readme.generate_device_section("15", "OnePlus 15", history_data)
        content = "\n".join(lines)
        self.assertIn("### OnePlus 15 - Global (CPH2747)", content)
        self.assertIn("| 15.0.0.1 | **1** |", content)
        self.assertIn("🟢 Current", content)

class TestUpdateHistory(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.history_file = Path(self.test_dir) / "test_history.json"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_history_new(self):
        data = update_history.load_history(self.history_file)
        self.assertEqual(data, {"history": []})

    def test_update_history_entry_new(self):
        history = {"history": []}
        is_new = update_history.update_history_entry(history, "15.0.0.1", 1, 15, 0)
        self.assertTrue(is_new)
        self.assertEqual(len(history['history']), 1)
        self.assertEqual(history['history'][0]['version'], "15.0.0.1")
        self.assertEqual(history['history'][0]['status'], "current")

    def test_update_history_entry_existing(self):
        history = {
            "history": [
                {
                    "version": "15.0.0.1",
                    "status": "current",
                    "last_checked": "2020-01-01"
                }
            ]
        }
        is_new = update_history.update_history_entry(history, "15.0.0.1", 1, 15, 0)
        self.assertFalse(is_new)
        # Should update last_checked
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(history['history'][0]['last_checked'], today)

    def test_update_history_entry_promotion(self):
        # Test promoting an archived version to current (e.g. rollback situation or error correction)
        # Though the logic in update_history mainly handles "not is_historical" => promote
        history = {
            "history": [
                {
                    "version": "16.0.0.0",
                    "status": "current"
                },
                {
                    "version": "15.0.0.1",
                    "status": "archived"
                }
            ]
        }
        # Update 15.0.0.1 as current (not historical)
        is_new = update_history.update_history_entry(history, "15.0.0.1", 1, 15, 0, is_historical=False)
        self.assertTrue(is_new) # It returns True because it modified the list order/status significantly
        self.assertEqual(history['history'][0]['version'], "15.0.0.1")
        self.assertEqual(history['history'][0]['status'], "current")
        self.assertEqual(history['history'][1]['status'], "archived")

class TestFetchFirmware(unittest.TestCase):
    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_success(self, mock_session):
        # Mock response for the initial GET request (device mapping)
        mock_response_get = MagicMock()
        mock_response_get.text = """
        <html>
            <select id="device" data-devices="{&quot;OP 15&quot;: {&quot;GLO&quot;: [&quot;v1&quot;]}}"></select>
        </html>
        """

        # Mock response for the POST request (getting URL)
        mock_response_post = MagicMock()
        mock_response_post.text = """
        <html>
            <div id="resultBox" data-url="https://example.com/signed.zip"></div>
        </html>
        """

        mock_session.return_value.get.return_value = mock_response_get
        mock_session.return_value.post.return_value = mock_response_post

        url = fetch_firmware.get_signed_url("oneplus_15", "GLO")
        self.assertEqual(url, "https://example.com/signed.zip")

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_device_not_found(self, mock_session):
        mock_response_get = MagicMock()
        mock_response_get.text = """
        <html>
            <select id="device" data-devices="{&quot;OP 15&quot;: {}}"></select>
        </html>
        """
        mock_session.return_value.get.return_value = mock_response_get

        # "oneplus_99" doesn't exist in our config/mapping or the mocked HTML
        url = fetch_firmware.get_signed_url("oneplus_99", "GLO")
        self.assertIsNone(url)

if __name__ == '__main__':
    unittest.main()
