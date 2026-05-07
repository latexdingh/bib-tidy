"""
Tests for bibtidy.isbn_normalizer.
"""

import pytest
from bibtidy.isbn_normalizer import (
    normalize_isbn,
    normalize_entry_isbn,
    normalize_bibliography_isbns,
    _isbn10_check,
    _isbn13_check,
    _isbn10_to_isbn13,
)


# ---------------------------------------------------------------------------
# _isbn10_check
# ---------------------------------------------------------------------------

def test_isbn10_check_valid():
    assert _isbn10_check('0306406152') is True


def test_isbn10_check_valid_x():
    assert _isbn10_check('047191595X') is True


def test_isbn10_check_invalid():
    assert _isbn10_check('0306406151') is False


def test_isbn10_check_wrong_length():
    assert _isbn10_check('030640615') is False


# ---------------------------------------------------------------------------
# _isbn13_check
# ---------------------------------------------------------------------------

def test_isbn13_check_valid():
    assert _isbn13_check('9780306406157') is True


def test_isbn13_check_invalid():
    assert _isbn13_check('9780306406158') is False


def test_isbn13_check_wrong_length():
    assert _isbn13_check('978030640615') is False


def test_isbn13_check_non_digit():
    assert _isbn13_check('978030640615X') is False


# ---------------------------------------------------------------------------
# _isbn10_to_isbn13
# ---------------------------------------------------------------------------

def test_isbn10_to_isbn13_conversion():
    result = _isbn10_to_isbn13('0306406152')
    assert result == '9780306406157'
    assert _isbn13_check(result) is True


# ---------------------------------------------------------------------------
# normalize_isbn
# ---------------------------------------------------------------------------

def test_normalize_isbn13_plain():
    assert normalize_isbn('9780306406157') == '9780306406157'


def test_normalize_isbn13_with_hyphens():
    assert normalize_isbn('978-0-306-40615-7') == '9780306406157'


def test_normalize_isbn10_converts_to_isbn13():
    assert normalize_isbn('0-306-40615-2') == '9780306406157'


def test_normalize_isbn_invalid_returns_none():
    assert normalize_isbn('0000000000') is None


def test_normalize_isbn_empty_returns_none():
    assert normalize_isbn('') is None


# ---------------------------------------------------------------------------
# normalize_entry_isbn
# ---------------------------------------------------------------------------

def _entry(isbn=''):
    return {'type': 'book', 'key': 'Smith2020', 'fields': {'title': 'A Book', 'isbn': isbn}}


def test_normalize_entry_isbn_valid():
    result = normalize_entry_isbn(_entry('978-0-306-40615-7'))
    assert result['fields']['isbn'] == '9780306406157'


def test_normalize_entry_isbn_invalid_leaves_unchanged():
    result = normalize_entry_isbn(_entry('0000000000'))
    assert result['fields']['isbn'] == '0000000000'


def test_normalize_entry_isbn_missing_field():
    entry = {'type': 'book', 'key': 'X', 'fields': {'title': 'No ISBN'}}
    result = normalize_entry_isbn(entry)
    assert 'isbn' not in result['fields']


def test_normalize_entry_isbn_does_not_mutate():
    original = _entry('978-0-306-40615-7')
    normalize_entry_isbn(original)
    assert original['fields']['isbn'] == '978-0-306-40615-7'


# ---------------------------------------------------------------------------
# normalize_bibliography_isbns
# ---------------------------------------------------------------------------

def test_normalize_bibliography_isbns_multiple():
    entries = [
        _entry('978-0-306-40615-7'),
        _entry('0-306-40615-2'),
    ]
    results = normalize_bibliography_isbns(entries)
    assert all(e['fields']['isbn'] == '9780306406157' for e in results)


def test_normalize_bibliography_isbns_empty():
    assert normalize_bibliography_isbns([]) == []
