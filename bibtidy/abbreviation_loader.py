"""Loader for journal abbreviation maps from CSV or JSON files.

Supports loading custom abbreviation tables to supplement or replace
the built-in DEFAULT_ABBREVIATIONS in abbreviator.py.
"""

import csv
import json
from pathlib import Path
from typing import Union


def load_from_json(path: Union[str, Path]) -> dict[str, str]:
    """Load abbreviations from a JSON file mapping full names to abbreviations.

    Expected format::

        {"Full Journal Name": "Abbrev. J. Name", ...}
    """
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}, got {type(data).__name__}")
    return {str(k): str(v) for k, v in data.items()}


def load_from_csv(
    path: Union[str, Path],
    full_name_col: str = "full",
    abbrev_col: str = "abbreviation",
) -> dict[str, str]:
    """Load abbreviations from a CSV file.

    The CSV must have a header row with at least two columns whose names
    are given by *full_name_col* and *abbrev_col*.
    """
    path = Path(path)
    result: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or full_name_col not in reader.fieldnames:
            raise ValueError(
                f"Column '{full_name_col}' not found in CSV header of {path}"
            )
        if abbrev_col not in reader.fieldnames:
            raise ValueError(
                f"Column '{abbrev_col}' not found in CSV header of {path}"
            )
        for row in reader:
            full = row[full_name_col].strip()
            abbrev = row[abbrev_col].strip()
            if full and abbrev:
                result[full] = abbrev
    return result


def merge_abbreviations(
    *maps: dict[str, str],
    prefer_last: bool = True,
) -> dict[str, str]:
    """Merge multiple abbreviation maps into one.

    If *prefer_last* is True (default), later maps overwrite earlier ones
    for the same key.
    """
    merged: dict[str, str] = {}
    for m in maps:
        if prefer_last:
            merged.update(m)
        else:
            for k, v in m.items():
                merged.setdefault(k, v)
    return merged
