"""
Tests for bibtidy.conference_normalizer_pipeline_hook.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from bibtidy.conference_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(**fields):
    return {"type": "inproceedings", "key": "k", **fields}


# ---------------------------------------------------------------------------
# apply
# ---------------------------------------------------------------------------

def test_apply_normalizes_booktitle():
    bib = [_make_entry(booktitle="ICML")]
    result = apply(bib)
    assert result[0]["booktitle"] == "International Conference on Machine Learning"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_entry_without_booktitle_unchanged():
    e = _make_entry(title="A paper", year="2024")
    result = apply([e])
    assert result[0]["title"] == "A paper"
    assert "booktitle" not in result[0]


def test_apply_returns_new_list():
    bib = [_make_entry(booktitle="CVPR")]
    result = apply(bib)
    assert result is not bib


def test_apply_custom_fields():
    bib = [_make_entry(journal="NeurIPS")]
    result = apply(bib, fields=["journal"])
    assert result[0]["journal"] == "Neural Information Processing Systems"


# ---------------------------------------------------------------------------
# run_on_file
# ---------------------------------------------------------------------------

def test_run_on_file_overwrites_in_place(tmp_path):
    bib_content = (
        "@inproceedings{foo,\n"
        "  booktitle = {ICML},\n"
        "  title     = {A great paper},\n"
        "}\n"
    )
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(str(bib_file))

    result = bib_file.read_text(encoding="utf-8")
    assert "International Conference on Machine Learning" in result


def test_run_on_file_unknown_venue_preserved(tmp_path):
    bib_content = (
        "@inproceedings{bar,\n"
        "  booktitle = {Some Obscure Workshop},\n"
        "}\n"
    )
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(str(bib_file))

    result = bib_file.read_text(encoding="utf-8")
    assert "Some Obscure Workshop" in result
