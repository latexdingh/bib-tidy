"""Tests for bibtidy.doi_normalizer."""

import pytest
from bibtidy.doi_normalizer import normalize_doi, normalize_entry_doi, normalize_bibliography_dois


# ---------------------------------------------------------------------------
# normalize_doi
# ---------------------------------------------------------------------------

def test_normalize_bare_doi_unchanged():
    assert normalize_doi("10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_https_prefix():
    assert normalize_doi("https://doi.org/10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_http_prefix():
    assert normalize_doi("http://doi.org/10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_dx_doi_https():
    assert normalize_doi("https://dx.doi.org/10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_dx_doi_http():
    assert normalize_doi("http://dx.doi.org/10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_doi_colon_prefix():
    assert normalize_doi("doi:10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_doi_colon_with_space():
    assert normalize_doi("doi: 10.1000/xyz123") == "10.1000/xyz123"


def test_normalize_doi_strips_trailing_period():
    assert normalize_doi("10.1000/xyz123.") == "10.1000/xyz123"


def test_normalize_doi_strips_surrounding_braces():
    assert normalize_doi("{10.1000/xyz123}") == "10.1000/xyz123"


def test_normalize_doi_returns_none_for_none():
    assert normalize_doi(None) is None


def test_normalize_doi_returns_none_for_empty():
    assert normalize_doi("") is None


def test_normalize_doi_returns_none_for_invalid():
    assert normalize_doi("not-a-doi") is None


def test_normalize_doi_extracts_from_embedded_string():
    result = normalize_doi("See also https://doi.org/10.9999/abc for details.")
    assert result == "10.9999/abc"


def test_normalize_doi_strips_leading_whitespace():
    assert normalize_doi("  10.1234/hello") == "10.1234/hello"


# ---------------------------------------------------------------------------
# normalize_entry_doi
# ---------------------------------------------------------------------------

def _entry(doi_value):
    return {"type": "article", "key": "k", "fields": {"doi": doi_value, "title": "T"}}


def test_entry_doi_normalised():
    entry = _entry("https://doi.org/10.1234/test")
    result = normalize_entry_doi(entry)
    assert result["fields"]["doi"] == "10.1234/test"


def test_entry_doi_removed_when_invalid():
    entry = _entry("not-a-doi")
    result = normalize_entry_doi(entry)
    assert "doi" not in result["fields"]


def test_entry_other_fields_preserved():
    entry = _entry("10.1234/x")
    result = normalize_entry_doi(entry)
    assert result["fields"]["title"] == "T"


def test_entry_original_not_mutated():
    entry = _entry("https://doi.org/10.1234/test")
    normalize_entry_doi(entry)
    assert entry["fields"]["doi"] == "https://doi.org/10.1234/test"


# ---------------------------------------------------------------------------
# normalize_bibliography_dois
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalised():
    bib = [
        _entry("https://doi.org/10.1/a"),
        _entry("http://dx.doi.org/10.2/b"),
    ]
    result = normalize_bibliography_dois(bib)
    assert result[0]["fields"]["doi"] == "10.1/a"
    assert result[1]["fields"]["doi"] == "10.2/b"


def test_bibliography_empty_returns_empty():
    assert normalize_bibliography_dois([]) == []
