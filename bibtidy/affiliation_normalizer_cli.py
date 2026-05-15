"""
CLI entry-point for affiliation normalization.

Usage
-----
    python -m bibtidy.affiliation_normalizer_cli input.bib [--field affiliation]
    python -m bibtidy.affiliation_normalizer_cli input.bib --stdout
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.affiliation_normalizer import normalize_bibliography_affiliations


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bibtidy-affiliation",
        description="Normalize affiliation fields in a BibTeX file.",
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        help="Path to the input .bib file.",
    )
    parser.add_argument(
        "--field",
        default="affiliation",
        metavar="FIELD",
        help="Name of the field to normalize (default: affiliation).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write result to stdout instead of overwriting the input file.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        metavar="ENCODING",
        help="File encoding (default: utf-8).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    path = Path(args.input)
    source = path.read_text(encoding=args.encoding)
    bibliography = parse_bibliography(source)
    normalized = normalize_bibliography_affiliations(bibliography, field=args.field)
    output = format_bibliography(normalized)

    if args.stdout:
        sys.stdout.write(output)
    else:
        path.write_text(output, encoding=args.encoding)


if __name__ == "__main__":  # pragma: no cover
    main()
