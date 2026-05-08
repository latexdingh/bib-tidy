"""
Pipeline hook for edition normalization.

Exposes `apply` (works on an in-memory bibliography list) and
`run_on_file` (reads, normalizes, and overwrites a .bib file).
"""

from __future__ import annotations

from pathlib import Path

from bibtidy.edition_normalizer import normalize_bibliography_editions
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(entries: list[dict]) -> list[dict]:
    """Normalize edition fields for all entries and return the updated list."""
    return normalize_bibliography_editions(entries)


def run_on_file(path: str | Path) -> None:
    """Read *path*, normalize edition fields in-place, and write back."""
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    entries = parse_bibliography(source)
    updated = apply(entries)
    path.write_text(format_bibliography(updated), encoding="utf-8")
