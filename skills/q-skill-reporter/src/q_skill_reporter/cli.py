from __future__ import annotations

import argparse
from pathlib import Path

from .core import render_findings_file, render_markdown_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Q-Forge reporter core CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    markdown_parser = subparsers.add_parser("render-markdown", help="Render a markdown file into HTML")
    markdown_parser.add_argument("--input", required=True, help="Path to a markdown input file")
    markdown_parser.add_argument("--output", required=True, help="Path to the HTML output file")
    markdown_parser.add_argument("--title", help="Optional HTML report title")

    findings_parser = subparsers.add_parser("render-findings", help="Render a structured findings JSON file into HTML")
    findings_parser.add_argument("--input", required=True, help="Path to a JSON findings file")
    findings_parser.add_argument("--output", required=True, help="Path to the HTML output file")
    findings_parser.add_argument("--title", help="Optional HTML report title")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "render-markdown":
        output_file = render_markdown_file(args.input, args.output, title=args.title)
    else:
        output_file = render_findings_file(args.input, args.output, title=args.title)

    print(Path(output_file).resolve())
    return 0
