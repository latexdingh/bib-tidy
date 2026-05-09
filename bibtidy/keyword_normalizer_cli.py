"""
Standalone CLI entry point for the keyword normalizer.

Usage::

    python -m bibtidy.keyword_normalizer_cli refs.bib [--separator "; "]
"""

from __future__ import annotations

import argparse
import sys

from bibtidy.keyword_normalizer_pipeline_hook import run_on_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bib-tidy-keywords",
        description="Normalize, deduplicate and sort BibTeX keyword fields.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="FILE",
        help=".bib file(s) to process (modified in place).",
    )
    parser.add_argument(
        "--separator",
        default="; ",
        metavar="SEP",
        help="Separator used between keywords in output (default: '; ').",
    )
    parser.add_argument(
        "--field",
        default="keywords",
        metavar="FIELD",
        help="BibTeX field to normalize (default: keywords).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    errors = 0
    for path in args.files:
        try:
            run_on_file(path, field=args.field, separator=args.separator)
            print(f"Normalized keywords in {path}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR processing {path}: {exc}", file=sys.stderr)
            errors += 1
    return errors


if __name__ == "__main__":
    sys.exit(main())
