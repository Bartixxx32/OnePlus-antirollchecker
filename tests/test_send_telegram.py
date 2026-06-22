import pytest
from send_telegram import escape_markdown


class TestEscapeMarkdown:
    def test_no_special_chars(self):
        assert escape_markdown("Hello World") == "Hello World"

    def test_underscore(self):
        assert escape_markdown("Hello_World") == "Hello\\_World"

    def test_asterisk(self):
        assert escape_markdown("Hello*World") == "Hello\\*World"

    def test_backtick(self):
        assert escape_markdown("Hello`World") == "Hello\\`World"

    def test_brackets(self):
        assert escape_markdown("[Hello]") == "\\[Hello\\]"

    def test_mixed_special_chars(self):
        result = escape_markdown("_*`[Test]")
        assert result == "\\_\\*\\`\\[Test\\]"

    def test_none_input(self):
        assert escape_markdown(None) is None

    def test_empty_string(self):
        assert escape_markdown("") == ""

    def test_multiple_underscores(self):
        assert escape_markdown("a_b_c") == "a\\_b\\_c"

    def test_numbers_only(self):
        assert escape_markdown("12345") == "12345"

    def test_telegram_username(self):
        assert escape_markdown("@username") == "@username"

    def test_url_text(self):
        assert escape_markdown("Check this link") == "Check this link"

    def test_version_with_underscores(self):
        assert escape_markdown("14.0.0.800(EX01)") == "14.0.0.800(EX01)"

    def test_device_with_parentheses(self):
        """Parentheses are not escaped in V1 but could cause issues in some contexts."""
        result = escape_markdown("OnePlus 12 (Global)")
        assert result == "OnePlus 12 (Global)"
