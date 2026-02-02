#!/usr/bin/env python3
"""
Comprehensive tests for config.py
Tests configuration constants, device metadata, and mapping functions.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    BASE_URL, OOS_API_URL, USER_AGENT, HISTORY_DIR,
    DEVICE_METADATA, SPRING_MAPPING, OOS_MAPPING,
    get_display_name, get_model_number
)


class TestConfigConstants(unittest.TestCase):
    """Test suite for configuration constants."""

    def test_base_url_defined(self):
        """Test that BASE_URL is properly defined."""
        self.assertIsNotNone(BASE_URL)
        self.assertIsInstance(BASE_URL, str)
        self.assertTrue(BASE_URL.startswith('http'))

    def test_oos_api_url_defined(self):
        """Test that OOS_API_URL is properly defined."""
        self.assertIsNotNone(OOS_API_URL)
        self.assertIsInstance(OOS_API_URL, str)
        self.assertTrue(OOS_API_URL.startswith('http'))

    def test_user_agent_defined(self):
        """Test that USER_AGENT is properly defined."""
        self.assertIsNotNone(USER_AGENT)
        self.assertIsInstance(USER_AGENT, str)
        self.assertIn('Mozilla', USER_AGENT)

    def test_history_dir_defined(self):
        """Test that HISTORY_DIR is properly defined."""
        self.assertIsNotNone(HISTORY_DIR)
        self.assertIsInstance(HISTORY_DIR, str)
        self.assertEqual(HISTORY_DIR, 'data/history')


class TestDeviceMetadata(unittest.TestCase):
    """Test suite for DEVICE_METADATA dictionary."""

    def test_device_metadata_not_empty(self):
        """Test that DEVICE_METADATA is not empty."""
        self.assertIsNotNone(DEVICE_METADATA)
        self.assertGreater(len(DEVICE_METADATA), 0)

    def test_device_metadata_structure(self):
        """Test that all device entries have required structure."""
        for device_id, meta in DEVICE_METADATA.items():
            with self.subTest(device_id=device_id):
                self.assertIn('name', meta)
                self.assertIn('models', meta)
                self.assertIsInstance(meta['name'], str)
                self.assertIsInstance(meta['models'], dict)

    def test_device_names_are_strings(self):
        """Test that all device names are non-empty strings."""
        for device_id, meta in DEVICE_METADATA.items():
            with self.subTest(device_id=device_id):
                name = meta['name']
                self.assertIsInstance(name, str)
                self.assertGreater(len(name), 0)

    def test_model_numbers_structure(self):
        """Test that model numbers have valid structure."""
        valid_regions = ['GLO', 'EU', 'IN', 'CN', 'NA', 'ID', 'MY']

        for device_id, meta in DEVICE_METADATA.items():
            models = meta['models']
            with self.subTest(device_id=device_id):
                self.assertGreater(len(models), 0, f"Device {device_id} has no models")

                for region, model in models.items():
                    self.assertIn(region, valid_regions,
                                  f"Invalid region {region} for device {device_id}")
                    self.assertIsInstance(model, str)

    def test_specific_devices_exist(self):
        """Test that specific expected devices are present."""
        expected_devices = ['15', '15R', '13', '12', '12R', '11']

        for device in expected_devices:
            with self.subTest(device=device):
                self.assertIn(device, DEVICE_METADATA)

    def test_oneplus_15_metadata(self):
        """Test OnePlus 15 metadata is complete."""
        self.assertIn('15', DEVICE_METADATA)
        meta = DEVICE_METADATA['15']

        self.assertEqual(meta['name'], 'OnePlus 15')
        self.assertIn('GLO', meta['models'])
        self.assertIn('EU', meta['models'])
        self.assertIn('IN', meta['models'])
        self.assertIn('CN', meta['models'])

    def test_oneplus_15r_metadata(self):
        """Test OnePlus 15R metadata is complete and excludes CN."""
        self.assertIn('15R', DEVICE_METADATA)
        meta = DEVICE_METADATA['15R']

        self.assertEqual(meta['name'], 'OnePlus 15R')
        self.assertIn('GLO', meta['models'])
        self.assertIn('EU', meta['models'])
        self.assertIn('IN', meta['models'])
        # 15R should not have CN variant
        self.assertNotIn('CN', meta['models'])

    def test_oppo_devices_exist(self):
        """Test that Oppo devices are present in metadata."""
        oppo_devices = ['Find X8', 'Find X8 Pro', 'Find X8 Ultra', 'Find N3']

        for device in oppo_devices:
            with self.subTest(device=device):
                self.assertIn(device, DEVICE_METADATA)
                self.assertIn('Oppo', DEVICE_METADATA[device]['name'])

    def test_ace_devices_exist(self):
        """Test that OnePlus Ace devices are present."""
        ace_devices = ['Ace 6T', 'Ace 5', 'Ace 5 Pro', 'Ace 5 Ultimate']

        for device in ace_devices:
            with self.subTest(device=device):
                self.assertIn(device, DEVICE_METADATA)
                self.assertIn('Ace', DEVICE_METADATA[device]['name'])

    def test_pad_devices_exist(self):
        """Test that OnePlus Pad devices are present."""
        pad_devices = ['Pad 2 Pro', 'Pad 3', 'Pad 2']

        for device in pad_devices:
            with self.subTest(device=device):
                self.assertIn(device, DEVICE_METADATA)
                self.assertIn('Pad', DEVICE_METADATA[device]['name'])


class TestSpringMapping(unittest.TestCase):
    """Test suite for SPRING_MAPPING dictionary."""

    def test_spring_mapping_not_empty(self):
        """Test that SPRING_MAPPING is not empty."""
        self.assertIsNotNone(SPRING_MAPPING)
        self.assertGreater(len(SPRING_MAPPING), 0)

    def test_spring_mapping_keys_are_snake_case(self):
        """Test that SPRING_MAPPING keys follow snake_case convention."""
        for key in SPRING_MAPPING.keys():
            with self.subTest(key=key):
                # Snake case should be all lowercase with underscores
                self.assertEqual(key, key.lower())
                self.assertNotIn(' ', key)

    def test_spring_mapping_values_format(self):
        """Test that SPRING_MAPPING values follow expected format."""
        for key, value in SPRING_MAPPING.items():
            with self.subTest(key=key):
                self.assertIsInstance(value, str)
                self.assertGreater(len(value), 0)
                # Values should be uppercase abbreviations
                self.assertTrue(any(c.isupper() for c in value))

    def test_spring_mapping_specific_entries(self):
        """Test specific expected SPRING_MAPPING entries."""
        expected_mappings = {
            'oneplus_15': 'OP 15',
            'oneplus_15r': 'OP 15R',
            'oneplus_13': 'OP 13',
            'oneplus_12': 'OP 12',
        }

        for key, expected_value in expected_mappings.items():
            with self.subTest(key=key):
                self.assertIn(key, SPRING_MAPPING)
                self.assertEqual(SPRING_MAPPING[key], expected_value)

    def test_spring_mapping_oppo_devices(self):
        """Test that Oppo devices are in SPRING_MAPPING."""
        oppo_keys = ['oppo_find_x8', 'oppo_find_x8_pro', 'oppo_find_x8_ultra']

        for key in oppo_keys:
            with self.subTest(key=key):
                self.assertIn(key, SPRING_MAPPING)
                self.assertIn('OPPO', SPRING_MAPPING[key].upper())


class TestOOSMapping(unittest.TestCase):
    """Test suite for OOS_MAPPING dictionary."""

    def test_oos_mapping_not_empty(self):
        """Test that OOS_MAPPING is not empty."""
        self.assertIsNotNone(OOS_MAPPING)
        self.assertGreater(len(OOS_MAPPING), 0)

    def test_oos_mapping_keys_match_device_metadata(self):
        """Test that OOS_MAPPING keys correspond to DEVICE_METADATA keys."""
        # Most OOS_MAPPING keys should exist in DEVICE_METADATA
        for key in OOS_MAPPING.keys():
            with self.subTest(key=key):
                self.assertIn(key, DEVICE_METADATA,
                              f"OOS_MAPPING key '{key}' not found in DEVICE_METADATA")

    def test_oos_mapping_values_are_snake_case(self):
        """Test that OOS_MAPPING values follow snake_case convention."""
        for key, value in OOS_MAPPING.items():
            with self.subTest(key=key):
                self.assertIsInstance(value, str)
                self.assertEqual(value, value.lower())
                # Should use underscores, not spaces
                self.assertNotIn(' ', value)

    def test_oos_mapping_specific_entries(self):
        """Test specific expected OOS_MAPPING entries."""
        expected_mappings = {
            '15': 'oneplus_15',
            '15R': 'oneplus_15r',
            '13': 'oneplus_13',
            '12': 'oneplus_12',
            '12R': 'oneplus_12r',
        }

        for key, expected_value in expected_mappings.items():
            with self.subTest(key=key):
                self.assertIn(key, OOS_MAPPING)
                self.assertEqual(OOS_MAPPING[key], expected_value)

    def test_oos_mapping_spring_overlap(self):
        """Test that OOS_MAPPING and SPRING_MAPPING have reasonable overlap."""
        # Not all devices in OOS_MAPPING need to be in SPRING_MAPPING
        # Some devices may only use OOS API or have different sources
        common_devices = []
        for device_id, oos_key in OOS_MAPPING.items():
            if oos_key in SPRING_MAPPING:
                common_devices.append(device_id)

        # At least 50% of devices should be in both mappings
        overlap_ratio = len(common_devices) / len(OOS_MAPPING)
        self.assertGreater(overlap_ratio, 0.5,
                          f"Only {overlap_ratio:.1%} overlap between OOS and SPRING mappings")


class TestGetDisplayName(unittest.TestCase):
    """Test suite for get_display_name function."""

    def test_get_display_name_valid_device(self):
        """Test get_display_name with valid device ID."""
        name = get_display_name('15')
        self.assertEqual(name, 'OnePlus 15')

    def test_get_display_name_multiple_devices(self):
        """Test get_display_name with multiple valid devices."""
        test_cases = {
            '15': 'OnePlus 15',
            '15R': 'OnePlus 15R',
            '13': 'OnePlus 13',
            '12': 'OnePlus 12',
        }

        for device_id, expected_name in test_cases.items():
            with self.subTest(device_id=device_id):
                name = get_display_name(device_id)
                self.assertEqual(name, expected_name)

    def test_get_display_name_invalid_device(self):
        """Test get_display_name with invalid device ID returns fallback."""
        name = get_display_name('invalid_device')
        self.assertIn('OnePlus', name)
        self.assertIn('invalid_device', name)

    def test_get_display_name_oppo_device(self):
        """Test get_display_name with Oppo device."""
        name = get_display_name('Find X8')
        self.assertEqual(name, 'Oppo Find X8')

    def test_get_display_name_ace_device(self):
        """Test get_display_name with Ace device."""
        name = get_display_name('Ace 5')
        self.assertIn('Ace', name)

    def test_get_display_name_empty_string(self):
        """Test get_display_name with empty string."""
        name = get_display_name('')
        self.assertIsNotNone(name)
        self.assertIsInstance(name, str)

    def test_get_display_name_returns_string(self):
        """Test that get_display_name always returns a string."""
        for device_id in DEVICE_METADATA.keys():
            with self.subTest(device_id=device_id):
                name = get_display_name(device_id)
                self.assertIsInstance(name, str)
                self.assertGreater(len(name), 0)


class TestGetModelNumber(unittest.TestCase):
    """Test suite for get_model_number function."""

    def test_get_model_number_valid_device_region(self):
        """Test get_model_number with valid device and region."""
        model = get_model_number('15', 'GLO')
        self.assertEqual(model, 'CPH2747')

    def test_get_model_number_multiple_regions(self):
        """Test get_model_number with multiple valid regions for OnePlus 15."""
        test_cases = {
            'GLO': 'CPH2747',
            'EU': 'CPH2747',
            'IN': 'CPH2745',
            'CN': 'PLK110',
        }

        for region, expected_model in test_cases.items():
            with self.subTest(region=region):
                model = get_model_number('15', region)
                self.assertEqual(model, expected_model)

    def test_get_model_number_invalid_device(self):
        """Test get_model_number with invalid device ID."""
        model = get_model_number('invalid_device', 'GLO')
        self.assertEqual(model, 'Unknown')

    def test_get_model_number_invalid_region(self):
        """Test get_model_number with invalid region."""
        model = get_model_number('15', 'INVALID')
        self.assertEqual(model, 'Unknown')

    def test_get_model_number_missing_region(self):
        """Test get_model_number with device that doesn't have requested region."""
        # 15R doesn't have CN variant
        model = get_model_number('15R', 'CN')
        self.assertEqual(model, 'Unknown')

    def test_get_model_number_all_devices(self):
        """Test get_model_number for all devices and their regions."""
        for device_id, meta in DEVICE_METADATA.items():
            for region in meta['models'].keys():
                with self.subTest(device_id=device_id, region=region):
                    model = get_model_number(device_id, region)
                    self.assertIsInstance(model, str)
                    # Should not be empty (though it might be "Unknown")
                    self.assertGreater(len(model), 0)

    def test_get_model_number_returns_string(self):
        """Test that get_model_number always returns a string."""
        model = get_model_number('15', 'GLO')
        self.assertIsInstance(model, str)

    def test_get_model_number_case_sensitivity(self):
        """Test get_model_number with different region case."""
        # Test exact case
        model_upper = get_model_number('15', 'GLO')
        # Regions should be case-sensitive
        model_lower = get_model_number('15', 'glo')

        self.assertEqual(model_upper, 'CPH2747')
        self.assertEqual(model_lower, 'Unknown')


