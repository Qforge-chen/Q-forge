from __future__ import annotations

from pathlib import Path

from .core import render_findings_file, render_markdown_file

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - optional dependency only
    FastMCP = None


if FastMCP is not None:
    mcp = FastMCP("q-skill-reporter")

    @mcp.tool()
    def render_markdown_report(input_path: str, output_path: str, title: str = "") -> dict:
        output = render_markdown_file(input_path, output_path, title=title or None)
        return {"status": "success", "output_path": str(Path(output).resolve())}

    @mcp.tool()
    def render_findings_report(input_path: str, output_path: str, title: str = "") -> dict:
        output = render_findings_file(input_path, output_path, title=title or None)
        return {"status": "success", "output_path": str(Path(output).resolve())}


def main() -> None:
    if FastMCP is None:
        raise RuntimeError("Install q-skill-reporter with the 'mcp' extra to use the optional MCP wrapper.")
    mcp.run(transport="stdio")
