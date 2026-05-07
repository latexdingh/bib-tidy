"""
Normalize author/editor name fields in BibTeX entries.

Converts names to a consistent 'Last, First' format and handles
name list separators (" and ").
"""

import re
from typing import Optional

_NAME_FIELDS = ("author", "editor")


def _normalize_single_name(name: str) -> str:
    """Normalize a single personal name to 'Last, First' format."""
    name = name.strip()
    if not name:
        return name

    # Already in 'Last, First' format
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        return f"{parts[0]}, {parts[1]}" if len(parts) == 2 else name

    # Natural order: 'First [Middle] Last'
    tokens = name.split()
    if len(tokens) == 1:
        return name
    last = tokens[-1]
    first = " ".join(tokens[:-1])
    return f"{last}, {first}"


def normalize_name_list(name_list: str) -> str:
    """Normalize a BibTeX name list (names separated by ' and ')."""
    # Split on " and " (case-insensitive)
    names = re.split(r"\s+and\s+", name_list, flags=re.IGNORECASE)
    normalized = [_normalize_single_name(n) for n in names]
    return " and ".join(normalized)


def normalize_entry_names(
    entry: dict,
    fields: Optional[tuple] = None,
) -> dict:
    """Return a copy of *entry* with name fields normalized."""
    if fields is None:
        fields = _NAME_FIELDS
    result = dict(entry)
    for field in fields:
        if field in result and result[field]:
            result[field] = normalize_name_list(result[field])
    return result


def normalize_bibliography_names(
    bibliography: list,
    fields: Optional[tuple] = None,
) -> list:
    """Normalize name fields in every entry of *bibliography*."""
    return [normalize_entry_names(entry, fields) for entry in bibliography]
