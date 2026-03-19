# q-skill-supplier

**Open Tier: lite-core**

Q-Forge package for IQC and supplier quality monitoring.

## What It Does

- Reads supplier quality inputs such as inspection or metric tables
- Tracks quality performance, risk signals, and ranking logic
- Supports supplier-facing quality monitoring workflows

In the current internal baseline, this capability family is also carried forward inside the OpenClaw QMS overlay as a deterministic skill protocol plus runner path.

This public package stays at the lite-core layer for now:

- public analysis schema
- synthetic summary fixture
- smoke-level contract test
- existing public MCP-era code preserved for reference

## Public Proof And Position In This Pass

This package is already part of the working Q-Forge stack.

Public proof currently includes:

- [Supplier mobile proof HTML](../../docs/mobile-proof/supplier-mobile-proof-20260316.html)
- [Supplier mobile screenshot](../../docs/mobile-proof/supplier-mobile-proof-20260316.jpg)

The public repo is still visually centered on the 8D and RCA proof chains first, but supplier is no longer only a future promise.

## Public Structure In This Pass

- `schemas/`: public supplier-analysis contract
- `fixtures/`: synthetic public summary fixture
- `tests/`: smoke checks for the public contract layer

## Install

```bash
pip install -e .
```
