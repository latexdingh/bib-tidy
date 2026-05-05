"""Tests for bibtidy.crossref_resolver."""

import pytest
from bibtidy.crossref_resolver import resolve_crossref, resolve_all_crossrefs


def _e(key, fields=None, entry_type="article"):
    return {"type": entry_type, "key": key, "fields": fields or {}}


def test_resolve_no_crossref():
    entry = _e("child", {"title": "My Paper"})
    result = resolve_crossref(entry, {})
    assert result["fields"] == {"title": "My Paper"}


def test_resolve_inherits_parent_fields():
    parent = _e("conf2020", {"booktitle": "Proc. ICSE 2020", "year": "2020"})
    child = _e("doe2020", {"author": "Doe", "crossref": "conf2020"})
    index = {"conf2020": parent}
    result = resolve_crossref(child, index)
    assert result["fields"]["booktitle"] == "Proc. ICSE 2020"
    assert result["fields"]["year"] == "2020"
    assert result["fields"]["author"] == "Doe"


def test_child_fields_override_parent():
    parent = _e("conf", {"year": "2019", "booktitle": "Old Conf"})
    child = _e("entry", {"year": "2020", "crossref": "conf"})
    index = {"conf": parent}
    result = resolve_crossref(child, index)
    assert result["fields"]["year"] == "2020"


def test_resolve_missing_parent_returns_entry_unchanged():
    child = _e("orphan", {"crossref": "nonexistent", "title": "T"})
    result = resolve_crossref(child, {})
    assert result["fields"]["title"] == "T"
    assert result["fields"]["crossref"] == "nonexistent"


def test_resolve_does_not_mutate_original():
    parent = _e("p", {"year": "2021"})
    child = _e("c", {"crossref": "p"})
    index = {"p": parent}
    resolve_crossref(child, index)
    assert "year" not in child["fields"]


def test_resolve_all_crossrefs():
    parent = _e("proc", {"booktitle": "ICML", "year": "2022"})
    c1 = _e("a", {"author": "Alice", "crossref": "proc"})
    c2 = _e("b", {"author": "Bob", "crossref": "proc"})
    result = resolve_all_crossrefs([parent, c1, c2])
    assert result[1]["fields"]["booktitle"] == "ICML"
    assert result[2]["fields"]["year"] == "2022"


def test_resolve_all_crossrefs_empty():
    assert resolve_all_crossrefs([]) == []


def test_max_depth_prevents_infinite_loop():
    # Circular crossref chain should not hang
    a = _e("a", {"crossref": "b"})
    b = _e("b", {"crossref": "a"})
    index = {"a": a, "b": b}
    # Should return without raising
    result = resolve_crossref(a, index, max_depth=3)
    assert result is not None
