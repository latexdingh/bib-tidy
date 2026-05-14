"""Tests for bibtidy.arxiv_normalizer_pipeline_hook."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from bibtidy.arxiv_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(fields: dict) -> dict:
    return {"type": "article", "key": "k", "fields": fields}


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def test_apply_normalizes_eprint():
    entries = [_make_entry({"eprint": "arXiv:2301.12345"})]
    result = apply(entries)
    assert result[0]["fields"]["eprint"] == "2301.12345"
    assert result[0]["fields"]["archiveprefix"] == "arXiv"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_entry_without_arxiv_unchanged():
    e = _make_entry({"title": "No arXiv here"})
    result = apply([e])
    assert result[0]["fields"] == e["fields"]


def test_apply_returns_new_list():
    entries = [_make_entry({"eprint": "2301.00001"})]
    result = apply(entries)
    assert result is not entries


# ---------------------------------------------------------------------------
# run_on_file
# ---------------------------------------------------------------------------

def test_run_on_file_overwrites_in_place(tmp_path: Path):
    bib_content = (
        "@article{foo2024,\n"
        "  eprint = {arXiv:2301.12345},\n"
        "}\n"
    )
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(str(bib_file))

    result = bib_file.read_text(encoding="utf-8")
    # The normalized ID should appear in the output
    assert "2301.12345" in result
    # The arXiv: prefix should have been stripped from the eprint value
    assert "arXiv:2301.12345" not in result
