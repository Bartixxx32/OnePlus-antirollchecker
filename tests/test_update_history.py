import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
from datetime import datetime
from update_history import load_history, update_history_entry

class TestUpdateHistory(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"history": []}')
    def test_load_history_exists(self, mock_file):
        """Test loading existing history."""
        mock_path = MagicMock()
        mock_path.exists.return_value = True

        result = load_history(mock_path)
        self.assertEqual(result, {"history": []})
        mock_file.assert_called_once()

    def test_load_history_new(self):
        """Test loading (creating) new history."""
        mock_path = MagicMock()
        mock_path.exists.return_value = False

        result = load_history(mock_path)
        self.assertEqual(result, {"history": []})

    def test_update_history_new_version(self):
        """Test adding a completely new version."""
        history = {"history": []}
        version = "1.0.0"
        is_new = update_history_entry(history, version, 0, 1, 0, is_historical=False)

        self.assertTrue(is_new)
        self.assertEqual(len(history['history']), 1)
        self.assertEqual(history['history'][0]['version'], version)
        self.assertEqual(history['history'][0]['status'], 'current')

    def test_update_history_existing_version(self):
        """Test updating an existing version (timestamp update)."""
        history = {
            "history": [
                {"version": "1.0.0", "arb": 0, "status": "current", "last_checked": "2020-01-01"}
            ]
        }
        is_new = update_history_entry(history, "1.0.0", 0, 1, 0, is_historical=False)

        self.assertFalse(is_new)
        self.assertEqual(len(history['history']), 1)
        # Check that date was updated
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(history['history'][0]['last_checked'], today)

    def test_update_history_new_version_displaces_old(self):
        """Test that a new version archives the old one."""
        history = {
            "history": [
                {"version": "1.0.0", "arb": 0, "status": "current"}
            ]
        }
        is_new = update_history_entry(history, "2.0.0", 1, 1, 0, is_historical=False)

        self.assertTrue(is_new)
        self.assertEqual(len(history['history']), 2)

        # New version should be first and current
        self.assertEqual(history['history'][0]['version'], "2.0.0")
        self.assertEqual(history['history'][0]['status'], 'current')

        # Old version should be archived
        self.assertEqual(history['history'][1]['version'], "1.0.0")
        self.assertEqual(history['history'][1]['status'], 'archived')

    def test_update_history_historical_backfill(self):
        """Test adding a historical version (should not displace current)."""
        history = {
            "history": [
                {"version": "2.0.0", "arb": 1, "status": "current"}
            ]
        }
        is_new = update_history_entry(history, "1.0.0", 0, 1, 0, is_historical=True)

        self.assertFalse(is_new) # historical doesn't count as "new" release logic-wise in terms of notification usually, but let's check return
        self.assertEqual(len(history['history']), 2)

        # Current should still be current
        self.assertEqual(history['history'][0]['version'], "2.0.0")
        self.assertEqual(history['history'][0]['status'], 'current')

        # Historical should be at end
        self.assertEqual(history['history'][1]['version'], "1.0.0")
        self.assertEqual(history['history'][1]['status'], 'archived')

    def test_update_history_promote_archived(self):
        """Test that re-checking an archived version as current promotes it."""
        history = {
            "history": [
                {"version": "2.0.0", "arb": 1, "status": "current"},
                {"version": "1.0.0", "arb": 0, "status": "archived"}
            ]
        }
        # Suppose 2.0.0 was pulled, and we are back to 1.0.0 (downgrade detected as current? or just re-release)
        # The logic `update_history_entry` handles "Promote to current"
        is_new = update_history_entry(history, "1.0.0", 0, 1, 0, is_historical=False)

        self.assertTrue(is_new)
        self.assertEqual(history['history'][0]['version'], "1.0.0")
        self.assertEqual(history['history'][0]['status'], 'current')
        self.assertEqual(history['history'][1]['version'], "2.0.0")
        self.assertEqual(history['history'][1]['status'], 'archived')

    def test_md5_update(self):
        """Test that MD5 is updated if provided."""
        history = {
            "history": [
                {"version": "1.0.0", "arb": 0, "status": "current", "md5": "old_md5"}
            ]
        }
        update_history_entry(history, "1.0.0", 0, 1, 0, md5="new_md5")
        self.assertEqual(history['history'][0]['md5'], "new_md5")

if __name__ == '__main__':
    unittest.main()
