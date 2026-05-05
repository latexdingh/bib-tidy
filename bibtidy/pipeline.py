"""High-level pipeline: parse → enrich → deduplicate → normalize keys → format."""

from typing import Optional

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.doi_resolver import enrich_entry
from bibtidy.key_normalizer import normalize_key
from bibtidy.deduplicator import deduplicate


def run(
    bibtex_input: str,
    resolve_dois: bool = True,
    dedup: bool = True,
    normalize_keys: bool = True,
    title_threshold: float = 0.85,
) -> str:
    """Run the full bib-tidy pipeline on a BibTeX string.

    Args:
        bibtex_input: Raw BibTeX source text.
        resolve_dois: Whether to fetch missing metadata via DOI lookup.
        dedup: Whether to remove duplicate entries.
        normalize_keys: Whether to regenerate citation keys.
        title_threshold: Similarity threshold used for title-based deduplication.

    Returns:
        Formatted, cleaned BibTeX string.
    """
    entries = parse_bibliography(bibtex_input)

    if resolve_dois:
        enriched = []
        for entry in entries:
            try:
                enriched.append(enrich_entry(entry))
            except Exception:
                # Network errors or bad DOIs should not abort the pipeline.
                enriched.append(entry)
        entries = enriched

    if dedup:
        entries = deduplicate(entries, title_threshold=title_threshold)

    if normalize_keys:
        entries = [normalize_key(entry) for entry in entries]

    return format_bibliography(entries)


def run_file(
    input_path: str,
    output_path: Optional[str] = None,
    **kwargs,
) -> str:
    """Read a .bib file, process it, and optionally write the result.

    Args:
        input_path: Path to the input .bib file.
        output_path: If provided, write the result to this path.
        **kwargs: Forwarded to :func:`run`.

    Returns:
        Formatted BibTeX string.
    """
    with open(input_path, 'r', encoding='utf-8') as fh:
        raw = fh.read()

    result = run(raw, **kwargs)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as fh:
            fh.write(result)

    return result
