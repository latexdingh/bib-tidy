"""
Pipeline hook: conference name normalisation.

Drops into the bib-tidy pipeline as a callable that accepts a
list of parsed BibTeX entry dicts and returns the normalised list.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional

from bibtidy.conference_normalizer import normalize_bibliography_conferences
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(
    bibliography: List[Dict],
    fields: Optional[List[str]] = None,
) -> List[Dict]:
    """Normalise conference names in *bibliography* and return the result.

    Parameters
    ----------
    bibliography:
        List of entry dicts as produced by :func:`bibtidy.parser.parse_bibliography`.
    fields:
        BibTeX fields to normalise.  Defaults to ``['booktitle', 'journal']``.
    """
    return normalize_bibliography_conferences(bibliography, fields=fields)


def run_on_file(
    path: str,
    fields: Optional[List[str]] = None,
    encoding: str = "utf-8",
) -> None:
    """Read *path*, normalise conference names in-place, and write back."""
    source = Path(path).read_text(encoding=encoding)
    bibliography = parse_bibliography(source)
    normalised = apply(bibliography, fields=fields)
    Path(path).write_text(format_bibliography(normalised), encoding=encoding)
