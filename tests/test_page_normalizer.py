import pytest
from bibtidy.page_normalizer import (
    normalize_pages,
    normalize_entry_pages,
    normalize_bibliography_pages,
)


# ---------------------------------------------------------------------------
# normalize_pages
# ---------------------------------------------------------------------------

def test_normalize_single_page():
    assert normalize_pages("5") == "5"


def test_normalize_already_canonical_range():
    assert normalize_pages("5--10") == "5--10"


def test_normalize_single_hyphen_range():
    assert normalize_pages("5-10") == "5--10"


def test_normalize_em_dash_range():
    assert normalize_pages("5\u201410") == "5--10"


def test_normalize_en_dash_range():
    assert normalize_pages("5\u201310") == "5--10"


def test_normalize_spaces_around_hyphen():
    assert normalize_pages("5 - 10") == "5--10"


def test_normalize_reversed_range_is_sorted():
    assert normalize_pages("10--5") == "5--10"


def test_normalize_page_with_letter_prefix():
    assert normalize_pages("A1--A9") == "A1--A9"


def test_normalize_electronic_id():
    """e.g. 'e12345' should pass through as-is."""
    assert normalize_pages("e12345") == "e12345"


def test_normalize_empty_string_returns_none():
    assert normalize_pages("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_pages("   ") is None


def test_normalize_strips_surrounding_whitespace():
    assert normalize_pages("  3--7  ") == "3--7"


# ---------------------------------------------------------------------------
# normalize_entry_pages
# ---------------------------------------------------------------------------

def _entry(pages=None, **extra_fields):
    fields = {"title": "Test"}
    if pages is not None:
        fields["pages"] = pages
    fields.update(extra_fields)
    return {"type": "article", "key": "test2024", "fields": fields}


def test_entry_pages_normalized():
    entry = _entry(pages="1-9")
    result = normalize_entry_pages(entry)
    assert result["fields"]["pages"] == "1--9"


def test_entry_without_pages_unchanged():
    entry = _entry()
    result = normalize_entry_pages(entry)
    assert "pages" not in result["fields"]


def test_entry_is_not_mutated():
    entry = _entry(pages="3-8")
    original_pages = entry["fields"]["pages"]
    normalize_entry_pages(entry)
    assert entry["fields"]["pages"] == original_pages


# ---------------------------------------------------------------------------
# normalize_bibliography_pages
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalized():
    entries = [
        _entry(pages="1-5"),
        _entry(pages="10-20"),
    ]
    results = normalize_bibliography_pages(entries)
    assert results[0]["fields"]["pages"] == "1--5"
    assert results[1]["fields"]["pages"] == "10--20"


def test_bibliography_returns_new_list():
    entries = [_entry(pages="1-5")]
    results = normalize_bibliography_pages(entries)
    assert results is not entries
