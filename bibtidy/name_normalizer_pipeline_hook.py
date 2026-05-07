"""
Pipeline hook for name normalization.

Drops into the bib-tidy pipeline to normalize author/editor fields
across an entire bibliography loaded from a file.
"""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.name_normalizer import normalize_bibliography_names, _NAME_FIELDS


def apply(
    bibliography: list,
    fields: Optional[tuple] = None,
) -> list:
    """Apply name normalization to *bibliography* and return the result."""
    return normalize_bibliography_names(bibliography, fields=fields)


def run_on_file(
    input_path: str,
    output_path: Optional[str] = None,
    fields: Optional[tuple] = None,
) -> None:
    """Read a .bib file, normalize names, and write the result.

    If *output_path* is None the input file is overwritten in-place.
    """
    src = Path(input_path).read_text(encoding="utf-8")
    bibliography = parse_bibliography(src)
    normalized = normalize_bibliography_names(bibliography, fields=fields)
    out = format_bibliography(normalized)
    dest = output_path if output_path is not None else input_path
    Path(dest).write_text(out, encoding="utf-8")
