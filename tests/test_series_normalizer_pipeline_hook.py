"""Tests for bibtidy.series_normalizer_pipeline_hook."""

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from bibtidy.series_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(series: str = "lncs") -> dict:
    return {"ENTRYTYPE": "book", "ID": "k1", "series": series}


def test_apply_normalizes_series():
    entries = [_make_entry("lncs"), _make_entry("pmlr")]
    result = apply(entries)
    assert result[0]["series"] == "Lecture Notes in Computer Science"
    assert result[1]["series"] == "Proceedings of Machine Learning Research"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_entry_without_series_unchanged():
    entry = {"ENTRYTYPE": "article", "ID": "x", "title": "Paper"}
    result = apply([entry])
    assert "series" not in result[0]
    assert result[0]["title"] == "Paper"


def test_apply_returns_new_list():
    entries = [_make_entry()]
    result = apply(entries)
    assert result is not entries


def test_run_on_file_overwrites_in_place(tmp_path: Path):
    bib_content = "@book{k1,\n  series = {lncs},\n}\n"
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(str(bib_file))

    output = bib_file.read_text(encoding="utf-8")
    assert "Lecture Notes in Computer Science" in output
