import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_direct_url_keeps_supplied_md5(tmp_path):
    output = tmp_path / "fw_info.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "fetch_firmware.py"),
            "15",
            "NA",
            "CPH2749_16.0.9.400(EX01)",
            "--source",
            "ou_url",
            "--direct-url",
            "https://example.test/old.zip",
            "--md5",
            "deadbeef",
            "--output",
            str(output),
        ],
        check=True,
        cwd=ROOT,
    )

    assert json.loads(output.read_text()) == {
        "url": "https://example.test/old.zip",
        "version": "CPH2749_16.0.9.400(EX01)",
        "md5": "deadbeef",
    }


def test_direct_url_without_md5_stays_null(tmp_path):
    output = tmp_path / "fw_info.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "fetch_firmware.py"),
            "15",
            "NA",
            "CPH2749_16.0.9.400(EX01)",
            "--source",
            "ou_url",
            "--direct-url",
            "https://example.test/old.zip",
            "--output",
            str(output),
        ],
        check=True,
        cwd=ROOT,
    )

    assert json.loads(output.read_text())["md5"] is None
