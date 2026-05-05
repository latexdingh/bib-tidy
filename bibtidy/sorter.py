"""Sorting utilities for BibTeX bibliography entries."""

from typing import List, Dict, Any, Optional

SORT_FIELDS = ["year", "author", "title", "key", "entrytype"]


def _get_sort_key_for_field(entry: Dict[str, Any], field: str) -> str:
    """Extract a normalized sort key from an entry for a given field."""
    if field == "key":
        return (entry.get("key") or "").lower()
    if field == "entrytype":
        return (entry.get("entrytype") or "").lower()
    value = entry.get("fields", {}).get(field, "")
    if field == "year":
        # Pad year for correct numeric sorting
        try:
            return str(int(value)).zfill(4)
        except (ValueError, TypeError):
            return "0000"
    if field == "author":
        # Sort by first author last name
        first = value.split(" and ")[0].strip()
        if "," in first:
            return first.split(",")[0].strip().lower()
        parts = first.split()
        return parts[-1].lower() if parts else ""
    return value.lower()


def sort_entries(
    entries: List[Dict[str, Any]],
    fields: Optional[List[str]] = None,
    reverse: bool = False,
) -> List[Dict[str, Any]]:
    """Sort a list of BibTeX entries by one or more fields.

    Args:
        entries: List of parsed BibTeX entry dicts.
        fields: Ordered list of fields to sort by. Defaults to ['year', 'author'].
        reverse: If True, sort in descending order.

    Returns:
        New sorted list of entries.
    """
    if fields is None:
        fields = ["year", "author"]

    invalid = [f for f in fields if f not in SORT_FIELDS]
    if invalid:
        raise ValueError(f"Invalid sort field(s): {invalid}. Valid: {SORT_FIELDS}")

    def composite_key(entry: Dict[str, Any]):
        return tuple(_get_sort_key_for_field(entry, f) for f in fields)

    return sorted(entries, key=composite_key, reverse=reverse)
