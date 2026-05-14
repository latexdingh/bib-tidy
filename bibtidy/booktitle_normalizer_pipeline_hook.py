"""
Pipeline hook that applies booktitle normalisation to a .bib file.

Usage
-----
    from bibtidy import booktitle_normalizer_pipeline_hook as hook
    hook.run_on_file("references.bib")
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from bibtidy.booktitle_normalizer import normalize_bibliography_booktitles
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(entries: List[dict]) -> List[dict]:
    """Normalise booktitles in *entries* and return the updated list."""
    return normalize_bibliography_booktitles(entries)


def run_on_file(path: str | Path) -> None:
    """Read *path*, normalise booktitles in-place, and write back."""
    p = Path(path)
    source = p.read_text(encoding="utf-8")
    entries = parse_bibliography(source)
    updated = apply(entries)
    p.write_text(format_bibliography(updated), encoding="utf-8")
