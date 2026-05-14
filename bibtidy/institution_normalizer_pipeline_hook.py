"""Pipeline hook for institution/organization field normalization."""

from pathlib import Path
from typing import Optional

from bibtidy.institution_normalizer import normalize_bibliography_institutions
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography

_DEFAULT_FIELDS = ("institution", "organization", "school")


def apply(
    bibliography: list[dict],
    fields: Optional[tuple[str, ...]] = None,
) -> list[dict]:
    """Normalize institution-like fields in *bibliography* and return the result.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts.
    fields:
        Tuple of field names to normalize.  Defaults to
        ``("institution", "organization", "school")``.
    """
    effective_fields = fields if fields is not None else _DEFAULT_FIELDS
    return normalize_bibliography_institutions(bibliography, fields=effective_fields)


def run_on_file(
    path: str | Path,
    fields: Optional[tuple[str, ...]] = None,
    encoding: str = "utf-8",
) -> None:
    """Read *path*, normalize institution fields, and overwrite the file."""
    path = Path(path)
    source = path.read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalized = apply(bibliography, fields=fields)
    path.write_text(format_bibliography(normalized), encoding=encoding)
