from unittest.mock import patch

from fetch_firmware import get_from_ou_latest


class TestGetFromOuLatest:
    def test_returns_latest_na_package(self):
        package = {
            "url": "https://example.test/firmware.zip",
            "version": "CPH2771_16.0.10.600(EX01)",
            "md5": "abc123",
        }
        with patch("fetch_firmware.OU_NA_DEVICE_IDS", {"15R": 903}), \
             patch("fetch_firmware.get_latest_package", return_value=package) as latest:
            result = get_from_ou_latest("15R", "NA")

        latest.assert_called_once_with(903)
        assert result == {
            "url": "https://example.test/firmware.zip",
            "version": "CPH2771_16.0.10.600(EX01)",
            "md5": "abc123",
        }

    def test_ignores_non_na_region(self):
        assert get_from_ou_latest("15", "GLO") is None

    def test_unknown_device_returns_none(self):
        assert get_from_ou_latest("15T", "NA") is None
