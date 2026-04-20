"""Command-line interface for loven.

Usage
-----
    loven search <query> [--limit N] [--themes k1,k2]
    loven export <query> --output results.csv [--limit N]
    loven themes list

Examples
--------
    loven search "energilov miljø"
    loven search "vannressursloven" --limit 10
    loven export "miljøvern" --output results.csv
    loven themes list
"""

from __future__ import annotations

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="loven",
        description="WorldPeace-Lovdata-Kompendium – query Norwegian law from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ------------------------------------------------------------------ search
    search_parser = subparsers.add_parser(
        "search",
        help="Search Lovdata and print peace-relevant results.",
    )
    search_parser.add_argument("query", help="Norwegian search term(s).")
    search_parser.add_argument(
        "--limit", type=int, default=20, help="Max results to request (default: 20)."
    )
    search_parser.add_argument(
        "--themes",
        default=None,
        help="Comma-separated list of peace-theme keywords to override defaults.",
    )
    search_parser.add_argument(
        "--base-url",
        default=None,
        help="Override the Lovdata API base URL.",
    )

    # ------------------------------------------------------------------ export
    export_parser = subparsers.add_parser(
        "export",
        help="Search Lovdata and export results to a file.",
    )
    export_parser.add_argument("query", help="Norwegian search term(s).")
    export_parser.add_argument(
        "--output", required=True, help="Output file path (CSV or Excel .xlsx)."
    )
    export_parser.add_argument(
        "--limit", type=int, default=20, help="Max results to request (default: 20)."
    )
    export_parser.add_argument(
        "--themes",
        default=None,
        help="Comma-separated list of peace-theme keywords to override defaults.",
    )
    export_parser.add_argument(
        "--base-url",
        default=None,
        help="Override the Lovdata API base URL.",
    )

    # ------------------------------------------------------------------ themes
    themes_parser = subparsers.add_parser("themes", help="Manage peace themes.")
    themes_sub = themes_parser.add_subparsers(dest="themes_command", required=True)
    themes_sub.add_parser("list", help="List all current peace-theme keywords.")

    return parser


def _parse_themes(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    return [t.strip() for t in raw.split(",") if t.strip()]


def cmd_search(args: argparse.Namespace) -> None:
    from loven import LovDataClient, analyze_peace_laws

    themes = _parse_themes(args.themes)
    kwargs = {}
    if args.base_url:
        kwargs["base_url"] = args.base_url

    client = LovDataClient(**kwargs)
    df = analyze_peace_laws(client, args.query, limit=args.limit, themes=themes)

    if df.empty:
        print("No peace-relevant results found.")
        return

    # Pretty-print with pandas
    with __import__("pandas").option_context("display.max_colwidth", 80, "display.max_rows", 50):
        print(df[["tittel", "url", "tema_treff"]].to_string(index=False))


def cmd_export(args: argparse.Namespace) -> None:
    from loven import LovDataClient, analyze_peace_laws

    themes = _parse_themes(args.themes)
    kwargs = {}
    if args.base_url:
        kwargs["base_url"] = args.base_url

    client = LovDataClient(**kwargs)
    df = analyze_peace_laws(client, args.query, limit=args.limit, themes=themes)

    output = args.output
    if output.endswith(".xlsx"):
        df.to_excel(output, index=False)
    else:
        df.to_csv(output, index=False)

    print(f"Saved {len(df)} rows to '{output}'.")


def cmd_themes_list() -> None:
    from loven import PEACE_THEMES

    translations = {
        "energi": "energy",
        "vann": "water",
        "miljø": "environment",
        "etikk": "ethics",
        "selskap": "company / corporation",
        "oppløsning": "dissolution",
        "fred": "peace",
        "klima": "climate",
        "bolig": "housing",
        "arbeidsmiljø": "working environment",
    }

    print(f"{'Norwegian':<20} {'English'}")
    print("-" * 40)
    for theme in PEACE_THEMES:
        print(f"{theme:<20} {translations.get(theme, '—')}")


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "search":
        cmd_search(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "themes":
        if args.themes_command == "list":
            cmd_themes_list()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
