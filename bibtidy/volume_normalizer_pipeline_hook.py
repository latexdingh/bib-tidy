"""Pipeline hook for volume/number normalization."""

from pathlib import Path

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.volume_normalizer import normalize_bibliography_volumes


def apply(
    bibliography: list[dict],
    volume_field: str = 'volume',
    number_field: str = 'number',
) -> list[dict]:
    """Normalize volume and number fields for every entry.

    Parameters
    ----------
    bibliography:
        List of parsed BibTeX entry dicts.
    volume_field:
        Name of the volume field (default ``'volume'``).
    number_field:
        Name of the number/issue field (default ``'number'``).

    Returns
    -------
    list[dict]
        New list with normalized entries.
    """
    from bibtidy.volume_normalizer import normalize_entry_volume

    return [
        normalize_entry_volume(entry, volume_field=volume_field, number_field=number_field)
        for entry in bibliography
    ]


def run_on_file(
    path: str | Path,
    volume_field: str = 'volume',
    number_field: str = 'number',
) -> None:
    """Read *path*, normalize volume/number fields in place, and overwrite."""
    path = Path(path)
    source = path.read_text(encoding='utf-8')
    bibliography = parse_bibliography(source)
    normalized = apply(bibliography, volume_field=volume_field, number_field=number_field)
    path.write_text(format_bibliography(normalized), encoding='utf-8')
