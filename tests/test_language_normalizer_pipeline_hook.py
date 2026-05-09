"""Tests for bibtidy.language_normalizer_pipeline_hook."""

import pytest
from unittest.mock import patch, MagicMock
from bibtidy.language_normalizer_pipeline_hook import apply, run_on_file


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _make_entry(language=None):
    fields = {}
    if language is not None:
        fields["language"] = language
    return {"type": "article", "key": "k", "fields": fields}


# ---------------------------------------------------------------------------
# apply()
# ---------------------------------------------------------------------------

def test_apply_normalises_entries():
    entries = [_make_entry("English"), _make_entry("deutsch")]
    result = apply(entries)
    assert result[0]["fields"]["language"] == "en"
    assert result[1]["fields"]["language"] == "de"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_leaves_unknown_language_unchanged():
    entries = [_make_entry("klingon")]
    result = apply(entries)
    assert result[0]["fields"]["language"] == "klingon"


# ---------------------------------------------------------------------------
# run_on_file()
# ---------------------------------------------------------------------------

BIB_SOURCE = """@article{smith2020,
  language = {English},
}
"""


def test_run_on_file_overwrites_in_place(tmp_path):
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(BIB_SOURCE, encoding="utf-8")

    with (
        patch("bibtidy.language_normalizer_pipeline_hook.parse_bibliography") as mock_parse,
        patch("bibtidy.language_normalizer_pipeline_hook.format_bibliography") as mock_fmt,
    ):
        entry = _make_entry("English")
        mock_parse.return_value = [entry]
        mock_fmt.return_value = "@article{smith2020,\n  language = {en},\n}\n"

        run_on_file(bib_file)

        mock_parse.assert_called_once()
        mock_fmt.assert_called_once()
        written = bib_file.read_text(encoding="utf-8")
        assert "language = {en}" in written
