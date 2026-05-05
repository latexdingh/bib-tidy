"""BibTeX formatter module for bib-tidy.

Serialises structured entry dicts back into formatted BibTeX strings.
"""

INDENT = "  "
DEFAULT_FIELD_ORDER = [
    "author",
    "title",
    "year",
    "journal",
    "booktitle",
    "volume",
    "number",
    "pages",
    "publisher",
    "doi",
    "url",
    "note",
]


def format_entry(entry: dict, field_order: list[str] | None = None) -> str:
    """Serialise a single entry dict into a formatted BibTeX string.

    Args:
        entry: A parsed entry dict with 'type', 'key', and 'fields'.
        field_order: Optional list specifying preferred field ordering.

    Returns:
        A formatted BibTeX entry string.
    """
    if field_order is None:
        field_order = DEFAULT_FIELD_ORDER

    entry_type = entry["type"]
    citation_key = entry["key"]
    fields = entry["fields"]

    ordered_keys = [k for k in field_order if k in fields]
    remaining_keys = sorted(k for k in fields if k not in field_order)
    all_keys = ordered_keys + remaining_keys

    field_lines = []
    for key in all_keys:
        value = fields[key]
        field_lines.append(f"{INDENT}{key} = {{{value}}}")

    fields_str = ",\n".join(field_lines)
    return f"@{entry_type}{{{citation_key},\n{fields_str}\n}}"


def format_bibliography(entries: list[dict], field_order: list[str] | None = None) -> str:
    """Serialise a list of entry dicts into a formatted BibTeX bibliography.

    Args:
        entries: List of parsed entry dicts.
        field_order: Optional list specifying preferred field ordering.

    Returns:
        A formatted .bib file string.
    """
    return "\n\n".join(format_entry(e, field_order) for e in entries) + "\n"
