"""
Normalizes BibTeX month fields to a consistent abbreviated format.

Accepts full month names, abbreviations, numeric strings, and integers.
Outputs three-letter lowercase abbreviations (e.g., 'jan', 'feb', ...).
"""

import re
from typing import Optional

_MONTH_MAP: dict[str, str] = {
    # Full names
    "january": "jan", "february": "feb", "march": "mar",
    "april": "apr", "may": "may", "june": "jun",
    "july": "jul", "august": "aug", "september": "sep",
    "october": "oct", "november": "nov", "december": "dec",
    # Three-letter abbreviations
    "jan": "jan", "feb": "feb", "mar": "mar",
    "apr": "apr", "jun": "jun", "jul": "jul",
    "aug": "aug", "sep": "sep", "oct": "oct",
    "nov": "nov", "dec": "dec",
    # Numeric strings
    "1": "jan", "2": "feb", "3": "mar",
    "4": "apr", "5": "may", "6": "jun",
    "7": "jul", "8": "aug", "9": "sep",
    "10": "oct", "11": "nov", "12": "dec",
}


def normalize_month(raw: str) -> Optional[str]:
    """Return a normalized three-letter month abbreviation or None if unrecognized."""
    cleaned = raw.strip().lower()
    # Strip surrounding braces or quotes that BibTeX parsers may leave
    cleaned = re.sub(r'^[{"]+|[}"]+$', '', cleaned).strip()
    return _MONTH_MAP.get(cleaned)


def normalize_entry_month(entry: dict) -> dict:
    """
    Normalize the 'month' field of a single BibTeX entry dict.

    The entry dict is expected to have a 'fields' key mapping field names to values.
    Returns a new entry dict with the month field normalized (or unchanged if
    the value is unrecognized or absent).
    """
    fields: dict = dict(entry.get("fields", {}))
    raw_month = fields.get("month")
    if raw_month is not None:
        normalized = normalize_month(str(raw_month))
        if normalized is not None:
            fields["month"] = normalized
    return {**entry, "fields": fields}


def normalize_bibliography_months(entries: list[dict]) -> list[dict]:
    """Apply month normalization to every entry in a bibliography list."""
    return [normalize_entry_month(e) for e in entries]
