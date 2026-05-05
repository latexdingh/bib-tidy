"""
year_normalizer_pipeline_hook.py — Pipeline integration for year normalization.

Exposes a single :func:`apply` function that plugs into :mod:`bibtidy.pipeline`
and a convenience :func:`run_on_file` helper for standalone use.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.year_normalizer import normalize_bibliography_years


def apply(entries: list, *, strict: bool = False) -> list:
    """Normalize year fields for every entry in *entries*.

    Parameters
    ----------
    entries:
        List of parsed BibTeX entry dicts.
    strict:
        When *True*, entries whose year field cannot be reduced to a
        4-digit year are flagged with a ``_year_warning`` metadata key
        so downstream pipeline stages can report them.

    Returns
    -------
    list
        New list of entries with normalized year fields.
    """
    normalized = normalize_bibliography_years(entries)
    if strict:
        result = []
        for entry in normalized:
            year = entry.get('fields', {}).get('year', '')
            if year and not year.isdigit():
                entry = {**entry, '_year_warning': f"Unusual year value: {year!r}"}
            result.append(entry)
        return result
    return normalized


def run_on_file(
    input_path: str | Path,
    output_path: Optional[str | Path] = None,
    *,
    strict: bool = False,
) -> str:
    """Read a .bib file, normalize years, and write the result.

    Parameters
    ----------
    input_path:
        Path to the source ``.bib`` file.
    output_path:
        Destination path.  Defaults to overwriting *input_path* in-place.
    strict:
        Passed through to :func:`apply`.

    Returns
    -------
    str
        The formatted bibliography string that was written to disk.
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path

    source = input_path.read_text(encoding='utf-8')
    entries = parse_bibliography(source)
    entries = apply(entries, strict=strict)
    output = format_bibliography(entries)
    output_path.write_text(output, encoding='utf-8')
    return output
