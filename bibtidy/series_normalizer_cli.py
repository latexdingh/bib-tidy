"""CLI entry point for standalone series normalization."""

import argparse
import sys
from pathlib import Path

from bibtidy.parser import parse_bibliography
from bibtidy.formatter import format_bibliography
from bibtidy.series_normalizer import normalize_bibliography_series


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bibtidy-series",
        description="Normalize the 'series' field in a BibTeX file.",
    )
    parser.add_argument("input", help="Input .bib file")
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: overwrite input)",
        default=None,
    )
    parser.add_argument(
        "--encoding",
        help="File encoding (default: utf-8)",
        default="utf-8",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    source = Path(args.input).read_text(encoding=args.encoding)
    entries = parse_bibliography(source)
    normalized = normalize_bibliography_series(entries)
    output = format_bibliography(normalized)

    dest = args.output if args.output else args.input
    Path(dest).write_text(output, encoding=args.encoding)
    print(f"Series normalization complete. Output written to: {dest}")


if __name__ == "__main__":
    main()
