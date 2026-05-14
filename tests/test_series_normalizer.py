"""Tests for bibtidy.series_normalizer."""

import pytest
from bibtidy.series_normalizer import (
    normalize_series,
    normalize_entry_series,
    normalize_bibliography_series,
)


# ---------------------------------------------------------------------------
# normalize_series
# ---------------------------------------------------------------------------

def test_normalize_series_returns_none_for_none():
    assert normalize_series(None) is None


def test_normalize_series_returns_none_for_empty():
    assert normalize_series("") is None
    assert normalize_series("   ") is None


def test_normalize_series_strips_braces():
    assert normalize_series("{LNCS}") == "Lecture Notes in Computer Science"


def test_normalize_series_lncs_alias():
    assert normalize_series("lncs") == "Lecture Notes in Computer Science"


def test_normalize_series_lncs_full_name():
    result = normalize_series("Lecture Notes in Computer Science")
    assert result == "Lecture Notes in Computer Science"


def test_normalize_series_lnai_alias():
    assert normalize_series("LNAI") == "Lecture Notes in Artificial Intelligence"


def test_normalize_series_pmlr_alias():
    assert normalize_series("pmlr") == "Proceedings of Machine Learning Research"


def test_normalize_series_neurips_alias():
    assert normalize_series("NeurIPS") == "Advances in Neural Information Processing Systems"


def test_normalize_series_nips_alias():
    assert normalize_series("nips") == "Advances in Neural Information Processing Systems"


def test_normalize_series_collapses_whitespace():
    result = normalize_series("  Lecture   Notes  in  Computer   Science  ")
    assert result == "Lecture Notes in Computer Science"


def test_normalize_series_unknown_title_cased():
    result = normalize_series("my custom series")
    assert result == "My Custom Series"


def test_normalize_series_unknown_preserves_known_caps_via_title():
    result = normalize_series("oxford studies in philosophy")
    assert result == "Oxford Studies In Philosophy"


# ---------------------------------------------------------------------------
# normalize_entry_series
# ---------------------------------------------------------------------------

def test_normalize_entry_series_normalizes_field():
    entry = {"ENTRYTYPE": "book", "ID": "k1", "series": "lncs"}
    result = normalize_entry_series(entry)
    assert result["series"] == "Lecture Notes in Computer Science"


def test_normalize_entry_series_removes_empty_field():
    entry = {"ENTRYTYPE": "book", "ID": "k1", "series": ""}
    result = normalize_entry_series(entry)
    assert "series" not in result


def test_normalize_entry_series_leaves_other_fields_unchanged():
    entry = {"ENTRYTYPE": "book", "ID": "k1", "series": "pmlr", "title": "My Book"}
    result = normalize_entry_series(entry)
    assert result["title"] == "My Book"
    assert result["ENTRYTYPE"] == "book"


def test_normalize_entry_series_no_series_field_unchanged():
    entry = {"ENTRYTYPE": "article", "ID": "k2", "title": "A Paper"}
    result = normalize_entry_series(entry)
    assert result == entry


def test_normalize_entry_series_does_not_mutate_original():
    entry = {"ENTRYTYPE": "book", "ID": "k1", "series": "lncs"}
    _ = normalize_entry_series(entry)
    assert entry["series"] == "lncs"


# ---------------------------------------------------------------------------
# normalize_bibliography_series
# ---------------------------------------------------------------------------

def test_normalize_bibliography_series_processes_all_entries():
    entries = [
        {"ENTRYTYPE": "book", "ID": "a", "series": "lncs"},
        {"ENTRYTYPE": "book", "ID": "b", "series": "pmlr"},
    ]
    result = normalize_bibliography_series(entries)
    assert result[0]["series"] == "Lecture Notes in Computer Science"
    assert result[1]["series"] == "Proceedings of Machine Learning Research"


def test_normalize_bibliography_series_empty_list():
    assert normalize_bibliography_series([]) == []


def test_normalize_bibliography_series_returns_new_list():
    entries = [{"ENTRYTYPE": "book", "ID": "a", "series": "lncs"}]
    result = normalize_bibliography_series(entries)
    assert result is not entries
