# q-skill-rootcause

**Open Tier: protocol-core**

Q-Forge package for constrained root cause analysis workflows.

## What It Does

- Guides root cause reasoning with process maps and fault-tree logic
- Uses elimination and branch pruning instead of free-form chat
- Produces saved markdown outputs that can be rendered into HTML

In the current internal baseline, this capability family is also carried forward inside the OpenClaw QMS overlay as a skill protocol with evidence-chain discipline and deterministic support steps.

This public package stays at the protocol-core layer for now:

- public evidence-chain schema
- synthetic protocol fixture
- smoke-level checker for the public contract
- existing MCP-era package preserved as a public bridge reference

## Public Proof

- [Markdown output](../../examples/rootcause/output/rootcause-pm-ring.md)
- [Rendered HTML output](../../examples/rootcause/output/rootcause-pm-ring.html)

## Public Structure In This Pass

- `schemas/`: public evidence-chain contract
- `fixtures/`: synthetic protocol fixture
- `tests/`: smoke checks for the public contract layer

## Install

```bash
pip install -e .
```
