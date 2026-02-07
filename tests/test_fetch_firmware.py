import unittest
from unittest.mock import patch, MagicMock
import requests
import json
from fetch_firmware import requests_get_with_retry, get_from_oos_api, get_springer_versions, get_signed_url_springer

class TestFetchFirmware(unittest.TestCase):

    @patch('fetch_firmware.requests.get')
    @patch('fetch_firmware.time.sleep')
    def test_requests_get_with_retry_success(self, mock_sleep, mock_get):
        """Test successful request with retry logic."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = requests_get_with_retry("http://test.url")
        self.assertEqual(response, mock_response)
        mock_get.assert_called_once()

    @patch('fetch_firmware.requests.get')
    @patch('fetch_firmware.time.sleep')
    def test_requests_get_with_retry_failure_then_success(self, mock_sleep, mock_get):
        """Test request failing once then succeeding."""
        mock_response_fail = MagicMock()
        mock_response_fail.raise_for_status.side_effect = requests.RequestException("Fail")

        mock_response_success = MagicMock()
        mock_response_success.raise_for_status.return_value = None

        mock_get.side_effect = [mock_response_fail, mock_response_success]

        response = requests_get_with_retry("http://test.url", retries=3)
        self.assertEqual(response, mock_response_success)
        self.assertEqual(mock_get.call_count, 2)

    @patch('fetch_firmware.requests.get')
    @patch('fetch_firmware.time.sleep')
    def test_requests_get_with_retry_all_fail(self, mock_sleep, mock_get):
        """Test request failing all retries."""
        mock_response_fail = MagicMock()
        mock_response_fail.raise_for_status.side_effect = requests.RequestException("Fail")
        mock_get.return_value = mock_response_fail

        with self.assertRaises(requests.RequestException):
            requests_get_with_retry("http://test.url", retries=2, delay=0.1)
        self.assertEqual(mock_get.call_count, 2)

    @patch('fetch_firmware.requests_get_with_retry')
    def test_get_from_oos_api_success(self, mock_get):
        """Test OOS API success."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "download_url": "http://firmware.zip",
            "version_number": "1.0",
            "md5sum": "abcdef"
        }
        mock_get.return_value = mock_response

        result = get_from_oos_api("15", "GLO")
        self.assertEqual(result["url"], "http://firmware.zip")
        self.assertEqual(result["version"], "1.0")
        self.assertEqual(result["md5"], "abcdef")

    def test_get_from_oos_api_cn_skip(self):
        """Test skipping CN region for OOS API."""
        result = get_from_oos_api("15", "CN")
        self.assertIsNone(result)

    @patch('fetch_firmware.requests_get_with_retry')
    def test_get_from_oos_api_fail(self, mock_get):
        """Test OOS API failure."""
        mock_get.side_effect = requests.RequestException("API Down")
        result = get_from_oos_api("15", "GLO")
        self.assertIsNone(result)

    @patch('fetch_firmware.requests.Session')
    def test_get_springer_versions_success(self, mock_session_cls):
        """Test getting versions from Springer."""
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        # Mock HTML with data-devices
        devices_data = {
            "OP 15": {
                "GLO": ["Version A", "Version B"]
            }
        }
        escaped_json = json.dumps(devices_data).replace('"', '&quot;')
        html_content = f"""
        <html>
            <select id="device" data-devices="{escaped_json}"></select>
        </html>
        """
        mock_response.text = html_content
        mock_session.get.return_value = mock_response

        versions, name = get_springer_versions("15", "GLO")
        self.assertEqual(versions, ["Version A", "Version B"])
        self.assertEqual(name, "OP 15")

    @patch('fetch_firmware.get_springer_versions')
    @patch('fetch_firmware.requests.Session')
    def test_get_signed_url_springer_success(self, mock_session_cls, mock_get_versions):
        """Test getting signed URL from Springer."""
        mock_get_versions.return_value = (["Version A"], "OP 15")

        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        # Mock HTML result
        html_content = """
        <div id="resultBox" data-url="http://signed.url/file.zip"></div>
        """
        mock_response.text = html_content
        mock_session.post.return_value = mock_response

        result = get_signed_url_springer("15", "GLO")
        self.assertEqual(result["url"], "http://signed.url/file.zip")
        self.assertEqual(result["version"], "Version A")

if __name__ == '__main__':
    unittest.main()
