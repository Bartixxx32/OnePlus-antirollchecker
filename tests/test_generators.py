import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path

# Import the modules
from generate_site import process_data, generate
from generate_readme import generate_readme

class TestGenerators(unittest.TestCase):

    @patch('generate_site.Path.exists')
    @patch('generate_site.load_all_history')
    @patch('generate_site.Environment')
    @patch('builtins.open', new_callable=mock_open)
    @patch('generate_site.Path.mkdir')
    def test_site_generate_flow(self, mock_mkdir, mock_open_file, mock_env, mock_load, mock_exists):
        """Test the full site generation flow (mocked)."""
        mock_exists.return_value = True
        mock_load.return_value = {}
        mock_template = MagicMock()
        mock_env.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html></html>"

        generate(Path("history"), Path("output"), Path("templates"))

        mock_load.assert_called_once()
        mock_template.render.assert_called_once()
        mock_mkdir.assert_called_once()
        mock_open_file.assert_called_once()

    def test_site_process_data(self):
        """Test processing history data for the website."""
        # Setup mock data
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [
                    {"version": "1.0.0", "arb": 0, "status": "current", "last_checked": "2024-01-01"},
                    {"version": "0.9.0", "arb": 0, "status": "archived", "last_checked": "2023-12-01"}
                ]
            },
            "15_CN": {
                "model": "PLK110",
                "history": [
                    {"version": "1.0.0_CN", "arb": 1, "status": "current", "last_checked": "2024-01-01"}
                ]
            }
        }

        # We need to mock DEVICE_METADATA to ensure "15" is processed
        with patch('generate_site.DEVICE_METADATA', {
            "15": {
                "name": "OnePlus 15",
                "models": {"GLO": "CPH2747", "CN": "PLK110"}
            }
        }):
            with patch('generate_site.DEVICE_ORDER', ["15"]):
                devices = process_data(history_data)

                self.assertEqual(len(devices), 1)
                device = devices[0]
                self.assertEqual(device['name'], "OnePlus 15")
                self.assertEqual(len(device['variants']), 2)

                # Check Global variant
                glo = next(v for v in device['variants'] if v['region_name'] == 'Global')
                self.assertEqual(glo['version'], "1.0.0")
                self.assertEqual(glo['arb'], 0)
                self.assertTrue(glo['is_safe'])

                # Check CN variant
                cn = next(v for v in device['variants'] if v['region_name'] == 'China')
                self.assertEqual(cn['version'], "1.0.0_CN")
                self.assertEqual(cn['arb'], 1)
                self.assertFalse(cn['is_safe'])

    def test_generate_readme_content(self):
        """Test that README generation produces expected strings."""
        history_data = {
            "15_GLO": {
                "model": "CPH2747",
                "history": [
                    {"version": "1.0.0", "arb": 0, "status": "current", "last_checked": "2024-01-01", "major": 1, "minor": 0}
                ]
            }
        }

        with patch('generate_readme.DEVICE_METADATA', {
            "15": {
                "name": "OnePlus 15",
                "models": {"GLO": "CPH2747"}
            }
        }):
            with patch('generate_readme.DEVICE_ORDER', ["15"]):
                readme = generate_readme(history_data)

                self.assertIn("# OnePlus Anti-Rollback (ARB) Checker", readme)
                self.assertIn("OnePlus 15", readme)
                self.assertIn("| Global | CPH2747 | 1.0.0", readme)
                self.assertIn("**0**", readme) # ARB index
                self.assertIn("✅", readme) # Safe icon

if __name__ == '__main__':
    unittest.main()
