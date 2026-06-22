import json
import os
import pytest
import tempfile

from parse_result import main as parse_main


def run_parse(result_data):
    """Helper: write result_data to temp result.json, run parse_result, return fw_env dict."""
    orig_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            with open('result.json', 'w') as f:
                json.dump(result_data, f)

            # Need to mock sys.argv or just call main() which reads result.json
            # But parse_result.main() prints to stdout and writes fw_env
            # Let's capture the output
            import io
            from contextlib import redirect_stdout

            f_out = io.StringIO()
            with redirect_stdout(f_out):
                parse_main()

            env = {}
            if os.path.exists('fw_env'):
                with open('fw_env') as f:
                    for line in f:
                        if '=' in line:
                            k, v = line.strip().split('=', 1)
                            env[k] = v.strip('"')
            return env, f_out.getvalue()
        finally:
            os.chdir(orig_cwd)


class TestParseResultFullMetadata:
    def test_standard_ota(self):
        data = {
            "arb_index": "0",
            "major": "3",
            "minor": "1",
            "ota_metadata": {
                "pre-device": "CPH2581",
                "product_name": "OnePlus 12",
                "version_name_show": "14.0.0.800(EX01)",
                "post-security-patch-level": "2024-03-01",
                "post-build": "CPH2581_14.0.0.800(EX01)"
            }
        }
        env, _ = run_parse(data)
        assert env['DETECTED_DEVICE'] == 'CPH2581'
        assert env['DETECTED_PRODUCT'] == 'OnePlus 12'
        assert env['DETECTED_VERSION'] == '14.0.0.800(EX01)'
        assert env['DETECTED_PATCH'] == '2024-03-01'
        assert env['DETECTED_BUILD'] == 'CPH2581_14.0.0.800(EX01)'
        assert env['DETECTED_ARB'] == '0'
        assert env['IMAGE_CHECK'] == 'false'

    def test_img_check_no_metadata(self):
        data = {
            "arb_index": "1",
            "major": "3",
            "minor": "0"
        }
        env, _ = run_parse(data)
        assert env['DETECTED_DEVICE'] == 'Direct .img Check'
        assert env['DETECTED_PRODUCT'] == 'N/A'
        assert env['DETECTED_VERSION'] == 'N/A'
        assert env['DETECTED_ARB'] == '1'
        assert env['IMAGE_CHECK'] == 'true'

    def test_arb_unknown(self):
        data = {
            "arb_index": "Unknown",
            "ota_metadata": {
                "pre-device": "CPH2581",
                "product_name": "OnePlus 12",
            }
        }
        env, _ = run_parse(data)
        assert env['DETECTED_ARB'] == 'Unknown'

    def test_device_with_comma(self):
        data = {
            "arb_index": "0",
            "ota_metadata": {
                "pre-device": "CPH2581,CPH2583",
                "product_name": "OnePlus 12"
            }
        }
        env, _ = run_parse(data)
        assert env['DETECTED_DEVICE'] == 'CPH2581'

    def test_fallback_fields(self):
        data = {
            "arb_index": "0",
            "ota_metadata": {
                "pre-device": "CPH2581",
                "display-version": "14.0.0.800(EX01)",
                "security_patch": "2024-03-01",
                "post-build": "BuildID"
            }
        }
        env, _ = run_parse(data)
        assert env['DETECTED_VERSION'] == '14.0.0.800(EX01)'
        assert env['DETECTED_PATCH'] == '2024-03-01'
        assert env['DETECTED_BUILD'] == 'BuildID'

    def test_unknown_device_fallback(self):
        data = {
            "arb_index": "0",
            "ota_metadata": {
                "product_name": "Unknown"
            }
        }
        env, _ = run_parse(data)
        assert 'Unknown' in env['DETECTED_DEVICE']
        assert env['DETECTED_BUILD'] == 'Unknown'


class TestParseResultMissingFile:
    def test_no_result_json(self):
        """Should not crash, just print message."""
        orig_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                import io
                from contextlib import redirect_stdout
                f_out = io.StringIO()
                with redirect_stdout(f_out):
                    parse_main()
                assert "not found" in f_out.getvalue().lower()
            finally:
                os.chdir(orig_cwd)


class TestParseResultInvalidJson:
    def test_invalid_json(self):
        orig_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                with open('result.json', 'w') as f:
                    f.write("not valid json")
                with pytest.raises(SystemExit):
                    parse_main()
            finally:
                os.chdir(orig_cwd)
