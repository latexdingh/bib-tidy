"""Deduplication logic for BibTeX entries."""

from typing import Optional
from difflib import SequenceMatcher


def _normalize_title(title: str) -> str:
    """Lowercase and strip punctuation for comparison."""
    import re
    return re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()


def _title_similarity(a: str, b: str) -> float:
    """Return similarity ratio between two titles."""
    return SequenceMatcher(None, _normalize_title(a), _normalize_title(b)).ratio()


def _same_doi(entry_a: dict, entry_b: dict) -> bool:
    """Return True if both entries share the same non-empty DOI."""
    doi_a = entry_a.get('fields', {}).get('doi', '').strip().lower()
    doi_b = entry_b.get('fields', {}).get('doi', '').strip().lower()
    return bool(doi_a) and doi_a == doi_b


def are_duplicates(
    entry_a: dict,
    entry_b: dict,
    title_threshold: float = 0.85,
) -> bool:
    """Determine if two parsed BibTeX entries are duplicates.

    Two entries are considered duplicates if:
    - They share the same DOI, OR
    - Their titles are sufficiently similar AND they share the same year.
    """
    if _same_doi(entry_a, entry_b):
        return True

    fields_a = entry_a.get('fields', {})
    fields_b = entry_b.get('fields', {})

    title_a = fields_a.get('title', '')
    title_b = fields_b.get('title', '')
    if not title_a or not title_b:
        return False

    year_a = fields_a.get('year', '').strip()
    year_b = fields_b.get('year', '').strip()
    if year_a and year_b and year_a != year_b:
        return False

    return _title_similarity(title_a, title_b) >= title_threshold


def _preferred_entry(entry_a: dict, entry_b: dict) -> dict:
    """Return the entry with more fields (richer metadata)."""
    if len(entry_a.get('fields', {})) >= len(entry_b.get('fields', {})):
        return entry_a
    return entry_b


def deduplicate(entries: list[dict], title_threshold: float = 0.85) -> list[dict]:
    """Remove duplicate entries, keeping the richest version of each.

    Args:
        entries: List of parsed BibTeX entry dicts.
        title_threshold: Minimum title similarity to consider entries duplicates.

    Returns:
        Deduplicated list of entries.
    """
    kept: list[dict] = []
    for candidate in entries:
        duplicate_found = False
        for i, existing in enumerate(kept):
            if are_duplicates(candidate, existing, title_threshold):
                kept[i] = _preferred_entry(candidate, existing)
                duplicate_found = True
                break
        if not duplicate_found:
            kept.append(candidate)
    return kept
