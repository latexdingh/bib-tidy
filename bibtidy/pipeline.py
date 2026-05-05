"""End-to-end pipeline for bib-tidy.

Orchestrates parsing, deduplication, DOI enrichment, key normalization,
field filtering, journal abbreviation, sorting, and formatting.
"""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.deduplicator import deduplicate
from bibtidy.doi_resolver import enrich_entry
from bibtidy.key_normalizer import normalize_key
from bibtidy.field_filter import filter_bibliography
from bibtidy.sorter import sort_entries
from bibtidy.abbreviator import abbreviate_bibliography


def run(
    source: str,
    *,
    sort_field: Optional[str] = "year",
    sort_reverse: bool = False,
    keep_fields: Optional[list[str]] = None,
    drop_fields: Optional[list[str]] = None,
    resolve_doi: bool = False,
    normalize_keys: bool = True,
    abbreviate_journals: bool = False,
    abbreviations: Optional[dict[str, str]] = None,
) -> str:
    """Run the full bib-tidy pipeline on *source* BibTeX text.

    Returns formatted BibTeX as a string.
    """
    entries = parse_bibliography(source)

    # Deduplicate
    entries = deduplicate(entries)

    # Optionally resolve DOIs
    if resolve_doi:
        enriched = []
        for entry in entries:
            try:
                enriched.append(enrich_entry(entry))
            except Exception:
                enriched.append(entry)
        entries = enriched

    # Normalize citation keys
    if normalize_keys:
        entries = [normalize_key(e) for e in entries]

    # Filter fields
    entries = filter_bibliography(
        entries, keep=keep_fields or [], drop=drop_fields or []
    )

    # Abbreviate journal names
    if abbreviate_journals:
        entries = abbreviate_bibliography(entries, abbreviations=abbreviations)

    # Sort
    if sort_field:
        entries = sort_entries(entries, field=sort_field, reverse=sort_reverse)

    return format_bibliography(entries)


def run_file(
    input_path: str,
    output_path: Optional[str] = None,
    **kwargs,
) -> str:
    """Run the pipeline on a BibTeX file.

    If *output_path* is given, writes the result there as well as returning it.
    """
    source = Path(input_path).read_text(encoding="utf-8")
    result = run(source, **kwargs)
    if output_path:
        Path(output_path).write_text(result, encoding="utf-8")
    return result
