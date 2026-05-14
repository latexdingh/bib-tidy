"""Pipeline hook: normalize arXiv identifiers across a bibliography file."""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.arxiv_normalizer import normalize_bibliography_arxiv


def apply(entries: list[dict]) -> list[dict]:
    """Normalize arXiv fields for all entries and return the updated list."""
    return normalize_bibliography_arxiv(entries)


def run_on_file(path: str, encoding: str = "utf-8") -> None:
    """Read *path*, normalize arXiv fields in-place, and write back.

    Parameters
    ----------
    path:
        Path to a ``.bib`` file.
    encoding:
        File encoding (default ``utf-8``).
    """
    bib_path = Path(path)
    source = bib_path.read_text(encoding=encoding)
    entries = parse_bibliography(source)
    updated = apply(entries)
    bib_path.write_text(format_bibliography(updated), encoding=encoding)
