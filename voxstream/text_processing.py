"""Text splitting utilities for VoxStream."""

import re

from voxstream.config import MAX_CHARS


def _split_by_words(text: str, max_chars: int) -> list[str]:
    """Break an oversized sentence into word-level chunks."""
    words = text.split()
    chunks: list[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split *text* into chunks ≤ *max_chars*, preserving sentence punctuation.

    Parameters
    ----------
    text:
        Input text to split.
    max_chars:
        Maximum number of characters per chunk.

    Returns
    -------
    list[str]
        List of text chunks, each at most *max_chars* characters long.
    """
    if len(text) <= max_chars:
        return [text]

    raw_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    parts: list[str] = []
    current_part = ""

    for sentence in raw_sentences:
        if len(sentence) > max_chars:
            if current_part:
                parts.append(current_part.strip())
                current_part = ""
            parts.extend(_split_by_words(sentence, max_chars))
            continue
        candidate = (current_part + " " + sentence).strip()
        if len(candidate) <= max_chars:
            current_part = candidate
        else:
            if current_part:
                parts.append(current_part.strip())
            current_part = sentence

    if current_part:
        parts.append(current_part.strip())

    return parts if parts else [text]
