"""
tests/test_note_cleaner.py

Unit tests for bibtidy.note_cleaner.
"""

import pytest
from bibtidy.note_cleaner import (
    clean_note,
    clean_entry_note,
    clean_bibliography_notes,
    MAX_NOTE_LENGTH,
)


# ---------------------------------------------------------------------------
# clean_note
# ---------------------------------------------------------------------------

def test_clean_note_strips_whitespace():
    assert clean_note('  hello world  ') == 'hello world'


def test_clean_note_returns_none_for_empty():
    assert clean_note('') is None
    assert clean_note('   ') is None


def test_clean_note_unwraps_url_macro():
    result = clean_note(r'See \url{https://example.com} for details.')
    assert '\\url' not in result
    assert 'https://example.com' in result


def test_clean_note_strips_html_tags():
    result = clean_note('Published in <em>Nature</em>.')
    assert '<em>' not in result
    assert 'Nature' in result


def test_clean_note_collapses_internal_spaces():
    result = clean_note('too   many    spaces')
    assert '  ' not in result
    assert result == 'too many spaces'


def test_clean_note_truncates_long_text():
    long_text = 'a' * 400
    result = clean_note(long_text, max_length=100)
    assert result is not None
    assert len(result) <= 101  # 100 chars + ellipsis character
    assert result.endswith('…')


def test_clean_note_no_truncation_when_short():
    text = 'Short note.'
    assert clean_note(text, max_length=MAX_NOTE_LENGTH) == text


def test_clean_note_no_truncation_when_max_length_none():
    long_text = 'b' * 500
    result = clean_note(long_text, max_length=None)
    assert result == long_text


# ---------------------------------------------------------------------------
# clean_entry_note
# ---------------------------------------------------------------------------

def _entry(note=None):
    fields = {}
    if note is not None:
        fields['note'] = note
    return {'type': 'article', 'key': 'Doe2024', 'fields': fields}


def test_clean_entry_note_cleans_field():
    e = _entry(note='  See <b>here</b>.  ')
    result = clean_entry_note(e)
    assert result['fields']['note'] == 'See here.'


def test_clean_entry_note_removes_empty_note():
    e = _entry(note='   ')
    result = clean_entry_note(e)
    assert 'note' not in result['fields']


def test_clean_entry_note_no_note_field_unchanged():
    e = _entry()
    result = clean_entry_note(e)
    assert 'note' not in result['fields']


def test_clean_entry_note_does_not_mutate_original():
    e = _entry(note='  raw  ')
    clean_entry_note(e)
    assert e['fields']['note'] == '  raw  '


# ---------------------------------------------------------------------------
# clean_bibliography_notes
# ---------------------------------------------------------------------------

def test_clean_bibliography_notes_applies_to_all():
    bib = [
        _entry(note='  note one  '),
        _entry(note='<b>bold</b>'),
        _entry(),
    ]
    results = clean_bibliography_notes(bib)
    assert results[0]['fields']['note'] == 'note one'
    assert results[1]['fields']['note'] == 'bold'
    assert 'note' not in results[2]['fields']


def test_clean_bibliography_notes_empty_list():
    assert clean_bibliography_notes([]) == []
