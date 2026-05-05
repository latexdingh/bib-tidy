"""Tests for bibtidy.abbreviation_loader module."""

import json
import csv
import pytest
from pathlib import Path
from bibtidy.abbreviation_loader import (
    load_from_json,
    load_from_csv,
    merge_abbreviations,
)


def test_load_from_json(tmp_path: Path):
    data = {"Full Journal": "Full J.", "Another Journal": "Another J."}
    p = tmp_path / "abbrev.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    result = load_from_json(p)
    assert result == data


def test_load_from_json_invalid_type(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
    with pytest.raises(ValueError, match="Expected a JSON object"):
        load_from_json(p)


def test_load_from_csv(tmp_path: Path):
    p = tmp_path / "abbrev.csv"
    p.write_text(
        "full,abbreviation\nFull Journal,Full J.\nAnother Journal,Another J.\n",
        encoding="utf-8",
    )
    result = load_from_csv(p)
    assert result == {"Full Journal": "Full J.", "Another Journal": "Another J."}


def test_load_from_csv_custom_columns(tmp_path: Path):
    p = tmp_path / "abbrev.csv"
    p.write_text(
        "name,short\nFull Journal,Full J.\n",
        encoding="utf-8",
    )
    result = load_from_csv(p, full_name_col="name", abbrev_col="short")
    assert result == {"Full Journal": "Full J."}


def test_load_from_csv_missing_column(tmp_path: Path):
    p = tmp_path / "abbrev.csv"
    p.write_text("name,short\nFull Journal,Full J.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Column 'full' not found"):
        load_from_csv(p)  # expects 'full' column by default


def test_load_from_csv_skips_empty_rows(tmp_path: Path):
    p = tmp_path / "abbrev.csv"
    p.write_text(
        "full,abbreviation\nFull Journal,Full J.\n,,\n",
        encoding="utf-8",
    )
    result = load_from_csv(p)
    assert len(result) == 1


def test_merge_abbreviations_prefer_last():
    a = {"Journal A": "J. A.", "Journal B": "J. B."}
    b = {"Journal B": "J.B. Updated", "Journal C": "J. C."}
    result = merge_abbreviations(a, b, prefer_last=True)
    assert result["Journal B"] == "J.B. Updated"
    assert result["Journal A"] == "J. A."
    assert result["Journal C"] == "J. C."


def test_merge_abbreviations_prefer_first():
    a = {"Journal B": "J. B. Original"}
    b = {"Journal B": "J.B. Updated"}
    result = merge_abbreviations(a, b, prefer_last=False)
    assert result["Journal B"] == "J. B. Original"
