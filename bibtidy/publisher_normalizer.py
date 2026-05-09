"""
Normalize publisher and address fields in BibTeX entries.

Handles common publisher name variations, strips redundant suffixes
(e.g. 'Inc.', 'Ltd.', 'LLC'), and standardizes well-known publisher names.
"""

import re
from typing import Optional

# Map of known publisher name variants to canonical forms
PUBLISHER_ALIASES: dict[str, str] = {
    "springer-verlag": "Springer",
    "springer verlag": "Springer",
    "springer science & business media": "Springer",
    "springer science+business media": "Springer",
    "ieee computer society": "IEEE",
    "institute of electrical and electronics engineers": "IEEE",
    "acm press": "ACM",
    "association for computing machinery": "ACM",
    "elsevier science": "Elsevier",
    "elsevier b.v.": "Elsevier",
    "elsevier bv": "Elsevier",
    "mit press": "MIT Press",
    "the mit press": "MIT Press",
    "oxford university press": "Oxford University Press",
    "cambridge university press": "Cambridge University Press",
    "john wiley & sons": "Wiley",
    "john wiley and sons": "Wiley",
    "wiley-blackwell": "Wiley",
    "wiley-interscience": "Wiley",
    "taylor & francis": "Taylor & Francis",
    "taylor and francis": "Taylor & Francis",
}

_STRIP_SUFFIXES = re.compile(
    r",?\s*(Inc\.?|Ltd\.?|LLC\.?|GmbH|Corp\.?|Co\.?)\s*$",
    re.IGNORECASE,
)


def normalize_publisher(name: Optional[str]) -> Optional[str]:
    """Return a canonical publisher name, or None if input is None/empty."""
    if not name or not name.strip():
        return None

    cleaned = name.strip()
    # Strip corporate suffixes
    cleaned = _STRIP_SUFFIXES.sub("", cleaned).strip()

    lookup = cleaned.lower()
    if lookup in PUBLISHER_ALIASES:
        return PUBLISHER_ALIASES[lookup]

    return cleaned


def normalize_entry_publisher(
    entry: dict,
    fields: tuple[str, ...] = ("publisher", "organization", "institution"),
) -> dict:
    """Normalize publisher-related fields in a single entry dict."""
    result = dict(entry)
    for field in fields:
        if field in result:
            normalized = normalize_publisher(result[field])
            if normalized is None:
                result.pop(field)
            else:
                result[field] = normalized
    return result


def normalize_bibliography_publishers(bibliography: list[dict], **kwargs) -> list[dict]:
    """Apply publisher normalization to every entry in a bibliography."""
    return [normalize_entry_publisher(entry, **kwargs) for entry in bibliography]
