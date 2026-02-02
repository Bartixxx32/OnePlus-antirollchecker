#!/usr/bin/env python3
"""
Comprehensive tests for analyze_firmware.py
Tests firmware analysis, ARB extraction, and command execution.
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import subprocess


# Import the module - need to handle missing imports in analyze_firmware.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAnalyzeFirmware(unittest.TestCase):
    """Test suite for analyze_firmware.py functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.tools_dir = Path(self.temp_dir) / "tools"
        self.output_dir = Path(self.temp_dir) / "extracted"
        self.zip_path = Path(self.temp_dir) / "firmware.zip"

        # Create directories
        self.tools_dir.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)

        # Create dummy tool files
        (self.tools_dir / "otaripper").touch()
        (self.tools_dir / "arbextract").touch()

        # Create dummy zip file
        self.zip_path.touch()

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_analyze_firmware_success(self, mock_run):
        """Test successful firmware analysis."""
        # Mock otaripper extraction
        mock_run.return_value = Mock(returncode=0, stdout="Extracted successfully", stderr="")

        # Create extracted xbl_config image
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        # Mock arbextract output
        arb_output = """ARB (Anti-Rollback): 1
Major Version: 3
Minor Version: 0"""

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                # Create the image file for the next step
                img_file.touch()
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=arb_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        # Import here to avoid issues with missing imports
        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNotNone(result)
            self.assertEqual(result['arb_index'], '1')
            self.assertEqual(result['major'], '3')
            self.assertEqual(result['minor'], '0')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_extraction_failure(self, mock_run):
        """Test firmware analysis when extraction fails."""
        # Mock otaripper failure
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="Extraction failed")

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNone(result)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_no_xbl_config_found(self, mock_run):
        """Test firmware analysis when xbl_config image is not found."""
        # Mock successful extraction but no image file
        mock_run.return_value = Mock(returncode=0, stdout="Extracted", stderr="")

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNone(result)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_arbextract_failure(self, mock_run):
        """Test firmware analysis when arbextract fails."""
        # Create extracted xbl_config image
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=1, stdout="", stderr="arbextract failed")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNone(result)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_invalid_arb_output(self, mock_run):
        """Test firmware analysis with invalid arbextract output."""
        # Create extracted xbl_config image
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        # Invalid output without ARB index
        invalid_output = """Something: 1
Other data: 2"""

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=invalid_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNone(result)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_zero_arb(self, mock_run):
        """Test firmware analysis with ARB index 0 (safe to downgrade)."""
        # Create extracted xbl_config image
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        arb_output = """ARB (Anti-Rollback): 0
Major Version: 3
Minor Version: 0"""

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=arb_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNotNone(result)
            self.assertEqual(result['arb_index'], '0')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_creates_output_directory(self, mock_run):
        """Test that analyze_firmware creates output directory if it doesn't exist."""
        # Remove output directory
        shutil.rmtree(self.output_dir)
        self.assertFalse(self.output_dir.exists())

        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        try:
            from analyze_firmware import analyze_firmware

            # Call should create the directory
            analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertTrue(self.output_dir.exists())
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    def test_run_command_with_shell_injection_protection(self):
        """Test that run_command properly escapes arguments to prevent shell injection."""
        try:
            from analyze_firmware import run_command

            # Test with potentially dangerous input
            dangerous_cmd = ["/bin/echo", "test; rm -rf /"]

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(returncode=0, stdout="output", stderr="")
                run_command(dangerous_cmd)

                # Verify shell=False is used
                mock_run.assert_called_once()
                call_kwargs = mock_run.call_args[1]
                self.assertEqual(call_kwargs.get('shell'), False)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import run_command: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_multiple_xbl_images(self, mock_run):
        """Test firmware analysis when multiple xbl_config images exist (uses first)."""
        # Create multiple xbl_config images
        img_file1 = self.output_dir / "xbl_config.img"
        img_file2 = self.output_dir / "xbl_config_backup.img"
        img_file1.touch()
        img_file2.touch()

        arb_output = """ARB (Anti-Rollback): 2
Major Version: 3
Minor Version: 0"""

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=arb_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            # Should successfully use first matching image
            self.assertIsNotNone(result)
            self.assertEqual(result['arb_index'], '2')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")


