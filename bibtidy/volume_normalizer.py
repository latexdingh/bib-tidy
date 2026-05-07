"""Normalize volume and number/issue fields in BibTeX entries."""

import re
from typing import Optional


def normalize_volume(value: str) -> Optional[str]:
    """Extract and normalize a volume string.

    Strips non-numeric prefixes/suffixes such as 'vol.', 'volume', etc.,
    and returns only the numeric (or alphanumeric) core.

    Returns None if no usable value can be extracted.
    """
    if not value or not value.strip():
        return None
    cleaned = value.strip()
    # Remove common textual prefixes
    cleaned = re.sub(
        r'^(?:vol(?:ume)?[.:]?\s*)', '', cleaned, flags=re.IGNORECASE
    )
    cleaned = cleaned.strip().rstrip('.')
    if not cleaned:
        return None
    return cleaned


def normalize_number(value: str) -> Optional[str]:
    """Extract and normalize an issue/number string.

    Strips textual prefixes such as 'no.', 'number', 'issue', etc.
    Returns None if no usable value can be extracted.
    """
    if not value or not value.strip():
        return None
    cleaned = value.strip()
    cleaned = re.sub(
        r'^(?:(?:no|num|number|issue)[.:]?\s*)', '', cleaned, flags=re.IGNORECASE
    )
    cleaned = cleaned.strip().rstrip('.')
    if not cleaned:
        return None
    return cleaned


def normalize_entry_volume(
    entry: dict,
    volume_field: str = 'volume',
    number_field: str = 'number',
) -> dict:
    """Return a copy of *entry* with normalized volume and number fields."""
    result = dict(entry)
    fields: dict = dict(result.get('fields', {}))

    if volume_field in fields:
        normalized = normalize_volume(fields[volume_field])
        if normalized is not None:
            fields[volume_field] = normalized
        else:
            del fields[volume_field]

    if number_field in fields:
        normalized = normalize_number(fields[number_field])
        if normalized is not None:
            fields[number_field] = normalized
        else:
            del fields[number_field]

    result['fields'] = fields
    return result


def normalize_bibliography_volumes(bibliography: list[dict]) -> list[dict]:
    """Apply volume/number normalization to every entry in *bibliography*."""
    return [normalize_entry_volume(entry) for entry in bibliography]
