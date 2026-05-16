"""Tests for bibtidy.funding_normalizer."""

import pytest
from bibtidy.funding_normalizer import (
    normalize_funding,
    normalize_entry_funding,
    normalize_bibliography_funding,
)


# ---------------------------------------------------------------------------
# normalize_funding
# ---------------------------------------------------------------------------

def test_normalize_nsf_abbreviation():
    assert normalize_funding("NSF") == "National Science Foundation"


def test_normalize_nih_abbreviation():
    assert normalize_funding("NIH") == "National Institutes of Health"


def test_normalize_case_insensitive():
    assert normalize_funding("nsf") == "National Science Foundation"
    assert normalize_funding("Nsf") == "National Science Foundation"


def test_normalize_full_name_nsf():
    assert normalize_funding("National Science Foundation") == "National Science Foundation"


def test_normalize_dfg():
    assert normalize_funding("DFG") == "Deutsche Forschungsgemeinschaft"


def test_normalize_snsf_alias():
    assert normalize_funding("SNSF") == "Swiss National Science Foundation"
    assert normalize_funding("SNF") == "Swiss National Science Foundation"


def test_normalize_erc():
    assert normalize_funding("ERC") == "European Research Council"


def test_normalize_unknown_returns_original():
    assert normalize_funding("Some Custom Funder") == "Some Custom Funder"


def test_normalize_strips_braces():
    assert normalize_funding("{NSF}") == "National Science Foundation"


def test_normalize_collapses_whitespace():
    assert normalize_funding("  NSF  ") == "National Science Foundation"


def test_normalize_none_returns_none():
    assert normalize_funding(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_funding("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_funding("   ") is None


def test_normalize_braces_only_returns_none():
    assert normalize_funding("{}") is None


# ---------------------------------------------------------------------------
# normalize_entry_funding
# ---------------------------------------------------------------------------

def test_entry_funding_normalized():
    entry = {"key": "Smith2020", "type": "article", "funding": "NSF"}
    result = normalize_entry_funding(entry)
    assert result["funding"] == "National Science Foundation"


def test_entry_funding_removed_when_empty():
    entry = {"key": "Smith2020", "type": "article", "funding": ""}
    result = normalize_entry_funding(entry)
    assert "funding" not in result


def test_entry_without_funding_unchanged():
    entry = {"key": "Smith2020", "type": "article", "title": "Test"}
    result = normalize_entry_funding(entry)
    assert result == entry


def test_entry_original_not_mutated():
    entry = {"key": "Smith2020", "type": "article", "funding": "NSF"}
    original_funding = entry["funding"]
    normalize_entry_funding(entry)
    assert entry["funding"] == original_funding


# ---------------------------------------------------------------------------
# normalize_bibliography_funding
# ---------------------------------------------------------------------------

def test_bibliography_normalizes_all_entries():
    bib = [
        {"key": "A", "funding": "NSF"},
        {"key": "B", "funding": "DFG"},
    ]
    result = normalize_bibliography_funding(bib)
    assert result[0]["funding"] == "National Science Foundation"
    assert result[1]["funding"] == "Deutsche Forschungsgemeinschaft"


def test_bibliography_empty_list():
    assert normalize_bibliography_funding([]) == []


def test_bibliography_returns_new_list():
    bib = [{"key": "A", "funding": "NIH"}]
    result = normalize_bibliography_funding(bib)
    assert result is not bib
