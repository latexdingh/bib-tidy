"""Pipeline hook for journal name normalization.

Integrates the journal normalizer into the bib-tidy pipeline,
expanding abbreviations and standardizing journal names in-place
or on a file.
"""

from __future__ import annotations

import copy
from typing import Any

from .journal_normalizer import normalize_bibliography_journals
from .parser import parse_bibliography
from .formatter import format_bibliography


def apply(
    bibliography: list[dict[str, Any]],
    custom_map: dict[str, str] | None = None,
    prefer_full: bool = True,
) -> list[dict[str, Any]]:
    """Normalize journal names for every entry in *bibliography*.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts, each with at least
        ``'type'``, ``'key'``, and ``'fields'`` keys.
    custom_map:
        Optional mapping of additional abbreviation ↔ full-name pairs
        to merge with the built-in lookup table.
    prefer_full:
        When *True* (default) expand abbreviations to their canonical
        full names.  When *False* the hook leaves unknown names
        unchanged but still applies alias resolution.

    Returns
    -------
    list[dict[str, Any]]
        A new list of entry dicts with journal names normalized;
        original entries are not mutated.
    """
    # Work on deep copies so callers retain their original objects.
    entries = [copy.deepcopy(e) for e in bibliography]
    return normalize_bibliography_journals(entries, custom_map=custom_map)


def run_on_file(
    path: str,
    custom_map: dict[str, str] | None = None,
    prefer_full: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Read *path*, normalize journal names, and overwrite the file.

    Parameters
    ----------
    path:
        Filesystem path to a ``.bib`` file.
    custom_map:
        Optional extra abbreviation mappings forwarded to :func:`apply`.
    prefer_full:
        Forwarded to :func:`apply`.
    encoding:
        File encoding used for both reading and writing (default UTF-8).
    """
    with open(path, encoding=encoding) as fh:
        source = fh.read()

    bibliography = parse_bibliography(source)
    normalized = apply(bibliography, custom_map=custom_map, prefer_full=prefer_full)
    output = format_bibliography(normalized)

    with open(path, "w", encoding=encoding) as fh:
        fh.write(output)
