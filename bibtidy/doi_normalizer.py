"""Normalize DOI fields to a canonical bare form (without resolver prefix)."""

import re
from typing import Optional

# Patterns for various DOI representations
_DOI_URL_PREFIXES = (
    "https://doi.org/",
    "http://doi.org/",
    "https://dx.doi.org/",
    "http://dx.doi.org/",
    "doi.org/",
    "dx.doi.org/",
)
_DOI_PREFIX_RE = re.compile(r"^doi:\s*", re.IGNORECASE)
_DOI_PATTERN = re.compile(r"10\.\d{4,9}/\S+")


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    """Return a bare DOI (e.g. ``10.1234/foo``) from various representations.

    Handles:
    - Already bare DOIs
    - ``doi:10.xxx/yyy`` prefix
    - Full resolver URLs (https://doi.org/…, http://dx.doi.org/…, etc.)
    - Surrounding whitespace and trailing punctuation (period, comma)

    Returns *None* for *None* or empty input, and for strings that do not
    contain a recognisable DOI.
    """
    if not doi:
        return None

    value = doi.strip()

    # Strip resolver URL prefix
    for prefix in _DOI_URL_PREFIXES:
        if value.lower().startswith(prefix.lower()):
            value = value[len(prefix):]
            break
    else:
        # Strip "doi:" textual prefix
        value = _DOI_PREFIX_RE.sub("", value)

    # Remove surrounding braces or quotes
    value = value.strip("{}\'\"")

    # Strip trailing punctuation that is clearly not part of the DOI
    value = value.rstrip(".,;")

    # Validate that we have something that looks like a real DOI
    if not _DOI_PATTERN.match(value):
        # Try to extract a DOI from anywhere in the string
        match = _DOI_PATTERN.search(value)
        if match:
            value = match.group(0).rstrip(".,;")
        else:
            return None

    return value


def normalize_entry_doi(entry: dict) -> dict:
    """Return a copy of *entry* with the ``doi`` field normalised."""
    raw = entry.get("doi")
    normalised = normalize_doi(raw)
    fields = dict(entry.get("fields", {}))
    if normalised is not None:
        fields["doi"] = normalised
    elif "doi" in fields:
        del fields["doi"]
    return {**entry, "fields": fields}


def normalize_bibliography_dois(bibliography: list) -> list:
    """Return a new bibliography with every entry's DOI normalised."""
    return [normalize_entry_doi(e) for e in bibliography]
