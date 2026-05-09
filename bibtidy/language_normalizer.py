"""
Normalize the `language` field of BibTeX entries to ISO 639-1 two-letter
language codes (e.g. "en", "de", "fr").
"""

from __future__ import annotations
from typing import Dict, List, Optional

# Map common variants / full names to ISO 639-1 codes
_LANGUAGE_MAP: Dict[str, str] = {
    # English
    "english": "en",
    "eng": "en",
    "en": "en",
    # German
    "german": "de",
    "deutsch": "de",
    "ger": "de",
    "deu": "de",
    "de": "de",
    # French
    "french": "fr",
    "francais": "fr",
    "français": "fr",
    "fre": "fr",
    "fra": "fr",
    "fr": "fr",
    # Spanish
    "spanish": "es",
    "espanol": "es",
    "español": "es",
    "spa": "es",
    "es": "es",
    # Italian
    "italian": "it",
    "italiano": "it",
    "ita": "it",
    "it": "it",
    # Portuguese
    "portuguese": "pt",
    "portugues": "pt",
    "português": "pt",
    "por": "pt",
    "pt": "pt",
    # Dutch
    "dutch": "nl",
    "nederlands": "nl",
    "nld": "nl",
    "nl": "nl",
    # Russian
    "russian": "ru",
    "rus": "ru",
    "ru": "ru",
    # Chinese
    "chinese": "zh",
    "chi": "zh",
    "zho": "zh",
    "zh": "zh",
    # Japanese
    "japanese": "ja",
    "jpn": "ja",
    "ja": "ja",
}


def normalize_language(value: str) -> Optional[str]:
    """Return ISO 639-1 code for *value*, or None if unrecognised."""
    key = value.strip().lower()
    return _LANGUAGE_MAP.get(key)


def normalize_entry_language(entry: Dict) -> Dict:
    """Normalise the `language` field of a single entry in-place and return it."""
    raw = entry.get("fields", {}).get("language")
    if raw is None:
        return entry
    normalised = normalize_language(raw)
    if normalised is not None:
        entry["fields"]["language"] = normalised
    return entry


def normalize_bibliography_languages(entries: List[Dict]) -> List[Dict]:
    """Normalise the `language` field of every entry in *entries*."""
    return [normalize_entry_language(e) for e in entries]
