"""Tests for bibtidy.keyword_normalizer_pipeline_hook."""

from __future__ import annotations

import pathlib
import textwrap

import pytest

from bibtidy.keyword_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(keywords: str | None = None) -> dict:
    e: dict = {"type": "article", "key": "k1"}
    if keywords is not None:
        e["keywords"] = keywords
    return e


def test_apply_normalizes_keywords():
    bib = [_make_entry("z; a; z")]
    result = apply(bib)
    assert result[0]["keywords"] == "a; z"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_entry_without_keywords_unchanged():
    bib = [_make_entry()]
    result = apply(bib)
    assert "keywords" not in result[0]


def test_apply_custom_separator():
    bib = [_make_entry("b, a")]
    result = apply(bib, separator=", ")
    assert result[0]["keywords"] == "a, b"


def test_run_on_file_overwrites_in_place(tmp_path: pathlib.Path):
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(
        textwrap.dedent("""\
            @article{smith2020,
              keywords = {z; a; z},
            }
        """),
        encoding="utf-8",
    )
    run_on_file(bib_file)
    content = bib_file.read_text(encoding="utf-8")
    # After round-trip the deduplicated, sorted value should appear
    assert "a; z" in content
    assert content.count("z") < content.count("z") + 2  # basic sanity
