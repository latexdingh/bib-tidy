"""
Pipeline hook for affiliation normalization.

Integrates affiliation_normalizer into the bib-tidy pipeline.
"""

from pathlib import Path
from typing import Optional

from bibtidy.affiliation_normalizer import normalize_bibliography_affiliations
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(
    bibliography: list[dict],
    field: str = "affiliation",
) -> list[dict]:
    """Apply affiliation normalization to a bibliography.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts.
    field:
        The field name to normalize (default: ``"affiliation"``).

    Returns
    -------
    list[dict]
        New list with affiliation fields normalized.
    """
    return normalize_bibliography_affiliations(bibliography, field=field)


def run_on_file(
    path: str | Path,
    field: str = "affiliation",
    encoding: str = "utf-8",
) -> None:
    """Normalize affiliation fields in a .bib file in-place.

    Parameters
    ----------
    path:
        Path to the ``.bib`` file.
    field:
        The field name to normalize.
    encoding:
        File encoding (default: ``"utf-8"``).
    """
    path = Path(path)
    source = path.read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalized = apply(bibliography, field=field)
    path.write_text(format_bibliography(normalized), encoding=encoding)
