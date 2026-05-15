"""Pipeline hook for title normalization.

Applies title normalization to every entry in a bibliography, optionally
writing the result back to a .bib file in-place.
"""

from __future__ import annotations

from typing import Any

from bibtidy.title_normalizer import normalize_bibliography_titles
from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography


def apply(
    bibliography: list[dict[str, Any]],
    *,
    mode: str = "title",
    protect_all_caps: bool = True,
) -> list[dict[str, Any]]:
    """Normalize titles in every entry of *bibliography*.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts, each with at least ``"type"``,
        ``"key"``, and ``"fields"`` keys.
    mode:
        Casing strategy passed through to :func:`normalize_bibliography_titles`.
        Accepted values are ``"title"`` (Title Case, default) and
        ``"sentence"`` (Sentence case).
    protect_all_caps:
        When *True*, sequences of ALL-CAPS letters (acronyms) are wrapped in
        braces so that BibTeX renderers preserve their capitalisation.

    Returns
    -------
    list[dict[str, Any]]
        A new list of entry dicts with normalised ``title`` fields.  Entries
        that have no ``title`` field are returned unchanged.
    """
    return normalize_bibliography_titles(
        bibliography,
        mode=mode,
        protect_all_caps=protect_all_caps,
    )


def run_on_file(
    path: str,
    *,
    mode: str = "title",
    protect_all_caps: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Read *path*, normalise all entry titles, and write the result back.

    Parameters
    ----------
    path:
        File-system path to a ``.bib`` file.  The file is overwritten in place.
    mode:
        Casing strategy; see :func:`apply`.
    protect_all_caps:
        Wrap ALL-CAPS tokens in braces; see :func:`apply`.
    encoding:
        Character encoding used when reading and writing the file.
    """
    with open(path, "r", encoding=encoding) as fh:
        source = fh.read()

    bibliography = parse_bibliography(source)
    normalised = apply(
        bibliography,
        mode=mode,
        protect_all_caps=protect_all_caps,
    )
    output = format_bibliography(normalised)

    with open(path, "w", encoding=encoding) as fh:
        fh.write(output)
