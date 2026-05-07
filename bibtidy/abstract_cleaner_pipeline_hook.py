"""
Pipeline hook: integrate abstract cleaning into the bib-tidy pipeline.

Usage from pipeline.py::

    from bibtidy.abstract_cleaner_pipeline_hook import apply
    entries = apply(entries, max_words=300)
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from bibtidy.abstract_cleaner import clean_bibliography_abstracts
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(
    entries: list[dict],
    max_words: Optional[int] = None,
) -> list[dict]:
    """Clean abstract fields for all *entries* and return the updated list.

    Parameters
    ----------
    entries:
        List of parsed bibliography entry dicts.
    max_words:
        If given, truncate abstracts longer than this many words.
    """
    return clean_bibliography_abstracts(entries, max_words=max_words)


def run_on_file(
    path: str | Path,
    max_words: Optional[int] = None,
    encoding: str = "utf-8",
) -> None:
    """Read a .bib file, clean its abstracts, and overwrite it in place.

    Parameters
    ----------
    path:
        Filesystem path to the .bib file.
    max_words:
        Optional word-count cap for abstracts.
    encoding:
        File encoding (default UTF-8).
    """
    path = Path(path)
    source = path.read_text(encoding=encoding)
    entries = parse_bibliography(source)
    entries = apply(entries, max_words=max_words)
    path.write_text(format_bibliography(entries), encoding=encoding)
