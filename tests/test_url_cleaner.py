"""Tests for bibtidy.url_cleaner."""

import pytest
from bibtidy.url_cleaner import (
    clean_url,
    should_drop_url,
    clean_entry_url,
    clean_bibliography_urls,
)


def _entry(url=None, doi=None):
    fields = {}
    if url is not None:
        fields["url"] = url
    if doi is not None:
        fields["doi"] = doi
    return {"type": "article", "key": "test2024", "fields": fields}


# --- clean_url ---

def test_clean_url_removes_utm_params():
    url = "https://example.com/paper?utm_source=google&utm_medium=email&page=1"
    result = clean_url(url)
    assert "utm_source" not in result
    assert "utm_medium" not in result
    assert "page=1" in result


def test_clean_url_removes_fbclid():
    url = "https://journal.org/article?fbclid=abc123&id=42"
    result = clean_url(url)
    assert "fbclid" not in result
    assert "id=42" in result


def test_clean_url_upgrades_doi_http_to_https():
    url = "http://doi.org/10.1000/xyz123"
    result = clean_url(url)
    assert result.startswith("https://doi.org/")


def test_clean_url_upgrades_dx_doi_http_to_https():
    url = "http://dx.doi.org/10.1000/xyz123"
    result = clean_url(url)
    assert result.startswith("https://dx.doi.org/")


def test_clean_url_leaves_plain_url_unchanged():
    url = "https://arxiv.org/abs/2301.00001"
    result = clean_url(url)
    assert result == url


def test_clean_url_strips_whitespace():
    url = "  https://example.com/paper  "
    result = clean_url(url)
    assert result == "https://example.com/paper"


def test_clean_url_empty_string_returns_empty():
    assert clean_url("") == ""


def test_clean_url_none_returns_none():
    assert clean_url(None) is None


# --- should_drop_url ---

def test_should_drop_url_true_when_doi_and_url_present():
    entry = _entry(url="https://example.com", doi="10.1000/xyz")
    assert should_drop_url(entry, drop_if_doi=True) is True


def test_should_drop_url_false_when_no_doi():
    entry = _entry(url="https://example.com")
    assert should_drop_url(entry, drop_if_doi=True) is False


def test_should_drop_url_false_when_flag_disabled():
    entry = _entry(url="https://example.com", doi="10.1000/xyz")
    assert should_drop_url(entry, drop_if_doi=False) is False


# --- clean_entry_url ---

def test_clean_entry_url_removes_tracking():
    entry = _entry(url="https://example.com?utm_source=x&id=1")
    result = clean_entry_url(entry)
    assert "utm_source" not in result["fields"]["url"]
    assert "id=1" in result["fields"]["url"]


def test_clean_entry_url_drops_url_when_doi_present_and_flag_set():
    entry = _entry(url="https://example.com", doi="10.1000/xyz")
    result = clean_entry_url(entry, drop_if_doi=True)
    assert "url" not in result["fields"]
    assert result["fields"]["doi"] == "10.1000/xyz"


def test_clean_entry_url_keeps_url_when_no_doi():
    entry = _entry(url="https://example.com")
    result = clean_entry_url(entry, drop_if_doi=True)
    assert "url" in result["fields"]


def test_clean_entry_url_does_not_mutate_original():
    entry = _entry(url="https://example.com?utm_source=x")
    _ = clean_entry_url(entry)
    assert "utm_source" in entry["fields"]["url"]


# --- clean_bibliography_urls ---

def test_clean_bibliography_urls_processes_all_entries():
    bib = [
        _entry(url="https://a.com?utm_source=x"),
        _entry(url="https://b.com?fbclid=y"),
    ]
    result = clean_bibliography_urls(bib)
    for entry in result:
        assert "utm_source" not in entry["fields"].get("url", "")
        assert "fbclid" not in entry["fields"].get("url", "")


def test_clean_bibliography_urls_empty_list():
    assert clean_bibliography_urls([]) == []
