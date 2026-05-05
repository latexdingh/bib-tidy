"""
Tests for bibtidy.year_normalizer
"""

import pytest
from bibtidy.year_normalizer import (
    extract_year,
    normalize_year,
    normalize_entry_year,
    normalize_bibliography_years,
)


# ---------------------------------------------------------------------------
# extract_year
# ---------------------------------------------------------------------------

def test_extract_year_plain_integer():
    assert extract_year('2021') == '2021'


def test_extract_year_range_returns_first():
    assert extract_year('2019-2020') == '2019'


def test_extract_year_with_text_prefix():
    assert extract_year('circa 1998') == '1998'


def test_extract_year_none_when_missing():
    assert extract_year('no year here') is None


def test_extract_year_none_for_empty_string():
    assert extract_year('') is None


def test_extract_year_rejects_three_digit_number():
    assert extract_year('999') is None


def test_extract_year_rejects_year_below_range():
    # 0999 is not matched by the regex
    assert extract_year('0999') is None


# ---------------------------------------------------------------------------
# normalize_year
# ---------------------------------------------------------------------------

def test_normalize_year_clean_value():
    assert normalize_year('2023') == '2023'


def test_normalize_year_strips_whitespace():
    assert normalize_year('  2017  ') == '2017'


def test_normalize_year_in_press_passthrough():
    result = normalize_year('in press')
    assert result == 'in press'


def test_normalize_year_empty_string_passthrough():
    assert normalize_year('') == ''


# ---------------------------------------------------------------------------
# normalize_entry_year
# ---------------------------------------------------------------------------

def _entry(year=None, **extra_fields):
    fields = dict(extra_fields)
    if year is not None:
        fields['year'] = year
    return {'type': 'article', 'key': 'test2024', 'fields': fields}


def test_normalize_entry_year_normalizes_field():
    e = _entry(year='2020-2021', title='Some Paper')
    result = normalize_entry_year(e)
    assert result['fields']['year'] == '2020'


def test_normalize_entry_year_no_year_field_unchanged():
    e = _entry(title='No Year Paper')
    result = normalize_entry_year(e)
    assert 'year' not in result['fields']


def test_normalize_entry_year_preserves_other_fields():
    e = _entry(year='2018', title='My Title', author='Doe, John')
    result = normalize_entry_year(e)
    assert result['fields']['title'] == 'My Title'
    assert result['fields']['author'] == 'Doe, John'


def test_normalize_entry_year_does_not_mutate_original():
    e = _entry(year='circa 2005')
    _ = normalize_entry_year(e)
    assert e['fields']['year'] == 'circa 2005'


# ---------------------------------------------------------------------------
# normalize_bibliography_years
# ---------------------------------------------------------------------------

def test_normalize_bibliography_years_processes_all():
    bib = [
        _entry(year='2010-2011'),
        _entry(year='in press'),
        _entry(year='1999'),
    ]
    result = normalize_bibliography_years(bib)
    assert result[0]['fields']['year'] == '2010'
    assert result[1]['fields']['year'] == 'in press'
    assert result[2]['fields']['year'] == '1999'


def test_normalize_bibliography_years_empty_list():
    assert normalize_bibliography_years([]) == []
