"""
Pipeline hook that applies language normalisation to a bibliography file.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.language_normalizer import normalize_bibliography_languages


def apply(entries: List[Dict]) -> List[Dict]:
    """Normalise language fields and return the updated entry list."""
    return normalize_bibliography_languages(entries)


def run_on_file(path: str | Path) -> None:
    """
    Read *path*, normalise all language fields, and overwrite the file
    with the formatted result.
    """
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    entries = parse_bibliography(source)
    entries = apply(entries)
    path.write_text(format_bibliography(entries), encoding="utf-8")
