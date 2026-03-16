# Framework Snapshot

This folder is the public framework skeleton for QMS Lite.

It is intentionally smaller than the private working forks. The purpose is to let other builders follow the architecture and logic boundaries without exposing the entire local implementation.

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

## Not included

- live secrets
- real local runtime config values
- full private forks
- complete Android private source

## Files to read first

- `openclaw-qms-lite/openclaw.qms.local.example.jsonc`
- `openclaw-qms-lite/tool-contracts.snapshot.ts`
- `openclaw-qms-lite/qms_bridge_reference.py`
- `openclaw-qms-lite/logic-paths.md`
- `openclaw-qms-lite/rca_detective_flow.md`
- `openclaw-qms-lite/mobile_runtime_boundary.md`
