"""
Abstract field cleaner: strips HTML tags, normalizes whitespace,
and optionally truncates overly long abstracts.
"""

import re
from typing import Optional

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    return _HTML_TAG_RE.sub(" ", text)


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace into a single space and strip ends."""
    return _WHITESPACE_RE.sub(" ", text).strip()


def truncate_abstract(text: str, max_words: int = 300) -> str:
    """Truncate abstract to at most *max_words* words, appending '...' if cut."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " ..."


def clean_abstract(text: str, max_words: Optional[int] = None) -> str:
    """Full cleaning pipeline for a single abstract string."""
    text = strip_html(text)
    text = normalize_whitespace(text)
    if max_words is not None:
        text = truncate_abstract(text, max_words)
    return text


def clean_entry_abstract(
    entry: dict, max_words: Optional[int] = None
) -> dict:
    """Return a copy of *entry* with its 'abstract' field cleaned (if present)."""
    if "abstract" not in entry.get("fields", {}):
        return entry
    cleaned = dict(entry)
    cleaned["fields"] = dict(entry["fields"])
    cleaned["fields"]["abstract"] = clean_abstract(
        entry["fields"]["abstract"], max_words=max_words
    )
    return cleaned


def clean_bibliography_abstracts(
    entries: list[dict], max_words: Optional[int] = None
) -> list[dict]:
    """Apply abstract cleaning to every entry in *entries*."""
    return [clean_entry_abstract(e, max_words=max_words) for e in entries]
