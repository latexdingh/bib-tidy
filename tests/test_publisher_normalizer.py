"""Tests for bibtidy.publisher_normalizer."""

import pytest
from bibtidy.publisher_normalizer import (
    normalize_publisher,
    normalize_entry_publisher,
    normalize_bibliography_publishers,
)


# ---------------------------------------------------------------------------
# normalize_publisher
# ---------------------------------------------------------------------------

def test_normalize_known_springer_variant():
    assert normalize_publisher("Springer-Verlag") == "Springer"


def test_normalize_known_ieee_variant():
    assert normalize_publisher("IEEE Computer Society") == "IEEE"


def test_normalize_known_acm_variant():
    assert normalize_publisher("ACM Press") == "ACM"


def test_normalize_known_elsevier_bv():
    assert normalize_publisher("Elsevier B.V.") == "Elsevier"


def test_normalize_known_wiley_variant():
    assert normalize_publisher("John Wiley & Sons") == "Wiley"


def test_normalize_strips_inc_suffix():
    assert normalize_publisher("Acme Publishing, Inc.") == "Acme Publishing"


def test_normalize_strips_ltd_suffix():
    assert normalize_publisher("Acme Publishing Ltd.") == "Acme Publishing"


def test_normalize_strips_llc_suffix():
    assert normalize_publisher("Acme Books LLC") == "Acme Books"


def test_normalize_unknown_publisher_returns_stripped():
    assert normalize_publisher("  University of Somewhere  ") == "University of Somewhere"


def test_normalize_none_returns_none():
    assert normalize_publisher(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_publisher("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_publisher("   ") is None


def test_normalize_case_insensitive_lookup():
    assert normalize_publisher("SPRINGER VERLAG") == "Springer"


def test_normalize_taylor_and_francis():
    assert normalize_publisher("Taylor and Francis") == "Taylor & Francis"


# ---------------------------------------------------------------------------
# normalize_entry_publisher
# ---------------------------------------------------------------------------

def _entry(**fields) -> dict:
    return {"type": "article", "key": "k", **fields}


def test_entry_publisher_normalized():
    entry = _entry(publisher="Springer-Verlag")
    result = normalize_entry_publisher(entry)
    assert result["publisher"] == "Springer"


def test_entry_organization_normalized():
    entry = _entry(organization="IEEE Computer Society")
    result = normalize_entry_publisher(entry)
    assert result["organization"] == "IEEE"


def test_entry_empty_publisher_removed():
    entry = _entry(publisher="")
    result = normalize_entry_publisher(entry)
    assert "publisher" not in result


def test_entry_missing_publisher_unchanged():
    entry = _entry(title="A Paper")
    result = normalize_entry_publisher(entry)
    assert "publisher" not in result
    assert result["title"] == "A Paper"


def test_entry_original_not_mutated():
    entry = _entry(publisher="Elsevier B.V.")
    original = dict(entry)
    normalize_entry_publisher(entry)
    assert entry == original


# ---------------------------------------------------------------------------
# normalize_bibliography_publishers
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalized():
    bib = [
        _entry(publisher="Springer-Verlag"),
        _entry(publisher="ACM Press"),
        _entry(publisher="Unknown House"),
    ]
    result = normalize_bibliography_publishers(bib)
    assert result[0]["publisher"] == "Springer"
    assert result[1]["publisher"] == "ACM"
    assert result[2]["publisher"] == "Unknown House"


def test_bibliography_empty_list():
    assert normalize_bibliography_publishers([]) == []
