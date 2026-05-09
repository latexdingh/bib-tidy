"""Tests for bibtidy.language_normalizer."""

import pytest
from bibtidy.language_normalizer import (
    normalize_language,
    normalize_entry_language,
    normalize_bibliography_languages,
)


# ---------------------------------------------------------------------------
# normalize_language
# ---------------------------------------------------------------------------

def test_normalize_full_name_english():
    assert normalize_language("English") == "en"


def test_normalize_full_name_german():
    assert normalize_language("German") == "de"


def test_normalize_full_name_french():
    assert normalize_language("french") == "fr"


def test_normalize_iso3_code():
    assert normalize_language("spa") == "es"


def test_normalize_already_iso2():
    assert normalize_language("it") == "it"


def test_normalize_strips_whitespace():
    assert normalize_language("  de  ") == "de"


def test_normalize_case_insensitive():
    assert normalize_language("FRENCH") == "fr"


def test_normalize_unknown_returns_none():
    assert normalize_language("klingon") is None


def test_normalize_empty_string_returns_none():
    assert normalize_language("") is None


# ---------------------------------------------------------------------------
# normalize_entry_language
# ---------------------------------------------------------------------------

def _entry(language=None):
    fields = {}
    if language is not None:
        fields["language"] = language
    return {"type": "article", "key": "k1", "fields": fields}


def test_entry_language_normalised():
    e = _entry("German")
    result = normalize_entry_language(e)
    assert result["fields"]["language"] == "de"


def test_entry_language_unknown_unchanged():
    e = _entry("klingon")
    result = normalize_entry_language(e)
    assert result["fields"]["language"] == "klingon"


def test_entry_language_missing_unchanged():
    e = _entry()
    result = normalize_entry_language(e)
    assert "language" not in result["fields"]


def test_entry_returns_same_object():
    e = _entry("en")
    assert normalize_entry_language(e) is e


# ---------------------------------------------------------------------------
# normalize_bibliography_languages
# ---------------------------------------------------------------------------

def test_bibliography_normalises_all_entries():
    entries = [_entry("English"), _entry("deutsch"), _entry("fr")]
    result = normalize_bibliography_languages(entries)
    assert [r["fields"]["language"] for r in result] == ["en", "de", "fr"]


def test_bibliography_empty_list():
    assert normalize_bibliography_languages([]) == []


def test_bibliography_skips_entries_without_language():
    entries = [_entry(), _entry("it")]
    result = normalize_bibliography_languages(entries)
    assert "language" not in result[0]["fields"]
    assert result[1]["fields"]["language"] == "it"
