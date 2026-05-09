"""
Normalizes BibTeX entry types to canonical lowercase forms and maps
common aliases to their standard equivalents.
"""

from typing import Optional

# Maps known aliases/variants to canonical BibTeX entry types
_TYPE_ALIASES: dict[str, str] = {
    "article": "article",
    "journal": "article",
    "journalarticle": "article",
    "book": "book",
    "textbook": "book",
    "bookchapter": "inbook",
    "inbook": "inbook",
    "incollection": "incollection",
    "chapter": "incollection",
    "inproceedings": "inproceedings",
    "conference": "inproceedings",
    "confpaper": "inproceedings",
    "proceedings": "proceedings",
    "phdthesis": "phdthesis",
    "phd": "phdthesis",
    "mastersthesis": "mastersthesis",
    "masters": "mastersthesis",
    "mscthesis": "mastersthesis",
    "techreport": "techreport",
    "report": "techreport",
    "misc": "misc",
    "online": "misc",
    "electronic": "misc",
    "unpublished": "unpublished",
    "preprint": "unpublished",
    "manual": "manual",
    "booklet": "booklet",
}


def normalize_type(entry_type: Optional[str]) -> Optional[str]:
    """
    Normalize a BibTeX entry type string.

    Returns the canonical type string if recognized, otherwise returns
    the input lowercased. Returns None if input is None or empty.
    """
    if not entry_type or not entry_type.strip():
        return None
    key = entry_type.strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    return _TYPE_ALIASES.get(key, entry_type.strip().lower())


def normalize_entry_type(entry: dict) -> dict:
    """Return a copy of entry with its 'type' field normalized."""
    result = dict(entry)
    result["type"] = normalize_type(entry.get("type"))
    return result


def normalize_bibliography_types(bibliography: list[dict]) -> list[dict]:
    """Normalize entry types for every entry in a bibliography list."""
    return [normalize_entry_type(e) for e in bibliography]
