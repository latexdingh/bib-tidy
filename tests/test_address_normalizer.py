"""Tests for bibtidy.address_normalizer."""

import pytest
from bibtidy.address_normalizer import (
    normalize_address,
    normalize_entry_address,
    normalize_bibliography_addresses,
)


# ---------------------------------------------------------------------------
# normalize_address
# ---------------------------------------------------------------------------

def test_normalize_address_returns_none_for_none():
    assert normalize_address(None) is None


def test_normalize_address_returns_none_for_empty():
    assert normalize_address("") is None


def test_normalize_address_collapses_whitespace():
    assert normalize_address("  Berlin   ") == "Berlin, Germany"


def test_normalize_address_strips_braces():
    assert normalize_address("{London}") == "London, UK"


def test_normalize_address_known_alias_ny():
    assert normalize_address("NY") == "New York, NY"


def test_normalize_address_known_alias_nyc():
    assert normalize_address("NYC") == "New York, NY"


def test_normalize_address_known_alias_new_york_full():
    assert normalize_address("New York") == "New York, NY"


def test_normalize_address_known_alias_sf():
    assert normalize_address("SF") == "San Francisco, CA"


def test_normalize_address_known_alias_paris():
    assert normalize_address("paris") == "Paris, France"


def test_normalize_address_unknown_returns_original_stripped():
    result = normalize_address("  Zurich  ")
    assert result == "Zurich"


def test_normalize_address_unknown_multiword():
    result = normalize_address("Amsterdam, Netherlands")
    assert result == "Amsterdam, Netherlands"


# ---------------------------------------------------------------------------
# normalize_entry_address
# ---------------------------------------------------------------------------

def _entry(address=None, **extra_fields):
    fields = {**extra_fields}
    if address is not None:
        fields["address"] = address
    return {"type": "article", "key": "test2024", "fields": fields}


def test_normalize_entry_address_known_city():
    entry = _entry(address="Berlin")
    result = normalize_entry_address(entry)
    assert result["fields"]["address"] == "Berlin, Germany"


def test_normalize_entry_address_removes_field_when_empty():
    entry = _entry(address="")
    result = normalize_entry_address(entry)
    assert "address" not in result["fields"]


def test_normalize_entry_address_no_address_field_unchanged():
    entry = _entry(title="Some Title")
    result = normalize_entry_address(entry)
    assert result == entry


def test_normalize_entry_address_does_not_mutate_original():
    entry = _entry(address="london")
    _ = normalize_entry_address(entry)
    assert entry["fields"]["address"] == "london"


# ---------------------------------------------------------------------------
# normalize_bibliography_addresses
# ---------------------------------------------------------------------------

def test_normalize_bibliography_addresses_processes_all_entries():
    entries = [
        _entry(address="Berlin"),
        _entry(address="paris"),
        _entry(address="NYC"),
    ]
    results = normalize_bibliography_addresses(entries)
    assert results[0]["fields"]["address"] == "Berlin, Germany"
    assert results[1]["fields"]["address"] == "Paris, France"
    assert results[2]["fields"]["address"] == "New York, NY"


def test_normalize_bibliography_addresses_empty_list():
    assert normalize_bibliography_addresses([]) == []


def test_normalize_bibliography_addresses_does_not_mutate_originals():
    entries = [_entry(address="London")]
    _ = normalize_bibliography_addresses(entries)
    assert entries[0]["fields"]["address"] == "London"
