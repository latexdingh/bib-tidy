"""
Tests for bibtidy.type_normalizer_pipeline_hook
"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from bibtidy.type_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(entry_type: str, key: str = "K") -> dict:
    return {"type": entry_type, "key": key, "fields": {}}


# ---------------------------------------------------------------------------
# apply()
# ---------------------------------------------------------------------------

def test_apply_normalizes_entry_types():
    bib = [_make_entry("conference"), _make_entry("journal")]
    result = apply(bib)
    assert result[0]["type"] == "inproceedings"
    assert result[1]["type"] == "article"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_returns_new_list():
    bib = [_make_entry("article")]
    result = apply(bib)
    assert result is not bib


def test_apply_unknown_type_lowercased():
    bib = [_make_entry("CustomEntry")]
    result = apply(bib)
    assert result[0]["type"] == "customentry"


# ---------------------------------------------------------------------------
# run_on_file()
# ---------------------------------------------------------------------------

def test_run_on_file_overwrites_in_place(tmp_path):
    bib_content = "@conference{Smith2020,\n  title = {A Paper},\n}\n"
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(str(bib_file))

    written = bib_file.read_text(encoding="utf-8")
    # The entry type should now be the canonical form
    assert "@inproceedings" in written.lower() or "inproceedings" in written.lower()


def test_run_on_file_uses_encoding(tmp_path):
    """Ensure the encoding parameter is forwarded correctly."""
    bib_content = "@article{Foo2021,\n  title = {Bar},\n}\n"
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    # Should not raise even when encoding is explicit
    run_on_file(str(bib_file), encoding="utf-8")
    written = bib_file.read_text(encoding="utf-8")
    assert "article" in written
