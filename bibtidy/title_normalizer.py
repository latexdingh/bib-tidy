"""Normalize BibTeX title fields: strip outer braces, fix whitespace,
and apply consistent title-casing while preserving protected groups."""

import re
from typing import Optional

# Words that should remain lowercase in title case (unless first word)
_STOPWORDS = {
    "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet",
    "at", "by", "in", "of", "on", "to", "up", "as", "is", "it",
    "via", "vs", "with", "from", "into", "onto", "over", "than",
}


def _strip_outer_braces(value: str) -> str:
    """Remove a single layer of wrapping braces if present."""
    s = value.strip()
    if s.startswith("{") and s.endswith("}"):
        # Only strip if the braces are truly the outer wrapper
        depth = 0
        for i, ch in enumerate(s):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if depth == 0 and i < len(s) - 1:
                return s  # inner brace closes before end — not a simple wrapper
        return s[1:-1].strip()
    return s


def _collapse_whitespace(value: str) -> str:
    """Collapse runs of whitespace into a single space."""
    return re.sub(r"\s+", " ", value).strip()


def _title_case_preserving_braces(value: str) -> str:
    """Apply title-case to *value*, leaving content inside {...} untouched."""
    # Tokenise into protected segments and plain text
    parts = re.split(r"(\{[^}]*\})", value)
    result = []
    word_index = 0
    for part in parts:
        if part.startswith("{"):
            result.append(part)  # protected group — keep as-is
        else:
            words = re.split(r"(\s+)", part)
            for token in words:
                if re.match(r"\s+", token):
                    result.append(token)
                else:
                    if not token:
                        continue
                    lower = token.lower()
                    if word_index == 0 or lower not in _STOPWORDS:
                        result.append(token.capitalize())
                    else:
                        result.append(lower)
                    word_index += 1
    return "".join(result)


def normalize_title(
    title: Optional[str],
    title_case: bool = False,
    strip_braces: bool = True,
) -> Optional[str]:
    """Normalize a single title string.

    Parameters
    ----------
    title:        Raw title value (may be None).
    title_case:   If True, apply title-casing (preserving brace-protected groups).
    strip_braces: If True, remove a single outer brace wrapper.
    """
    if not title:
        return None
    value = title
    if strip_braces:
        value = _strip_outer_braces(value)
    value = _collapse_whitespace(value)
    if title_case:
        value = _title_case_preserving_braces(value)
    return value or None


def normalize_entry_title(
    entry: dict,
    title_case: bool = False,
    strip_braces: bool = True,
) -> dict:
    """Return a copy of *entry* with the title field normalized."""
    raw = entry.get("fields", {}).get("title")
    normalized = normalize_title(raw, title_case=title_case, strip_braces=strip_braces)
    new_fields = dict(entry.get("fields", {}))
    if normalized is not None:
        new_fields["title"] = normalized
    elif "title" in new_fields:
        del new_fields["title"]
    return {**entry, "fields": new_fields}


def normalize_bibliography_titles(
    bibliography: list,
    title_case: bool = False,
    strip_braces: bool = True,
) -> list:
    """Apply title normalization to every entry in *bibliography*."""
    return [
        normalize_entry_title(e, title_case=title_case, strip_braces=strip_braces)
        for e in bibliography
    ]
