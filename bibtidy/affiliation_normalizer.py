"""
Normalize author affiliation fields in BibTeX entries.

Handles common variants, abbreviations, and formatting inconsistencies.
"""

import re
from typing import Optional

# Map of known affiliation variants to canonical forms
_CANONICAL: dict[str, str] = {
    "mit": "Massachusetts Institute of Technology",
    "massachusetts institute of technology": "Massachusetts Institute of Technology",
    "stanford": "Stanford University",
    "stanford univ": "Stanford University",
    "stanford univ.": "Stanford University",
    "cmu": "Carnegie Mellon University",
    "carnegie mellon": "Carnegie Mellon University",
    "carnegie mellon univ": "Carnegie Mellon University",
    "carnegie mellon univ.": "Carnegie Mellon University",
    "eth zurich": "ETH Zurich",
    "eth zürich": "ETH Zurich",
    "eidgenössische technische hochschule zürich": "ETH Zurich",
    "epfl": "École Polytechnique Fédérale de Lausanne",
    "ucb": "University of California, Berkeley",
    "uc berkeley": "University of California, Berkeley",
    "university of california berkeley": "University of California, Berkeley",
    "ucla": "University of California, Los Angeles",
    "uc los angeles": "University of California, Los Angeles",
    "oxford": "University of Oxford",
    "cambridge": "University of Cambridge",
    "imperial college": "Imperial College London",
    "imperial college london": "Imperial College London",
}


def _strip_braces(value: str) -> str:
    """Remove surrounding LaTeX braces."""
    return re.sub(r'^\{(.*)\}$', r'\1', value.strip())


def _collapse_whitespace(value: str) -> str:
    """Collapse multiple whitespace characters into a single space."""
    return re.sub(r'\s+', ' ', value).strip()


def normalize_affiliation(affiliation: Optional[str]) -> Optional[str]:
    """Normalize a single affiliation string.

    Returns the canonical form if known, otherwise returns a cleaned version.
    Returns None for empty or None input.
    """
    if not affiliation:
        return None
    cleaned = _collapse_whitespace(_strip_braces(affiliation))
    if not cleaned:
        return None
    lookup = cleaned.lower().rstrip('.')
    canonical = _CANONICAL.get(lookup)
    if canonical:
        return canonical
    return cleaned


def normalize_entry_affiliation(
    entry: dict,
    field: str = "affiliation",
) -> dict:
    """Return a copy of *entry* with the affiliation field normalized."""
    value = entry.get(field)
    normalized = normalize_affiliation(value)
    result = dict(entry)
    if normalized is None:
        result.pop(field, None)
    else:
        result[field] = normalized
    return result


def normalize_bibliography_affiliations(
    bibliography: list[dict],
    field: str = "affiliation",
) -> list[dict]:
    """Normalize affiliation fields across an entire bibliography."""
    return [normalize_entry_affiliation(entry, field=field) for entry in bibliography]
