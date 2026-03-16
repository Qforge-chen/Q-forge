# Public Examples

This folder contains the public example set for the current Q-Forge release.

## Principles

- Files are exported from saved local Q-Forge runs.
- Inputs and outputs are lightly sanitized before publication.
- The goal is clear public understanding, not full private runtime disclosure.

## What Is Included

### 8D

- `input/8d-case-good.docx`: positive 8D input sample
- `input/8d-case-bad.docx`: negative 8D input sample for input-gate context
- `output/8d-review-approved.md`: approved audit output
- `output/8d-review-rendered.html`: rendered HTML report from the same 8D chain

### Root Cause

- `output/rootcause-pm-ring.md`: markdown output from a saved RCA run
- `output/rootcause-pm-ring.html`: rendered HTML page for the same RCA case

## Usage Note

GitHub shows checked-in HTML files as source view. Download or open them locally if you want the final rendered page. Preview screenshots are available in the repository `assets/` folder.
