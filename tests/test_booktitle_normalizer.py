"""
Tests for bibtidy.booktitle_normalizer
"""

from __future__ import annotations

import pytest

from bibtidy.booktitle_normalizer import (
    normalize_booktitle,
    normalize_entry_booktitle,
    normalize_bibliography_booktitles,
)


# ---------------------------------------------------------------------------
# normalize_booktitle
# ---------------------------------------------------------------------------

def test_normalize_known_alias_neurips():
    result = normalize_booktitle("neurips")
    assert result == "Advances in Neural Information Processing Systems"


def test_normalize_known_alias_case_insensitive():
    result = normalize_booktitle("NeurIPS")
    assert result == "Advances in Neural Information Processing Systems"


def test_normalize_known_alias_nips():
    result = normalize_booktitle("NIPS")
    assert result == "Advances in Neural Information Processing Systems"


def test_normalize_known_alias_icml():
    result = normalize_booktitle("ICML")
    assert result == "Proceedings of the International Conference on Machine Learning"


def test_normalize_known_alias_cvpr():
    result = normalize_booktitle("cvpr")
    assert "Computer Vision" in normalize_booktitle("cvpr")


def test_normalize_unknown_applies_title_case():
    result = normalize_booktitle("proceedings of the workshop on something")
    assert result == "Proceedings of the Workshop on Something"


def test_normalize_preserves_acronym_case():
    result = normalize_booktitle("workshop on NLP techniques")
    assert "NLP" in result


def test_normalize_strips_braces():
    result = normalize_booktitle("{Proceedings} of the {Conference}")
    assert "{" not in result
    assert "}" not in result


def test_normalize_collapses_whitespace():
    result = normalize_booktitle("Proceedings   of   the   Conference")
    assert "  " not in result


def test_normalize_returns_none_for_none():
    assert normalize_booktitle(None) is None


def test_normalize_returns_none_for_empty_string():
    assert normalize_booktitle("") is None


def test_normalize_returns_none_for_whitespace_only():
    assert normalize_booktitle("   ") is None


# ---------------------------------------------------------------------------
# normalize_entry_booktitle
# ---------------------------------------------------------------------------

def _entry(**fields) -> dict:
    return {"type": "inproceedings", "key": "Smith2024", **fields}


def test_entry_booktitle_normalised():
    e = _entry(booktitle="ICML")
    result = normalize_entry_booktitle(e)
    assert "International Conference on Machine Learning" in result["booktitle"]


def test_entry_without_booktitle_unchanged():
    e = _entry(title="Some Paper")
    result = normalize_entry_booktitle(e)
    assert "booktitle" not in result


def test_entry_empty_booktitle_removed():
    e = _entry(booktitle="")
    result = normalize_entry_booktitle(e)
    assert "booktitle" not in result


def test_entry_original_not_mutated():
    e = _entry(booktitle="icml")
    normalize_entry_booktitle(e)
    assert e["booktitle"] == "icml"


# ---------------------------------------------------------------------------
# normalize_bibliography_booktitles
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalised():
    bib = [
        _entry(booktitle="neurips"),
        _entry(booktitle="aaai"),
    ]
    results = normalize_bibliography_booktitles(bib)
    assert len(results) == 2
    assert "Neural Information Processing" in results[0]["booktitle"]
    assert "AAAI" in results[1]["booktitle"]


def test_bibliography_empty_list():
    assert normalize_bibliography_booktitles([]) == []
