"""
Pipeline hook for publisher normalization.

Integrates publisher_normalizer into the bib-tidy pipeline,
supporting both in-memory bibliography lists and file-based workflows.
"""

from pathlib import Path

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.publisher_normalizer import normalize_bibliography_publishers


def apply(
    bibliography: list[dict],
    fields: tuple[str, ...] = ("publisher", "organization", "institution"),
) -> list[dict]:
    """
    Normalize publisher fields for every entry in *bibliography*.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts.
    fields:
        Tuple of field names to normalize (default covers the three most
        common publisher-like fields).

    Returns
    -------
    A new list with normalized entries.
    """
    return normalize_bibliography_publishers(bibliography, fields=fields)


def run_on_file(
    path: str | Path,
    fields: tuple[str, ...] = ("publisher", "organization", "institution"),
    encoding: str = "utf-8",
) -> None:
    """
    Read *path*, normalize publisher fields, and overwrite the file in-place.

    Parameters
    ----------
    path:
        Path to the ``.bib`` file.
    fields:
        Publisher-like fields to normalize.
    encoding:
        File encoding (default ``utf-8``).
    """
    path = Path(path)
    source = path.read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalized = apply(bibliography, fields=fields)
    path.write_text(format_bibliography(normalized), encoding=encoding)