class TestMappingConsistency(unittest.TestCase):
    """Test suite for consistency across all mappings."""

    def test_all_device_metadata_has_oos_mapping(self):
        """Test that all DEVICE_METADATA entries have corresponding OOS_MAPPING."""
        for device_id in DEVICE_METADATA.keys():
            with self.subTest(device_id=device_id):
                self.assertIn(device_id, OOS_MAPPING,
                              f"Device {device_id} missing from OOS_MAPPING")

    def test_oos_mappings_subset_in_spring(self):
        """Test that OOS_MAPPING and SPRING_MAPPING have reasonable overlap."""
        # Not all devices need to be in both mappings (some may only be in OOS API)
        # but there should be significant overlap
        common_keys = set(OOS_MAPPING.values()) & set(SPRING_MAPPING.keys())

        # At least 50% overlap is expected
        overlap_ratio = len(common_keys) / len(OOS_MAPPING)
        self.assertGreater(overlap_ratio, 0.5,
                          f"Only {overlap_ratio:.1%} overlap between OOS_MAPPING and SPRING_MAPPING")

    def test_no_duplicate_device_ids(self):
        """Test that there are no duplicate device IDs in DEVICE_METADATA."""
        device_ids = list(DEVICE_METADATA.keys())
        unique_ids = set(device_ids)
        self.assertEqual(len(device_ids), len(unique_ids),
                         "Duplicate device IDs found in DEVICE_METADATA")

    def test_no_duplicate_oos_mapping_keys(self):
        """Test that there are no duplicate keys in OOS_MAPPING."""
        oos_keys = list(OOS_MAPPING.keys())
        unique_keys = set(oos_keys)
        self.assertEqual(len(oos_keys), len(unique_keys),
                         "Duplicate keys found in OOS_MAPPING")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_get_display_name_with_none(self):
        """Test get_display_name behavior with None (should not crash)."""
        try:
            name = get_display_name(None)
            # If it doesn't crash, it should return something reasonable
            self.assertIsNotNone(name)
        except (TypeError, AttributeError):
            # Acceptable to raise error for None
            pass

    def test_device_metadata_no_empty_names(self):
        """Test that no device has an empty name."""
        for device_id, meta in DEVICE_METADATA.items():
            with self.subTest(device_id=device_id):
                name = meta['name']
                self.assertNotEqual(name, '')
                self.assertNotEqual(name.strip(), '')

    def test_model_numbers_reasonable_format(self):
        """Test that model numbers follow reasonable format (letters and numbers)."""
        import re

        for device_id, meta in DEVICE_METADATA.items():
            for region, model in meta['models'].items():
                with self.subTest(device_id=device_id, region=region):
                    if model != 'Unknown':
                        # Model should contain letters and/or numbers
                        self.assertTrue(re.match(r'^[A-Z0-9]+$', model) or model == 'Unknown',
                                        f"Invalid model format: {model}")

    def test_constants_not_none(self):
        """Test that all major constants are not None."""
        self.assertIsNotNone(BASE_URL)
        self.assertIsNotNone(OOS_API_URL)
        self.assertIsNotNone(USER_AGENT)
        self.assertIsNotNone(HISTORY_DIR)
        self.assertIsNotNone(DEVICE_METADATA)
        self.assertIsNotNone(SPRING_MAPPING)
        self.assertIsNotNone(OOS_MAPPING)


if __name__ == '__main__':
    unittest.main()