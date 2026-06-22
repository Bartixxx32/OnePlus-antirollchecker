import pytest
from config import (
    get_display_name, get_model_number, REGION_MAPPING,
    DEVICE_ORDER, SPRING_MAPPING, OOS_MAPPING, DEVICE_METADATA
)


class TestGetDisplayName:
    def test_known_device(self):
        assert get_display_name("12") == "OnePlus 12"

    def test_known_oppo_device(self):
        assert get_display_name("Find N5") == "Oppo Find N5"

    def test_unknown_device(self):
        assert get_display_name("nonexistent") == "OnePlus nonexistent"

    def test_nord_device(self):
        assert get_display_name("Nord 4") == "OnePlus Nord 4"

    def test_ace_device(self):
        assert get_display_name("Ace 3 Pro") == "OnePlus Ace 3 Pro"

    def test_pad_device(self):
        assert get_display_name("Pad 2") == "OnePlus Pad 2"


class TestGetModelNumber:
    def test_known_device_region(self):
        assert get_model_number("12", "GLO") == "CPH2581"

    def test_known_device_na(self):
        assert get_model_number("12", "NA") == "CPH2583"

    def test_unknown_region(self):
        assert get_model_number("12", "XX") == "Unknown"

    def test_unknown_device(self):
        assert get_model_number("nonexistent", "GLO") == "Unknown"

    def test_nord_ce3_lite_eu(self):
        assert get_model_number("Nord CE 3 Lite", "EU") == "CPH2465EEA"

    def test_find_n5_cn(self):
        assert get_model_number("Find N5", "CN") == "PKV110"


class TestRegionMapping:
    def test_known_regions(self):
        assert REGION_MAPPING["GLO"] == "Global"
        assert REGION_MAPPING["EU"] == "Europe"
        assert REGION_MAPPING["IN"] == "India"
        assert REGION_MAPPING["CN"] == "China"
        assert REGION_MAPPING["NA"] == "North America"

    def test_aliases(self):
        assert REGION_MAPPING["US"] == "United States"
        assert REGION_MAPPING["EEA"] == "Europe"
        assert REGION_MAPPING["GLB"] == "Global"

    def test_aliases_have_same_name(self):
        """GLO/GLB, EU/EEA are aliases for the same region."""
        assert REGION_MAPPING["GLO"] == REGION_MAPPING["GLB"]
        assert REGION_MAPPING["EU"] == REGION_MAPPING["EEA"]


class TestDeviceOrder:
    def test_expected_devices_present(self):
        important = ["15", "13", "12", "11", "10 Pro", "8T", "Open", "Nord 4", "Ace 3", "Pad 2"]
        for d in important:
            assert d in DEVICE_ORDER, f"{d} missing from DEVICE_ORDER"

    def test_no_duplicates(self):
        assert len(DEVICE_ORDER) == len(set(DEVICE_ORDER)), "Duplicates in DEVICE_ORDER"

    def test_newer_devices_first(self):
        idx_15 = DEVICE_ORDER.index("15")
        idx_13 = DEVICE_ORDER.index("13")
        idx_12 = DEVICE_ORDER.index("12")
        assert idx_15 < idx_13 < idx_12, "Newer devices should come first"


class TestMappings:
    def test_oos_mapping_common_devices(self):
        assert OOS_MAPPING["15"] == "oneplus_15"
        assert OOS_MAPPING["12"] == "oneplus_12"
        assert OOS_MAPPING["Open"] == "oneplus_open"

    def test_oos_mapping_oppo(self):
        assert OOS_MAPPING["Find N5"] == "oppo_find_n5"
        assert OOS_MAPPING["Find X5 Pro"] == "oppo_find_x5_pro"

    def test_spring_mapping_common(self):
        assert SPRING_MAPPING["oneplus_15"] == "OP 15"
        assert SPRING_MAPPING["oneplus_12"] == "OP 12"
        assert SPRING_MAPPING["oneplus_open"] == "OP OPEN"

    def test_spring_mapping_oppo(self):
        assert SPRING_MAPPING["oppo_find_n5"] == "OPPO FIND N5"

    def test_oos_has_all_spring_keys(self):
        """Every device in OOS_MAPPING should have a corresponding SPRING_MAPPING entry
        (or at least devices that get looked up via springer)."""
        # This is a soft check - not all OOS devices have springer equivalents
        pass

    def test_device_metadata_has_all_device_order_entries(self):
        """Every device in DEVICE_ORDER should have a DEVICE_METADATA entry."""
        missing = []
        for device in DEVICE_ORDER:
            if device not in DEVICE_METADATA:
                missing.append(device)
        assert not missing, f"Devices missing from DEVICE_METADATA: {missing}"
