"""
CLI entry-point for the conference normaliser.

Usage::

    python -m bibtidy.conference_normalizer_cli refs.bib
    python -m bibtidy.conference_normalizer_cli refs.bib --fields booktitle
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from bibtidy.conference_normalizer_pipeline_hook import run_on_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bibtidy-conference",
        description="Normalise conference/venue names in a BibTeX file.",
    )
    parser.add_argument("file", help="Path to the .bib file to process.")
    parser.add_argument(
        "--fields",
        nargs="+",
        default=None,
        metavar="FIELD",
        help="BibTeX fields to normalise (default: booktitle journal).",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding (default: utf-8).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    run_on_file(str(path), fields=args.fields, encoding=args.encoding)
    print(f"Conference names normalised in {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
