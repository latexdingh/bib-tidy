"""Tests for bibtidy.deduplicator."""

import pytest
from bibtidy.deduplicator import are_duplicates, deduplicate, _title_similarity


def _entry(key, title='', year='', doi='', extra_fields=None):
    fields = {'title': title, 'year': year}
    if doi:
        fields['doi'] = doi
    if extra_fields:
        fields.update(extra_fields)
    return {'type': 'article', 'key': key, 'fields': fields}


# --- _title_similarity ---

def test_title_similarity_identical():
    assert _title_similarity('Deep Learning', 'Deep Learning') == 1.0


def test_title_similarity_different():
    score = _title_similarity('Deep Learning', 'Quantum Computing')
    assert score < 0.5


def test_title_similarity_ignores_punctuation():
    score = _title_similarity('Deep Learning!', 'Deep Learning')
    assert score == 1.0


# --- are_duplicates ---

def test_duplicates_same_doi():
    a = _entry('a1', doi='10.1234/abc')
    b = _entry('b1', doi='10.1234/abc')
    assert are_duplicates(a, b) is True


def test_not_duplicates_different_doi():
    a = _entry('a1', doi='10.1234/abc')
    b = _entry('b1', doi='10.9999/xyz')
    assert are_duplicates(a, b) is False


def test_duplicates_similar_title_same_year():
    a = _entry('a1', title='A Survey of Deep Learning Methods', year='2020')
    b = _entry('b1', title='A Survey of Deep Learning Methods', year='2020')
    assert are_duplicates(a, b) is True


def test_not_duplicates_similar_title_different_year():
    a = _entry('a1', title='A Survey of Deep Learning Methods', year='2019')
    b = _entry('b1', title='A Survey of Deep Learning Methods', year='2021')
    assert are_duplicates(a, b) is False


def test_not_duplicates_missing_title():
    a = _entry('a1', title='', year='2020')
    b = _entry('b1', title='Deep Learning', year='2020')
    assert are_duplicates(a, b) is False


def test_not_duplicates_completely_different():
    a = _entry('a1', title='Quantum Computing Advances', year='2021')
    b = _entry('b1', title='History of the Roman Empire', year='2021')
    assert are_duplicates(a, b) is False


# --- deduplicate ---

def test_deduplicate_removes_exact_doi_duplicate():
    entries = [
        _entry('a1', title='Deep Learning', year='2020', doi='10.1/x'),
        _entry('b1', title='Deep Learning', year='2020', doi='10.1/x'),
    ]
    result = deduplicate(entries)
    assert len(result) == 1


def test_deduplicate_keeps_richer_entry():
    a = _entry('a1', title='Deep Learning', year='2020', doi='10.1/x',
               extra_fields={'journal': 'Nature', 'volume': '5'})
    b = _entry('b1', title='Deep Learning', year='2020', doi='10.1/x')
    result = deduplicate([b, a])
    assert len(result) == 1
    assert result[0]['fields'].get('journal') == 'Nature'


def test_deduplicate_preserves_unique_entries():
    entries = [
        _entry('a1', title='Deep Learning', year='2020', doi='10.1/a'),
        _entry('b1', title='Quantum Computing', year='2021', doi='10.1/b'),
        _entry('c1', title='Graph Neural Networks', year='2022', doi='10.1/c'),
    ]
    result = deduplicate(entries)
    assert len(result) == 3


def test_deduplicate_empty_list():
    assert deduplicate([]) == []
