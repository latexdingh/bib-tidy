"""BibTeX parser module for bib-tidy.

Parses raw BibTeX strings into structured entry dictionaries.
"""

import re
from typing import Optional


BIBTEX_ENTRY_PATTERN = re.compile(
    r"@(\w+)\s*\{\s*([^,]+),\s*",
    re.IGNORECASE,
)

FIELD_PATTERN = re.compile(
    r"(\w+)\s*=\s*(?:\{([^{}]*)\}|\"([^\"]*)\"|([\w\d]+))",
    re.IGNORECASE,
)


def parse_entry(raw: str) -> Optional[dict]:
    """Parse a single BibTeX entry string into a dictionary.

    Args:
        raw: A raw BibTeX entry string.

    Returns:
        A dict with 'type', 'key', and 'fields', or None if parsing fails.
    """
    header_match = BIBTEX_ENTRY_PATTERN.match(raw.strip())
    if not header_match:
        return None

    entry_type = header_match.group(1).lower()
    citation_key = header_match.group(2).strip()

    fields = {}
    for match in FIELD_PATTERN.finditer(raw):
        field_name = match.group(1).lower()
        field_value = match.group(2) or match.group(3) or match.group(4) or ""
        fields[field_name] = field_value.strip()

    return {
        "type": entry_type,
        "key": citation_key,
        "fields": fields,
    }


def parse_bibliography(bibtex_str: str) -> list[dict]:
    """Parse a full BibTeX bibliography string into a list of entries.

    Args:
        bibtex_str: The full contents of a .bib file.

    Returns:
        A list of parsed entry dicts.
    """
    raw_entries = re.split(r"(?=@\w+\s*\{)", bibtex_str)
    entries = []
    for raw in raw_entries:
        raw = raw.strip()
        if not raw:
            continue
        entry = parse_entry(raw)
        if entry:
            entries.append(entry)
    return entries
