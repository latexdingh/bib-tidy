"""
bibtidy/note_cleaner_pipeline_hook.py

Pipeline hook that integrates note cleaning into bib-tidy's run_file workflow.
"""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.note_cleaner import clean_bibliography_notes, MAX_NOTE_LENGTH


def apply(
    entries: list,
    max_length: Optional[int] = MAX_NOTE_LENGTH,
) -> list:
    """Clean note fields for all *entries* and return the updated list."""
    return clean_bibliography_notes(entries, max_length=max_length)


def run_on_file(
    path: str,
    max_length: Optional[int] = MAX_NOTE_LENGTH,
    encoding: str = 'utf-8',
) -> None:
    """Read a .bib file, clean note fields in-place, and overwrite the file."""
    bib_path = Path(path)
    source = bib_path.read_text(encoding=encoding)
    entries = parse_bibliography(source)
    cleaned = clean_bibliography_notes(entries, max_length=max_length)
    bib_path.write_text(format_bibliography(cleaned), encoding=encoding)
