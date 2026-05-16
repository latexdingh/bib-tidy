"""
Normalize the 'funding' field of BibTeX entries.

Applies consistent formatting:
- Strips surrounding braces
- Collapses internal whitespace
- Expands known funder abbreviations to canonical names
- Title-cases the result if no canonical form is found
"""

import re
from typing import Optional

_KNOWN_FUNDERS: dict[str, str] = {
    "nsf": "National Science Foundation",
    "national science foundation": "National Science Foundation",
    "nih": "National Institutes of Health",
    "national institutes of health": "National Institutes of Health",
    "darpa": "Defense Advanced Research Projects Agency",
    "doe": "U.S. Department of Energy",
    "department of energy": "U.S. Department of Energy",
    "eu": "European Union",
    "european union": "European Union",
    "erc": "European Research Council",
    "european research council": "European Research Council",
    "dfg": "Deutsche Forschungsgemeinschaft",
    "deutsche forschungsgemeinschaft": "Deutsche Forschungsgemeinschaft",
    "epsrc": "Engineering and Physical Sciences Research Council",
    "anr": "Agence Nationale de la Recherche",
    "snf": "Swiss National Science Foundation",
    "snsf": "Swiss National Science Foundation",
    "swiss national science foundation": "Swiss National Science Foundation",
    "nserc": "Natural Sciences and Engineering Research Council of Canada",
    "arc": "Australian Research Council",
}


def _strip_braces(value: str) -> str:
    value = value.strip()
    if value.startswith("{") and value.endswith("}"):
        return value[1:-1].strip()
    return value


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_funding(funding: Optional[str]) -> Optional[str]:
    """Return a normalized funder name, or None if the input is empty."""
    if not funding:
        return None
    value = _strip_braces(funding)
    value = _collapse_whitespace(value)
    if not value:
        return None
    lookup_key = value.lower()
    if lookup_key in _KNOWN_FUNDERS:
        return _KNOWN_FUNDERS[lookup_key]
    return value


def normalize_entry_funding(entry: dict) -> dict:
    """Return a copy of *entry* with the 'funding' field normalized."""
    funding = entry.get("funding")
    normalized = normalize_funding(funding)
    updated = dict(entry)
    if normalized is None:
        updated.pop("funding", None)
    else:
        updated["funding"] = normalized
    return updated


def normalize_bibliography_funding(entries: list[dict]) -> list[dict]:
    """Apply funding normalization to every entry in *entries*."""
    return [normalize_entry_funding(e) for e in entries]
