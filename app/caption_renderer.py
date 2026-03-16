"""Caption renderer module for typewriter-style FFmpeg drawtext captions.

This module exposes pure functions for escaping text for FFmpeg drawtext
filters and generating filter expressions. No classes, no I/O.
"""

import logging
import unicodedata

logger = logging.getLogger(__name__)

# Characters that require backslash escaping in FFmpeg drawtext filter syntax
_FFMPEG_SPECIAL_CHARS = r""":\'[];="""

# Caption style constants
FONT_FAMILY = "Sans-Bold"
FONT_SIZE_HORIZONTAL = 96
FONT_SIZE_VERTICAL = 84
FONT_COLOR = "white"
BORDER_W = 4  # Black stroke border around each letter
MAX_WIDTH_RATIO = 0.8
LOWER_THIRD_Y_RATIO = 0.75
ROLLING_WINDOW_SECONDS = 1.0  # Show only words from the last ~1 second


def _is_renderable(ch: str) -> bool:
    """Return True if a character is considered renderable by FFmpeg drawtext.

    Renderable characters are printable ASCII (0x20-0x7E) plus common Unicode
    letters, marks, numbers, punctuation, symbols, and whitespace (categories
    starting with L, M, N, P, S, Z).  Control characters and unassigned
    codepoints are not renderable.
    """
    if ch == "\n" or ch == "\r" or ch == "\t":
        # Treat common whitespace as renderable (mapped to space later if needed)
        return True
    cat = unicodedata.category(ch)
    # Categories: L=letter, M=mark, N=number, P=punctuation, S=symbol, Z=separator
    return cat[0] in ("L", "M", "N", "P", "S", "Z")


def escape_ffmpeg_text(text: str) -> str:
    """Escape special characters for FFmpeg drawtext filter.

    Characters requiring escaping: : \\ ' ; [ ] =
    FFmpeg drawtext uses backslash escaping.
    Non-renderable characters are replaced with a space.

    Round-trip property: unescape(escape(text)) == text
    for all valid narration_text strings (those containing only renderable
    characters).
    """
    result: list[str] = []
    for ch in text:
        if not _is_renderable(ch):
            result.append(" ")
            continue
        if ch in _FFMPEG_SPECIAL_CHARS:
            result.append("\\" + ch)
        else:
            result.append(ch)
    return "".join(result)


def unescape_ffmpeg_text(escaped: str) -> str:
    """Reverse the escaping performed by escape_ffmpeg_text.

    Used for testing the round-trip property.
    """
    result: list[str] = []
    i = 0
    while i < len(escaped):
        if escaped[i] == "\\" and i + 1 < len(escaped) and escaped[i + 1] in _FFMPEG_SPECIAL_CHARS:
            result.append(escaped[i + 1])
            i += 2
        else:
            result.append(escaped[i])
            i += 1
    return "".join(result)


def build_drawtext_filter(
    text: str,
    duration: float,
    video_width: int,
    video_height: int,
    start_time: float = 0.0,
    crossfade_duration: float = 0.0,
) -> str:
    """Generate FFmpeg drawtext filter expressions for rolling-window captions.

    Instead of accumulating all words, shows only a sliding window of recent
    words (roughly the last ROLLING_WINDOW_SECONDS worth). Each window chunk
    replaces the previous one with a hard cut (no fade). Text is line-wrapped
    to fit within MAX_WIDTH_RATIO of the frame.

    Args:
        text: Raw narration text (will be escaped internally).
        duration: Audio duration in seconds for this scene.
        video_width: Output video width in pixels.
        video_height: Output video height in pixels.
        start_time: Offset in seconds from the start of the final video
                     where this scene begins.
        crossfade_duration: Duration of crossfade transition in seconds.
                            Caption starts after crossfade completes.

    Returns:
        A comma-separated chain of FFmpeg drawtext filter strings, or
        empty string for empty text input.

    Raises:
        ValueError: If duration is non-positive.
    """
    if duration <= 0:
        raise ValueError(f"Duration must be positive, got {duration}")

    if not text or not text.strip():
        logger.warning("Empty caption text, skipping drawtext filter")
        return ""

    words = text.split()
    if not words:
        return ""

    n_words = len(words)

    # Choose font size based on orientation
    is_vertical = video_height > video_width
    font_size = FONT_SIZE_VERTICAL if is_vertical else FONT_SIZE_HORIZONTAL

    # Max text width in pixels (approximate: ~0.55 * font_size per char for sans-bold)
    max_text_width = int(video_width * MAX_WIDTH_RATIO)
    avg_char_width = font_size * 0.55

    # Y position in the lower third
    y_pos = int(video_height * LOWER_THIRD_Y_RATIO)

    # Timing
    caption_start = start_time + crossfade_duration
    scene_end = start_time + duration
    caption_duration = scene_end - caption_start
    if caption_duration <= 0:
        caption_duration = duration

    # Compute per-word reveal times proportional to character count
    total_chars = sum(len(w) for w in words)
    if total_chars == 0:
        return ""

    word_times: list[float] = []
    cumulative = 0
    for w in words:
        t = caption_start + (cumulative / total_chars) * caption_duration
        word_times.append(t)
        cumulative += len(w)

    # Build rolling window chunks: for each word, show words from
    # (current_time - ROLLING_WINDOW_SECONDS) to current_time
    filters: list[str] = []

    for i in range(n_words):
        reveal_time = word_times[i]
        # End time: next word's reveal time, or scene end for the last word
        end_time = word_times[i + 1] if i + 1 < n_words else scene_end

        # Find the start of the rolling window
        window_start_time = reveal_time - ROLLING_WINDOW_SECONDS
        # Include words whose reveal time >= window_start_time up to word i
        window_start_idx = i
        for j in range(i, -1, -1):
            if word_times[j] >= window_start_time:
                window_start_idx = j
            else:
                break

        # Get the window of words to display
        window_words = words[window_start_idx: i + 1]

        # Line-wrap: break into lines that fit within max_text_width
        lines: list[str] = []
        current_line: list[str] = []
        current_width = 0.0
        for w in window_words:
            w_width = len(w) * avg_char_width
            space_width = avg_char_width if current_line else 0
            if current_line and (current_width + space_width + w_width) > max_text_width:
                lines.append(" ".join(current_line))
                current_line = [w]
                current_width = w_width
            else:
                current_line.append(w)
                current_width += space_width + w_width
        if current_line:
            lines.append(" ".join(current_line))

        # Join lines with actual newline for FFmpeg drawtext
        display_text = "\n".join(lines)
        escaped_text = escape_ffmpeg_text(display_text)

        # Horizontal centering with margin
        x_margin = int(video_width * (1 - MAX_WIDTH_RATIO) / 2)

        # Build drawtext filter with black stroke border, no background box
        dt_filter = (
            f"drawtext=text='{escaped_text}'"
            f":font='{FONT_FAMILY}'"
            f":fontsize={font_size}"
            f":fontcolor={FONT_COLOR}"
            f":borderw={BORDER_W}:bordercolor=black"
            f":x=max({x_margin}\\,(w-text_w)/2)"
            f":y={y_pos}"
            f":enable='between(t,{reveal_time:.4f},{end_time:.4f})'"
        )

        filters.append(dt_filter)

    return ",".join(filters)
