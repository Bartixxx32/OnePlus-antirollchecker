import pytest
from hardcode_rules import is_hardcode_protected, version_sort_key


class TestIsHardcodeProtected:
    def test_nord_ce_3_lite_below_threshold(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "CPH2467_11.0.0.1400(EX01)") is False

    def test_nord_ce_3_lite_at_threshold(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "CPH2467_11.0.0.1600(EX01)") is True

    def test_nord_ce_3_lite_above_threshold(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "CPH2467_11.0.0.1700(EX01)") is True

    def test_nord_ce_3_lite_with_underscore(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "CPH2467_11.0.0.1600_EXT") is True

    def test_nord_ce_3_non_lite_below(self):
        assert is_hardcode_protected("oneplus_nord_ce_3", "CPH2569_11.0.0.1500(EX01)") is False

    def test_nord_ce_3_non_lite_above(self):
        assert is_hardcode_protected("oneplus_nord_ce_3", "CPH2569_11.0.0.1600(EX01)") is True

    def test_nord_ce_2_lite_below(self):
        assert is_hardcode_protected("oneplus_nord_ce_2_lite", "CPH2381_11.0.0.2800(EX01)") is False

    def test_nord_ce_2_lite_above(self):
        assert is_hardcode_protected("oneplus_nord_ce_2_lite", "CPH2381_11.0.0.2900(EX01)") is True

    def test_nord_ce_4_lite_below(self):
        assert is_hardcode_protected("oneplus_nord_ce_4_lite", "CPH2619_11.0.0.300(EX01)") is False

    def test_nord_ce_4_lite_at_threshold(self):
        assert is_hardcode_protected("oneplus_nord_ce_4_lite", "CPH2619_11.0.0.303(EX01)") is True

    def test_nord_ce_4_lite_above(self):
        assert is_hardcode_protected("oneplus_nord_ce_4_lite", "CPH2619_11.0.0.310(EX01)") is True

    def test_9rt_below(self):
        assert is_hardcode_protected("oneplus_9rt", "MT2111_11.0.0.2700(EX01)") is False

    def test_9rt_above(self):
        assert is_hardcode_protected("oneplus_9rt", "MT2111_11.0.0.2702(EX01)") is True

    def test_unknown_device(self):
        assert is_hardcode_protected("oneplus_12", "CPH2581_14.0.0.800(EX01)") is False

    def test_empty_version(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "") is False

    def test_none_version(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", None) is False

    def test_non_matching_version_format(self):
        assert is_hardcode_protected("oneplus_nord_ce_3_lite", "some-random-string") is False

    def test_oppo_device(self):
        assert is_hardcode_protected("oppo_find_n5", "CPH2671_15.0.0.100(EX01)") is False


class TestVersionSortKey:
    def test_normal_version(self):
        assert version_sort_key("14.0.0.800") == (14, 0, 0, 800)

    def test_version_with_prefix(self):
        assert version_sort_key("CPH2581_14.0.0.800(EX01)") == (2581, 14, 0, 0, 800, 1)

    def test_simple_version(self):
        assert version_sort_key("14") == (14,)

    def test_empty_string(self):
        assert version_sort_key("") == (0,)

    def test_none(self):
        assert version_sort_key(None) == (0,)

    def test_no_numbers(self):
        assert version_sort_key("abc.def") == ()

    def test_sorts_descending(self):
        versions = ["14.0.0.800", "14.0.0.700", "14.0.0.900"]
        sorted_v = sorted(versions, key=version_sort_key, reverse=True)
        assert sorted_v == ["14.0.0.900", "14.0.0.800", "14.0.0.700"]

    def test_different_major_versions(self):
        versions = ["15.0.0.100", "14.0.0.800", "13.0.0.500"]
        sorted_v = sorted(versions, key=version_sort_key, reverse=True)
        assert sorted_v == ["15.0.0.100", "14.0.0.800", "13.0.0.500"]
