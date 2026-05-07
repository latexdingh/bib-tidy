import pytest
from bibtidy.month_normalizer import (
    normalize_month,
    normalize_entry_month,
    normalize_bibliography_months,
)


# ---------------------------------------------------------------------------
# normalize_month
# ---------------------------------------------------------------------------

def test_normalize_full_name_lowercase():
    assert normalize_month("january") == "jan"


def test_normalize_full_name_titlecase():
    assert normalize_month("March") == "mar"


def test_normalize_full_name_uppercase():
    assert normalize_month("DECEMBER") == "dec"


def test_normalize_abbreviation():
    assert normalize_month("sep") == "sep"


def test_normalize_abbreviation_mixed_case():
    assert normalize_month("Nov") == "nov"


def test_normalize_numeric_string():
    assert normalize_month("6") == "jun"


def test_normalize_numeric_string_leading_zero_not_supported():
    # Leading zeros are not in the map; should return None
    assert normalize_month("06") is None


def test_normalize_with_surrounding_braces():
    assert normalize_month("{August}") == "aug"


def test_normalize_with_surrounding_quotes():
    assert normalize_month('"july"') == "jul"


def test_normalize_unknown_returns_none():
    assert normalize_month("springtime") is None


def test_normalize_empty_string_returns_none():
    assert normalize_month("") is None


# ---------------------------------------------------------------------------
# normalize_entry_month
# ---------------------------------------------------------------------------

def _entry(month=None, **extra_fields):
    fields = {**extra_fields}
    if month is not None:
        fields["month"] = month
    return {"type": "article", "key": "Smith2024", "fields": fields}


def test_entry_month_normalized():
    result = normalize_entry_month(_entry(month="February"))
    assert result["fields"]["month"] == "feb"


def test_entry_month_numeric():
    result = normalize_entry_month(_entry(month="10"))
    assert result["fields"]["month"] == "oct"


def test_entry_month_already_normalized():
    result = normalize_entry_month(_entry(month="apr"))
    assert result["fields"]["month"] == "apr"


def test_entry_month_unknown_left_unchanged():
    result = normalize_entry_month(_entry(month="Q3"))
    assert result["fields"]["month"] == "Q3"


def test_entry_without_month_unchanged():
    entry = _entry(title="Some Title")
    result = normalize_entry_month(entry)
    assert "month" not in result["fields"]
    assert result["fields"]["title"] == "Some Title"


def test_entry_other_fields_preserved():
    entry = _entry(month="may", year="2024", author="Doe, J.")
    result = normalize_entry_month(entry)
    assert result["fields"]["year"] == "2024"
    assert result["fields"]["author"] == "Doe, J."


# ---------------------------------------------------------------------------
# normalize_bibliography_months
# ---------------------------------------------------------------------------

def test_bibliography_months_normalizes_all_entries():
    bib = [
        _entry(month="January", key="A"),
        _entry(month="12", key="B"),
        _entry(month="aug", key="C"),
    ]
    result = normalize_bibliography_months(bib)
    assert result[0]["fields"]["month"] == "jan"
    assert result[1]["fields"]["month"] == "dec"
    assert result[2]["fields"]["month"] == "aug"


def test_bibliography_months_skips_entries_without_month():
    bib = [
        _entry(title="No month here"),
        _entry(month="March"),
    ]
    result = normalize_bibliography_months(bib)
    assert "month" not in result[0]["fields"]
    assert result[1]["fields"]["month"] == "mar"


def test_bibliography_months_empty_list():
    assert normalize_bibliography_months([]) == []


def test_bibliography_months_returns_new_list():
    bib = [_entry(month="July")]
    result = normalize_bibliography_months(bib)
    assert result is not bib
