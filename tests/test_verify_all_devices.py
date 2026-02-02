#!/usr/bin/env python3
"""
Comprehensive tests for verify_all_devices.py
Tests device verification and batch checking functionality.
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from verify_all_devices import verify_all


class TestVerifyAll(unittest.TestCase):
    """Test suite for verify_all function."""

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_success(self, mock_metadata, mock_run):
        """Test verify_all with all devices successful."""
        # Mock device metadata
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747', 'EU': 'CPH2747'}})
        ]

        # Mock successful subprocess
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            # Should have printed results
            self.assertGreater(mock_print.call_count, 0)

            # Check that success message was printed
            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('OK', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_failure(self, mock_metadata, mock_run):
        """Test verify_all with device failure."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        # Mock failed subprocess
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ''
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('FAIL', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_invalid_url_output(self, mock_metadata, mock_run):
        """Test verify_all with invalid URL output."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        # Mock subprocess with non-URL output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'not a url'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('FAIL', output)
            self.assertIn('Invalid Output', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_timeout(self, mock_metadata, mock_run):
        """Test verify_all with subprocess timeout."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired('cmd', 30)

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('FAIL', output)
            self.assertIn('Timeout', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_exception(self, mock_metadata, mock_run):
        """Test verify_all with unexpected exception."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        # Mock exception
        mock_run.side_effect = Exception('Unexpected error')

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            self.assertIn('FAIL', output)
            self.assertIn('Unexpected error', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_multiple_devices(self, mock_metadata, mock_run):
        """Test verify_all with multiple devices."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747', 'EU': 'CPH2747'}}),
            ('13', {'name': 'OnePlus 13', 'models': {'GLO': 'CPH2649'}})
        ]

        # Mock successful subprocess
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print'):
            verify_all()

            # Should be called for each device/region combination (3 total)
            self.assertEqual(mock_run.call_count, 3)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_uses_shell_false(self, mock_metadata, mock_run):
        """Test that verify_all uses shell=False for security."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print'):
            verify_all()

            # Verify shell=False was used
            mock_run.assert_called()
            call_kwargs = mock_run.call_args[1]
            self.assertEqual(call_kwargs.get('shell'), False)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_prints_summary(self, mock_metadata, mock_run):
        """Test that verify_all prints summary at the end."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should have summary message
            self.assertTrue('passed' in output or 'failures' in output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_mixed_results(self, mock_metadata, mock_run):
        """Test verify_all with mixed success and failure."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747', 'EU': 'CPH2747'}})
        ]

        # Alternate between success and failure
        success_result = Mock()
        success_result.returncode = 0
        success_result.stdout = 'https://example.com/firmware.zip'

        failure_result = Mock()
        failure_result.returncode = 1
        failure_result.stdout = ''

        mock_run.side_effect = [success_result, failure_result]

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should show both OK and FAIL
            self.assertIn('OK', output)
            self.assertIn('FAIL', output)


class TestVerifyAllOutput(unittest.TestCase):
    """Test suite for verify_all output formatting."""

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_table_header(self, mock_metadata, mock_run):
        """Test that verify_all prints proper table header."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Check for table headers
            self.assertIn('Device', output)
            self.assertIn('Region', output)
            self.assertIn('Status', output)
            self.assertIn('Result', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_separator_line(self, mock_metadata, mock_run):
        """Test that verify_all prints separator line."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should have separator lines
            self.assertIn('-' * 60, output)


class TestVerifyAllCommandConstruction(unittest.TestCase):
    """Test suite for command construction in verify_all."""

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_command_format(self, mock_metadata, mock_run):
        """Test that verify_all constructs correct command."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print'):
            verify_all()

            # Check command structure
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]

            self.assertEqual(call_args[0], 'python')
            self.assertEqual(call_args[1], 'fetch_firmware.py')
            self.assertEqual(call_args[2], '15')
            self.assertEqual(call_args[3], 'GLO')
            self.assertEqual(call_args[4], '--url-only')

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_uses_url_only_flag(self, mock_metadata, mock_run):
        """Test that verify_all uses --url-only flag."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print'):
            verify_all()

            call_args = mock_run.call_args[0][0]
            self.assertIn('--url-only', call_args)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_timeout_value(self, mock_metadata, mock_run):
        """Test that verify_all uses 30 second timeout."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print'):
            verify_all()

            call_kwargs = mock_run.call_args[1]
            self.assertEqual(call_kwargs.get('timeout'), 30)


class TestVerifyAllEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_empty_metadata(self, mock_metadata, mock_run):
        """Test verify_all with empty device metadata."""
        mock_metadata.items.return_value = []

        with patch('builtins.print') as mock_print:
            verify_all()

            # Should still print header and footer
            calls = [str(call) for call in mock_print.call_args_list]
            self.assertGreater(len(calls), 0)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_device_with_no_models(self, mock_metadata, mock_run):
        """Test verify_all with device that has no models."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {}})
        ]

        with patch('builtins.print'):
            verify_all()

            # Should not call subprocess for device with no models
            mock_run.assert_not_called()

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_url_with_whitespace(self, mock_metadata, mock_run):
        """Test verify_all handles URL with whitespace."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '  https://example.com/firmware.zip  \n'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should be treated as OK since it starts with http after strip
            self.assertIn('OK', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_very_long_output(self, mock_metadata, mock_run):
        """Test verify_all with very long output (should truncate in message)."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'x' * 1000  # Very long non-URL
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should truncate in output (check for ... or truncation)
            self.assertIn('FAIL', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_special_characters_in_device_name(self, mock_metadata, mock_run):
        """Test verify_all with special characters in device name."""
        mock_metadata.items.return_value = [
            ('Ace 5 Pro', {'name': 'OnePlus Ace 5 Pro', 'models': {'CN': 'Unknown'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should handle device name with spaces
            self.assertIn('Ace 5 Pro', output)


class TestVerifyAllIntegration(unittest.TestCase):
    """Integration tests for verify_all function."""

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_full_run_all_success(self, mock_metadata, mock_run):
        """Integration test: full run with all devices successful."""
        # Use realistic device metadata
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747', 'EU': 'CPH2747'}}),
            ('13', {'name': 'OnePlus 13', 'models': {'GLO': 'CPH2649', 'CN': 'PJZ110'}})
        ]

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'https://example.com/firmware.zip'
        mock_run.return_value = mock_result

        with patch('builtins.print') as mock_print:
            verify_all()

            # Should be called 4 times (2 devices × 2 regions each)
            self.assertEqual(mock_run.call_count, 4)

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should show all passed
            self.assertIn('All devices passed', output)

    @patch('verify_all_devices.subprocess.run')
    @patch('verify_all_devices.DEVICE_METADATA')
    def test_verify_all_full_run_with_failures(self, mock_metadata, mock_run):
        """Integration test: full run with some failures."""
        mock_metadata.items.return_value = [
            ('15', {'name': 'OnePlus 15', 'models': {'GLO': 'CPH2747', 'EU': 'CPH2747'}})
        ]

        # First call succeeds, second fails
        success_result = Mock()
        success_result.returncode = 0
        success_result.stdout = 'https://example.com/firmware.zip'

        failure_result = Mock()
        failure_result.returncode = 1
        failure_result.stdout = ''

        mock_run.side_effect = [success_result, failure_result]

        with patch('builtins.print') as mock_print:
            verify_all()

            calls = [str(call) for call in mock_print.call_args_list]
            output = ' '.join(calls)
            # Should show failures
            self.assertIn('Found', output)
            self.assertIn('failures', output)


if __name__ == '__main__':
    unittest.main()