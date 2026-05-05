"""Tests for bibtidy.doi_resolver."""

import json
from unittest.mock import patch, MagicMock
import pytest

from bibtidy.doi_resolver import extract_doi, fetch_doi_metadata, enrich_entry


SAMPLE_ENTRY = {
    'type': 'article',
    'key': 'Smith2021',
    'fields': {
        'doi': '10.1234/example.2021',
        'title': '',
        'author': '',
        'year': '',
    },
}

CROSSREF_RESPONSE = {
    'message': {
        'title': ['Deep Learning Revisited'],
        'author': [{'family': 'Smith', 'given': 'John'}],
        'issued': {'date-parts': [[2021]]},
        'container-title': ['Journal of AI'],
        'volume': '10',
        'page': '1-15',
        'publisher': 'Springer',
    }
}


def test_extract_doi_from_doi_field():
    entry = {'fields': {'doi': '10.1000/xyz123'}}
    assert extract_doi(entry) == '10.1000/xyz123'


def test_extract_doi_from_url_field():
    entry = {'fields': {'doi': '', 'url': 'https://doi.org/10.1000/xyz123'}}
    assert extract_doi(entry) == '10.1000/xyz123'


def test_extract_doi_returns_none_when_missing():
    entry = {'fields': {'title': 'No DOI here'}}
    assert extract_doi(entry) is None


def _make_mock_response(data: dict):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(data).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_fetch_doi_metadata_success():
    with patch('urllib.request.urlopen', return_value=_make_mock_response(CROSSREF_RESPONSE)):
        meta = fetch_doi_metadata('10.1234/example.2021')
    assert meta is not None
    assert meta['title'] == 'Deep Learning Revisited'
    assert meta['year'] == '2021'
    assert 'Smith' in meta['author']
    assert meta['journal'] == 'Journal of AI'


def test_fetch_doi_metadata_returns_none_on_error():
    import urllib.error
    with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('timeout')):
        meta = fetch_doi_metadata('10.9999/bad')
    assert meta is None


def test_enrich_entry_fills_missing_fields():
    with patch('urllib.request.urlopen', return_value=_make_mock_response(CROSSREF_RESPONSE)):
        enriched = enrich_entry(SAMPLE_ENTRY)
    assert enriched['fields']['title'] == 'Deep Learning Revisited'
    assert enriched['fields']['year'] == '2021'


def test_enrich_entry_does_not_overwrite_existing_fields():
    entry = {
        'type': 'article',
        'key': 'X',
        'fields': {'doi': '10.1234/example.2021', 'title': 'Original Title'},
    }
    with patch('urllib.request.urlopen', return_value=_make_mock_response(CROSSREF_RESPONSE)):
        enriched = enrich_entry(entry)
    assert enriched['fields']['title'] == 'Original Title'
