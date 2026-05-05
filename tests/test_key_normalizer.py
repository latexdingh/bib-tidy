"""Tests for bibtidy.key_normalizer."""

import pytest
from bibtidy.key_normalizer import (
    generate_key,
    normalize_key,
    _first_author_lastname,
    _title_word,
)


def test_first_author_lastname_comma_format():
    assert _first_author_lastname('Smith, John') == 'Smith'


def test_first_author_lastname_natural_format():
    assert _first_author_lastname('John Smith') == 'Smith'


def test_first_author_lastname_multiple_authors():
    assert _first_author_lastname('Smith, John and Doe, Jane') == 'Smith'


def test_first_author_lastname_unicode():
    assert _first_author_lastname('Müller, Hans') == 'Muller'


def test_title_word_skips_stopwords():
    word = _title_word('A Deep Learning Approach')
    assert word == 'deep'


def test_title_word_empty():
    assert _title_word('') == ''


def test_generate_key_standard():
    entry = {
        'fields': {
            'author': 'Smith, John',
            'year': '2021',
            'title': 'A Deep Learning Survey',
        }
    }
    assert generate_key(entry) == 'Smith2021deep'


def test_generate_key_no_title():
    entry = {'fields': {'author': 'Smith, John', 'year': '2021', 'title': ''}}
    key = generate_key(entry)
    assert key == 'Smith2021'


def test_generate_key_returns_none_when_insufficient():
    entry = {'fields': {}}
    assert generate_key(entry) is None


def test_normalize_key_updates_entry_key():
    entry = {
        'type': 'article',
        'key': 'old_key',
        'fields': {'author': 'Doe, Jane', 'year': '2020', 'title': 'Neural Networks'},
    }
    result = normalize_key(entry)
    assert result['key'] == 'Doe2020neural'


def test_normalize_key_deduplicates_with_suffix():
    existing = {'Doe2020neural'}
    entry = {
        'type': 'article',
        'key': 'old_key',
        'fields': {'author': 'Doe, Jane', 'year': '2020', 'title': 'Neural Networks'},
    }
    result = normalize_key(entry, existing_keys=existing)
    assert result['key'] == 'Doe2020neurala'
    assert 'Doe2020neurala' in existing


def test_normalize_key_does_not_mutate_original():
    entry = {
        'type': 'article',
        'key': 'original',
        'fields': {'author': 'Lee, Bruce', 'year': '1999', 'title': 'Kung Fu Methods'},
    }
    normalize_key(entry)
    assert entry['key'] == 'original'
