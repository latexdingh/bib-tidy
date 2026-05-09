"""
Pipeline hook for the keyword normalizer.
"""

from __future__ import annotations

import pathlib

from bibtidy.keyword_normalizer import normalize_bibliography_keywords
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(
    bibliography: list[dict],
    field: str = "keywords",
    separator: str = "; ",
) -> list[dict]:
    """Normalize keyword fields in *bibliography* and return the result."""
    return normalize_bibliography_keywords(
        bibliography, field=field, separator=separator
    )


def run_on_file(
    path: str | pathlib.Path,
    field: str = "keywords",
    separator: str = "; ",
) -> None:
    """Read a .bib file, normalize keyword fields, and overwrite the file."""
    path = pathlib.Path(path)
    source = path.read_text(encoding="utf-8")
    bibliography = parse_bibliography(source)
    bibliography = apply(bibliography, field=field, separator=separator)
    path.write_text(format_bibliography(bibliography), encoding="utf-8")
