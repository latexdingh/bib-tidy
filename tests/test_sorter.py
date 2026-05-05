"""Tests for bibtidy.sorter module."""

import pytest
from bibtidy.sorter import sort_entries, SORT_FIELDS


def _e(key, year="2020", author="Smith, John", title="A Paper"):
    return {
        "key": key,
        "entrytype": "article",
        "fields": {"year": year, "author": author, "title": title},
    }


def test_sort_by_year_ascending():
    entries = [_e("c", year="2022"), _e("a", year="2019"), _e("b", year="2021")]
    result = sort_entries(entries, fields=["year"])
    assert [e["key"] for e in result] == ["a", "b", "c"]


def test_sort_by_year_descending():
    entries = [_e("c", year="2022"), _e("a", year="2019"), _e("b", year="2021")]
    result = sort_entries(entries, fields=["year"], reverse=True)
    assert [e["key"] for e in result] == ["c", "b", "a"]


def test_sort_by_key():
    entries = [_e("zebra"), _e("apple"), _e("mango")]
    result = sort_entries(entries, fields=["key"])
    assert [e["key"] for e in result] == ["apple", "mango", "zebra"]


def test_sort_by_author_lastname():
    entries = [
        _e("x", author="Zhao, Wei"),
        _e("y", author="Adams, John"),
        _e("z", author="Miller, Ann"),
    ]
    result = sort_entries(entries, fields=["author"])
    assert result[0]["key"] == "y"
    assert result[1]["key"] == "z"
    assert result[2]["key"] == "x"


def test_sort_by_multiple_fields():
    entries = [
        _e("b", year="2020", author="Zhao, Wei"),
        _e("a", year="2020", author="Adams, John"),
        _e("c", year="2019", author="Adams, John"),
    ]
    result = sort_entries(entries, fields=["year", "author"])
    assert result[0]["key"] == "c"  # 2019
    assert result[1]["key"] == "a"  # 2020, Adams
    assert result[2]["key"] == "b"  # 2020, Zhao


def test_sort_invalid_field_raises():
    with pytest.raises(ValueError, match="Invalid sort field"):
        sort_entries([_e("x")], fields=["nonexistent"])


def test_sort_empty_list():
    assert sort_entries([], fields=["year"]) == []


def test_sort_default_fields():
    entries = [_e("b", year="2021"), _e("a", year="2018")]
    result = sort_entries(entries)  # default: year, author
    assert result[0]["key"] == "a"
