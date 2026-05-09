"""
Keyword field normalizer: deduplicates, sorts, and standardizes keyword
separators in BibTeX `keywords` fields.
"""

from __future__ import annotations

import re
from typing import Optional

# Accepted input separators between individual keywords
_SPLIT_RE = re.compile(r"[;,|]+")


def normalize_keywords(raw: str, separator: str = "; ") -> str:
    """Split *raw* on common separators, strip each token, deduplicate while
    preserving first-seen order, then rejoin with *separator*."""
    parts = _SPLIT_RE.split(raw)
    seen: dict[str, None] = {}
    cleaned: list[str] = []
    for part in parts:
        token = " ".join(part.split())  # collapse internal whitespace
        if token and token.lower() not in seen:
            seen[token.lower()] = None
            cleaned.append(token)
    cleaned.sort(key=str.casefold)
    return separator.join(cleaned)


def normalize_entry_keywords(
    entry: dict,
    field: str = "keywords",
    separator: str = "; ",
) -> dict:
    """Return a copy of *entry* with the keyword field normalized."""
    entry = dict(entry)
    raw: Optional[str] = entry.get(field)
    if raw:
        entry[field] = normalize_keywords(raw, separator=separator)
    return entry


def normalize_bibliography_keywords(
    bibliography: list[dict],
    field: str = "keywords",
    separator: str = "; ",
) -> list[dict]:
    """Apply :func:`normalize_entry_keywords` to every entry in *bibliography*."""
    return [
        normalize_entry_keywords(entry, field=field, separator=separator)
        for entry in bibliography
    ]
