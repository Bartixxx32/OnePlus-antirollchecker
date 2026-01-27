import unittest
import sys
import os
from pathlib import Path

# Add root directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from parse_ini import get_section_name, parse_ini_section
from update_history import update_history_entry
from generate_readme import get_region_name

class TestConfig(unittest.TestCase):
    def test_devices_structure(self):
        for device_id, data in config.DEVICES.items():
            self.assertIn('name', data)
            self.assertIn('short_name', data)
            self.assertIn('models', data)
            self.assertIn('id', data)

    def test_mappings(self):
        self.assertEqual(config.DEVICE_ID_TO_NAME['oneplus_15'], 'OP 15')
        self.assertEqual(config.DEVICE_SHORT_TO_NAME['15'], 'OP 15')

class TestParseIni(unittest.TestCase):
    def test_get_section_name(self):
        self.assertEqual(get_section_name('15', 'CN'), 'OP 15 CN')
        self.assertEqual(get_section_name('12', 'GLO'), 'OP 12 GLO')

    def test_parse_ini_section(self):
        ini_content = """
[OP 15 CN]
url=http://example.com/1.zip
version=1.0.0
url=http://example.com/2.zip
version=2.0.0

[OP 12 GLO]
url=http://other.com
version=3.0
"""
        results = parse_ini_section(ini_content, 'OP 15 CN')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['version'], '1.0.0')
        self.assertEqual(results[0]['url'], 'http://example.com/1.zip')
        self.assertEqual(results[1]['version'], '2.0.0')

        results_empty = parse_ini_section(ini_content, 'NONEXISTENT')
        self.assertEqual(len(results_empty), 0)

class TestUpdateHistory(unittest.TestCase):
    def test_update_new_version(self):
        history = {'history': []}
        updated = update_history_entry(history, "1.0.0", 1, 1, 0, is_historical=False)
        self.assertTrue(updated)
        self.assertEqual(len(history['history']), 1)
        self.assertEqual(history['history'][0]['version'], "1.0.0")
        self.assertEqual(history['history'][0]['status'], "current")

    def test_update_existing_version(self):
        history = {'history': [{'version': "1.0.0", 'status': "current", 'last_checked': "2020-01-01"}]}
        updated = update_history_entry(history, "1.0.0", 1, 1, 0, is_historical=False)
        self.assertFalse(updated)
        self.assertNotEqual(history['history'][0]['last_checked'], "2020-01-01")

    def test_promote_archived(self):
        history = {'history': [{'version': "1.0.0", 'status': "archived"}]}
        updated = update_history_entry(history, "1.0.0", 1, 1, 0, is_historical=False)
        self.assertTrue(updated)
        self.assertEqual(history['history'][0]['version'], "1.0.0")
        self.assertEqual(history['history'][0]['status'], "current")

class TestGenerateReadme(unittest.TestCase):
    def test_get_region_name(self):
        self.assertEqual(get_region_name('CN'), 'China')
        self.assertEqual(get_region_name('UNKNOWN'), 'UNKNOWN')

if __name__ == '__main__':
    unittest.main()
