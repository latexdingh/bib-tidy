"""Tests for bibtidy.tex_encoder."""

import pytest
from bibtidy.tex_encoder import (
    encode_unicode,
    decode_latex,
    encode_entry,
    decode_entry,
)


# --- encode_unicode ---

def test_encode_umlaut():
    assert encode_unicode("Müller") == 'M{\\"u}ller'


def test_encode_accent_acute():
    assert encode_unicode("café") == "caf{\'e}"


def test_encode_accent_grave():
    assert encode_unicode("Ève") == "{\\`E}ve"


def test_encode_tilde():
    assert encode_unicode("señor") == "se{\\~n}or"


def test_encode_no_special_chars():
    assert encode_unicode("hello world") == "hello world"


def test_encode_multiple_chars():
    result = encode_unicode("Ångström")
    assert "{\\aa}" in result or "Å" not in result  # Å not in table, stays as-is


def test_encode_sharp_s():
    assert encode_unicode("Straße") == "Stra{\\ss}e"


# --- decode_latex ---

def test_decode_umlaut():
    assert decode_latex('M{\\"u}ller') == "Müller"


def test_decode_acute():
    assert decode_latex("caf{\'e}") == "café"


def test_decode_tilde():
    assert decode_latex("{\\~n}") == "ñ"


def test_decode_no_latex():
    assert decode_latex("plain text") == "plain text"


def test_decode_unknown_sequence_unchanged():
    # \v is not in our table
    original = "{\\v{s}}"
    assert decode_latex(original) == original


def test_roundtrip_encode_decode():
    original = "Müller, André"
    assert decode_latex(encode_unicode(original)) == original


# --- encode_entry / decode_entry ---

def _make_entry(**fields):
    return {"ENTRYTYPE": "article", "ID": "key1", **fields}


def test_encode_entry_encodes_author():
    entry = _make_entry(author="Müller, Hans", title="Test")
    result = encode_entry(entry)
    assert result["author"] == 'M{\\"u}ller, Hans'
    assert result["ENTRYTYPE"] == "article"
    assert result["ID"] == "key1"


def test_encode_entry_specific_fields_only():
    entry = _make_entry(author="André", title="café")
    result = encode_entry(entry, fields=["author"])
    assert result["author"] == "Andr{\'e}"
    assert result["title"] == "café"  # untouched


def test_decode_entry_decodes_title():
    entry = _make_entry(title="caf{\'e}", year="2020")
    result = decode_entry(entry)
    assert result["title"] == "café"
    assert result["year"] == "2020"


def test_decode_entry_specific_fields():
    entry = _make_entry(author='M{\\"u}ller', title='caf{\'e}')
    result = decode_entry(entry, fields=["title"])
    assert result["title"] == "café"
    assert result["author"] == 'M{\\"u}ller'  # untouched


def test_encode_entry_preserves_id_and_entrytype():
    entry = _make_entry(author="ü")
    result = encode_entry(entry)
    assert result["ID"] == "key1"
    assert result["ENTRYTYPE"] == "article"
