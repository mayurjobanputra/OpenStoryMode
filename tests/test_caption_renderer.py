"""Unit tests for caption renderer escape/unescape functions."""

import pytest

from app.caption_renderer import escape_ffmpeg_text, unescape_ffmpeg_text


class TestEscapeFfmpegText:
    """Tests for escape_ffmpeg_text — Requirements 7.1, 7.2, 7.3."""

    def test_plain_text_unchanged(self):
        assert escape_ffmpeg_text("hello world") == "hello world"

    def test_escapes_colon(self):
        assert escape_ffmpeg_text("time: now") == r"time\: now"

    def test_escapes_backslash(self):
        assert escape_ffmpeg_text(r"path\to") == r"path\\to"

    def test_escapes_single_quote(self):
        assert escape_ffmpeg_text("it's") == r"it\'s"

    def test_escapes_semicolon(self):
        assert escape_ffmpeg_text("a;b") == r"a\;b"

    def test_escapes_brackets(self):
        assert escape_ffmpeg_text("[tag]") == r"\[tag\]"

    def test_escapes_equals(self):
        assert escape_ffmpeg_text("a=b") == r"a\=b"

    def test_all_special_chars_individually(self):
        """Verify each special character is escaped with a backslash."""
        for ch in r""":\'[];=""":
            escaped = escape_ffmpeg_text(ch)
            assert escaped == "\\" + ch, f"Character {ch!r} not properly escaped"

    def test_non_renderable_replaced_with_space(self):
        # Null byte is non-renderable
        assert escape_ffmpeg_text("hello\x00world") == "hello world"

    def test_control_characters_replaced(self):
        # Bell character, vertical tab
        assert escape_ffmpeg_text("a\x07b\x0bc") == "a b c"

    def test_empty_string(self):
        assert escape_ffmpeg_text("") == ""

    def test_unicode_letters_preserved(self):
        assert escape_ffmpeg_text("café résumé") == "café résumé"

    def test_emoji_preserved(self):
        # Emoji are in the Symbol category, should be renderable
        result = escape_ffmpeg_text("hello 😀")
        assert "hello" in result
        assert "😀" in result

    def test_newline_and_tab_preserved(self):
        # Common whitespace should be renderable
        result = escape_ffmpeg_text("line1\nline2\ttab")
        assert "\n" in result
        assert "\t" in result


class TestUnescapeFfmpegText:
    """Tests for unescape_ffmpeg_text — Requirement 7.3."""

    def test_plain_text_unchanged(self):
        assert unescape_ffmpeg_text("hello world") == "hello world"

    def test_unescapes_colon(self):
        assert unescape_ffmpeg_text(r"\:") == ":"

    def test_unescapes_backslash(self):
        assert unescape_ffmpeg_text(r"\\") == "\\"

    def test_unescapes_single_quote(self):
        assert unescape_ffmpeg_text(r"\'") == "'"

    def test_unescapes_semicolon(self):
        assert unescape_ffmpeg_text(r"\;") == ";"

    def test_unescapes_brackets(self):
        assert unescape_ffmpeg_text(r"\[tag\]") == "[tag]"

    def test_unescapes_equals(self):
        assert unescape_ffmpeg_text(r"\=") == "="

    def test_empty_string(self):
        assert unescape_ffmpeg_text("") == ""

    def test_trailing_backslash_preserved(self):
        # A lone backslash at end with no following special char stays as-is
        assert unescape_ffmpeg_text("abc\\") == "abc\\"

    def test_backslash_before_non_special_preserved(self):
        # Backslash before a non-special char is not an escape sequence
        assert unescape_ffmpeg_text("\\n") == "\\n"


class TestRoundTrip:
    """Round-trip property: unescape(escape(text)) == text for renderable text.

    Requirement 7.3.
    """

    @pytest.mark.parametrize(
        "text",
        [
            "hello world",
            "it's a test: yes; no [maybe] = true",
            r"backslash \ here",
            "café résumé naïve",
            "",
            "a",
            "multiple\nlines\there",
            "all special :;'[]=\\",
        ],
    )
    def test_round_trip(self, text):
        assert unescape_ffmpeg_text(escape_ffmpeg_text(text)) == text
