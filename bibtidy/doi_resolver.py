"""DOI resolution utilities for bib-tidy.

Fetches metadata from doi.org and crossref.org to enrich BibTeX entries.
"""

import re
import urllib.request
import urllib.error
import json
from typing import Optional

DOI_PATTERN = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
CROSSREF_API = "https://api.crossref.org/works/{doi}"


def extract_doi(entry: dict) -> Optional[str]:
    """Extract DOI string from an entry's 'doi' or 'url' field."""
    doi = entry.get('fields', {}).get('doi', '').strip()
    if doi:
        match = DOI_PATTERN.search(doi)
        return match.group(0) if match else None
    url = entry.get('fields', {}).get('url', '').strip()
    if url:
        match = DOI_PATTERN.search(url)
        return match.group(0) if match else None
    return None


def fetch_doi_metadata(doi: str, timeout: int = 10) -> Optional[dict]:
    """Query the Crossref API for metadata about a given DOI.

    Returns a dict with keys: title, author, year, journal, volume, pages, publisher.
    Returns None if the request fails or the DOI is not found.
    """
    url = CROSSREF_API.format(doi=urllib.request.quote(doi, safe='/'))
    req = urllib.request.Request(url, headers={'User-Agent': 'bib-tidy/1.0 (mailto:user@example.com)'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return None

    msg = data.get('message', {})
    title_list = msg.get('title', [])
    title = title_list[0] if title_list else ''

    authors = msg.get('author', [])
    author_str = ' and '.join(
        f"{a.get('family', '')}, {a.get('given', '')}".strip(', ')
        for a in authors
    )

    issued = msg.get('issued', {}).get('date-parts', [[]])[0]
    year = str(issued[0]) if issued else ''

    container = msg.get('container-title', [])
    journal = container[0] if container else ''

    return {
        'title': title,
        'author': author_str,
        'year': year,
        'journal': journal,
        'volume': msg.get('volume', ''),
        'pages': msg.get('page', ''),
        'publisher': msg.get('publisher', ''),
        'doi': doi,
    }


def enrich_entry(entry: dict) -> dict:
    """Fill missing fields in a BibTeX entry using DOI metadata.

    Only updates fields that are absent or empty in the original entry.
    Returns the (possibly modified) entry dict.
    """
    doi = extract_doi(entry)
    if not doi:
        return entry

    metadata = fetch_doi_metadata(doi)
    if not metadata:
        return entry

    fields = entry.setdefault('fields', {})
    for key, value in metadata.items():
        if value and not fields.get(key):
            fields[key] = value

    return entry
