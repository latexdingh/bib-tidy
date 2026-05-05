"""Tests for the BibTeX parser and formatter modules."""

import pytest
from bibtidy.parser import parse_entry, parse_bibliography
from bibtidy.formatter import format_entry, format_bibliography


SAMPLE_ENTRY = """@article{smith2023example,
  author = {Smith, John},
  title = {An Example Article},
  year = {2023},
  journal = {Journal of Examples},
  doi = {10.1234/example.2023}
}"""


def test_parse_entry_type_and_key():
    entry = parse_entry(SAMPLE_ENTRY)
    assert entry is not None
    assert entry["type"] == "article"
    assert entry["key"] == "smith2023example"


def test_parse_entry_fields():
    entry = parse_entry(SAMPLE_ENTRY)
    assert entry["fields"]["author"] == "Smith, John"
    assert entry["fields"]["title"] == "An Example Article"
    assert entry["fields"]["year"] == "2023"
    assert entry["fields"]["doi"] == "10.1234/example.2023"


def test_parse_entry_returns_none_for_invalid():
    result = parse_entry("this is not bibtex")
    assert result is None


def test_parse_bibliography_multiple_entries():
    bib = SAMPLE_ENTRY + "\n\n" + """@book{doe2020book,
  author = {Doe, Jane},
  title = {A Book},
  year = {2020},
  publisher = {Some Press}
}"""
    entries = parse_bibliography(bib)
    assert len(entries) == 2
    assert entries[0]["key"] == "smith2023example"
    assert entries[1]["key"] == "doe2020book"


def test_format_entry_contains_key_and_type():
    entry = parse_entry(SAMPLE_ENTRY)
    formatted = format_entry(entry)
    assert "@article{smith2023example," in formatted


def test_format_entry_field_order():
    entry = parse_entry(SAMPLE_ENTRY)
    formatted = format_entry(entry)
    author_pos = formatted.index("author")
    title_pos = formatted.index("title")
    year_pos = formatted.index("year")
    assert author_pos < title_pos < year_pos


def test_format_bibliography_roundtrip():
    entries = parse_bibliography(SAMPLE_ENTRY)
    output = format_bibliography(entries)
    assert "smith2023example" in output
    assert "An Example Article" in output
    assert output.endswith("\n")
