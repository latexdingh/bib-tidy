"""Normalize issue/number fields in BibTeX entries.

Handles stripping of common prefixes (e.g. 'No.', 'Issue', '#'),
collapsing whitespace, and converting to a clean integer string
where possible.
"""

from __future__ import annotations

import re
from typing import Optional

# Prefixes to strip before the actual number
_PREFIX_RE = re.compile(
    r"^(?:no\.?|num\.?|number|issue|#)\s*",
    re.IGNORECASE,
)

# Match a simple integer (possibly with surrounding whitespace)
_INTEGER_RE = re.compile(r"^\s*(\d+)\s*$")

# Match a range like "3-4" or "3–4"
_RANGE_RE = re.compile(r"^\s*(\d+)\s*[-\u2013\u2014]\s*(\d+)\s*$")


def normalize_issue(value: Optional[str]) -> Optional[str]:
    """Return a normalised issue/number string, or None if blank."""
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None

    # Strip surrounding braces
    if text.startswith("{") and text.endswith("}"):
        text = text[1:-1].strip()

    # Strip common prefixes
    text = _PREFIX_RE.sub("", text).strip()

    if not text:
        return None

    # Normalise range separators to en-dash
    m_range = _RANGE_RE.match(text)
    if m_range:
        return f"{m_range.group(1)}--{m_range.group(2)}"

    # Plain integer — return as-is (no leading zeros)
    m_int = _INTEGER_RE.match(text)
    if m_int:
        return str(int(m_int.group(1)))

    # Anything else: collapse internal whitespace and return
    return re.sub(r"\s+", " ", text)


def normalize_entry_issue(
    entry: dict,
    field: str = "number",
) -> dict:
    """Return a copy of *entry* with the issue/number field normalised."""
    result = dict(entry)
    if field in result:
        result[field] = normalize_issue(result[field])
        if result[field] is None:
            del result[field]
    return result


def normalize_bibliography_issues(
    bibliography: list[dict],
    field: str = "number",
) -> list[dict]:
    """Normalise the issue/number field for every entry in *bibliography*."""
    return [normalize_entry_issue(entry, field=field) for entry in bibliography]
