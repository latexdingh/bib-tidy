"""Resolve BibTeX @string macros via crossref inheritance.

When an entry contains a ``crossref`` field pointing to another entry,
this module merges the parent's fields into the child (child fields win).
"""

from typing import Dict, List, Optional


def _build_index(entries: List[Dict]) -> Dict[str, Dict]:
    """Build a citation-key -> entry lookup table."""
    return {e["key"]: e for e in entries if "key" in e}


def resolve_crossref(
    entry: Dict, index: Dict[str, Dict], max_depth: int = 5
) -> Dict:
    """Return *entry* with fields inherited from its crossref parent.

    Inheritance is non-destructive: existing child fields are preserved.
    Chains up to *max_depth* levels deep are followed.
    """
    if max_depth <= 0:
        return entry

    parent_key: Optional[str] = entry.get("fields", {}).get("crossref")
    if not parent_key:
        return entry

    parent = index.get(parent_key)
    if parent is None:
        return entry

    # Recursively resolve the parent first
    resolved_parent = resolve_crossref(parent, index, max_depth - 1)

    merged_fields = dict(resolved_parent.get("fields", {}))
    merged_fields.update(entry.get("fields", {}))

    result = dict(entry)
    result["fields"] = merged_fields
    return result


def resolve_all_crossrefs(
    entries: List[Dict], max_depth: int = 5
) -> List[Dict]:
    """Apply crossref resolution to every entry in *entries*."""
    index = _build_index(entries)
    return [resolve_crossref(e, index, max_depth) for e in entries]
