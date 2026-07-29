import pytest
from config import (
    get_display_name, get_model_number, REGION_MAPPING,
    DEVICE_ORDER, SPRING_MAPPING, OOS_MAPPING, DEVICE_METADATA,
    HARDWARE_FEATURES
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

    def test_new_flagships(self):
        assert get_display_name("15") == "OnePlus 15"
        assert get_display_name("15R") == "OnePlus 15R"
        assert get_display_name("15T") == "OnePlus 15T"
        assert get_display_name("13") == "OnePlus 13"
        assert get_display_name("13R") == "OnePlus 13R"
        assert get_display_name("13T") == "OnePlus 13T"
        assert get_display_name("13s") == "OnePlus 13s"

    def test_nord_6(self):
        assert get_display_name("Nord 6") == "OnePlus Nord 6"

    def test_nord_5(self):
        assert get_display_name("Nord 5") == "OnePlus Nord 5"

    def test_ace_6t(self):
        assert get_display_name("Ace 6T") == "OnePlus Ace 6T"

    def test_find_x8_ultra(self):
        assert get_display_name("Find X8 Ultra") == "Oppo Find X8 Ultra"

    def test_empty_string(self):
        assert get_display_name("") == "OnePlus "

    def test_case_sensitive(self):
        assert get_display_name("15") != "Oneplus 15"


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

    def test_new_devices(self):
        assert get_model_number("15", "GLO") == "CPH2747"
        assert get_model_number("15", "CN") == "PLK110"
        assert get_model_number("15R", "IN") == "CPH2767"
        assert get_model_number("15T", "CN") == "PLZ110"
        assert get_model_number("13", "NA") == "CPH2655"
        assert get_model_number("13R", "IN") == "CPH2691"
        assert get_model_number("13T", "CN") == "PKX110"
        assert get_model_number("13s", "IN") == "CPH2723"

    def test_nord_6_models(self):
        assert get_model_number("Nord 6", "GLO") == "CPH2795"
        assert get_model_number("Nord 6", "IN") == "CPH2793"

    def test_ace_6t(self):
        assert get_model_number("Ace 6T", "CN") == "PLR110"

    def test_pad_3(self):
        assert get_model_number("Pad 3", "GLO") == "OPD2415"

    def test_reno10_pro_multi_region(self):
        assert get_model_number("Reno10 Pro", "ID") == "CPH2525ID"
        assert get_model_number("Reno10 Pro", "IN") == "CPH2525IN"
        assert get_model_number("Reno10 Pro", "PH") == "CPH2525PH"

    def test_open_same_model_all_regions(self):
        assert get_model_number("Open", "EU") == "CPH2551"
        assert get_model_number("Open", "IN") == "CPH2551"
        assert get_model_number("Open", "NA") == "CPH2551"


class TestHardwareFeatures:
    def test_flagships_with_esim(self):
        assert HARDWARE_FEATURES["CPH2747"]["expect_esim"] is True
        assert HARDWARE_FEATURES["CPH2653"]["expect_esim"] is True
        assert HARDWARE_FEATURES["CPH2581"]["expect_esim"] is True

    def test_oneplus_open_has_barometer(self):
        assert HARDWARE_FEATURES["CPH2551"]["expect_barometer"] is True

    def test_nord_n200_has_barometer(self):
        assert HARDWARE_FEATURES["DE2117"]["expect_barometer"] is True
        assert HARDWARE_FEATURES["DE2117"]["expect_esim"] is False

    def test_older_devices_no_esim(self):
        assert HARDWARE_FEATURES.get("CPH2449", {}).get("expect_esim", False) is True
        assert HARDWARE_FEATURES.get("CPH2409", {}).get("expect_esim", False) is False

    def test_new_devices_have_hardware_features(self):
        for model_id in ["CPH2747", "CPH2749", "CPH2769", "CPH2767", "CPH2653", "CPH2645"]:
            assert model_id in HARDWARE_FEATURES, f"{model_id} missing from HARDWARE_FEATURES"


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
        assert REGION_MAPPING["GLO"] == REGION_MAPPING["GLB"]
        assert REGION_MAPPING["EU"] == REGION_MAPPING["EEA"]

    def test_all_oos_regions_covered(self):
        oos_regions = set()
        for meta in DEVICE_METADATA.values():
            oos_regions.update(meta.get("models", {}).keys())
        unknown = [r for r in oos_regions if r not in REGION_MAPPING]
        assert not unknown, f"Regions missing from REGION_MAPPING: {unknown}"

    def test_rare_regions(self):
        assert REGION_MAPPING["MX"] == "Mexico"
        assert REGION_MAPPING["APC"] == "Asia Pacific"
        assert REGION_MAPPING["OCA"] == "Oceania"
        assert REGION_MAPPING["VISIBLE"] == "Visible USA"


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

    def test_15r_after_15(self):
        assert DEVICE_ORDER.index("15") < DEVICE_ORDER.index("15R")

    def test_flagships_before_nords(self):
        op12_idx = DEVICE_ORDER.index("12")
        nord4_idx = DEVICE_ORDER.index("Nord 4")
        assert op12_idx < nord4_idx, "Flagships should come before Nords"

    def test_china_aces_after_nords(self):
        nord4_idx = DEVICE_ORDER.index("Nord 4")
        ace3_idx = DEVICE_ORDER.index("Ace 3")
        assert nord4_idx < ace3_idx, "Nords should come before Ace series"


class TestMappings:
    def test_oos_mapping_common_devices(self):
        assert OOS_MAPPING["15"] == "oneplus_15"
        assert OOS_MAPPING["12"] == "oneplus_12"
        assert OOS_MAPPING["Open"] == "oneplus_open"

    def test_oos_mapping_new_devices(self):
        assert OOS_MAPPING["15R"] == "oneplus_15r"
        assert OOS_MAPPING["15T"] == "oneplus_15t"
        assert OOS_MAPPING["13"] == "oneplus_13"
        assert OOS_MAPPING["13R"] == "oneplus_13r"
        assert OOS_MAPPING["13T"] == "oneplus_13t"
        assert OOS_MAPPING["13s"] == "oneplus_13s"

    def test_oos_mapping_nord_6(self):
        assert OOS_MAPPING["Nord 6"] == "oneplus_nord_6"
        assert OOS_MAPPING["Nord 5"] == "oneplus_nord_5"

    def test_oos_mapping_oppo(self):
        assert OOS_MAPPING["Find N5"] == "oppo_find_n5"
        assert OOS_MAPPING["Find X5 Pro"] == "oppo_find_x5_pro"
        assert OOS_MAPPING["Find X8 Ultra"] == "oppo_find_x8_ultra"

    def test_oos_mapping_pads(self):
        assert OOS_MAPPING["Pad 3"] == "oneplus_pad_3"
        assert OOS_MAPPING["Pad 2 Pro"] == "oneplus_pad2_pro"
        assert OOS_MAPPING["Pad 2"] == "oneplus_pad_2"

    def test_oos_mapping_ace_series(self):
        assert OOS_MAPPING["Ace 6T"] == "oneplus_ace_6t"
        assert OOS_MAPPING["Ace 6"] == "oneplus_ace_6"
        assert OOS_MAPPING["Ace 5 Pro"] == "oneplus_ace_5_pro"

    def test_spring_mapping_common(self):
        assert SPRING_MAPPING["oneplus_15"] == "OP 15"
        assert SPRING_MAPPING["oneplus_12"] == "OP 12"
        assert SPRING_MAPPING["oneplus_open"] == "OP OPEN"
        assert SPRING_MAPPING["oneplus_15r"] == "OP 15R"
        assert SPRING_MAPPING["oneplus_15t"] == "OP 15T"

    def test_spring_mapping_oppo(self):
        assert SPRING_MAPPING["oppo_find_n5"] == "OPPO FIND N5"
        assert SPRING_MAPPING["oppo_find_x8_ultra"] == "OPPO FIND X8 ULTRA"

    def test_spring_mapping_nords(self):
        assert SPRING_MAPPING["oneplus_nord_6"] == "OP NORD 6"
        assert SPRING_MAPPING["oneplus_nord_5"] == "OP NORD 5"

    def test_device_metadata_has_all_device_order_entries(self):
        missing = []
        for device in DEVICE_ORDER:
            if device not in DEVICE_METADATA:
                missing.append(device)
        assert not missing, f"Devices missing from DEVICE_METADATA: {missing}"

    def test_device_metadata_no_stale_entries(self):
        extra = []
        for device in DEVICE_METADATA:
            if device not in DEVICE_ORDER:
                extra.append(device)
        assert not extra, f"Devices in DEVICE_METADATA but not DEVICE_ORDER: {extra}"
