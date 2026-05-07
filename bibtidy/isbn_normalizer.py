"""
ISBN normalization for BibTeX entries.

Normalizes ISBN-10 and ISBN-13 fields: strips hyphens/spaces,
validates check digits, and converts ISBN-10 to ISBN-13 where possible.
"""

import re
from typing import Optional


def _strip_isbn(raw: str) -> str:
    """Remove hyphens and spaces from an ISBN string."""
    return re.sub(r'[\s\-]', '', raw.strip())


def _isbn10_check(digits: str) -> bool:
    """Return True if the 10-character string is a valid ISBN-10."""
    if len(digits) != 10:
        return False
    total = 0
    for i, ch in enumerate(digits):
        if i == 9 and ch in ('X', 'x'):
            val = 10
        elif ch.isdigit():
            val = int(ch)
        else:
            return False
        total += val * (10 - i)
    return total % 11 == 0


def _isbn13_check(digits: str) -> bool:
    """Return True if the 13-character string is a valid ISBN-13."""
    if len(digits) != 13 or not digits.isdigit():
        return False
    total = sum(
        int(d) * (1 if i % 2 == 0 else 3)
        for i, d in enumerate(digits)
    )
    return total % 10 == 0


def _isbn10_to_isbn13(digits: str) -> Optional[str]:
    """Convert a valid ISBN-10 to ISBN-13 format."""
    body = '978' + digits[:9]
    check = (10 - sum(
        int(d) * (1 if i % 2 == 0 else 3)
        for i, d in enumerate(body)
    ) % 10) % 10
    return body + str(check)


def normalize_isbn(raw: str) -> Optional[str]:
    """
    Normalize an ISBN string.

    Returns the canonical ISBN-13 (digits only) if valid,
    or None if the value cannot be recognized as a valid ISBN.
    """
    cleaned = _strip_isbn(raw)
    if _isbn13_check(cleaned):
        return cleaned
    if _isbn10_check(cleaned):
        return _isbn10_to_isbn13(cleaned)
    return None


def normalize_entry_isbn(entry: dict) -> dict:
    """Normalize the 'isbn' field of a single BibTeX entry dict."""
    entry = dict(entry)
    fields = dict(entry.get('fields', {}))
    raw = fields.get('isbn', '')
    if raw:
        normalized = normalize_isbn(raw)
        if normalized:
            fields['isbn'] = normalized
    entry['fields'] = fields
    return entry


def normalize_bibliography_isbns(entries: list) -> list:
    """Apply ISBN normalization to every entry in a bibliography list."""
    return [normalize_entry_isbn(e) for e in entries]
