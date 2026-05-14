"""Normalize the 'series' field in BibTeX entries."""

import re
from typing import Optional

# Known series aliases mapping variant names to canonical forms
_SERIES_ALIASES: dict[str, str] = {
    "lecture notes in computer science": "Lecture Notes in Computer Science",
    "lncs": "Lecture Notes in Computer Science",
    "lecture notes in artificial intelligence": "Lecture Notes in Artificial Intelligence",
    "lnai": "Lecture Notes in Artificial Intelligence",
    "proceedings of machine learning research": "Proceedings of Machine Learning Research",
    "pmlr": "Proceedings of Machine Learning Research",
    "advances in neural information processing systems": "Advances in Neural Information Processing Systems",
    "nips": "Advances in Neural Information Processing Systems",
    "neurips": "Advances in Neural Information Processing Systems",
    "acm symposium": "ACM Symposium",
    "springer series in statistics": "Springer Series in Statistics",
    "ieee press series": "IEEE Press Series",
}


def normalize_series(series: Optional[str]) -> Optional[str]:
    """Normalize a series string to a canonical form.

    - Returns None for None or empty input.
    - Strips surrounding whitespace and braces.
    - Collapses internal whitespace.
    - Applies known alias mappings.
    - Falls back to title-casing unknown series.
    """
    if not series:
        return None

    # Strip braces and whitespace
    value = series.strip().strip("{}")
    # Collapse internal whitespace
    value = re.sub(r"\s+", " ", value).strip()

    if not value:
        return None

    lookup = value.lower()
    if lookup in _SERIES_ALIASES:
        return _SERIES_ALIASES[lookup]

    # Title-case as fallback
    return value.title()


def normalize_entry_series(entry: dict) -> dict:
    """Return a copy of entry with the 'series' field normalized."""
    result = dict(entry)
    if "series" in result:
        normalized = normalize_series(result["series"])
        if normalized is None:
            result.pop("series")
        else:
            result["series"] = normalized
    return result


def normalize_bibliography_series(entries: list[dict]) -> list[dict]:
    """Normalize the 'series' field across all entries."""
    return [normalize_entry_series(e) for e in entries]
