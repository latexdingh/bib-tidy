"""
Normalise journal names: expand known abbreviations to full names,
strip extra whitespace and braces, and title-case the result.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

# Canonical full name -> list of known abbreviations / variants
_JOURNAL_ALIASES: Dict[str, List[str]] = {
    "Nature": ["nat", "nature"],
    "Science": ["sci", "science"],
    "Physical Review Letters": ["prl", "phys. rev. lett.", "phys rev lett"],
    "Physical Review B": ["prb", "phys. rev. b", "phys rev b"],
    "Journal of Chemical Physics": ["j. chem. phys.", "j chem phys", "jcp"],
    "Journal of the American Chemical Society": [
        "j. am. chem. soc.",
        "j am chem soc",
        "jacs",
    ],
    "Proceedings of the National Academy of Sciences": [
        "pnas",
        "proc. natl. acad. sci.",
        "proc natl acad sci",
    ],
    "IEEE Transactions on Neural Networks and Learning Systems": [
        "ieee trans. neural netw. learn. syst.",
        "tnnls",
    ],
    "Artificial Intelligence": ["artif. intell.", "artif intell"],
    "Machine Learning": ["mach. learn.", "mach learn"],
}

# Build reverse lookup: normalised variant -> canonical name
_LOOKUP: Dict[str, str] = {}
for _canonical, _variants in _JOURNAL_ALIASES.items():
    _LOOKUP[_canonical.lower()] = _canonical
    for _v in _variants:
        _LOOKUP[_v.lower()] = _canonical


def _strip_braces(value: str) -> str:
    return value.strip("{} ")


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_journal(journal: Optional[str]) -> Optional[str]:
    """Return the canonical journal name, or the cleaned original if unknown."""
    if not journal:
        return None
    cleaned = _collapse_whitespace(_strip_braces(journal))
    if not cleaned:
        return None
    canonical = _LOOKUP.get(cleaned.lower())
    return canonical if canonical is not None else cleaned


def normalize_entry_journal(entry: dict) -> dict:
    """Return a copy of *entry* with the journal field normalised."""
    journal = entry.get("fields", {}).get("journal")
    normalised = normalize_journal(journal)
    new_fields = dict(entry.get("fields", {}))
    if normalised is not None:
        new_fields["journal"] = normalised
    elif "journal" in new_fields:
        del new_fields["journal"]
    return {**entry, "fields": new_fields}


def normalize_bibliography_journals(entries: List[dict]) -> List[dict]:
    """Return a new list with journal fields normalised in every entry."""
    return [normalize_entry_journal(e) for e in entries]
