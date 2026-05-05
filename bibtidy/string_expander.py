"""Expand BibTeX @string macros within bibliography entries."""

import re
from typing import Dict, List

# Matches @string{key = {value}} or @string{key = "value"}
_STRING_PATTERN = re.compile(
    r'@string\s*\{\s*([\w]+)\s*=\s*[{"](.*?)[}"]\s*\}',
    re.IGNORECASE | re.DOTALL,
)


def extract_string_macros(bib_source: str) -> Dict[str, str]:
    """Parse @string definitions from raw BibTeX source.

    Returns a dict mapping macro name -> expanded value.
    """
    macros: Dict[str, str] = {}
    for match in _STRING_PATTERN.finditer(bib_source):
        key, value = match.group(1).strip(), match.group(2).strip()
        macros[key] = value
    return macros


def expand_value(value: str, macros: Dict[str, str]) -> str:
    """Expand macro references inside a field value.

    Handles simple concatenation with '#', e.g. ``jan # " 2020"``.
    """
    parts = [p.strip() for p in value.split("#")]
    expanded_parts: List[str] = []
    for part in parts:
        # Strip surrounding braces or quotes if present
        if (part.startswith("{") and part.endswith("}")) or (
            part.startswith('"') and part.endswith('"')
        ):
            expanded_parts.append(part[1:-1])
        elif part in macros:
            expanded_parts.append(macros[part])
        else:
            # Unknown macro: leave as-is
            expanded_parts.append(part)
    return "".join(expanded_parts)


def expand_entry(
    entry: Dict, macros: Dict[str, str]
) -> Dict:
    """Return a copy of *entry* with all field values macro-expanded."""
    expanded = dict(entry)
    expanded["fields"] = {
        k: expand_value(v, macros) for k, v in entry.get("fields", {}).items()
    }
    return expanded


def expand_bibliography(
    entries: List[Dict], macros: Dict[str, str]
) -> List[Dict]:
    """Expand macros in every entry of a bibliography list."""
    return [expand_entry(e, macros) for e in entries]
