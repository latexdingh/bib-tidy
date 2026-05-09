"""Tests for bibtidy.keyword_normalizer."""

from __future__ import annotations

import pytest

from bibtidy.keyword_normalizer import (
    normalize_keywords,
    normalize_entry_keywords,
    normalize_bibliography_keywords,
)


def _entry(keywords: str | None = None) -> dict:
    e = {"type": "article", "key": "k1", "fields": {}}
    if keywords is not None:
        e["fields"]["keywords"] = keywords  # type: ignore[index]
    # The normalizer accesses entry["keywords"] directly like other normalizers
    if keywords is not None:
        e["keywords"] = keywords  # type: ignore[assignment]
    return e


# ---------------------------------------------------------------------------
# normalize_keywords
# ---------------------------------------------------------------------------

def test_normalize_keywords_deduplicates():
    result = normalize_keywords("machine learning; ML; machine learning")
    assert result.count("machine learning") == 1


def test_normalize_keywords_sorts_alphabetically():
    result = normalize_keywords("zebra; apple; mango")
    assert result == "apple; mango; zebra"


def test_normalize_keywords_comma_separated():
    result = normalize_keywords("deep learning, neural networks, deep learning")
    assert "deep learning" in result
    assert result.count("deep learning") == 1


def test_normalize_keywords_pipe_separated():
    result = normalize_keywords("alpha|beta|gamma")
    tokens = [t.strip() for t in result.split(";")]
    assert "alpha" in tokens
    assert "beta" in tokens
    assert "gamma" in tokens


def test_normalize_keywords_collapses_whitespace():
    result = normalize_keywords("  deep   learning ;  NLP  ")
    assert "deep learning" in result
    assert "NLP" in result


def test_normalize_keywords_case_insensitive_dedup():
    result = normalize_keywords("NLP; nlp; Nlp")
    parts = [p.strip() for p in result.split(";")]
    assert len(parts) == 1


def test_normalize_keywords_custom_separator():
    result = normalize_keywords("b; a; c", separator=", ")
    assert result == "a, b, c"


def test_normalize_keywords_empty_string():
    result = normalize_keywords("")
    assert result == ""


# ---------------------------------------------------------------------------
# normalize_entry_keywords
# ---------------------------------------------------------------------------

def test_normalize_entry_keywords_modifies_field():
    entry = {"type": "article", "key": "e1", "keywords": "b; a; a"}
    result = normalize_entry_keywords(entry)
    assert result["keywords"] == "a; b"


def test_normalize_entry_keywords_missing_field_unchanged():
    entry = {"type": "article", "key": "e1"}
    result = normalize_entry_keywords(entry)
    assert "keywords" not in result


def test_normalize_entry_keywords_does_not_mutate_original():
    entry = {"type": "article", "key": "e1", "keywords": "z; a"}
    original_kw = entry["keywords"]
    normalize_entry_keywords(entry)
    assert entry["keywords"] == original_kw


# ---------------------------------------------------------------------------
# normalize_bibliography_keywords
# ---------------------------------------------------------------------------

def test_normalize_bibliography_keywords_applies_to_all():
    bib = [
        {"type": "article", "key": "e1", "keywords": "b; a"},
        {"type": "article", "key": "e2", "keywords": "z; m; z"},
    ]
    result = normalize_bibliography_keywords(bib)
    assert result[0]["keywords"] == "a; b"
    assert result[1]["keywords"] == "m; z"


def test_normalize_bibliography_keywords_empty_list():
    assert normalize_bibliography_keywords([]) == []
