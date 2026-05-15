"""Tests for bibtidy.title_normalizer."""

import pytest
from bibtidy.title_normalizer import (
    normalize_title,
    normalize_entry_title,
    normalize_bibliography_titles,
    _strip_outer_braces,
    _collapse_whitespace,
)


# ---------------------------------------------------------------------------
# _strip_outer_braces
# ---------------------------------------------------------------------------

def test_strip_outer_braces_removes_wrapper():
    assert _strip_outer_braces("{Hello World}") == "Hello World"


def test_strip_outer_braces_no_braces_unchanged():
    assert _strip_outer_braces("Hello World") == "Hello World"


def test_strip_outer_braces_inner_braces_preserved():
    # Outer braces wrap the whole string; inner group stays
    assert _strip_outer_braces("{Hello {World}}") == "Hello {World}"


def test_strip_outer_braces_partial_not_stripped():
    # Brace closes before end — not a simple wrapper
    assert _strip_outer_braces("{A} and B") == "{A} and B"


# ---------------------------------------------------------------------------
# _collapse_whitespace
# ---------------------------------------------------------------------------

def test_collapse_whitespace_multiple_spaces():
    assert _collapse_whitespace("Hello   World") == "Hello World"


def test_collapse_whitespace_tabs_and_newlines():
    assert _collapse_whitespace("Hello\t\nWorld") == "Hello World"


def test_collapse_whitespace_leading_trailing():
    assert _collapse_whitespace("  hello  ") == "hello"


# ---------------------------------------------------------------------------
# normalize_title
# ---------------------------------------------------------------------------

def test_normalize_title_none_returns_none():
    assert normalize_title(None) is None


def test_normalize_title_empty_returns_none():
    assert normalize_title("") is None


def test_normalize_title_strips_braces_by_default():
    assert normalize_title("{Deep Learning}") == "Deep Learning"


def test_normalize_title_no_strip_braces():
    assert normalize_title("{Deep Learning}", strip_braces=False) == "{Deep Learning}"


def test_normalize_title_collapses_whitespace():
    assert normalize_title("Deep   Learning") == "Deep   Learning".replace("   ", " ")


def test_normalize_title_title_case_basic():
    result = normalize_title("deep learning for nlp", title_case=True)
    assert result == "Deep Learning for Nlp"


def test_normalize_title_title_case_first_word_always_capitalized():
    result = normalize_title("the quick brown fox", title_case=True)
    assert result.startswith("The")


def test_normalize_title_title_case_preserves_braced_group():
    result = normalize_title("learning with {BERT} model", title_case=True)
    assert "{BERT}" in result


def test_normalize_title_stopwords_lowercased():
    result = normalize_title("attention is all you need", title_case=True)
    # 'is' and 'you' are stopwords; 'all' is not
    assert "Is" not in result or result.index("Is") == 0  # not first word
    assert result.startswith("Attention")


# ---------------------------------------------------------------------------
# normalize_entry_title
# ---------------------------------------------------------------------------

def _entry(title):
    return {"type": "article", "key": "k", "fields": {"title": title, "year": "2020"}}


def test_normalize_entry_title_updates_field():
    e = _entry("{Neural Networks}")
    result = normalize_entry_title(e)
    assert result["fields"]["title"] == "Neural Networks"


def test_normalize_entry_title_preserves_other_fields():
    e = _entry("{Test}")
    result = normalize_entry_title(e)
    assert result["fields"]["year"] == "2020"


def test_normalize_entry_title_no_title_field():
    e = {"type": "article", "key": "k", "fields": {"year": "2021"}}
    result = normalize_entry_title(e)
    assert "title" not in result["fields"]


def test_normalize_entry_title_does_not_mutate_original():
    e = _entry("{Original}")
    _ = normalize_entry_title(e)
    assert e["fields"]["title"] == "{Original}"


# ---------------------------------------------------------------------------
# normalize_bibliography_titles
# ---------------------------------------------------------------------------

def test_normalize_bibliography_titles_all_entries():
    bib = [_entry("{A}"), _entry("{B}")]
    result = normalize_bibliography_titles(bib)
    assert result[0]["fields"]["title"] == "A"
    assert result[1]["fields"]["title"] == "B"


def test_normalize_bibliography_titles_empty():
    assert normalize_bibliography_titles([]) == []


def test_normalize_bibliography_titles_title_case_propagated():
    bib = [_entry("the art of war")]
    result = normalize_bibliography_titles(bib, title_case=True)
    assert result[0]["fields"]["title"].startswith("The")
