"""Tests for bibtidy.institution_normalizer."""

import pytest
from bibtidy.institution_normalizer import (
    normalize_institution,
    normalize_entry_institution,
    normalize_bibliography_institutions,
)


def _entry(institution=None, organization=None, school=None):
    fields = {}
    if institution is not None:
        fields["institution"] = institution
    if organization is not None:
        fields["organization"] = organization
    if school is not None:
        fields["school"] = school
    return {"type": "techreport", "key": "k", "fields": fields}


# ---------------------------------------------------------------------------
# normalize_institution
# ---------------------------------------------------------------------------

def test_normalize_known_mit_abbrev():
    assert normalize_institution("MIT") == "Massachusetts Institute of Technology"


def test_normalize_known_mit_full():
    assert normalize_institution("Massachusetts Institute of Technology") == \
        "Massachusetts Institute of Technology"


def test_normalize_known_stanford():
    assert normalize_institution("Stanford") == "Stanford University"


def test_normalize_known_eth_umlaut():
    assert normalize_institution("ETH Zürich") == "ETH Zurich"


def test_normalize_known_berkeley_alias():
    assert normalize_institution("UC Berkeley") == "University of California, Berkeley"


def test_normalize_unknown_returns_cleaned():
    assert normalize_institution("  Some Random Lab  ") == "Some Random Lab"


def test_normalize_strips_braces():
    assert normalize_institution("{Stanford}") == "Stanford University"


def test_normalize_collapses_whitespace():
    result = normalize_institution("Stanford   University")
    assert result == "Stanford University"


def test_normalize_all_uppercase_unknown_title_cased():
    result = normalize_institution("SOME UNKNOWN PLACE")
    assert result == "Some Unknown Place"


def test_normalize_none_returns_none():
    assert normalize_institution(None) is None


def test_normalize_empty_returns_none():
    assert normalize_institution("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_institution("   ") is None


# ---------------------------------------------------------------------------
# normalize_entry_institution
# ---------------------------------------------------------------------------

def test_entry_normalizes_institution_field():
    entry = _entry(institution="MIT")
    result = normalize_entry_institution(entry)
    assert result["fields"]["institution"] == "Massachusetts Institute of Technology"


def test_entry_normalizes_school_field():
    entry = _entry(school="stanford")
    result = normalize_entry_institution(entry)
    assert result["fields"]["school"] == "Stanford University"


def test_entry_does_not_mutate_original():
    entry = _entry(institution="MIT")
    normalize_entry_institution(entry)
    assert entry["fields"]["institution"] == "MIT"


def test_entry_missing_field_unchanged():
    entry = _entry(organization="ACM")
    result = normalize_entry_institution(entry)
    assert "institution" not in result["fields"]


# ---------------------------------------------------------------------------
# normalize_bibliography_institutions
# ---------------------------------------------------------------------------

def test_bibliography_normalizes_all_entries():
    bib = [_entry(institution="MIT"), _entry(school="Oxford")]
    result = normalize_bibliography_institutions(bib)
    assert result[0]["fields"]["institution"] == "Massachusetts Institute of Technology"
    assert result[1]["fields"]["school"] == "University of Oxford"


def test_bibliography_returns_new_list():
    bib = [_entry(institution="MIT")]
    result = normalize_bibliography_institutions(bib)
    assert result is not bib


def test_bibliography_empty_returns_empty():
    assert normalize_bibliography_institutions([]) == []
