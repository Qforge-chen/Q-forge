# q-skill-8d

**Open Tier: lite-core**

Q-Forge package for 8D report intake and audit.

## What It Does

- Reads Word-based 8D reports
- Validates critical sections with deterministic rules
- Flags missing containment, weak root cause logic, and incomplete closure conditions
- Produces review outputs that can be rendered into HTML

In the current internal baseline, this capability family is also carried forward inside the OpenClaw QMS overlay as a skill protocol plus deterministic runner path.

This public package stays at the lite-core layer for now:

- public contract schema
- synthetic review-result fixture
- smoke-level contract test
- existing public MCP-era code preserved for reference

The full private overlay keeps denser rules, richer audit wording, and live regression material out of the public repo.

## Public Proof

- [Good input sample](../../examples/8d/input/8d-case-good.docx)
- [Bad input sample](../../examples/8d/input/8d-case-bad.docx)
- [Approved audit output](../../examples/8d/output/8d-review-approved.md)
- [Rendered HTML output](../../examples/8d/output/8d-review-rendered.html)

## Public Structure In This Pass

- `schemas/`: public review-result contract
- `fixtures/`: synthetic public output fixture
- `tests/`: smoke checks for the public contract layer

## Install

```bash
pip install -e .
```
