"""
Normalize page range fields in BibTeX entries.

Handles common variants:
  - Single page: "5" -> "5"
  - En-dash range: "5--10" (already canonical)
  - Hyphen range: "5-10" -> "5--10"
  - Em-dash range: "5—10" -> "5--10"
  - Spaces around separator: "5 - 10" -> "5--10"
  - Reversed ranges: "10--5" -> "5--10"
"""

import re
from typing import Optional


def normalize_pages(raw: str) -> Optional[str]:
    """Return a normalized BibTeX page range string, or None if unparseable."""
    if not raw or not raw.strip():
        return None

    raw = raw.strip()

    # Already canonical single page or key like "e12345"
    single = re.fullmatch(r'[A-Za-z]?\d+', raw)
    if single:
        return raw

    # Match a range with various separators: -, --, —, or whitespace combos
    range_pattern = re.compile(
        r'^([A-Za-z]?\d+)\s*(?:--|—|–|-)\s*([A-Za-z]?\d+)$'
    )
    m = range_pattern.match(raw)
    if m:
        start_str, end_str = m.group(1), m.group(2)
        # Extract numeric parts for comparison
        start_num = int(re.search(r'\d+', start_str).group())
        end_num = int(re.search(r'\d+', end_str).group())
        if start_num > end_num:
            start_str, end_str = end_str, start_str
        return f"{start_str}--{end_str}"

    # Fallback: return as-is (could be something like "iv--x")
    return raw


def normalize_entry_pages(entry: dict) -> dict:
    """Return a copy of *entry* with the 'pages' field normalized."""
    entry = dict(entry)
    fields = dict(entry.get("fields", {}))
    if "pages" in fields:
        normalized = normalize_pages(fields["pages"])
        if normalized is not None:
            fields["pages"] = normalized
    entry["fields"] = fields
    return entry


def normalize_bibliography_pages(entries: list) -> list:
    """Normalize page ranges for every entry in *entries*."""
    return [normalize_entry_pages(e) for e in entries]
