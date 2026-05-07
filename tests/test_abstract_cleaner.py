import pytest
from bibtidy.abstract_cleaner import (
    strip_html,
    normalize_whitespace,
    truncate_abstract,
    clean_abstract,
    clean_entry_abstract,
    clean_bibliography_abstracts,
)


def test_strip_html_removes_tags():
    assert strip_html("<b>Hello</b> <i>world</i>") == " Hello   world "


def test_strip_html_no_tags_unchanged():
    assert strip_html("Plain text.").strip() == "Plain text."


def test_normalize_whitespace_collapses_spaces():
    assert normalize_whitespace("  foo   bar  ") == "foo bar"


def test_normalize_whitespace_handles_newlines():
    assert normalize_whitespace("foo\n\nbar\t baz") == "foo bar baz"


def test_truncate_abstract_no_cut_when_short():
    text = "word " * 10
    result = truncate_abstract(text.strip(), max_words=20)
    assert "..." not in result
    assert len(result.split()) == 10


def test_truncate_abstract_cuts_long_text():
    text = " ".join(["word"] * 50)
    result = truncate_abstract(text, max_words=10)
    assert result.endswith("...")
    # 10 words + "..."
    assert len(result.split()) == 11


def test_clean_abstract_strips_html_and_whitespace():
    raw = "  <p>This is  an  <em>abstract</em>.  </p>  "
    result = clean_abstract(raw)
    assert result == "This is an abstract ."


def test_clean_abstract_truncates_when_max_words_given():
    raw = " ".join(["word"] * 400)
    result = clean_abstract(raw, max_words=300)
    assert result.endswith("...")


def test_clean_abstract_no_truncation_without_max_words():
    raw = " ".join(["word"] * 400)
    result = clean_abstract(raw)
    assert not result.endswith("...")


def _entry(abstract=None):
    fields = {}
    if abstract is not None:
        fields["abstract"] = abstract
    return {"type": "article", "key": "k1", "fields": fields}


def test_clean_entry_abstract_cleans_field():
    e = _entry("<b>Great</b>  paper.")
    result = clean_entry_abstract(e)
    assert result["fields"]["abstract"] == "Great paper."


def test_clean_entry_abstract_no_abstract_field_unchanged():
    e = _entry()
    result = clean_entry_abstract(e)
    assert "abstract" not in result["fields"]


def test_clean_entry_abstract_does_not_mutate_original():
    e = _entry("<em>test</em>")
    _ = clean_entry_abstract(e)
    assert e["fields"]["abstract"] == "<em>test</em>"


def test_clean_bibliography_abstracts_processes_all():
    entries = [
        _entry("<b>First</b>  abstract."),
        _entry("Second  abstract."),
        _entry(),
    ]
    results = clean_bibliography_abstracts(entries)
    assert results[0]["fields"]["abstract"] == "First abstract."
    assert results[1]["fields"]["abstract"] == "Second abstract."
    assert "abstract" not in results[2]["fields"]


def test_clean_bibliography_abstracts_respects_max_words():
    long_text = " ".join(["word"] * 500)
    entries = [_entry(long_text)]
    results = clean_bibliography_abstracts(entries, max_words=50)
    assert results[0]["fields"]["abstract"].endswith("...")
