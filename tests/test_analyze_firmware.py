import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import shutil
from pathlib import Path
from analyze_firmware import analyze_firmware, extract_ota_metadata, run_command

class TestAnalyzeFirmware(unittest.TestCase):

    @patch('analyze_firmware.subprocess.run')
    def test_run_command_success(self, mock_run):
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Success"
        mock_run.return_value = mock_process

        result = run_command(["ls", "-l"])
        self.assertEqual(result, "Success")
        mock_run.assert_called_once()

    @patch('analyze_firmware.subprocess.run')
    def test_run_command_failure(self, mock_run):
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "Error"
        mock_run.return_value = mock_process

        result = run_command(["ls", "-l"])
        self.assertIsNone(result)

    @patch('analyze_firmware.zipfile.ZipFile')
    def test_extract_ota_metadata(self, mock_zip):
        """Test extraction of metadata from zip."""
        mock_zip_instance = mock_zip.return_value.__enter__.return_value
        mock_zip_instance.namelist.return_value = ['META-INF/com/android/metadata']
        mock_zip_instance.read.return_value = b'post-timestamp=123456\npre-device=OnePlus15'

        result = extract_ota_metadata("dummy.zip")
        self.assertEqual(result['post-timestamp'], '123456')
        self.assertEqual(result['pre-device'], 'OnePlus15')

    @patch('analyze_firmware.Path')
    @patch('analyze_firmware.shutil.rmtree')
    @patch('analyze_firmware.shutil.move')
    @patch('analyze_firmware.run_command')
    @patch('analyze_firmware.extract_ota_metadata')
    def test_analyze_firmware_cache_hit(self, mock_meta, mock_run, mock_move, mock_rmtree, mock_path):
        """Test cache hit (image already exists)."""
        # Setup paths
        zip_path = MagicMock()
        tools_dir = MagicMock()
        output_dir = MagicMock()
        final_dir = MagicMock()
        mock_path.return_value.resolve.side_effect = [zip_path, tools_dir, output_dir, final_dir, zip_path]

        # Cache hit setup
        final_img = final_dir / "xbl_config.img"
        final_img.exists.return_value = True

        # Run command setup (for arbextract)
        mock_run.return_value = "ARB (Anti-Rollback): 1\nMajor Version: 3\nMinor Version: 0"

        mock_meta.return_value = {"version": "1.0"}

        result = analyze_firmware("fw.zip", "tools", "out", "final")

        self.assertEqual(result['arb_index'], '1')
        self.assertEqual(result['major'], '3')
        self.assertEqual(result['ota_metadata']['version'], '1.0')
        # Check that extraction was SKIPPED (no move, no rmtree of output)
        mock_move.assert_not_called()

    @patch('analyze_firmware.Path')
    @patch('analyze_firmware.shutil.rmtree')
    @patch('analyze_firmware.shutil.move')
    @patch('analyze_firmware.run_command')
    @patch('analyze_firmware.extract_ota_metadata')
    def test_analyze_firmware_extraction_otaripper(self, mock_meta, mock_run, mock_move, mock_rmtree, mock_path):
        """Test successful extraction with otaripper."""
        # Setup paths
        zip_path = MagicMock()
        zip_path.exists.return_value = True

        tools_dir = MagicMock()
        output_dir = MagicMock()
        final_dir = MagicMock()

        mock_path.return_value.resolve.side_effect = [zip_path, tools_dir, output_dir, final_dir, zip_path, zip_path]

        # Cache miss
        final_img = final_dir / "xbl_config.img"
        final_img.exists.return_value = False

        output_dir.exists.return_value = True
        output_dir.rglob.return_value = [Path("out/xbl_config.img")]

        # Run command setup:
        # 1. Otaripper (success)
        # 2. Arbextract (success)
        mock_run.side_effect = ["Success extraction", "ARB (Anti-Rollback): 0\nMajor Version: 2\nMinor Version: 0"]

        mock_meta.return_value = {}

        result = analyze_firmware("fw.zip", "tools", "out", "final")

        self.assertEqual(result['arb_index'], '0')
        self.assertEqual(mock_run.call_count, 2)
        mock_move.assert_called_once()


    @patch('analyze_firmware.Path')
    @patch('analyze_firmware.shutil.rmtree')
    @patch('analyze_firmware.shutil.move')
    @patch('analyze_firmware.run_command')
    @patch('analyze_firmware.extract_ota_metadata')
    def test_analyze_firmware_extraction_fallback(self, mock_meta, mock_run, mock_move, mock_rmtree, mock_path):
        """Test extraction fallback to payload-dumper-go."""
        # Setup paths
        zip_path = MagicMock()
        zip_path.exists.return_value = True

        tools_dir = MagicMock()
        output_dir = MagicMock()
        final_dir = MagicMock()

        mock_path.return_value.resolve.side_effect = [zip_path, tools_dir, output_dir, final_dir, zip_path, zip_path]

        # Cache miss
        final_img = final_dir / "xbl_config.img"
        final_img.exists.return_value = False

        output_dir.rglob.return_value = [Path("out/xbl_config.img")]

        # Run command setup:
        # 1. Otaripper (FAIL)
        # 2. Payload Dumper (Success)
        # 3. Arbextract (Success)
        mock_run.side_effect = [None, "Success fallback", "ARB (Anti-Rollback): 1\nMajor Version: 3"]

        mock_meta.return_value = {}

        result = analyze_firmware("fw.zip", "tools", "out", "final")

        self.assertEqual(result['arb_index'], '1')
        self.assertEqual(mock_run.call_count, 3)
        mock_move.assert_called_once()

    @patch('analyze_firmware.Path')
    @patch('analyze_firmware.shutil.rmtree')
    @patch('analyze_firmware.run_command')
    def test_analyze_firmware_fail_all_extractions(self, mock_run, mock_rmtree, mock_path):
        """Test failure when all extractions fail."""
        # Setup paths
        zip_path = MagicMock()
        zip_path.exists.return_value = True
        tools_dir = MagicMock()
        output_dir = MagicMock()
        final_dir = MagicMock()
        mock_path.return_value.resolve.side_effect = [zip_path, tools_dir, output_dir, final_dir, zip_path, zip_path]

        # Cache miss
        final_img = final_dir / "xbl_config.img"
        final_img.exists.return_value = False

        # Fail both
        mock_run.return_value = None

        result = analyze_firmware("fw.zip", "tools", "out", "final")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
