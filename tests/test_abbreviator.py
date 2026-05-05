"""Tests for bibtidy.abbreviator module."""

import pytest
from bibtidy.abbreviator import (
    abbreviate_journal,
    abbreviate_entry,
    abbreviate_bibliography,
    DEFAULT_ABBREVIATIONS,
)


def _entry(key: str, **fields) -> dict:
    return {"type": "article", "key": key, "fields": fields}


def test_abbreviate_known_journal():
    result = abbreviate_journal("Physical Review Letters")
    assert result == "Phys. Rev. Lett."


def test_abbreviate_unknown_journal_returns_original():
    result = abbreviate_journal("Unknown Journal of Stuff")
    assert result == "Unknown Journal of Stuff"


def test_abbreviate_case_insensitive():
    result = abbreviate_journal("physical review letters")
    assert result == "Phys. Rev. Lett."


def test_abbreviate_strips_extra_whitespace():
    result = abbreviate_journal("  Physical Review Letters  ")
    assert result == "Phys. Rev. Lett."


def test_abbreviate_with_custom_map():
    custom = {"My Special Journal": "My Spec. J."}
    result = abbreviate_journal("My Special Journal", abbreviations=custom)
    assert result == "My Spec. J."


def test_abbreviate_custom_map_does_not_use_defaults():
    custom = {"My Special Journal": "My Spec. J."}
    result = abbreviate_journal("Physical Review Letters", abbreviations=custom)
    # Not in custom map, so returns original
    assert result == "Physical Review Letters"


def test_abbreviate_entry_updates_journal_field():
    e = _entry("smith2020", journal="Nature Communications", year="2020")
    result = abbreviate_entry(e)
    assert result["fields"]["journal"] == "Nat. Commun."
    assert result["fields"]["year"] == "2020"


def test_abbreviate_entry_no_journal_field():
    e = _entry("smith2020", title="Some Title", year="2020")
    result = abbreviate_entry(e)
    assert "journal" not in result["fields"]
    assert result["fields"]["title"] == "Some Title"


def test_abbreviate_entry_does_not_mutate_original():
    e = _entry("smith2020", journal="Nature Communications")
    _ = abbreviate_entry(e)
    assert e["fields"]["journal"] == "Nature Communications"


def test_abbreviate_entry_custom_field():
    e = _entry("smith2020", booktitle="Physical Review Letters")
    result = abbreviate_entry(e, field="booktitle")
    assert result["fields"]["booktitle"] == "Phys. Rev. Lett."


def test_abbreviate_bibliography_applies_to_all():
    entries = [
        _entry("a", journal="Nature Communications"),
        _entry("b", journal="Physical Review Letters"),
        _entry("c", title="No Journal Here"),
    ]
    result = abbreviate_bibliography(entries)
    assert result[0]["fields"]["journal"] == "Nat. Commun."
    assert result[1]["fields"]["journal"] == "Phys. Rev. Lett."
    assert "journal" not in result[2]["fields"]


def test_default_abbreviations_not_empty():
    assert len(DEFAULT_ABBREVIATIONS) > 0
