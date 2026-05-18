"""
Normalize conference/venue names in BibTeX entries.

Maps common abbreviations and variants to canonical full names.
Applies to the `booktitle` field for inproceedings and the
`journal` field for conference-journal hybrids.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

# Canonical name -> list of known aliases / abbreviations
_CONFERENCE_ALIASES: Dict[str, List[str]] = {
    "International Conference on Machine Learning": [
        "ICML", "Int. Conf. Mach. Learn.",
    ],
    "Neural Information Processing Systems": [
        "NeurIPS", "NIPS", "Adv. Neural Inf. Process. Syst.",
    ],
    "International Conference on Learning Representations": [
        "ICLR",
    ],
    "IEEE Conference on Computer Vision and Pattern Recognition": [
        "CVPR", "Proc. CVPR",
    ],
    "International Conference on Computer Vision": [
        "ICCV",
    ],
    "European Conference on Computer Vision": [
        "ECCV",
    ],
    "ACM SIGKDD Conference on Knowledge Discovery and Data Mining": [
        "KDD", "SIGKDD",
    ],
    "AAAI Conference on Artificial Intelligence": [
        "AAAI",
    ],
    "International Joint Conference on Artificial Intelligence": [
        "IJCAI",
    ],
    "ACM Conference on Computer and Communications Security": [
        "CCS", "ACM CCS",
    ],
    "USENIX Security Symposium": [
        "USENIX Security", "Usenix Security",
    ],
}

# Build reverse lookup: normalised alias -> canonical name
def _build_lookup() -> Dict[str, str]:
    lookup: Dict[str, str] = {}
    for canonical, aliases in _CONFERENCE_ALIASES.items():
        lookup[canonical.lower()] = canonical
        for alias in aliases:
            lookup[alias.lower()] = canonical
    return lookup


_LOOKUP: Dict[str, str] = _build_lookup()


def _strip_braces(value: str) -> str:
    return value.strip("{}").strip()


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_conference(value: Optional[str]) -> Optional[str]:
    """Return the canonical conference name for *value*, or *value* unchanged."""
    if not value:
        return None
    cleaned = _collapse_whitespace(_strip_braces(value))
    canonical = _LOOKUP.get(cleaned.lower())
    return canonical if canonical is not None else cleaned


def normalize_entry_conference(
    entry: Dict, fields: Optional[List[str]] = None
) -> Dict:
    """Return a copy of *entry* with conference fields normalised."""
    if fields is None:
        fields = ["booktitle", "journal"]
    updated = dict(entry)
    for field in fields:
        if field in updated:
            updated[field] = normalize_conference(updated[field])
    return updated


def normalize_bibliography_conferences(
    bibliography: List[Dict], fields: Optional[List[str]] = None
) -> List[Dict]:
    """Apply :func:`normalize_entry_conference` to every entry."""
    return [normalize_entry_conference(e, fields) for e in bibliography]
