"""Tests for bibtidy.volume_normalizer."""

import pytest
from bibtidy.volume_normalizer import (
    normalize_volume,
    normalize_number,
    normalize_entry_volume,
    normalize_bibliography_volumes,
)


# ---------------------------------------------------------------------------
# normalize_volume
# ---------------------------------------------------------------------------

def test_normalize_volume_plain_number():
    assert normalize_volume('12') == '12'


def test_normalize_volume_strips_vol_prefix():
    assert normalize_volume('vol. 12') == '12'


def test_normalize_volume_strips_volume_prefix():
    assert normalize_volume('Volume 3') == '3'


def test_normalize_volume_strips_vol_colon():
    assert normalize_volume('vol:7') == '7'


def test_normalize_volume_alphanumeric():
    assert normalize_volume('vol. 12A') == '12A'


def test_normalize_volume_empty_returns_none():
    assert normalize_volume('') is None


def test_normalize_volume_whitespace_only_returns_none():
    assert normalize_volume('   ') is None


def test_normalize_volume_prefix_only_returns_none():
    assert normalize_volume('vol.') is None


# ---------------------------------------------------------------------------
# normalize_number
# ---------------------------------------------------------------------------

def test_normalize_number_plain():
    assert normalize_number('4') == '4'


def test_normalize_number_strips_no_prefix():
    assert normalize_number('no. 4') == '4'


def test_normalize_number_strips_number_prefix():
    assert normalize_number('Number 2') == '2'


def test_normalize_number_strips_issue_prefix():
    assert normalize_number('issue 10') == '10'


def test_normalize_number_strips_num_prefix():
    assert normalize_number('num. 3') == '3'


def test_normalize_number_empty_returns_none():
    assert normalize_number('') is None


def test_normalize_number_prefix_only_returns_none():
    assert normalize_number('no.') is None


# ---------------------------------------------------------------------------
# normalize_entry_volume
# ---------------------------------------------------------------------------

def _entry(**fields):
    return {'type': 'article', 'key': 'k', 'fields': fields}


def test_entry_volume_normalized():
    entry = _entry(volume='vol. 5', number='no. 2')
    result = normalize_entry_volume(entry)
    assert result['fields']['volume'] == '5'
    assert result['fields']['number'] == '2'


def test_entry_missing_volume_field_untouched():
    entry = _entry(number='3')
    result = normalize_entry_volume(entry)
    assert 'volume' not in result['fields']
    assert result['fields']['number'] == '3'


def test_entry_invalid_volume_removed():
    entry = _entry(volume='vol.', number='1')
    result = normalize_entry_volume(entry)
    assert 'volume' not in result['fields']


def test_entry_original_not_mutated():
    fields = {'volume': 'vol. 8'}
    entry = {'type': 'article', 'key': 'k', 'fields': fields}
    normalize_entry_volume(entry)
    assert fields['volume'] == 'vol. 8'


# ---------------------------------------------------------------------------
# normalize_bibliography_volumes
# ---------------------------------------------------------------------------

def test_bibliography_all_entries_normalized():
    bib = [
        _entry(volume='Volume 1', number='issue 1'),
        _entry(volume='vol. 2', number='no. 3'),
    ]
    result = normalize_bibliography_volumes(bib)
    assert result[0]['fields']['volume'] == '1'
    assert result[1]['fields']['number'] == '3'


def test_bibliography_empty():
    assert normalize_bibliography_volumes([]) == []
