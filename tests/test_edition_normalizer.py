"""
Tests for bibtidy.edition_normalizer.
"""

import pytest
from bibtidy.edition_normalizer import (
    normalize_edition,
    normalize_entry_edition,
    normalize_bibliography_editions,
)


# ---------------------------------------------------------------------------
# normalize_edition — word forms
# ---------------------------------------------------------------------------

def test_normalize_word_first():
    assert normalize_edition("first") == "1st"


def test_normalize_word_second_titlecase():
    assert normalize_edition("Second") == "2nd"


def test_normalize_word_third_upper():
    assert normalize_edition("THIRD") == "3rd"


def test_normalize_word_fourth():
    assert normalize_edition("fourth") == "4th"


# ---------------------------------------------------------------------------
# normalize_edition — numeric / ordinal forms
# ---------------------------------------------------------------------------

def test_normalize_plain_integer_1():
    assert normalize_edition("1") == "1st"


def test_normalize_plain_integer_2():
    assert normalize_edition("2") == "2nd"


def test_normalize_plain_integer_3():
    assert normalize_edition("3") == "3rd"


def test_normalize_plain_integer_4():
    assert normalize_edition("4") == "4th"


def test_normalize_plain_integer_11():
    assert normalize_edition("11") == "11th"


def test_normalize_plain_integer_12():
    assert normalize_edition("12") == "12th"


def test_normalize_plain_integer_21():
    assert normalize_edition("21") == "21st"


def test_normalize_already_ordinal_2nd():
    assert normalize_edition("2nd") == "2nd"


def test_normalize_already_ordinal_3rd_uppercase():
    assert normalize_edition("3RD") == "3rd"


# ---------------------------------------------------------------------------
# normalize_edition — edge cases
# ---------------------------------------------------------------------------

def test_normalize_none_returns_none():
    assert normalize_edition(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_edition("") is None


def test_normalize_unknown_string_returned_as_is():
    assert normalize_edition("revised") == "revised"


def test_normalize_strips_whitespace():
    assert normalize_edition("  2nd  ") == "2nd"


# ---------------------------------------------------------------------------
# normalize_entry_edition
# ---------------------------------------------------------------------------

def _entry(edition=None):
    fields = {}
    if edition is not None:
        fields["edition"] = edition
    return {"type": "book", "key": "k", "fields": fields}


def test_entry_edition_normalized():
    e = normalize_entry_edition(_entry(edition="second"))
    assert e["fields"]["edition"] == "2nd"


def test_entry_without_edition_unchanged():
    e = normalize_entry_edition(_entry())
    assert "edition" not in e["fields"]


def test_entry_other_fields_preserved():
    entry = {"type": "book", "key": "k", "fields": {"title": "T", "edition": "1"}}
    result = normalize_entry_edition(entry)
    assert result["fields"]["title"] == "T"
    assert result["fields"]["edition"] == "1st"


# ---------------------------------------------------------------------------
# normalize_bibliography_editions
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalized():
    bib = [
        _entry(edition="first"),
        _entry(edition="3"),
        _entry(edition="second"),
    ]
    result = normalize_bibliography_editions(bib)
    assert [e["fields"]["edition"] for e in result] == ["1st", "3rd", "2nd"]


def test_bibliography_empty_list():
    assert normalize_bibliography_editions([]) == []
