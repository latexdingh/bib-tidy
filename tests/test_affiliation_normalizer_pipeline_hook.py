"""
Tests for bibtidy.affiliation_normalizer_pipeline_hook.
"""

from pathlib import Path
import pytest

from bibtidy.affiliation_normalizer_pipeline_hook import apply, run_on_file


def _make_entry(**fields) -> dict:
    return {"type": "article", "key": "k", **fields}


def test_apply_normalizes_affiliations():
    bib = [
        _make_entry(affiliation="MIT"),
        _make_entry(affiliation="Stanford Univ."),
    ]
    result = apply(bib)
    assert result[0]["affiliation"] == "Massachusetts Institute of Technology"
    assert result[1]["affiliation"] == "Stanford University"


def test_apply_empty_bibliography():
    assert apply([]) == []


def test_apply_entry_without_affiliation_unchanged():
    bib = [_make_entry(title="No affiliation here")]
    result = apply(bib)
    assert "affiliation" not in result[0]
    assert result[0]["title"] == "No affiliation here"


def test_apply_returns_new_list():
    bib = [_make_entry(affiliation="Oxford")]
    result = apply(bib)
    assert result is not bib


def test_apply_custom_field():
    bib = [_make_entry(org="CMU")]
    result = apply(bib, field="org")
    assert result[0]["org"] == "Carnegie Mellon University"


def test_run_on_file_overwrites_in_place(tmp_path: Path):
    bib_content = (
        "@article{key1,\n"
        "  affiliation = {MIT},\n"
        "  title = {Test},\n"
        "}\n"
    )
    bib_file = tmp_path / "refs.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    run_on_file(bib_file)

    result = bib_file.read_text(encoding="utf-8")
    assert "Massachusetts Institute of Technology" in result
    assert "MIT" not in result.replace("Massachusetts Institute of Technology", "")
