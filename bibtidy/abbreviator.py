"""Journal name abbreviation module for bib-tidy.

Provides lookup and application of standard journal name abbreviations
based on a configurable abbreviation map.
"""

import re
from typing import Optional

# Common journal abbreviations (full name -> abbreviated name)
DEFAULT_ABBREVIATIONS: dict[str, str] = {
    "Nature": "Nature",
    "Science": "Science",
    "Physical Review Letters": "Phys. Rev. Lett.",
    "Physical Review B": "Phys. Rev. B",
    "Physical Review E": "Phys. Rev. E",
    "Journal of Chemical Physics": "J. Chem. Phys.",
    "Journal of the American Chemical Society": "J. Am. Chem. Soc.",
    "Angewandte Chemie International Edition": "Angew. Chem. Int. Ed.",
    "Proceedings of the National Academy of Sciences": "Proc. Natl. Acad. Sci.",
    "Nature Communications": "Nat. Commun.",
    "Nature Chemistry": "Nat. Chem.",
    "Nature Physics": "Nat. Phys.",
    "New Journal of Physics": "New J. Phys.",
    "Journal of Physics: Condensed Matter": "J. Phys.: Condens. Matter",
    "Reviews of Modern Physics": "Rev. Mod. Phys.",
    "Computational Materials Science": "Comput. Mater. Sci.",
    "Chemical Physics Letters": "Chem. Phys. Lett.",
}


def _normalize_for_lookup(name: str) -> str:
    """Normalize a journal name for case-insensitive lookup."""
    return re.sub(r"\s+", " ", name.strip().lower())


def _build_lookup(abbreviations: dict[str, str]) -> dict[str, str]:
    """Build a normalized lookup dict from an abbreviation map."""
    return {_normalize_for_lookup(k): v for k, v in abbreviations.items()}


def abbreviate_journal(
    name: str,
    abbreviations: Optional[dict[str, str]] = None,
) -> str:
    """Return the abbreviated form of a journal name, or the original if unknown."""
    abbrev_map = abbreviations if abbreviations is not None else DEFAULT_ABBREVIATIONS
    lookup = _build_lookup(abbrev_map)
    key = _normalize_for_lookup(name)
    return lookup.get(key, name)


def abbreviate_entry(
    entry: dict,
    abbreviations: Optional[dict[str, str]] = None,
    field: str = "journal",
) -> dict:
    """Return a copy of entry with the journal field abbreviated if present."""
    result = dict(entry)
    fields = dict(entry.get("fields", {}))
    if field in fields:
        fields[field] = abbreviate_journal(fields[field], abbreviations)
    result["fields"] = fields
    return result


def abbreviate_bibliography(
    entries: list[dict],
    abbreviations: Optional[dict[str, str]] = None,
    field: str = "journal",
) -> list[dict]:
    """Apply journal abbreviation to all entries in a bibliography."""
    return [abbreviate_entry(e, abbreviations, field) for e in entries]
