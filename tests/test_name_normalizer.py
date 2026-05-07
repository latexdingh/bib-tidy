"""
Tests for bibtidy.name_normalizer.
"""

import pytest
from bibtidy.name_normalizer import (
    _normalize_single_name,
    normalize_name_list,
    normalize_entry_names,
    normalize_bibliography_names,
)


# ---------------------------------------------------------------------------
# _normalize_single_name
# ---------------------------------------------------------------------------

def test_normalize_single_name_natural_order():
    assert _normalize_single_name("Alan Turing") == "Turing, Alan"


def test_normalize_single_name_three_tokens():
    assert _normalize_single_name("John von Neumann") == "Neumann, John von"


def test_normalize_single_name_already_comma_format():
    assert _normalize_single_name("Knuth, Donald E.") == "Knuth, Donald E."


def test_normalize_single_name_single_token():
    assert _normalize_single_name("Einstein") == "Einstein"


def test_normalize_single_name_strips_whitespace():
    assert _normalize_single_name("  Ada Lovelace  ") == "Lovelace, Ada"


# ---------------------------------------------------------------------------
# normalize_name_list
# ---------------------------------------------------------------------------

def test_normalize_name_list_single():
    assert normalize_name_list("Donald Knuth") == "Knuth, Donald"


def test_normalize_name_list_multiple():
    result = normalize_name_list("Alan Turing and Claude Shannon")
    assert result == "Turing, Alan and Shannon, Claude"


def test_normalize_name_list_case_insensitive_and():
    result = normalize_name_list("Ada Lovelace AND Charles Babbage")
    assert result == "Lovelace, Ada and Babbage, Charles"


def test_normalize_name_list_mixed_formats():
    result = normalize_name_list("Knuth, Donald and Linus Torvalds")
    assert result == "Knuth, Donald and Torvalds, Linus"


# ---------------------------------------------------------------------------
# normalize_entry_names
# ---------------------------------------------------------------------------

def test_normalize_entry_names_author_field():
    entry = {"key": "k1", "type": "article", "author": "Grace Hopper"}
    result = normalize_entry_names(entry)
    assert result["author"] == "Hopper, Grace"


def test_normalize_entry_names_editor_field():
    entry = {"key": "k2", "type": "book", "editor": "Tim Berners-Lee"}
    result = normalize_entry_names(entry)
    assert result["editor"] == "Berners-Lee, Tim"


def test_normalize_entry_names_does_not_mutate_original():
    entry = {"key": "k3", "type": "article", "author": "Jane Doe"}
    _ = normalize_entry_names(entry)
    assert entry["author"] == "Jane Doe"


def test_normalize_entry_names_missing_field_unchanged():
    entry = {"key": "k4", "type": "misc", "title": "Something"}
    result = normalize_entry_names(entry)
    assert "author" not in result


def test_normalize_entry_names_custom_fields():
    entry = {"key": "k5", "type": "misc", "translator": "Mary Shelley"}
    result = normalize_entry_names(entry, fields=("translator",))
    assert result["translator"] == "Shelley, Mary"


# ---------------------------------------------------------------------------
# normalize_bibliography_names
# ---------------------------------------------------------------------------

def test_normalize_bibliography_names_multiple_entries():
    bib = [
        {"key": "a", "type": "article", "author": "Alan Turing"},
        {"key": "b", "type": "book", "author": "Donald Knuth and Edsger Dijkstra"},
    ]
    result = normalize_bibliography_names(bib)
    assert result[0]["author"] == "Turing, Alan"
    assert result[1]["author"] == "Knuth, Donald and Dijkstra, Edsger"


def test_normalize_bibliography_names_empty():
    assert normalize_bibliography_names([]) == []
