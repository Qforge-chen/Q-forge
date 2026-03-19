# Framework Snapshot

This folder is the public framework skeleton for the OpenClaw quality edition.

It is intentionally smaller than the private working forks. The purpose is to let other builders follow the architecture and logic boundaries without exposing the entire local implementation.

The files here are a public snapshot, not a byte-for-byte mirror of the latest private working baseline. The current validated baseline is described in [docs/openclaw-v1-overlay-baseline.md](../docs/openclaw-v1-overlay-baseline.md).

## Included here

- local OpenClaw QMS profile example
- tool contract snapshot
- bridge reference snapshot
- workspace behavior rules for:
  - `qm-review`
  - `qm-rca`
- logic-path summary for the deterministic chains
- RCA detective flow summary
- mobile runtime boundary summary

## Why this folder exists

This repository should not be only screenshots and rendered proof.

If somebody wants to follow the build, they should be able to see:

- how the runtime is shaped
- how the agents are scoped
- how tool contracts are defined
- how the strict 8D path differs from detective-style RCA
- how the bridge enforces deterministic paths
- how the mobile client is kept inside a narrow runtime boundary

## Current interpretation

The latest private validated baseline has moved toward:

- a clean OpenClaw host
- a QMS overlay instead of core patches
- `secretary` as the front door
- `qms` as the specialist
- live regression and handoff checks

This public framework folder remains useful because it still shows the engineering logic behind the quality runtime, even when specific internal agent names or layouts continue to evolve.

## Not included

- live secrets
- real local runtime config values
- full private forks
- complete Android private source

## Files to read first

- `openclaw-quality-edition/openclaw.qms.local.example.jsonc`
- `openclaw-quality-edition/tool-contracts.snapshot.ts`
- `openclaw-quality-edition/qms_bridge_reference.py`
- `openclaw-quality-edition/logic-paths.md`
- `openclaw-quality-edition/rca_detective_flow.md`
- `openclaw-quality-edition/mobile_runtime_boundary.md`
