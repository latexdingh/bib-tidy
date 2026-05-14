"""Normalize arXiv identifiers and related fields in BibTeX entries."""

import re
from typing import Optional

# Matches both old-style (e.g. math/0612345) and new-style (e.g. 2301.12345) arXiv IDs
_ARXIV_NEW = re.compile(r"(?:arxiv[:\s/]*)?(\d{4}\.\d{4,5}(?:v\d+)?)", re.IGNORECASE)
_ARXIV_OLD = re.compile(r"(?:arxiv[:\s/]*)?([a-z\-]+/\d{7}(?:v\d+)?)", re.IGNORECASE)
_ARXIV_URL = re.compile(
    r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/([^\s/?#]+)", re.IGNORECASE
)


def extract_arxiv_id(raw: str) -> Optional[str]:
    """Extract a canonical arXiv ID from a raw string (field value or URL)."""
    if not raw:
        return None
    m = _ARXIV_URL.search(raw)
    if m:
        return m.group(1).rstrip("/")
    m = _ARXIV_NEW.search(raw)
    if m:
        return m.group(1)
    m = _ARXIV_OLD.search(raw)
    if m:
        return m.group(1).lower()
    return None


def normalize_arxiv(raw: Optional[str]) -> Optional[str]:
    """Return a normalized arXiv ID (bare identifier, no prefix/URL)."""
    if not raw:
        return None
    arxiv_id = extract_arxiv_id(raw)
    return arxiv_id


def normalize_entry_arxiv(entry: dict) -> dict:
    """Normalize the *eprint* / *arxivid* / *arxiv* field of a single entry.

    Looks for an arXiv ID in the following fields (in order):
    ``eprint``, ``arxivid``, ``arxiv``, ``url``.
    Writes the canonical bare ID back to ``eprint`` and sets
    ``archiveprefix = arXiv`` and ``primaryclass`` if determinable.
    """
    fields = entry.get("fields", {})

    raw = (
        fields.get("eprint")
        or fields.get("arxivid")
        or fields.get("arxiv")
        or fields.get("url")
    )
    arxiv_id = normalize_arxiv(raw) if raw else None

    if arxiv_id is None:
        return entry

    new_fields = dict(fields)
    new_fields["eprint"] = arxiv_id
    new_fields["archiveprefix"] = "arXiv"
    # Remove redundant aliases
    new_fields.pop("arxivid", None)
    new_fields.pop("arxiv", None)

    return {**entry, "fields": new_fields}


def normalize_bibliography_arxiv(entries: list[dict]) -> list[dict]:
    """Apply arXiv normalization to every entry in a bibliography."""
    return [normalize_entry_arxiv(e) for e in entries]
