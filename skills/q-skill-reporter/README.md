# q-skill-reporter

**Open Tier: full**

Q-Forge package for turning validated quality outputs into reviewable HTML artifacts.

## What Is Public In This Package

This package is intentionally published as a runnable core layer:

- CLI entrypoint
- reusable Python rendering library
- schemas for structured findings input
- fixtures and example outputs
- tests for rendering and CLI smoke

The primary public entry is the core renderer. The MCP wrapper is optional and not the main open-source surface.

## What It Does

- Renders markdown into a polished HTML report
- Renders structured findings JSON into a decision-ready HTML artifact
- Keeps report output deterministic and reviewable
- Avoids private runtime paths and customer-specific styling

## Quick Start

```bash
pip install -e .
q-skill-reporter render-markdown --input fixtures/sample-report.md --output examples/sample-report.html --title "Q-Forge Sample Report"
```

## Public Proof

- [8D rendered HTML](../../examples/8d/output/8d-review-rendered.html)
- [8D preview image](../../assets/8d-rendered-report-preview.png)
- [RCA rendered HTML](../../examples/rootcause/output/rootcause-pm-ring.html)
- [RCA preview image](../../assets/rootcause-rendered-report-preview.png)

## Package Layout

- `src/q_skill_reporter/`: reusable renderer core and CLI
- `schemas/`: public structured input contract
- `fixtures/`: synthetic inputs for smoke and regression checks
- `tests/`: runnable package tests
- `examples/`: generated sample outputs that are safe to publish

## Boundary

Included here:

- renderer core
- stable output template
- example artifacts

Not included here:

- private runtime paths
- private QMS overlay logic
- private customer branding or style packs
