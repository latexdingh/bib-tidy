"""
Tests for bibtidy.affiliation_normalizer.
"""

import pytest
from bibtidy.affiliation_normalizer import (
    normalize_affiliation,
    normalize_entry_affiliation,
    normalize_bibliography_affiliations,
)


# ---------------------------------------------------------------------------
# normalize_affiliation
# ---------------------------------------------------------------------------

def test_normalize_known_mit_abbrev():
    assert normalize_affiliation("MIT") == "Massachusetts Institute of Technology"


def test_normalize_known_mit_full():
    assert normalize_affiliation("Massachusetts Institute of Technology") == \
        "Massachusetts Institute of Technology"


def test_normalize_known_stanford():
    assert normalize_affiliation("Stanford Univ.") == "Stanford University"


def test_normalize_known_cmu():
    assert normalize_affiliation("CMU") == "Carnegie Mellon University"


def test_normalize_known_eth_umlaut():
    assert normalize_affiliation("ETH Zürich") == "ETH Zurich"


def test_normalize_known_eth_ascii():
    assert normalize_affiliation("ETH Zurich") == "ETH Zurich"


def test_normalize_known_uc_berkeley():
    assert normalize_affiliation("UC Berkeley") == "University of California, Berkeley"


def test_normalize_known_oxford():
    assert normalize_affiliation("Oxford") == "University of Oxford"


def test_normalize_unknown_returns_cleaned():
    result = normalize_affiliation("  Some  Random   University  ")
    assert result == "Some Random University"


def test_normalize_strips_braces():
    assert normalize_affiliation("{Stanford University}") == "Stanford University"


def test_normalize_none_returns_none():
    assert normalize_affiliation(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_affiliation("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_affiliation("   ") is None


def test_normalize_case_insensitive():
    assert normalize_affiliation("mit") == "Massachusetts Institute of Technology"
    assert normalize_affiliation("MIT") == "Massachusetts Institute of Technology"
    assert normalize_affiliation("Mit") == "Massachusetts Institute of Technology"


# ---------------------------------------------------------------------------
# normalize_entry_affiliation
# ---------------------------------------------------------------------------

def _entry(**fields) -> dict:
    return {"type": "article", "key": "k", **fields}


def test_entry_affiliation_normalized():
    e = _entry(affiliation="CMU")
    result = normalize_entry_affiliation(e)
    assert result["affiliation"] == "Carnegie Mellon University"


def test_entry_missing_affiliation_unchanged():
    e = _entry(title="No affiliation")
    result = normalize_entry_affiliation(e)
    assert "affiliation" not in result


def test_entry_empty_affiliation_removed():
    e = _entry(affiliation="")
    result = normalize_entry_affiliation(e)
    assert "affiliation" not in result


def test_entry_does_not_mutate_original():
    e = _entry(affiliation="MIT")
    _ = normalize_entry_affiliation(e)
    assert e["affiliation"] == "MIT"


# ---------------------------------------------------------------------------
# normalize_bibliography_affiliations
# ---------------------------------------------------------------------------

def test_bibliography_normalizes_all_entries():
    bib = [
        _entry(affiliation="MIT"),
        _entry(affiliation="Stanford"),
    ]
    result = normalize_bibliography_affiliations(bib)
    assert result[0]["affiliation"] == "Massachusetts Institute of Technology"
    assert result[1]["affiliation"] == "Stanford University"


def test_bibliography_empty():
    assert normalize_bibliography_affiliations([]) == []


def test_bibliography_custom_field():
    bib = [_entry(institution_affil="CMU")]
    result = normalize_bibliography_affiliations(bib, field="institution_affil")
    assert result[0]["institution_affil"] == "Carnegie Mellon University"
