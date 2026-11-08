from unittest.mock import patch

from bs4 import BeautifulSoup

from fetch_firmware import get_signed_url_springer, resolve_springer_package_url


RESULT_WITHOUT_URL = """
<div id="resultBox" data-url="">
  <form method="post" action="/index.php?view=ota&amp;ota_action=package" id="otaPackageForm">
    <input type="hidden" name="k" value="abc123">
    <input type="hidden" name="csrf" value="def456">
    <button type="submit">Download OTA package</button>
  </form>
</div>
"""

RESULT_WITH_URL = """
<div id="resultBox" data-url="https://cdn.example.com/firmware.zip?a=1&amp;b=2"></div>
"""


class FakeResponse:
    def __init__(self, text="", status_code=200, headers=None):
        self.text = text
        self.status_code = status_code
        self.headers = headers or {}

    @property
    def is_redirect(self):
        return self.status_code in (301, 302, 303, 307, 308) and "Location" in self.headers

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.posts = []

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        return self.responses.pop(0)


class TestResolveSpringerPackageUrl:
    def test_follows_package_form_redirect(self):
        session = FakeSession([
            FakeResponse(
                status_code=303,
                headers={"Location": "https://cdn.example.com/firmware.zip?token=xyz"},
            )
        ])
        soup = BeautifulSoup(RESULT_WITHOUT_URL, "html.parser")

        url = resolve_springer_package_url(soup, session, {"User-Agent": "test"})

        assert url == "https://cdn.example.com/firmware.zip?token=xyz"
        assert len(session.posts) == 1
        called_url, kwargs = session.posts[0]
        assert called_url == "https://roms.danielspringer.at/index.php?view=ota&ota_action=package"
        assert kwargs["data"] == {"k": "abc123", "csrf": "def456"}
        assert kwargs["allow_redirects"] is False

    def test_uses_url_from_direct_response(self):
        session = FakeSession([FakeResponse(text=RESULT_WITH_URL)])
        soup = BeautifulSoup(RESULT_WITHOUT_URL, "html.parser")

        url = resolve_springer_package_url(soup, session, {})

        assert url == "https://cdn.example.com/firmware.zip?a=1&b=2"

    def test_returns_none_without_package_form(self):
        soup = BeautifulSoup('<div id="resultBox" data-url=""></div>', "html.parser")

        assert resolve_springer_package_url(soup, FakeSession([]), {}) is None


class TestGetSignedUrlSpringer:
    def test_falls_back_to_package_form_when_data_url_missing(self):
        session = FakeSession([
            FakeResponse(text=RESULT_WITHOUT_URL),
            FakeResponse(
                status_code=303,
                headers={"Location": "https://cdn.example.com/firmware.zip?token=xyz"},
            ),
        ])

        with patch("fetch_firmware.requests.Session", return_value=session), \
             patch(
                 "fetch_firmware.get_springer_versions",
                 return_value=(["PYB110_17.0.0.155(CN01)", "PYB110_17.0.0.152(CN01)"], "OP 16"),
             ):
            result = get_signed_url_springer("16", "CN", "PYB110_17.0.0.155(CN01)")

        assert result == {
            "url": "https://cdn.example.com/firmware.zip?token=xyz",
            "version": "PYB110_17.0.0.155(CN01)",
            "md5": None,
        }
        assert session.posts[0][1]["data"]["version_index"] == "0"
        assert session.posts[1][1]["allow_redirects"] is False

    def test_keeps_using_data_url_when_present(self):
        session = FakeSession([FakeResponse(text=RESULT_WITH_URL)])

        with patch("fetch_firmware.requests.Session", return_value=session), \
             patch(
                 "fetch_firmware.get_springer_versions",
                 return_value=(["PYB110_17.0.1.201(CN01)"], "OP 16"),
             ):
            result = get_signed_url_springer("16", "CN", "PYB110_17.0.1.201(CN01)")

        assert result["url"] == "https://cdn.example.com/firmware.zip?a=1&b=2"
        assert len(session.posts) == 1
