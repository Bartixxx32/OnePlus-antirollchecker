from argparse import Namespace

from fetch_ou_arb import build_result


def make_args():
    return Namespace(
        device_short="15",
        variant="NA",
        version="CPH2749_16.0.2.401(EX01)",
        url="https://example.test/ota.zip",
        md5="abc123",
        ota_version="CPH2749_16.0.0.205(EX01)",
    )


class TestBuildResult:
    def test_carries_package_type_and_arb(self):
        result = build_result(
            make_args(),
            {
                "arb": 0,
                "major": 3,
                "minor": 0,
                "partition": "xbl_config",
                "package_type": "incremental",
            },
        )

        assert result["arb_index"] == "0"
        assert result["arb_detected"] is True
        assert result["package_type"] == "incremental"
        assert result["partition"] == "xbl_config"

    def test_undetectable_arb_is_marked(self):
        result = build_result(
            make_args(),
            {
                "arb": -1,
                "major": 0,
                "minor": 0,
                "partition": None,
                "package_type": "full",
            },
        )

        assert result["arb_index"] == "-1"
        assert result["arb_detected"] is False
        assert result["package_type"] == "full"
