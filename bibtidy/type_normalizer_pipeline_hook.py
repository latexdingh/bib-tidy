"""
Pipeline hook for entry-type normalization.

Integrates type_normalizer into the bib-tidy pipeline, supporting
both in-memory bibliography lists and file-based workflows.
"""

from pathlib import Path
from typing import Optional

from bibtidy.type_normalizer import normalize_bibliography_types
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(bibliography: list[dict]) -> list[dict]:
    """
    Apply entry-type normalization to a bibliography.

    Args:
        bibliography: List of parsed BibTeX entry dicts.

    Returns:
        New list with normalized entry types.
    """
    return normalize_bibliography_types(bibliography)


def run_on_file(path: str, encoding: str = "utf-8") -> None:
    """
    Read a .bib file, normalize all entry types, and overwrite the file.

    Args:
        path:     Path to the .bib file.
        encoding: File encoding (default utf-8).
    """
    bib_path = Path(path)
    source = bib_path.read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalized = normalize_bibliography_types(bibliography)
    bib_path.write_text(format_bibliography(normalized), encoding=encoding)
