import unittest
from config import (
    DEVICE_METADATA,
    DEVICE_ORDER,
    SPRING_MAPPING,
    OOS_MAPPING,
    get_display_name,
    get_model_number
)

class TestConfig(unittest.TestCase):
    def test_get_display_name(self):
        """Test getting display name for various devices."""
        self.assertEqual(get_display_name("15"), "OnePlus 15")
        self.assertEqual(get_display_name("12"), "OnePlus 12")
        self.assertEqual(get_display_name("Find X5 Pro"), "Oppo Find X5 Pro")
        self.assertEqual(get_display_name("UnknownDevice"), "OnePlus UnknownDevice")

    def test_get_model_number(self):
        """Test getting model number for device regions."""
        # Known device and region
        self.assertEqual(get_model_number("15", "EU"), "CPH2747")
        self.assertEqual(get_model_number("12", "IN"), "CPH2573")

        # Known device, unknown region
        self.assertEqual(get_model_number("15", "MARS"), "Unknown")

        # Unknown device
        self.assertEqual(get_model_number("AlienPhone", "GLO"), "Unknown")

    def test_device_metadata_structure(self):
        """Ensure DEVICE_METADATA has required keys."""
        for device_id, meta in DEVICE_METADATA.items():
            self.assertIn("name", meta, f"{device_id} missing 'name'")
            self.assertIn("models", meta, f"{device_id} missing 'models'")
            self.assertIsInstance(meta["models"], dict, f"{device_id} models is not a dict")

    def test_device_order_consistency(self):
        """Ensure devices in DEVICE_ORDER exist in METADATA (warning only if not)."""
        for device_id in DEVICE_ORDER:
            # It's okay if metadata has more devices, but order list should point to valid ones ideally
            if device_id not in DEVICE_METADATA:
                print(f"Warning: Device {device_id} in DEVICE_ORDER but not in DEVICE_METADATA")

    def test_mappings_exist(self):
        """Check that mappings cover most devices."""
        # Just check a few key ones to ensure the dicts aren't empty or broken
        self.assertIn("oneplus_15", SPRING_MAPPING)
        self.assertIn("15", OOS_MAPPING)

if __name__ == '__main__':
    unittest.main()
