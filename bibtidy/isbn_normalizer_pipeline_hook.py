"""
Pipeline hook for ISBN normalization.

Integrates isbn_normalizer with the bib-tidy pipeline, providing
`apply` for in-memory use and `run_on_file` for file-based workflows.
"""

from pathlib import Path

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.isbn_normalizer import normalize_bibliography_isbns


def apply(entries: list) -> list:
    """
    Normalize ISBN fields for all entries.

    Parameters
    ----------
    entries:
        List of parsed BibTeX entry dicts.

    Returns
    -------
    list
        Entries with normalized ISBN-13 values (invalid ISBNs are left as-is).
    """
    return normalize_bibliography_isbns(entries)


def run_on_file(path: str) -> None:
    """
    Read a .bib file, normalize all ISBN fields, and overwrite it in place.

    Parameters
    ----------
    path:
        Filesystem path to the .bib file.
    """
    bib_path = Path(path)
    source = bib_path.read_text(encoding='utf-8')
    entries = parse_bibliography(source)
    normalized = apply(entries)
    bib_path.write_text(format_bibliography(normalized), encoding='utf-8')
