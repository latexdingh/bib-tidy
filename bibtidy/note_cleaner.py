"""
bibtidy/note_cleaner.py

Cleans and normalises the `note` field of BibTeX entries:
- Strips leading/trailing whitespace and redundant internal spaces
- Removes purely empty notes
- Optionally truncates overly long notes
- Applies a configurable list of regex-based substitution rules
"""

import re
from typing import Dict, List, Optional, Tuple

# Each rule is (compiled_pattern, replacement)
_DEFAULT_RULES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'\\url\{([^}]+)\}', re.IGNORECASE), r'\1'),  # unwrap \url{}
    (re.compile(r'<[^>]+>'), ''),                               # strip HTML tags
    (re.compile(r'\s{2,}'), ' '),                              # collapse whitespace
]

MAX_NOTE_LENGTH = 300


def clean_note(raw: str, max_length: Optional[int] = MAX_NOTE_LENGTH) -> Optional[str]:
    """Return a cleaned version of *raw*, or None if the result is empty."""
    text = raw.strip()
    if not text:
        return None

    for pattern, replacement in _DEFAULT_RULES:
        text = pattern.sub(replacement, text)

    text = text.strip()
    if not text:
        return None

    if max_length and len(text) > max_length:
        text = text[:max_length].rstrip() + '…'

    return text


def clean_entry_note(
    entry: Dict,
    max_length: Optional[int] = MAX_NOTE_LENGTH,
) -> Dict:
    """Return a copy of *entry* with the `note` field cleaned."""
    entry = dict(entry)
    fields = dict(entry.get('fields', {}))

    raw = fields.get('note')
    if raw is not None:
        cleaned = clean_note(raw, max_length=max_length)
        if cleaned is None:
            fields.pop('note', None)
        else:
            fields['note'] = cleaned

    entry['fields'] = fields
    return entry


def clean_bibliography_notes(
    entries: List[Dict],
    max_length: Optional[int] = MAX_NOTE_LENGTH,
) -> List[Dict]:
    """Apply :func:`clean_entry_note` to every entry in *entries*."""
    return [clean_entry_note(e, max_length=max_length) for e in entries]
