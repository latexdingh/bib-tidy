"""
year_normalizer.py — Normalize and validate year fields in BibTeX entries.

Handles common year formats: plain integers, ranges, approximate years,
and extracts a canonical 4-digit year where possible.
"""

import re
from typing import Optional

# Matches a 4-digit year between 1000 and 2099
_YEAR_RE = re.compile(r'\b(1[0-9]{3}|20[0-9]{2})\b')


def extract_year(raw: str) -> Optional[str]:
    """Extract the first plausible 4-digit year from a raw string.

    Returns the year as a string, or None if no valid year is found.

    >>> extract_year('2021')
    '2021'
    >>> extract_year('2019-2020')
    '2019'
    >>> extract_year('circa 1998')
    '1998'
    >>> extract_year('no year here') is None
    True
    """
    if not raw:
        return None
    match = _YEAR_RE.search(raw.strip())
    return match.group(1) if match else None


def normalize_year(raw: str) -> str:
    """Return a normalized year string.

    If a 4-digit year can be extracted, return it.  Otherwise return the
    original value stripped of surrounding whitespace so we don't silently
    discard unusual but intentional values (e.g. 'in press').
    """
    if not raw:
        return raw
    extracted = extract_year(raw)
    return extracted if extracted is not None else raw.strip()


def normalize_entry_year(entry: dict) -> dict:
    """Return a copy of *entry* with its 'year' field normalized.

    If the entry has no 'year' field it is returned unchanged.
    """
    fields = dict(entry.get('fields', {}))
    if 'year' in fields:
        fields['year'] = normalize_year(fields['year'])
    return {**entry, 'fields': fields}


def normalize_bibliography_years(entries: list) -> list:
    """Apply :func:`normalize_entry_year` to every entry in *entries*."""
    return [normalize_entry_year(e) for e in entries]
