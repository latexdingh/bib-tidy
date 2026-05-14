"""Pipeline hook that normalises DOI fields across a bibliography file."""

from pathlib import Path
from typing import Optional

from bibtidy.doi_normalizer import normalize_bibliography_dois
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(bibliography: list) -> list:
    """Normalise DOI fields for every entry in *bibliography*.

    Suitable for use as a stage in the bib-tidy pipeline.

    Parameters
    ----------
    bibliography:
        List of parsed entry dicts as produced by :func:`parse_bibliography`.

    Returns
    -------
    list
        New list with normalised DOI fields.
    """
    return normalize_bibliography_dois(bibliography)


def run_on_file(path: str, encoding: str = "utf-8") -> None:
    """Normalise DOI fields in the .bib file at *path*, overwriting it.

    Parameters
    ----------
    path:
        Filesystem path to the target ``.bib`` file.
    encoding:
        File encoding (default ``utf-8``).
    """
    bib_path = Path(path)
    source = bib_path.read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalised = apply(bibliography)
    bib_path.write_text(format_bibliography(normalised), encoding=encoding)
