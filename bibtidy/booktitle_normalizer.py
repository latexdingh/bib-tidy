"""
Normalizer for the `booktitle` field in BibTeX entries.

Applies title-case formatting, expands common conference abbreviations,
and strips extraneous braces / whitespace.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

# Map of lowercased abbreviations / short forms -> canonical booktitle
CONFERENCE_ALIASES: Dict[str, str] = {
    "neurips": "Advances in Neural Information Processing Systems",
    "nips": "Advances in Neural Information Processing Systems",
    "icml": "Proceedings of the International Conference on Machine Learning",
    "iclr": "Proceedings of the International Conference on Learning Representations",
    "cvpr": "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition",
    "iccv": "Proceedings of the IEEE/CVF International Conference on Computer Vision",
    "eccv": "Proceedings of the European Conference on Computer Vision",
    "acl": "Proceedings of the Annual Meeting of the Association for Computational Linguistics",
    "emnlp": "Proceedings of the Conference on Empirical Methods in Natural Language Processing",
    "naacl": "Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics",
    "sigir": "Proceedings of the International ACM SIGIR Conference on Research and Development in Information Retrieval",
    "www": "Proceedings of the World Wide Web Conference",
    "kdd": "Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining",
    "aaai": "Proceedings of the AAAI Conference on Artificial Intelligence",
    "ijcai": "Proceedings of the International Joint Conference on Artificial Intelligence",
}

_STOP_WORDS = {
    "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet",
    "at", "by", "in", "of", "on", "to", "up", "as", "is",
}


def _strip_braces(value: str) -> str:
    return value.replace("{", "").replace("}", "")


def _title_case(value: str) -> str:
    """Apply title-case while preserving all-caps tokens (acronyms)."""
    words = value.split()
    result: List[str] = []
    for i, word in enumerate(words):
        clean = word.strip(",:;")
        if clean.isupper() and len(clean) > 1:
            result.append(word)  # keep acronym as-is
        elif i == 0 or clean.lower() not in _STOP_WORDS:
            result.append(word[0].upper() + word[1:] if word else word)
        else:
            result.append(word.lower())
    return " ".join(result)


def normalize_booktitle(value: Optional[str]) -> Optional[str]:
    """Return a normalised booktitle string, or None if input is empty."""
    if not value:
        return None
    value = _strip_braces(value)
    value = re.sub(r"\s+", " ", value).strip()
    lower = value.lower().strip()
    if lower in CONFERENCE_ALIASES:
        return CONFERENCE_ALIASES[lower]
    return _title_case(value)


def normalize_entry_booktitle(entry: dict) -> dict:
    """Return a copy of *entry* with a normalised `booktitle` field."""
    result = dict(entry)
    raw = result.get("booktitle")
    normalised = normalize_booktitle(raw)
    if normalised is None:
        result.pop("booktitle", None)
    else:
        result["booktitle"] = normalised
    return result


def normalize_bibliography_booktitles(entries: List[dict]) -> List[dict]:
    """Apply booktitle normalisation to every entry in *entries*."""
    return [normalize_entry_booktitle(e) for e in entries]
