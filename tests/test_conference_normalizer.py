"""
Tests for bibtidy.conference_normalizer.
"""

from __future__ import annotations

import pytest

from bibtidy.conference_normalizer import (
    normalize_conference,
    normalize_entry_conference,
    normalize_bibliography_conferences,
)


# ---------------------------------------------------------------------------
# normalize_conference
# ---------------------------------------------------------------------------

def test_normalize_known_icml_abbreviation():
    assert normalize_conference("ICML") == "International Conference on Machine Learning"


def test_normalize_known_neurips_abbreviation():
    assert normalize_conference("NeurIPS") == "Neural Information Processing Systems"


def test_normalize_known_nips_abbreviation():
    assert normalize_conference("NIPS") == "Neural Information Processing Systems"


def test_normalize_known_cvpr_abbreviation():
    assert normalize_conference("CVPR") == "IEEE Conference on Computer Vision and Pattern Recognition"


def test_normalize_case_insensitive():
    assert normalize_conference("icml") == "International Conference on Machine Learning"
    assert normalize_conference("cvpr") == "IEEE Conference on Computer Vision and Pattern Recognition"


def test_normalize_full_canonical_name_unchanged():
    name = "International Conference on Machine Learning"
    assert normalize_conference(name) == name


def test_normalize_unknown_returns_original():
    assert normalize_conference("Some Unknown Workshop") == "Some Unknown Workshop"


def test_normalize_none_returns_none():
    assert normalize_conference(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_conference("") is None


def test_normalize_strips_braces():
    assert normalize_conference("{ICML}") == "International Conference on Machine Learning"


def test_normalize_collapses_whitespace():
    assert normalize_conference("  ICML  ") == "International Conference on Machine Learning"


# ---------------------------------------------------------------------------
# normalize_entry_conference
# ---------------------------------------------------------------------------

def _entry(**fields):
    return {"type": "inproceedings", "key": "k", **fields}


def test_entry_booktitle_normalised():
    e = _entry(booktitle="ICML")
    result = normalize_entry_conference(e)
    assert result["booktitle"] == "International Conference on Machine Learning"


def test_entry_journal_normalised_when_in_fields():
    e = _entry(journal="NIPS")
    result = normalize_entry_conference(e, fields=["journal"])
    assert result["journal"] == "Neural Information Processing Systems"


def test_entry_other_fields_untouched():
    e = _entry(booktitle="ICML", title="My Paper", year="2023")
    result = normalize_entry_conference(e)
    assert result["title"] == "My Paper"
    assert result["year"] == "2023"


def test_entry_returns_new_dict():
    e = _entry(booktitle="ICML")
    result = normalize_entry_conference(e)
    assert result is not e


def test_entry_missing_field_not_added():
    e = _entry(title="No booktitle here")
    result = normalize_entry_conference(e)
    assert "booktitle" not in result


# ---------------------------------------------------------------------------
# normalize_bibliography_conferences
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalised():
    bib = [
        _entry(booktitle="ICML"),
        _entry(booktitle="CVPR"),
    ]
    result = normalize_bibliography_conferences(bib)
    assert result[0]["booktitle"] == "International Conference on Machine Learning"
    assert result[1]["booktitle"] == "IEEE Conference on Computer Vision and Pattern Recognition"


def test_bibliography_empty_list():
    assert normalize_bibliography_conferences([]) == []


def test_bibliography_returns_new_list():
    bib = [_entry(booktitle="ICML")]
    result = normalize_bibliography_conferences(bib)
    assert result is not bib
