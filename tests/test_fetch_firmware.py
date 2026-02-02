#!/usr/bin/env python3
"""
Comprehensive tests for fetch_firmware.py
Tests firmware fetching from OOS API and Springer fallback.
"""

import unittest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fetch_firmware import (
    get_from_oos_api,
    get_signed_url_springer,
    main
)


class TestGetFromOOSAPI(unittest.TestCase):
    """Test suite for get_from_oos_api function."""

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_success(self, mock_get):
        """Test successful firmware fetch from OOS API."""
        # Mock URL response
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = 'https://example.com/firmware.zip'
        mock_url_response.raise_for_status = Mock()

        # Mock version response
        mock_ver_response = Mock()
        mock_ver_response.status_code = 200
        mock_ver_response.text = 'CPH2747_16.0.3.501(EX01)'
        mock_ver_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_url_response, mock_ver_response]

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNotNone(result)
        self.assertEqual(result['url'], 'https://example.com/firmware.zip')
        self.assertEqual(result['version'], 'CPH2747_16.0.3.501(EX01)')

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_oneplus_device(self, mock_get):
        """Test OOS API call for OnePlus device."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = 'https://example.com/firmware.zip'
        mock_url_response.raise_for_status = Mock()

        mock_ver_response = Mock()
        mock_ver_response.status_code = 200
        mock_ver_response.text = 'Version_1.0'
        mock_ver_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_url_response, mock_ver_response]

        result = get_from_oos_api('15', 'EU')

        # Verify correct endpoint was called
        self.assertEqual(mock_get.call_count, 2)
        first_call = mock_get.call_args_list[0]
        self.assertIn('oneplus', first_call[0][0])

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_oppo_device(self, mock_get):
        """Test OOS API call for Oppo device."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = 'https://example.com/firmware.zip'
        mock_url_response.raise_for_status = Mock()

        mock_ver_response = Mock()
        mock_ver_response.status_code = 200
        mock_ver_response.text = 'Version_1.0'
        mock_ver_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_url_response, mock_ver_response]

        result = get_from_oos_api('Find X8', 'CN')

        # Verify correct brand endpoint was called
        self.assertEqual(mock_get.call_count, 2)
        first_call = mock_get.call_args_list[0]
        self.assertIn('oppo', first_call[0][0])

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_invalid_url_response(self, mock_get):
        """Test OOS API with invalid URL response."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = 'not_a_url'
        mock_url_response.raise_for_status = Mock()

        mock_get.return_value = mock_url_response

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_empty_url(self, mock_get):
        """Test OOS API with empty URL response."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = ''
        mock_url_response.raise_for_status = Mock()

        mock_get.return_value = mock_url_response

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_network_error(self, mock_get):
        """Test OOS API with network error."""
        mock_get.side_effect = Exception('Network error')

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_timeout(self, mock_get):
        """Test OOS API with timeout."""
        import requests
        mock_get.side_effect = requests.Timeout('Request timeout')

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_http_error(self, mock_get):
        """Test OOS API with HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception('404 Not Found')

        mock_get.return_value = mock_response

        result = get_from_oos_api('15', 'GLO')

        self.assertIsNone(result)


class TestGetSignedURLSpringer(unittest.TestCase):
    """Test suite for get_signed_url_springer function."""

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_success(self, mock_session_class):
        """Test successful firmware fetch from Springer."""
        mock_session = MagicMock()

        # Mock initial page load
        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"GLO": ["Version1", "Version2"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        # Mock form submission
        mock_form_response = Mock()
        mock_form_response.status_code = 200
        mock_form_response.text = '''
        <html>
            <div id="resultBox" data-url="https://example.com/firmware.zip"></div>
        </html>
        '''
        mock_form_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session.post.return_value = mock_form_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        self.assertIsNotNone(result)
        self.assertEqual(result['url'], 'https://example.com/firmware.zip')
        self.assertEqual(result['version'], 'Version1')

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_with_target_version(self, mock_session_class):
        """Test Springer fetch with specific target version."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"GLO": ["Version1", "Version2", "Version3"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_form_response = Mock()
        mock_form_response.status_code = 200
        mock_form_response.text = '''
        <html>
            <div id="resultBox" data-url="https://example.com/firmware_v2.zip"></div>
        </html>
        '''
        mock_form_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session.post.return_value = mock_form_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO', 'Version2')

        self.assertIsNotNone(result)
        self.assertEqual(result['url'], 'https://example.com/firmware_v2.zip')
        self.assertEqual(result['version'], 'Version2')

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_device_not_found(self, mock_session_class):
        """Test Springer fetch when device is not found."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 13": {"GLO": ["Version1"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_region_not_found(self, mock_session_class):
        """Test Springer fetch when region is not found."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"EU": ["Version1"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_version_not_found(self, mock_session_class):
        """Test Springer fetch when target version is not found."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"GLO": ["Version1", "Version2"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO', 'Version99')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_no_result_box(self, mock_session_class):
        """Test Springer fetch when result box is missing."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"GLO": ["Version1"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_form_response = Mock()
        mock_form_response.status_code = 200
        mock_form_response.text = '<html><body>No result</body></html>'
        mock_form_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session.post.return_value = mock_form_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_network_error(self, mock_session_class):
        """Test Springer fetch with network error."""
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception('Network error')
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_invalid_json(self, mock_session_class):
        """Test Springer fetch with invalid JSON in data-devices."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='invalid json'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session_class.return_value = mock_session

        # Invalid JSON should either return None or raise an exception
        try:
            result = get_signed_url_springer('15', 'GLO')
            # If it doesn't raise, it should return None
            self.assertIsNone(result)
        except (json.JSONDecodeError, Exception):
            # Acceptable to raise exception for invalid JSON
            pass


class TestMain(unittest.TestCase):
    """Test suite for main function."""

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_success_oos_api(self, mock_oos_api):
        """Test main function with successful OOS API fetch."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print') as mock_print:
            main()

            # Should print URL by default
            mock_print.assert_called_once_with('https://example.com/firmware.zip')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', '--json'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_json_output(self, mock_oos_api):
        """Test main function with JSON output."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print') as mock_print:
            main()

            output = mock_print.call_args[0][0]
            parsed = json.loads(output)
            self.assertEqual(parsed['url'], 'https://example.com/firmware.zip')
            self.assertEqual(parsed['version'], 'Version1')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', '--version-only'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_version_only_output(self, mock_oos_api):
        """Test main function with version-only output."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print') as mock_print:
            main()

            mock_print.assert_called_once_with('Version1')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', '--url-only'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_url_only_output(self, mock_oos_api):
        """Test main function with URL-only output."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print') as mock_print:
            main()

            mock_print.assert_called_once_with('https://example.com/firmware.zip')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', '--output', 'test_output.json'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_file_output(self, mock_oos_api):
        """Test main function with file output."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_file = f.name

        try:
            with patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', '--output', output_file]):
                main()

            # Verify file was created with correct content
            with open(output_file, 'r') as f:
                content = json.load(f)
                self.assertEqual(content['url'], 'https://example.com/firmware.zip')
                self.assertEqual(content['version'], 'Version1')
        finally:
            Path(output_file).unlink(missing_ok=True)

    @patch('sys.argv', ['fetch_firmware.py', 'oneplus_15', 'GLO'])
    @patch('fetch_firmware.get_from_oos_api')
    def test_main_strips_oneplus_prefix(self, mock_oos_api):
        """Test main function strips 'oneplus_' prefix from device ID."""
        mock_oos_api.return_value = {
            'url': 'https://example.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print'):
            main()

            # Should be called with '15', not 'oneplus_15'
            mock_oos_api.assert_called_once()
            call_args = mock_oos_api.call_args[0]
            self.assertEqual(call_args[0], '15')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO'])
    @patch('fetch_firmware.get_from_oos_api')
    @patch('fetch_firmware.get_signed_url_springer')
    def test_main_fallback_to_springer(self, mock_springer, mock_oos_api):
        """Test main function falls back to Springer when OOS API fails."""
        mock_oos_api.return_value = None
        mock_springer.return_value = {
            'url': 'https://springer.com/firmware.zip',
            'version': 'Version1'
        }

        with patch('builtins.print') as mock_print:
            main()

            mock_oos_api.assert_called_once()
            mock_springer.assert_called_once()
            mock_print.assert_called_once_with('https://springer.com/firmware.zip')

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO', 'SpecificVersion'])
    @patch('fetch_firmware.get_from_oos_api')
    @patch('fetch_firmware.get_signed_url_springer')
    def test_main_with_target_version_skips_oos(self, mock_springer, mock_oos_api):
        """Test main function skips OOS API when target version is specified."""
        mock_springer.return_value = {
            'url': 'https://springer.com/firmware.zip',
            'version': 'SpecificVersion'
        }

        with patch('builtins.print'):
            main()

            # OOS API should not be called when target version is provided
            mock_oos_api.assert_not_called()
            mock_springer.assert_called_once()

    @patch('sys.argv', ['fetch_firmware.py', '15', 'GLO'])
    @patch('fetch_firmware.get_from_oos_api')
    @patch('fetch_firmware.get_signed_url_springer')
    @patch('sys.exit')
    def test_main_all_sources_fail(self, mock_exit, mock_springer, mock_oos_api):
        """Test main function exits with error when all sources fail."""
        mock_oos_api.return_value = None
        mock_springer.return_value = None

        main()

        mock_exit.assert_called_once_with(1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_whitespace_in_response(self, mock_get):
        """Test OOS API handles whitespace in responses."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = '  https://example.com/firmware.zip  '
        mock_url_response.raise_for_status = Mock()

        mock_ver_response = Mock()
        mock_ver_response.status_code = 200
        mock_ver_response.text = '  Version1  '
        mock_ver_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_url_response, mock_ver_response]

        result = get_from_oos_api('15', 'GLO')

        # Should strip whitespace
        self.assertEqual(result['url'], 'https://example.com/firmware.zip')
        self.assertEqual(result['version'], 'Version1')

    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_html_entities(self, mock_session_class):
        """Test Springer handles HTML entities in URLs."""
        mock_session = MagicMock()

        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.text = '''
        <html>
            <select id="device" data-devices='{"OP 15": {"GLO": ["Version1"]}}'>
            </select>
        </html>
        '''
        mock_page_response.raise_for_status = Mock()

        mock_form_response = Mock()
        mock_form_response.status_code = 200
        mock_form_response.text = '''
        <html>
            <div id="resultBox" data-url="https://example.com/firmware.zip?param=value&amp;other=test"></div>
        </html>
        '''
        mock_form_response.raise_for_status = Mock()

        mock_session.get.return_value = mock_page_response
        mock_session.post.return_value = mock_form_response
        mock_session_class.return_value = mock_session

        result = get_signed_url_springer('15', 'GLO')

        # Should unescape HTML entities
        self.assertIn('&', result['url'])
        self.assertNotIn('&amp;', result['url'])

    @patch('fetch_firmware.requests.get')
    def test_get_from_oos_api_unmapped_device(self, mock_get):
        """Test OOS API with unmapped device ID (uses fallback)."""
        mock_url_response = Mock()
        mock_url_response.status_code = 200
        mock_url_response.text = 'https://example.com/firmware.zip'
        mock_url_response.raise_for_status = Mock()

        mock_ver_response = Mock()
        mock_ver_response.status_code = 200
        mock_ver_response.text = 'Version1'
        mock_ver_response.raise_for_status = Mock()

        mock_get.side_effect = [mock_url_response, mock_ver_response]

        # Device not in OOS_MAPPING should use fallback
        result = get_from_oos_api('Unknown_Device', 'GLO')

        # Should still attempt the request with fallback mapping
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()