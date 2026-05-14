"""Normalize institution/organization field values in BibTeX entries."""

import re
from typing import Optional

# Map of known variants to canonical forms
_KNOWN_INSTITUTIONS: dict[str, str] = {
    "mit": "Massachusetts Institute of Technology",
    "massachusetts institute of technology": "Massachusetts Institute of Technology",
    "stanford": "Stanford University",
    "stanford university": "Stanford University",
    "cmu": "Carnegie Mellon University",
    "carnegie mellon": "Carnegie Mellon University",
    "carnegie mellon university": "Carnegie Mellon University",
    "eth zurich": "ETH Zurich",
    "eth zürich": "ETH Zurich",
    "eidgenössische technische hochschule zürich": "ETH Zurich",
    "berkeley": "University of California, Berkeley",
    "uc berkeley": "University of California, Berkeley",
    "university of california berkeley": "University of California, Berkeley",
    "oxford": "University of Oxford",
    "university of oxford": "University of Oxford",
    "cambridge": "University of Cambridge",
    "university of cambridge": "University of Cambridge",
}


def normalize_institution(value: Optional[str]) -> Optional[str]:
    """Return a canonical institution name, or a cleaned-up version if unknown."""
    if not value:
        return None
    # Strip surrounding braces and whitespace
    cleaned = value.strip().strip("{}").strip()
    # Collapse internal whitespace
    cleaned = re.sub(r"\s+", " ", cleaned)
    if not cleaned:
        return None
    lookup_key = cleaned.lower()
    if lookup_key in _KNOWN_INSTITUTIONS:
        return _KNOWN_INSTITUTIONS[lookup_key]
    # Title-case if all-uppercase, otherwise leave as-is
    if cleaned.isupper():
        return cleaned.title()
    return cleaned


def normalize_entry_institution(
    entry: dict,
    fields: tuple[str, ...] = ("institution", "organization", "school"),
) -> dict:
    """Return a copy of *entry* with institution-like fields normalized."""
    updated = dict(entry)
    fields_copy = dict(entry.get("fields", {}))
    for field in fields:
        if field in fields_copy:
            fields_copy[field] = normalize_institution(fields_copy[field])
    updated["fields"] = fields_copy
    return updated


def normalize_bibliography_institutions(
    bibliography: list[dict],
    fields: tuple[str, ...] = ("institution", "organization", "school"),
) -> list[dict]:
    """Return a new bibliography with institution fields normalized in every entry."""
    return [normalize_entry_institution(entry, fields) for entry in bibliography]
