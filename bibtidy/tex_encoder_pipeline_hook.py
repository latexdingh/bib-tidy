"""Pipeline integration hook for tex_encoder.

Provides encode/decode steps that can be inserted into the bib-tidy pipeline
to normalize LaTeX encoding across all entries in a bibliography.
"""

from bibtidy.tex_encoder import encode_entry, decode_entry

# Fields typically containing human-readable text with potential special chars
_TEXT_FIELDS = [
    "author", "editor", "title", "booktitle", "journal",
    "series", "publisher", "address", "note", "abstract",
    "institution", "organization", "school",
]


def encode_bibliography(
    entries: list[dict],
    fields: list[str] | None = None,
    text_fields_only: bool = True,
) -> list[dict]:
    """Encode Unicode to LaTeX in all entries.

    Args:
        entries: List of parsed BibTeX entry dicts.
        fields: Explicit list of fields to encode. Overrides text_fields_only.
        text_fields_only: If True and fields is None, only encode known text fields.

    Returns:
        New list of entries with encoded fields.
    """
    target_fields = fields if fields is not None else (_TEXT_FIELDS if text_fields_only else None)
    return [encode_entry(e, fields=target_fields) for e in entries]


def decode_bibliography(
    entries: list[dict],
    fields: list[str] | None = None,
    text_fields_only: bool = True,
) -> list[dict]:
    """Decode LaTeX escapes to Unicode in all entries.

    Args:
        entries: List of parsed BibTeX entry dicts.
        fields: Explicit list of fields to decode. Overrides text_fields_only.
        text_fields_only: If True and fields is None, only decode known text fields.

    Returns:
        New list of entries with decoded fields.
    """
    target_fields = fields if fields is not None else (_TEXT_FIELDS if text_fields_only else None)
    return [decode_entry(e, fields=target_fields) for e in entries]


def normalize_encoding(
    entries: list[dict],
    mode: str = "encode",
    fields: list[str] | None = None,
) -> list[dict]:
    """Convenience wrapper: encode or decode a bibliography.

    Args:
        entries: List of BibTeX entry dicts.
        mode: 'encode' to convert Unicode -> LaTeX, 'decode' for the reverse.
        fields: Fields to process; None uses default text fields.

    Returns:
        Processed list of entries.

    Raises:
        ValueError: If mode is not 'encode' or 'decode'.
    """
    if mode == "encode":
        return encode_bibliography(entries, fields=fields)
    elif mode == "decode":
        return decode_bibliography(entries, fields=fields)
    else:
        raise ValueError(f"Unknown mode {mode!r}. Expected 'encode' or 'decode'.")
