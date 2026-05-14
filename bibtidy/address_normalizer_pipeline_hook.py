"""
Pipeline hook for address normalization.

Exposes `apply` (in-memory) and `run_on_file` (read-write) helpers
consistent with other pipeline hooks in this project.
"""

from __future__ import annotations

from pathlib import Path

from bibtidy.address_normalizer import normalize_bibliography_addresses
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(bibliography: list[dict]) -> list[dict]:
    """Normalize address fields for every entry in *bibliography*.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts.

    Returns
    -------
    list[dict]
        New list with address fields normalized.
    """
    return normalize_bibliography_addresses(bibliography)


def run_on_file(path: str | Path) -> None:
    """Read a .bib file, normalize address fields, and overwrite it.

    Parameters
    ----------
    path:
        Path to the BibTeX file to process in-place.
    """
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    bibliography = parse_bibliography(source)
    normalized = apply(bibliography)
    path.write_text(format_bibliography(normalized), encoding="utf-8")
