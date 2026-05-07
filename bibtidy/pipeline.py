"""
High-level pipeline that chains all bib-tidy transformations.

Each step is optional and controlled by keyword arguments.
"""

from pathlib import Path
from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.string_expander import expand_bibliography
from bibtidy.crossref_resolver import resolve_all_crossrefs
from bibtidy.key_normalizer import normalize_key
from bibtidy.deduplicator import deduplicate
from bibtidy.sorter import sort_entries
from bibtidy.field_filter import filter_bibliography
from bibtidy.year_normalizer import normalize_bibliography_years
from bibtidy.month_normalizer import normalize_bibliography_months
from bibtidy.page_normalizer import normalize_bibliography_pages
from bibtidy.url_cleaner import clean_bibliography_urls
from bibtidy.name_normalizer import normalize_bibliography_names


def run(
    source: str,
    *,
    expand_strings: bool = True,
    resolve_crossrefs: bool = True,
    normalize_keys: bool = True,
    dedup: bool = True,
    sort_field: Optional[str] = "year",
    sort_reverse: bool = False,
    keep_fields: Optional[list] = None,
    drop_fields: Optional[list] = None,
    normalize_years: bool = True,
    normalize_months: bool = True,
    normalize_pages: bool = True,
    clean_urls: bool = True,
    normalize_names: bool = True,
) -> str:
    """Run the full bib-tidy pipeline on *source* BibTeX text."""
    bibliography = parse_bibliography(source)

    if expand_strings:
        bibliography = expand_bibliography(bibliography)
    if resolve_crossrefs:
        bibliography = resolve_all_crossrefs(bibliography)
    if normalize_names:
        bibliography = normalize_bibliography_names(bibliography)
    if normalize_years:
        bibliography = normalize_bibliography_years(bibliography)
    if normalize_months:
        bibliography = normalize_bibliography_months(bibliography)
    if normalize_pages:
        bibliography = normalize_bibliography_pages(bibliography)
    if clean_urls:
        bibliography = clean_bibliography_urls(bibliography)
    if normalize_keys:
        bibliography = [
            {**e, "key": normalize_key(e)} for e in bibliography
        ]
    if dedup:
        bibliography = deduplicate(bibliography)
    if keep_fields is not None or drop_fields is not None:
        bibliography = filter_bibliography(
            bibliography,
            keep=keep_fields,
            drop=drop_fields,
        )
    if sort_field:
        bibliography = sort_entries(bibliography, sort_field, reverse=sort_reverse)

    return format_bibliography(bibliography)


def run_file(
    input_path: str,
    output_path: Optional[str] = None,
    **kwargs,
) -> None:
    """Read *input_path*, run the pipeline, write to *output_path*.

    If *output_path* is None the input file is overwritten in-place.
    """
    src = Path(input_path).read_text(encoding="utf-8")
    result = run(src, **kwargs)
    dest = output_path if output_path is not None else input_path
    Path(dest).write_text(result, encoding="utf-8")
