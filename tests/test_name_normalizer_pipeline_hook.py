"""
Tests for bibtidy.name_normalizer_pipeline_hook.
"""

import pytest
from unittest.mock import patch, MagicMock
from bibtidy.name_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(author: str) -> dict:
    return {"key": "k", "type": "article", "author": author}


def test_apply_normalizes_authors():
    bib = [_make_entry("Grace Hopper"), _make_entry("Alan Turing")]
    result = apply(bib)
    assert result[0]["author"] == "Hopper, Grace"
    assert result[1]["author"] == "Turing, Alan"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_custom_fields():
    entry = {"key": "k", "type": "misc", "editor": "Linus Torvalds"}
    result = apply([entry], fields=("editor",))
    assert result[0]["editor"] == "Torvalds, Linus"


@patch("bibtidy.name_normalizer_pipeline_hook.Path")
@patch("bibtidy.name_normalizer_pipeline_hook.format_bibliography")
@patch("bibtidy.name_normalizer_pipeline_hook.parse_bibliography")
def test_run_on_file_overwrites_in_place(mock_parse, mock_format, mock_path_cls):
    mock_path_instance = MagicMock()
    mock_path_instance.read_text.return_value = "@article{k, author={Ada Lovelace}}"
    mock_path_cls.return_value = mock_path_instance

    mock_parse.return_value = [{"key": "k", "type": "article", "author": "Ada Lovelace"}]
    mock_format.return_value = "@article{k, author={Lovelace, Ada}}"

    run_on_file("refs.bib")

    mock_path_instance.write_text.assert_called_once_with(
        "@article{k, author={Lovelace, Ada}}", encoding="utf-8"
    )


@patch("bibtidy.name_normalizer_pipeline_hook.Path")
@patch("bibtidy.name_normalizer_pipeline_hook.format_bibliography")
@patch("bibtidy.name_normalizer_pipeline_hook.parse_bibliography")
def test_run_on_file_uses_output_path(mock_parse, mock_format, mock_path_cls):
    instances = {}

    def path_factory(p):
        m = MagicMock()
        m.read_text.return_value = ""
        instances[p] = m
        return m

    mock_path_cls.side_effect = path_factory
    mock_parse.return_value = []
    mock_format.return_value = ""

    run_on_file("input.bib", output_path="output.bib")

    instances["output.bib"].write_text.assert_called_once()
