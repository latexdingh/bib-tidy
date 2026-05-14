import pytest
from bibtidy.journal_normalizer import (
    normalize_journal,
    normalize_entry_journal,
    normalize_bibliography_journals,
)


# ---------------------------------------------------------------------------
# normalize_journal
# ---------------------------------------------------------------------------

def test_normalize_known_full_name_unchanged():
    assert normalize_journal("Nature") == "Nature"


def test_normalize_known_abbreviation_expands():
    assert normalize_journal("pnas") == "Proceedings of the National Academy of Sciences"


def test_normalize_case_insensitive():
    assert normalize_journal("JACS") == "Journal of the American Chemical Society"


def test_normalize_dotted_abbreviation():
    assert normalize_journal("Phys. Rev. Lett.") == "Physical Review Letters"


def test_normalize_strips_braces():
    assert normalize_journal("{Nature}") == "Nature"


def test_normalize_collapses_whitespace():
    result = normalize_journal("  Machine   Learning  ")
    assert result == "Machine Learning"


def test_normalize_unknown_journal_returns_original():
    assert normalize_journal("Exotic Journal of Stuff") == "Exotic Journal of Stuff"


def test_normalize_none_returns_none():
    assert normalize_journal(None) is None


def test_normalize_empty_string_returns_none():
    assert normalize_journal("") is None


def test_normalize_whitespace_only_returns_none():
    assert normalize_journal("   ") is None


# ---------------------------------------------------------------------------
# normalize_entry_journal
# ---------------------------------------------------------------------------

def _entry(journal=None, **extra_fields):
    fields = {**extra_fields}
    if journal is not None:
        fields["journal"] = journal
    return {"type": "article", "key": "test2024", "fields": fields}


def test_entry_known_abbreviation_expanded():
    e = _entry(journal="prl")
    result = normalize_entry_journal(e)
    assert result["fields"]["journal"] == "Physical Review Letters"


def test_entry_unknown_journal_preserved():
    e = _entry(journal="Some Unknown Journal")
    result = normalize_entry_journal(e)
    assert result["fields"]["journal"] == "Some Unknown Journal"


def test_entry_missing_journal_field_unchanged():
    e = _entry(title="A paper")
    result = normalize_entry_journal(e)
    assert "journal" not in result["fields"]


def test_entry_empty_journal_removes_field():
    e = _entry(journal="")
    result = normalize_entry_journal(e)
    assert "journal" not in result["fields"]


def test_entry_does_not_mutate_original():
    e = _entry(journal="jcp")
    original_journal = e["fields"]["journal"]
    normalize_entry_journal(e)
    assert e["fields"]["journal"] == original_journal


def test_entry_other_fields_preserved():
    e = _entry(journal="Nature", title="My Title", year="2024")
    result = normalize_entry_journal(e)
    assert result["fields"]["title"] == "My Title"
    assert result["fields"]["year"] == "2024"


# ---------------------------------------------------------------------------
# normalize_bibliography_journals
# ---------------------------------------------------------------------------

def test_bibliography_normalizes_all_entries():
    bib = [
        _entry(journal="prl"),
        _entry(journal="jacs"),
        _entry(journal="Unknown"),
    ]
    result = normalize_bibliography_journals(bib)
    assert result[0]["fields"]["journal"] == "Physical Review Letters"
    assert result[1]["fields"]["journal"] == "Journal of the American Chemical Society"
    assert result[2]["fields"]["journal"] == "Unknown"


def test_bibliography_empty_list():
    assert normalize_bibliography_journals([]) == []


def test_bibliography_returns_new_list():
    bib = [_entry(journal="Nature")]
    result = normalize_bibliography_journals(bib)
    assert result is not bib