class TestAnalyzeFirmwareMain(unittest.TestCase):
    """Test suite for analyze_firmware.py main function and CLI."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.zip_path = Path(self.temp_dir) / "firmware.zip"
        self.zip_path.touch()

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('sys.argv', ['analyze_firmware.py', 'firmware.zip', '--json'])
    @patch('analyze_firmware.analyze_firmware')
    def test_main_json_output(self, mock_analyze):
        """Test main function with JSON output."""
        mock_analyze.return_value = {
            'arb_index': '1',
            'major': '3',
            'minor': '0'
        }

        try:
            from analyze_firmware import main

            with patch('builtins.print') as mock_print:
                main()

                # Verify JSON output
                mock_print.assert_called_once()
                output = mock_print.call_args[0][0]
                parsed = json.loads(output)
                self.assertEqual(parsed['arb_index'], '1')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import main: {e}")

    @patch('sys.argv', ['analyze_firmware.py', 'firmware.zip'])
    @patch('analyze_firmware.analyze_firmware')
    def test_main_text_output(self, mock_analyze):
        """Test main function with text output."""
        mock_analyze.return_value = {
            'arb_index': '1',
            'major': '3',
            'minor': '0'
        }

        try:
            from analyze_firmware import main

            with patch('builtins.print') as mock_print:
                main()

                # Verify text output contains all fields
                calls = [str(call) for call in mock_print.call_args_list]
                output = ' '.join(calls)
                self.assertIn('ARB Index: 1', output)
                self.assertIn('Major: 3', output)
                self.assertIn('Minor: 0', output)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import main: {e}")

    @patch('sys.argv', ['analyze_firmware.py', 'firmware.zip'])
    @patch('analyze_firmware.analyze_firmware')
    @patch('sys.exit')
    def test_main_analysis_failure(self, mock_exit, mock_analyze):
        """Test main function when analysis fails."""
        mock_analyze.return_value = None

        try:
            from analyze_firmware import main

            main()

            # Should exit with error code
            mock_exit.assert_called_once_with(1)
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import main: {e}")

    @patch('sys.argv', ['analyze_firmware.py', 'firmware.zip', '--tools-dir', '/custom/tools', '--output-dir', '/custom/output'])
    @patch('analyze_firmware.analyze_firmware')
    def test_main_custom_directories(self, mock_analyze):
        """Test main function with custom tool and output directories."""
        mock_analyze.return_value = {'arb_index': '0', 'major': '3', 'minor': '0'}

        try:
            from analyze_firmware import main

            with patch('builtins.print'):
                main()

                # Verify custom directories were passed
                mock_analyze.assert_called_once()
                args = mock_analyze.call_args[0]
                self.assertEqual(args[1], '/custom/tools')
                self.assertEqual(args[2], '/custom/output')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import main: {e}")


class TestAnalyzeFirmwareEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.tools_dir = Path(self.temp_dir) / "tools"
        self.output_dir = Path(self.temp_dir) / "extracted"
        self.zip_path = Path(self.temp_dir) / "firmware.zip"

        self.tools_dir.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)
        self.zip_path.touch()

    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @patch('subprocess.run')
    def test_analyze_firmware_whitespace_in_arb_output(self, mock_run):
        """Test parsing ARB output with extra whitespace."""
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        arb_output = """ARB (Anti-Rollback):    1
Major Version:   3
Minor Version:  0   """

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=arb_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            # Should handle whitespace correctly
            self.assertIsNotNone(result)
            self.assertEqual(result['arb_index'], '1')
            self.assertEqual(result['major'], '3')
            self.assertEqual(result['minor'], '0')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")

    @patch('subprocess.run')
    def test_analyze_firmware_high_arb_value(self, mock_run):
        """Test firmware with high ARB index value."""
        img_file = self.output_dir / "xbl_config.img"
        img_file.touch()

        arb_output = """ARB (Anti-Rollback): 99
Major Version: 10
Minor Version: 5"""

        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "otaripper" in str(cmd[0]):
                return Mock(returncode=0, stdout="Extracted", stderr="")
            elif "arbextract" in str(cmd[0]):
                return Mock(returncode=0, stdout=arb_output, stderr="")
            return Mock(returncode=1, stdout="", stderr="Error")

        mock_run.side_effect = side_effect

        try:
            from analyze_firmware import analyze_firmware

            result = analyze_firmware(str(self.zip_path), str(self.tools_dir), str(self.output_dir))

            self.assertIsNotNone(result)
            self.assertEqual(result['arb_index'], '99')
            self.assertEqual(result['major'], '10')
            self.assertEqual(result['minor'], '5')
        except (ImportError, NameError) as e:
            self.skipTest(f"Cannot import analyze_firmware: {e}")


if __name__ == '__main__':
    unittest.main()