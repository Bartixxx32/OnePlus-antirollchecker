import unittest
from config import (
    DEVICE_CONFIG,
    DEVICE_ORDER,
    get_device_map_for_fetch,
    get_device_metadata,
    get_device_short_name_map
)

class TestConfig(unittest.TestCase):
    def test_device_config_structure(self):
        """Verify that DEVICE_CONFIG has the correct structure."""
        self.assertIsInstance(DEVICE_CONFIG, dict)
        for key, value in DEVICE_CONFIG.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn("name", value)
            self.assertIn("short_name", value)
            self.assertIn("models", value)
            self.assertIsInstance(value["models"], dict)

    def test_device_order_validity(self):
        """Verify that all items in DEVICE_ORDER exist in DEVICE_CONFIG."""
        for device_id in DEVICE_ORDER:
            self.assertIn(device_id, DEVICE_CONFIG)

    def test_get_device_map_for_fetch(self):
        """Verify that get_device_map_for_fetch returns a valid mapping."""
        mapping = get_device_map_for_fetch()
        self.assertIsInstance(mapping, dict)
        for k, v in mapping.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, str)
        # Check expected value
        self.assertEqual(mapping.get("oneplus_15"), "OP 15")

    def test_get_device_metadata(self):
        """Verify that get_device_metadata returns expected metadata."""
        metadata = get_device_metadata()
        self.assertIsInstance(metadata, dict)
        for k, v in metadata.items():
            self.assertIsInstance(v, dict)
            self.assertIn("name", v)
            self.assertIn("models", v)
        # Check expected value
        self.assertEqual(metadata["15"]["name"], "OnePlus 15")

    def test_get_device_short_name_map(self):
        """Verify that get_device_short_name_map returns expected mapping."""
        mapping = get_device_short_name_map()
        self.assertIsInstance(mapping, dict)
        # Check expected value
        self.assertEqual(mapping.get("15"), "OP 15")

if __name__ == '__main__':
    unittest.main()
