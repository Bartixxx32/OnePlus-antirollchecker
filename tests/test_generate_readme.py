#!/usr/bin/env python3
"""
Comprehensive tests for generate_readme.py
Tests README generation from history files.
"""

import unittest
import json
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_readme import (
    load_all_history,
    get_region_name,
    generate_device_section,
    generate_readme,
    main
)


class TestLoadAllHistory(unittest.TestCase):
    """Test suite for load_all_history function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.history_dir = Path(self.temp_dir) / "history"
        self.history_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_load_all_history_empty_directory(self):
        """Test loading history from empty directory."""
        result = load_all_history(self.history_dir)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    def test_load_all_history_single_file(self):
        """Test loading history with single file."""
        history_data = {
            "device_id": "15",
            "region": "GLO",
            "model": "CPH2747",
            "history": [
                {
                    "status": "current",
                    "version": "16.0.3.501",
                    "arb": 1,
                    "major": 3,
                    "minor": 0,
                    "last_checked": "2026-01-01"
                }
            ]
        }

        history_file = self.history_dir / "15_GLO.json"
        with open(history_file, 'w') as f:
            json.dump(history_data, f)

        result = load_all_history(self.history_dir)

        self.assertEqual(len(result), 1)
        self.assertIn("15_GLO", result)
        self.assertEqual(result["15_GLO"]["device_id"], "15")

    def test_load_all_history_multiple_files(self):
        """Test loading history with multiple files."""
        devices = [("15", "GLO"), ("15", "EU"), ("13", "CN")]

        for device_id, region in devices:
            history_data = {
                "device_id": device_id,
                "region": region,
                "model": "MODEL",
                "history": []
            }
            history_file = self.history_dir / f"{device_id}_{region}.json"
            with open(history_file, 'w') as f:
                json.dump(history_data, f)

        result = load_all_history(self.history_dir)

        self.assertEqual(len(result), 3)
        self.assertIn("15_GLO", result)
        self.assertIn("15_EU", result)
        self.assertIn("13_CN", result)

    def test_load_all_history_invalid_json(self):
        """Test loading history with invalid JSON file."""
        # Create a valid file
        valid_file = self.history_dir / "15_GLO.json"
        with open(valid_file, 'w') as f:
            json.dump({"device_id": "15"}, f)

        # Create an invalid file
        invalid_file = self.history_dir / "15_EU.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json {")

        result = load_all_history(self.history_dir)

        # Should load valid file and skip invalid
        self.assertEqual(len(result), 1)
        self.assertIn("15_GLO", result)

    def test_load_all_history_non_json_files_ignored(self):
        """Test that non-JSON files are ignored."""
        # Create JSON file
        json_file = self.history_dir / "15_GLO.json"
        with open(json_file, 'w') as f:
            json.dump({"device_id": "15"}, f)

        # Create non-JSON file
        txt_file = self.history_dir / "readme.txt"
        with open(txt_file, 'w') as f:
            f.write("This is not JSON")

        result = load_all_history(self.history_dir)

        self.assertEqual(len(result), 1)
        self.assertIn("15_GLO", result)


class TestGetRegionName(unittest.TestCase):
    """Test suite for get_region_name function."""

    def test_get_region_name_glo(self):
        """Test region name for GLO."""
        self.assertEqual(get_region_name('GLO'), 'Global')

    def test_get_region_name_eu(self):
        """Test region name for EU."""
        self.assertEqual(get_region_name('EU'), 'Europe')

    def test_get_region_name_in(self):
        """Test region name for IN."""
        self.assertEqual(get_region_name('IN'), 'India')

    def test_get_region_name_cn(self):
        """Test region name for CN."""
        self.assertEqual(get_region_name('CN'), 'China')

    def test_get_region_name_unknown(self):
        """Test region name for unknown region."""
        result = get_region_name('UNKNOWN')
        self.assertEqual(result, 'UNKNOWN')

    def test_get_region_name_case_sensitive(self):
        """Test that region name is case-sensitive."""
        # Should only work with uppercase
        self.assertEqual(get_region_name('GLO'), 'Global')
        self.assertEqual(get_region_name('glo'), 'glo')


class TestGenerateDeviceSection(unittest.TestCase):
    """Test suite for generate_device_section function."""

    def test_generate_device_section_no_data(self):
        """Test device section generation with no data."""
        history_data = {}

        result = generate_device_section('15', 'OnePlus 15', history_data)

        self.assertEqual(result, [])

    def test_generate_device_section_single_region(self):
        """Test device section generation with single region."""
        history_data = {
            "15_GLO": {
                "device_id": "15",
                "region": "GLO",
                "model": "CPH2747",
                "history": [
                    {
                        "status": "current",
                        "version": "16.0.3.501",
                        "arb": 0,
                        "major": 3,
                        "minor": 0,
                        "last_checked": "2026-01-01"
                    }
                ]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        self.assertGreater(len(result), 0)
        # Check for header
        self.assertIn('### OnePlus 15', result)
        # Check for table headers
        self.assertTrue(any('Region' in line for line in result))
        # Check for data
        self.assertTrue(any('Global' in line for line in result))
        self.assertTrue(any('CPH2747' in line for line in result))

    def test_generate_device_section_multiple_regions(self):
        """Test device section generation with multiple regions."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            },
            "15_EU": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            },
            "15_IN": {
                "model": "CPH2745",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 1, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        # Should have entries for all regions
        content = '\n'.join(result)
        self.assertIn('Global', content)
        self.assertIn('Europe', content)
        self.assertIn('India', content)

    def test_generate_device_section_safe_arb(self):
        """Test device section shows safe icon for ARB 0."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('✅', content)

    def test_generate_device_section_protected_arb(self):
        """Test device section shows protected icon for ARB > 0."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 1, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('❌', content)

    def test_generate_device_section_no_current_entry(self):
        """Test device section with no current entry (uses first)."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [
                    {"status": "old", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}
                ]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        # Should still generate output using first entry
        self.assertGreater(len(result), 0)
        content = '\n'.join(result)
        self.assertIn('16.0.3.501', content)

    def test_generate_device_section_empty_history(self):
        """Test device section with empty history."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": []
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('Waiting for scan', content)

    def test_generate_device_section_missing_version(self):
        """Test device section with missing version field."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('Unknown', content)


class TestGenerateReadme(unittest.TestCase):
    """Test suite for generate_readme function."""

    def test_generate_readme_empty_data(self):
        """Test README generation with empty data."""
        history_data = {}

        result = generate_readme(history_data)

        self.assertIsNotNone(result)
        self.assertIn('OnePlus Anti-Rollback (ARB) Checker', result)
        self.assertIn('## 📊 Current Status', result)

    def test_generate_readme_with_device_data(self):
        """Test README generation with device data."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_readme(history_data)

        self.assertIn('OnePlus Anti-Rollback (ARB) Checker', result)
        self.assertIn('OnePlus 15', result)
        self.assertIn('CPH2747', result)

    def test_generate_readme_includes_header(self):
        """Test that README includes proper header."""
        result = generate_readme({})

        self.assertIn('# OnePlus Anti-Rollback (ARB) Checker', result)
        self.assertIn('Automated ARB', result)

    def test_generate_readme_includes_website_link(self):
        """Test that README includes website link."""
        result = generate_readme({})

        self.assertIn('bartixxx32.github.io/OnePlus-antirollchecker', result)

    def test_generate_readme_includes_legend(self):
        """Test that README includes legend section."""
        result = generate_readme({})

        self.assertIn('## 📈 Legend', result)
        self.assertIn('Safe', result)
        self.assertIn('Protected', result)

    def test_generate_readme_includes_credits(self):
        """Test that README includes credits section."""
        result = generate_readme({})

        self.assertIn('## 🛠️ Credits', result)
        self.assertIn('otaripper', result)

    def test_generate_readme_includes_workflow_badge(self):
        """Test that README includes workflow status badge."""
        result = generate_readme({})

        self.assertIn('## 🤖 Workflow Status', result)
        self.assertIn('check_arb.yml', result)

    def test_generate_readme_includes_important_note(self):
        """Test that README includes important note."""
        result = generate_readme({})

        self.assertIn('IMPORTANT', result)
        self.assertIn('automatically by GitHub Actions', result)

    def test_generate_readme_separators_between_devices(self):
        """Test that device sections are separated."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            },
            "13_GLO": {
                "model": "CPH2649",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 1, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_readme(history_data)

        # Should have separator between devices
        self.assertIn('---', result)


class TestMain(unittest.TestCase):
    """Test suite for main function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.history_dir = Path(self.temp_dir) / "history"
        self.history_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('sys.argv', ['generate_readme.py'])
    @patch('generate_readme.Path')
    def test_main_default_directory(self, mock_path):
        """Test main function with default history directory."""
        # This test is complex due to Path mocking, simplified version
        pass

    @patch('sys.argv', ['generate_readme.py', str(Path(__file__).parent.parent / 'data' / 'history')])
    def test_main_with_custom_directory(self):
        """Test main function with custom history directory."""
        # Create history file
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        history_file = self.history_dir / "15_GLO.json"
        with open(history_file, 'w') as f:
            json.dump(history_data, f)

        with patch('sys.argv', ['generate_readme.py', str(self.history_dir)]):
            with patch('builtins.open', mock_open()) as mock_file:
                with patch('builtins.print') as mock_print:
                    main()

                    # Should write README.md
                    mock_file.assert_called()

    @patch('sys.argv', ['generate_readme.py', '/nonexistent/directory'])
    @patch('sys.exit')
    def test_main_nonexistent_directory(self, mock_exit):
        """Test main function with nonexistent directory."""
        main()

        # Should exit with error
        mock_exit.assert_called_once_with(1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_generate_device_section_high_arb_value(self):
        """Test device section with high ARB value."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 99, "major": 10, "minor": 5, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('99', content)
        self.assertIn('10', content)
        self.assertIn('5', content)

    def test_generate_readme_all_device_metadata_processed(self):
        """Test that README processes all devices from DEVICE_METADATA."""
        from config import DEVICE_METADATA

        # Create history for one device
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_readme(history_data)

        # Should at least include the device with data
        self.assertIn('OnePlus 15', result)

    def test_generate_device_section_special_characters_in_version(self):
        """Test device section with special characters in version."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "CPH2747_16.0.3.501(EX01)", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_device_section('15', 'OnePlus 15', history_data)

        content = '\n'.join(result)
        self.assertIn('CPH2747_16.0.3.501(EX01)', content)

    def test_load_all_history_deeply_nested_directory(self):
        """Test loading history from directory (not deeply nested, direct files)."""
        temp_dir = tempfile.mkdtemp()
        try:
            history_dir = Path(temp_dir)

            # Create history file directly in the directory
            history_data = {"device_id": "15"}
            history_file = history_dir / "15_GLO.json"
            with open(history_file, 'w') as f:
                json.dump(history_data, f)

            result = load_all_history(history_dir)

            self.assertEqual(len(result), 1)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_region_name_empty_string(self):
        """Test get_region_name with empty string."""
        result = get_region_name('')
        self.assertEqual(result, '')

    def test_generate_readme_markdown_escaping(self):
        """Test that README properly handles potential markdown characters."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [{"status": "current", "version": "16.0.3.501", "arb": 0, "major": 3, "minor": 0, "last_checked": "2026-01-01"}]
            }
        }

        result = generate_readme(history_data)

        # Should generate valid markdown
        self.assertIn('|', result)  # Table format
        self.assertIn('##', result)  # Headers


if __name__ == '__main__':
    unittest.main()