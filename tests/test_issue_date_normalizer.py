"""Tests for bibtidy.issue_date_normalizer."""

import pytest
from bibtidy.issue_date_normalizer import (
    normalize_issue,
    normalize_entry_issue,
    normalize_bibliography_issues,
)


# ---------------------------------------------------------------------------
# normalize_issue
# ---------------------------------------------------------------------------

def test_normalize_plain_integer():
    assert normalize_issue("3") == "3"


def test_normalize_strips_leading_zeros():
    # 007 -> 7
    assert normalize_issue("007") == "7"


def test_normalize_strips_no_prefix():
    assert normalize_issue("No. 4") == "4"
    assert normalize_issue("no.4") == "4"


def test_normalize_strips_number_prefix():
    assert normalize_issue("Number 12") == "12"
    assert normalize_issue("num. 2") == "2"


def test_normalize_strips_issue_prefix():
    assert normalize_issue("Issue 5") == "5"
    assert normalize_issue("ISSUE 5") == "5"


def test_normalize_strips_hash_prefix():
    assert normalize_issue("#8") == "8"
    assert normalize_issue("# 8") == "8"


def test_normalize_range_single_hyphen():
    assert normalize_issue("3-4") == "3--4"


def test_normalize_range_en_dash():
    assert normalize_issue("3\u20134") == "3--4"


def test_normalize_range_em_dash():
    assert normalize_issue("3\u20144") == "3--4"


def test_normalize_strips_braces():
    assert normalize_issue("{6}") == "6"


def test_normalize_returns_none_for_none():
    assert normalize_issue(None) is None


def test_normalize_returns_none_for_empty():
    assert normalize_issue("") is None
    assert normalize_issue("   ") is None


def test_normalize_alphanumeric_passthrough():
    # Supplement issues like "S1" should pass through
    result = normalize_issue("S1")
    assert result == "S1"


def test_normalize_collapses_internal_whitespace():
    assert normalize_issue("Special  Issue") == "Special Issue"


# ---------------------------------------------------------------------------
# normalize_entry_issue
# ---------------------------------------------------------------------------

def test_entry_normalizes_number_field():
    entry = {"ENTRYTYPE": "article", "ID": "k", "number": "No. 3"}
    result = normalize_entry_issue(entry)
    assert result["number"] == "3"


def test_entry_drops_empty_number():
    entry = {"ENTRYTYPE": "article", "ID": "k", "number": ""}
    result = normalize_entry_issue(entry)
    assert "number" not in result


def test_entry_custom_field():
    entry = {"ENTRYTYPE": "article", "ID": "k", "issue": "Issue 7"}
    result = normalize_entry_issue(entry, field="issue")
    assert result["issue"] == "7"


def test_entry_missing_field_unchanged():
    entry = {"ENTRYTYPE": "article", "ID": "k"}
    result = normalize_entry_issue(entry)
    assert result == entry


# ---------------------------------------------------------------------------
# normalize_bibliography_issues
# ---------------------------------------------------------------------------

def test_bibliography_normalizes_all_entries():
    bib = [
        {"ENTRYTYPE": "article", "ID": "a", "number": "No. 1"},
        {"ENTRYTYPE": "article", "ID": "b", "number": "Issue 2"},
        {"ENTRYTYPE": "article", "ID": "c"},
    ]
    result = normalize_bibliography_issues(bib)
    assert result[0]["number"] == "1"
    assert result[1]["number"] == "2"
    assert "number" not in result[2]


def test_bibliography_returns_new_list():
    bib = [{"ENTRYTYPE": "article", "ID": "a", "number": "3"}]
    result = normalize_bibliography_issues(bib)
    assert result is not bib
