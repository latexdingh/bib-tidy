"""Citation key normalization for bib-tidy.

Generates consistent, human-readable BibTeX citation keys of the form:
    AuthorYYYYword  (e.g. Smith2021deep)
"""

import re
import unicodedata
from typing import Optional

_STOP_WORDS = frozenset({
    'a', 'an', 'the', 'of', 'in', 'on', 'at', 'to', 'for',
    'and', 'or', 'but', 'with', 'from', 'by', 'as', 'is',
})


def _ascii_fold(text: str) -> str:
    """Transliterate Unicode characters to ASCII equivalents."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


def _first_author_lastname(author_field: str) -> str:
    """Extract the last name of the first author."""
    if not author_field:
        return 'Unknown'
    first = author_field.split(' and ')[0].strip()
    if ',' in first:
        lastname = first.split(',')[0].strip()
    else:
        parts = first.split()
        lastname = parts[-1] if parts else first
    lastname = _ascii_fold(lastname)
    lastname = re.sub(r'[^A-Za-z]', '', lastname)
    return lastname.capitalize() if lastname else 'Unknown'


def _title_word(title: str) -> str:
    """Pick the first significant lowercase word from a title."""
    if not title:
        return ''
    words = re.sub(r'[^A-Za-z\s]', '', _ascii_fold(title)).lower().split()
    for word in words:
        if word not in _STOP_WORDS and len(word) > 2:
            return word
    return words[0] if words else ''


def generate_key(entry: dict) -> Optional[str]:
    """Generate a normalized citation key from entry metadata.

    Pattern: <LastName><Year><titleword>
    Returns None if insufficient data is available.
    """
    fields = entry.get('fields', {})
    author = fields.get('author', '')
    year = fields.get('year', '')
    title = fields.get('title', '')

    lastname = _first_author_lastname(author)
    year_str = re.sub(r'[^0-9]', '', year)[:4]
    word = _title_word(title)

    if lastname == 'Unknown' and not year_str:
        return None

    return f"{lastname}{year_str}{word}"


def normalize_key(entry: dict, existing_keys: Optional[set] = None) -> dict:
    """Replace the entry's citation key with a normalized version.

    If the generated key collides with an existing key, appends a letter suffix
    (a, b, c, …) to ensure uniqueness.
    """
    new_key = generate_key(entry)
    if not new_key:
        return entry

    if existing_keys is not None:
        candidate = new_key
        suffix_ord = ord('a')
        while candidate in existing_keys:
            candidate = f"{new_key}{chr(suffix_ord)}"
            suffix_ord += 1
        existing_keys.add(candidate)
        new_key = candidate

    entry = dict(entry)
    entry['key'] = new_key
    return entry
