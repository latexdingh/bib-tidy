"""
Tests for bibtidy.type_normalizer
"""

import pytest
from bibtidy.type_normalizer import (
    normalize_type,
    normalize_entry_type,
    normalize_bibliography_types,
)


# ---------------------------------------------------------------------------
# normalize_type
# ---------------------------------------------------------------------------

def test_normalize_type_article_lowercase():
    assert normalize_type("article") == "article"


def test_normalize_type_article_uppercase():
    assert normalize_type("ARTICLE") == "article"


def test_normalize_type_journal_alias():
    assert normalize_type("journal") == "article"


def test_normalize_type_conference_alias():
    assert normalize_type("conference") == "inproceedings"


def test_normalize_type_phd_alias():
    assert normalize_type("phd") == "phdthesis"


def test_normalize_type_masters_alias():
    assert normalize_type("mastersthesis") == "mastersthesis"


def test_normalize_type_msc_alias():
    assert normalize_type("mscthesis") == "mastersthesis"


def test_normalize_type_report_alias():
    assert normalize_type("report") == "techreport"


def test_normalize_type_preprint_alias():
    assert normalize_type("preprint") == "unpublished"


def test_normalize_type_unknown_returns_lowercase():
    assert normalize_type("CustomType") == "customtype"


def test_normalize_type_none_returns_none():
    assert normalize_type(None) is None


def test_normalize_type_empty_string_returns_none():
    assert normalize_type("") is None


def test_normalize_type_whitespace_only_returns_none():
    assert normalize_type("   ") is None


def test_normalize_type_strips_whitespace():
    assert normalize_type("  article  ") == "article"


def test_normalize_type_hyphenated_alias():
    # e.g. "journal-article" should collapse to "journalarticle" -> "article"
    assert normalize_type("journal-article") == "article"


# ---------------------------------------------------------------------------
# normalize_entry_type
# ---------------------------------------------------------------------------

def test_normalize_entry_type_updates_type_field():
    entry = {"type": "conference", "key": "Smith2020", "fields": {}}
    result = normalize_entry_type(entry)
    assert result["type"] == "inproceedings"


def test_normalize_entry_type_does_not_mutate_original():
    entry = {"type": "conference", "key": "Smith2020", "fields": {}}
    normalize_entry_type(entry)
    assert entry["type"] == "conference"


def test_normalize_entry_type_preserves_other_fields():
    entry = {"type": "article", "key": "Doe2021", "fields": {"title": "Foo"}}
    result = normalize_entry_type(entry)
    assert result["key"] == "Doe2021"
    assert result["fields"] == {"title": "Foo"}


# ---------------------------------------------------------------------------
# normalize_bibliography_types
# ---------------------------------------------------------------------------

def test_normalize_bibliography_types_all_entries():
    bib = [
        {"type": "journal", "key": "A", "fields": {}},
        {"type": "phd", "key": "B", "fields": {}},
        {"type": "misc", "key": "C", "fields": {}},
    ]
    result = normalize_bibliography_types(bib)
    assert [e["type"] for e in result] == ["article", "phdthesis", "misc"]


def test_normalize_bibliography_types_empty_list():
    assert normalize_bibliography_types([]) == []
