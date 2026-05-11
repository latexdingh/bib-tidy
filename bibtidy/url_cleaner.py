"""url_cleaner.py — Normalize and clean URL fields in BibTeX entries.

Removes tracking parameters, normalizes schemes, and optionally strips
redundant URL fields when a DOI is already present.
"""

import re
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs

# Query parameters commonly used for tracking that add no scholarly value
_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "ref", "referrer", "source",
}


def clean_url(url: str) -> str:
    """Remove tracking parameters and normalize a single URL string."""
    if not url or not isinstance(url, str):
        return url

    url = url.strip()

    # Upgrade http to https where safe to do so for known scholarly hosts
    url = re.sub(r'^http://(doi\.org|dx\.doi\.org)/', r'https://\1/', url)

    try:
        parsed = urlparse(url)
    except ValueError:
        return url

    # Filter out tracking query parameters
    if parsed.query:
        params = parse_qs(parsed.query, keep_blank_values=True)
        filtered = {k: v for k, v in params.items() if k.lower() not in _TRACKING_PARAMS}
        clean_query = urlencode(filtered, doseq=True)
        parsed = parsed._replace(query=clean_query)

    return urlunparse(parsed)


def is_doi_url(url: str) -> bool:
    """Return True if the URL is a DOI resolver link (doi.org or dx.doi.org).

    This is useful for detecting when a URL field is redundant because it
    simply encodes the same information as a DOI field.

    >>> is_doi_url("https://doi.org/10.1000/xyz")
    True
    >>> is_doi_url("https://example.com/paper")
    False
    """
    if not url or not isinstance(url, str):
        return False
    try:
        host = urlparse(url.strip()).netloc.lower()
    except ValueError:
        return False
    return host in ("doi.org", "dx.doi.org", "www.doi.org")


def should_drop_url(entry: dict, drop_if_doi: bool = True) -> bool:
    """Return True if the URL field should be removed from the entry.

    Drops the URL when *both* conditions hold:
    - ``drop_if_doi`` is True
    - The entry has a non-empty DOI field **or** the URL is itself a DOI
      resolver link (making it fully redundant).
    """
    if not drop_if_doi:
        return False
    fields = entry.get("fields", {})
    has_doi = bool(fields.get("doi", "").strip())
    url = fields.get("url", "").strip()
    has_url = bool(url)
    return has_url and (has_doi or is_doi_url(url))


def clean_entry_url(entry: dict, drop_if_doi: bool = False) -> dict:
    """Clean the URL field of a single BibTeX entry dict.

    Args:
        entry: Parsed entry dict with at least 'fields' key.
        drop_if_doi: If True, remove the URL field when a DOI is present.

    Returns:
        A new entry dict with the URL field cleaned or removed.
    """
    fields = dict(entry.get("fields", {}))

    if should_drop_url(entry, drop_if_doi):
        fields.pop("url", None)
    elif "url" in fields:
        fields["url"] = clean_url(fields["url"])

    return {**entry, "fields": fields}


def clean_bibliography_urls(bibliography: list, drop_if_doi: bool = False) -> list:
    """Apply URL cleaning to every entry in a bibliography list.

    Args:
        bibliography: List of parsed entry dicts.
        drop_if_doi: Passed through to clean_entry_url.

    Returns:
        New list with cleaned entries.
    """
    return [clean_entry_url(entry, drop_if_doi=drop_if_doi) for entry in bibliography]
