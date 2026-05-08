"""
Normalize the `edition` field of BibTeX entries.

Converts various edition representations to a canonical ordinal string:
  - "1", "1st", "first" -> "1st"
  - "2", "2nd", "second" -> "2nd"
  - "3", "3rd", "third" -> "3rd"
  - "4", "4th", "fourth" -> "4th"
  - Arbitrary integers -> "<n>th" (or correct suffix)
"""

import re
from typing import Optional

_WORD_TO_INT = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "eleventh": 11, "twelfth": 12,
}

_ORDINAL_RE = re.compile(r"^(\d+)(?:st|nd|rd|th)?$", re.IGNORECASE)


def _ordinal_suffix(n: int) -> str:
    """Return the ordinal suffix for a positive integer."""
    if 11 <= (n % 100) <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def normalize_edition(value: Optional[str]) -> Optional[str]:
    """Return a canonical ordinal edition string, or None if value is absent."""
    if not value:
        return None

    stripped = value.strip()
    lower = stripped.lower()

    # Word form (e.g. "first", "Second")
    if lower in _WORD_TO_INT:
        n = _WORD_TO_INT[lower]
        return f"{n}{_ordinal_suffix(n)}"

    # Numeric or already-ordinal form (e.g. "1", "2nd", "3rd")
    m = _ORDINAL_RE.match(stripped)
    if m:
        n = int(m.group(1))
        if n < 1:
            return stripped  # leave nonsensical values as-is
        return f"{n}{_ordinal_suffix(n)}"

    # Unknown format — return as-is (title-cased for consistency)
    return stripped


def normalize_entry_edition(entry: dict) -> dict:
    """Return a copy of *entry* with the edition field normalized."""
    result = dict(entry)
    fields = dict(entry.get("fields", {}))
    if "edition" in fields:
        fields["edition"] = normalize_edition(fields["edition"])
    result["fields"] = fields
    return result


def normalize_bibliography_editions(entries: list[dict]) -> list[dict]:
    """Apply edition normalization to every entry in *entries*."""
    return [normalize_entry_edition(e) for e in entries]
