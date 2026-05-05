"""Command-line interface for bib-tidy."""

import argparse
import sys
from typing import List, Optional

from bibtidy.pipeline import run_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bib-tidy",
        description="Opinionated BibTeX bibliography formatter and deduplicator.",
    )
    parser.add_argument("input", help="Input .bib file path")
    parser.add_argument("-o", "--output", help="Output .bib file path (default: stdout)")
    parser.add_argument(
        "--sort",
        nargs="+",
        metavar="FIELD",
        help="Sort entries by fields (e.g. --sort year author)",
        default=None,
    )
    parser.add_argument(
        "--sort-reverse",
        action="store_true",
        help="Sort in descending order",
    )
    parser.add_argument(
        "--keep-fields",
        nargs="+",
        metavar="FIELD",
        help="Only keep these fields in each entry",
        default=None,
    )
    parser.add_argument(
        "--drop-fields",
        nargs="+",
        metavar="FIELD",
        help="Remove these fields from each entry",
        default=None,
    )
    parser.add_argument(
        "--no-deduplicate",
        action="store_true",
        help="Skip deduplication step",
    )
    parser.add_argument(
        "--no-normalize-keys",
        action="store_true",
        help="Skip citation key normalization",
    )
    parser.add_argument(
        "--resolve-doi",
        action="store_true",
        help="Resolve DOIs to enrich entries via CrossRef",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = run_file(
        args.input,
        deduplicate=not args.no_deduplicate,
        normalize_keys=not args.no_normalize_keys,
        resolve_doi=args.resolve_doi,
        sort_fields=args.sort,
        sort_reverse=args.sort_reverse,
        keep_fields=args.keep_fields,
        drop_fields=args.drop_fields,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result)
    else:
        sys.stdout.write(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
