"""Tests for bibtidy.field_filter module."""

from bibtidy.field_filter import filter_fields, filter_bibliography, DEFAULT_KEEP_FIELDS


def _entry(fields=None):
    return {
        "key": "smith2020",
        "entrytype": "article",
        "fields": fields or {
            "title": "A Study",
            "author": "Smith, J.",
            "year": "2020",
            "abstract": "Long abstract text.",
            "keywords": "foo, bar",
            "doi": "10.1234/test",
        },
    }


def test_filter_keep_specific_fields():
    result = filter_fields(_entry(), keep=["title", "author", "year"])
    assert set(result["fields"].keys()) == {"title", "author", "year"}


def test_filter_drop_specific_fields():
    result = filter_fields(_entry(), drop=["abstract", "keywords"])
    assert "abstract" not in result["fields"]
    assert "keywords" not in result["fields"]
    assert "title" in result["fields"]


def test_filter_keep_takes_precedence_over_drop():
    result = filter_fields(_entry(), keep=["title"], drop=["title", "author"])
    assert set(result["fields"].keys()) == {"title"}


def test_filter_keep_empty_list():
    result = filter_fields(_entry(), keep=[])
    assert result["fields"] == {}


def test_filter_no_args_keeps_all():
    entry = _entry()
    result = filter_fields(entry)
    assert result["fields"] == entry["fields"]


def test_filter_preserves_entry_metadata():
    entry = _entry()
    result = filter_fields(entry, keep=["title"])
    assert result["key"] == "smith2020"
    assert result["entrytype"] == "article"


def test_filter_case_insensitive_keep():
    result = filter_fields(_entry(), keep=["TITLE", "DOI"])
    assert "title" in result["fields"]
    assert "doi" in result["fields"]


def test_filter_bibliography_applies_to_all():
    entries = [_entry(), _entry()]
    result = filter_bibliography(entries, drop=["abstract"])
    for e in result:
        assert "abstract" not in e["fields"]
        assert "title" in e["fields"]


def test_default_keep_fields_not_empty():
    assert len(DEFAULT_KEEP_FIELDS) > 0
    assert "title" in DEFAULT_KEEP_FIELDS
    assert "doi" in DEFAULT_KEEP_FIELDS
