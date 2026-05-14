"""Tests for bibtidy.arxiv_normalizer."""

import pytest
from bibtidy.arxiv_normalizer import (
    extract_arxiv_id,
    normalize_arxiv,
    normalize_entry_arxiv,
    normalize_bibliography_arxiv,
)


# ---------------------------------------------------------------------------
# extract_arxiv_id
# ---------------------------------------------------------------------------

def test_extract_bare_new_style():
    assert extract_arxiv_id("2301.12345") == "2301.12345"


def test_extract_bare_new_style_with_version():
    assert extract_arxiv_id("2301.12345v2") == "2301.12345v2"


def test_extract_with_arxiv_prefix_colon():
    assert extract_arxiv_id("arXiv:2301.12345") == "2301.12345"


def test_extract_with_arxiv_prefix_slash():
    assert extract_arxiv_id("arxiv/2301.12345") == "2301.12345"


def test_extract_old_style():
    result = extract_arxiv_id("math/0612345")
    assert result == "math/0612345"


def test_extract_from_abs_url():
    assert extract_arxiv_id("https://arxiv.org/abs/2301.12345") == "2301.12345"


def test_extract_from_pdf_url():
    assert extract_arxiv_id("https://arxiv.org/pdf/2301.12345v1") == "2301.12345v1"


def test_extract_returns_none_for_empty():
    assert extract_arxiv_id("") is None


def test_extract_returns_none_for_unrelated_string():
    assert extract_arxiv_id("https://example.com/paper") is None


# ---------------------------------------------------------------------------
# normalize_arxiv
# ---------------------------------------------------------------------------

def test_normalize_arxiv_bare_id():
    assert normalize_arxiv("2301.12345") == "2301.12345"


def test_normalize_arxiv_none_input():
    assert normalize_arxiv(None) is None


def test_normalize_arxiv_url_input():
    assert normalize_arxiv("https://arxiv.org/abs/1901.00001") == "1901.00001"


# ---------------------------------------------------------------------------
# normalize_entry_arxiv
# ---------------------------------------------------------------------------

def _entry(fields: dict) -> dict:
    return {"type": "article", "key": "test2024", "fields": fields}


def test_normalize_entry_sets_eprint():
    e = _entry({"eprint": "arXiv:2301.12345"})
    result = normalize_entry_arxiv(e)
    assert result["fields"]["eprint"] == "2301.12345"


def test_normalize_entry_sets_archiveprefix():
    e = _entry({"eprint": "2301.12345"})
    result = normalize_entry_arxiv(e)
    assert result["fields"]["archiveprefix"] == "arXiv"


def test_normalize_entry_removes_arxivid_alias():
    e = _entry({"arxivid": "2301.12345", "eprint": ""})
    result = normalize_entry_arxiv(e)
    assert "arxivid" not in result["fields"]
    assert result["fields"]["eprint"] == "2301.12345"


def test_normalize_entry_falls_back_to_url():
    e = _entry({"url": "https://arxiv.org/abs/2210.00001"})
    result = normalize_entry_arxiv(e)
    assert result["fields"]["eprint"] == "2210.00001"


def test_normalize_entry_no_arxiv_unchanged():
    e = _entry({"title": "Some paper", "journal": "Nature"})
    result = normalize_entry_arxiv(e)
    assert result == e


def test_normalize_entry_does_not_mutate_original():
    fields = {"eprint": "arXiv:2301.12345"}
    e = _entry(fields)
    normalize_entry_arxiv(e)
    assert fields["eprint"] == "arXiv:2301.12345"  # unchanged


# ---------------------------------------------------------------------------
# normalize_bibliography_arxiv
# ---------------------------------------------------------------------------

def test_normalize_bibliography_applies_to_all():
    bib = [
        _entry({"eprint": "arXiv:2301.00001"}),
        _entry({"eprint": "arXiv:2301.00002"}),
    ]
    result = normalize_bibliography_arxiv(bib)
    assert result[0]["fields"]["eprint"] == "2301.00001"
    assert result[1]["fields"]["eprint"] == "2301.00002"


def test_normalize_bibliography_empty():
    assert normalize_bibliography_arxiv([]) == []
