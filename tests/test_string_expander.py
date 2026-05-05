"""Tests for bibtidy.string_expander."""

import pytest
from bibtidy.string_expander import (
    extract_string_macros,
    expand_value,
    expand_entry,
    expand_bibliography,
)


BIB_SOURCE = """
@string{jan = {January}}
@string{feb = {February}}
@string{acm = {ACM Press}}

@article{doe2020,
  author = {Doe, John},
  month  = jan,
}
"""


def test_extract_string_macros_finds_all():
    macros = extract_string_macros(BIB_SOURCE)
    assert macros == {"jan": "January", "feb": "February", "acm": "ACM Press"}


def test_extract_string_macros_empty_source():
    assert extract_string_macros("") == {}


def test_extract_string_macros_no_strings():
    source = "@article{key, author={A}}"
    assert extract_string_macros(source) == {}


def test_expand_value_plain_macro():
    macros = {"jan": "January"}
    assert expand_value("jan", macros) == "January"


def test_expand_value_concatenation():
    macros = {"jan": "January"}
    result = expand_value('jan # " 2020"', macros)
    assert result == "January 2020"


def test_expand_value_braced_literal():
    result = expand_value("{Some Title}", {})
    assert result == "Some Title"


def test_expand_value_unknown_macro_passthrough():
    result = expand_value("unknownmacro", {})
    assert result == "unknownmacro"


def test_expand_entry_replaces_fields():
    macros = {"acm": "ACM Press"}
    entry = {"type": "inproceedings", "key": "x", "fields": {"publisher": "acm"}}
    result = expand_entry(entry, macros)
    assert result["fields"]["publisher"] == "ACM Press"


def test_expand_entry_does_not_mutate_original():
    macros = {"jan": "January"}
    entry = {"type": "article", "key": "y", "fields": {"month": "jan"}}
    expand_entry(entry, macros)
    assert entry["fields"]["month"] == "jan"


def test_expand_bibliography_all_entries():
    macros = {"feb": "February", "acm": "ACM Press"}
    entries = [
        {"type": "article", "key": "a", "fields": {"month": "feb"}},
        {"type": "inproceedings", "key": "b", "fields": {"publisher": "acm"}},
    ]
    result = expand_bibliography(entries, macros)
    assert result[0]["fields"]["month"] == "February"
    assert result[1]["fields"]["publisher"] == "ACM Press"


def test_expand_bibliography_empty():
    assert expand_bibliography([], {"jan": "January"}) == []
