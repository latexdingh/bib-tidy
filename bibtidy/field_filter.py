"""Field filtering and allowlist/blocklist utilities for BibTeX entries."""

from typing import List, Dict, Any, Optional

# Fields commonly kept for clean bibliographies
DEFAULT_KEEP_FIELDS = [
    "title", "author", "year", "journal", "booktitle",
    "volume", "number", "pages", "publisher", "doi",
    "url", "editor", "edition", "series", "address",
    "month", "note", "school", "institution", "howpublished",
]


def filter_fields(
    entry: Dict[str, Any],
    keep: Optional[List[str]] = None,
    drop: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Return a copy of entry with fields filtered.

    If `keep` is provided, only those fields are retained.
    If `drop` is provided, those fields are removed.
    `keep` takes precedence over `drop`.

    Args:
        entry: Parsed BibTeX entry dict.
        keep: Whitelist of field names to keep.
        drop: Blacklist of field names to remove.

    Returns:
        New entry dict with filtered fields.
    """
    fields = dict(entry.get("fields", {}))

    if keep is not None:
        keep_lower = {f.lower() for f in keep}
        fields = {k: v for k, v in fields.items() if k.lower() in keep_lower}
    elif drop is not None:
        drop_lower = {f.lower() for f in drop}
        fields = {k: v for k, v in fields.items() if k.lower() not in drop_lower}

    return {**entry, "fields": fields}


def filter_bibliography(
    entries: List[Dict[str, Any]],
    keep: Optional[List[str]] = None,
    drop: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Apply field filtering to every entry in a bibliography."""
    return [filter_fields(e, keep=keep, drop=drop) for e in entries]
