"""Pipeline hook for series normalization."""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.series_normalizer import normalize_bibliography_series


def apply(entries: list[dict]) -> list[dict]:
    """Apply series normalization to a list of bibliography entries."""
    return normalize_bibliography_series(entries)


def run_on_file(path: str, encoding: str = "utf-8") -> None:
    """Read a .bib file, normalize series fields, and overwrite it in place."""
    source = Path(path).read_text(encoding=encoding)
    entries = parse_bibliography(source)
    normalized = normalize_bibliography_series(entries)
    output = format_bibliography(normalized)
    Path(path).write_text(output, encoding=encoding)
