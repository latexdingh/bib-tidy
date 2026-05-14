"""
Normalizes the `address` field in BibTeX entries.

Applies consistent city/country formatting: strips extra whitespace,
expands common abbreviations (e.g. "NY" -> "New York"), and ensures
"City, Country" structure where detectable.
"""

import re
from typing import Optional

# Map of common abbreviations to canonical forms
_CITY_ALIASES: dict[str, str] = {
    "ny": "New York, NY",
    "new york": "New York, NY",
    "nyc": "New York, NY",
    "la": "Los Angeles, CA",
    "los angeles": "Los Angeles, CA",
    "sf": "San Francisco, CA",
    "san francisco": "San Francisco, CA",
    "dc": "Washington, DC",
    "washington dc": "Washington, DC",
    "washington, dc": "Washington, DC",
    "cambridge, ma": "Cambridge, MA",
    "cambridge, uk": "Cambridge, UK",
    "london": "London, UK",
    "berlin": "Berlin, Germany",
    "paris": "Paris, France",
    "tokyo": "Tokyo, Japan",
    "beijing": "Beijing, China",
    "sydney": "Sydney, Australia",
    "toronto": "Toronto, Canada",
}


def normalize_address(address: Optional[str]) -> Optional[str]:
    """Return a normalized address string, or None if input is None/empty."""
    if not address:
        return None
    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", address.strip())
    # Remove surrounding braces if present
    normalized = normalized.strip("{}").strip()
    # Lookup alias (case-insensitive)
    key = normalized.lower()
    if key in _CITY_ALIASES:
        return _CITY_ALIASES[key]
    return normalized


def normalize_entry_address(entry: dict) -> dict:
    """Return a copy of *entry* with the `address` field normalized."""
    if "address" not in entry.get("fields", {}):
        return entry
    new_fields = dict(entry["fields"])
    new_fields["address"] = normalize_address(new_fields["address"])
    if new_fields["address"] is None:
        del new_fields["address"]
    return {**entry, "fields": new_fields}


def normalize_bibliography_addresses(bibliography: list[dict]) -> list[dict]:
    """Apply address normalization to every entry in *bibliography*."""
    return [normalize_entry_address(e) for e in bibliography]
