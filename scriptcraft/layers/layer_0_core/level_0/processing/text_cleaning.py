"""Brace-aware text normalization for dictionary expected-values strings."""

import re

from typing import List


def _split_brace_groups(text: str) -> List[str]:
    """Split text into [{...}, outside_text, {...}] preserving braces."""
    return re.split(r"(\{[^}]*\})", text)


def _is_brace_block(segment: str) -> bool:
    return segment.startswith("{") and segment.endswith("}")


def prevent_pipe_inside_braces(text: str) -> str:
    """Insert ' | ' between digit-letter boundaries OUTSIDE braces."""
    parts = _split_brace_groups(text)

    for i, part in enumerate(parts):
        if not _is_brace_block(part):
            parts[i] = re.sub(r"(\d)\s([A-Za-z])", r"\1 | \2", part)

    return "".join(parts)


def fix_numeric_dash_inside_braces(text: str) -> str:
    """Normalize numeric ranges inside braces: 5 - 10 → 5-10."""
    parts = _split_brace_groups(text)

    for i, part in enumerate(parts):
        if _is_brace_block(part):
            parts[i] = re.sub(r"(\d+)\s*-\s*(\d+)", r"\1-\2", part)

    return "".join(parts)


def fix_word_number_dash_inside_braces(text: str) -> str:
    """Normalize word/number dash spacing inside braces."""
    parts = _split_brace_groups(text)

    for i, part in enumerate(parts):
        if _is_brace_block(part):
            part = re.sub(r"(?<=\d)\s*-\s*(?=[A-Za-z])", " - ", part)
            part = re.sub(r"(?<=[A-Za-z])\s*-\s*(?=\d)", "-", part)
            parts[i] = part

    return "".join(parts)


def clean_brace_formatting(text: str) -> str:
    """Full brace normalization pipeline (ordered)."""
    text = prevent_pipe_inside_braces(text)
    text = fix_numeric_dash_inside_braces(text)
    text = fix_word_number_dash_inside_braces(text)
    return text
