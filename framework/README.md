# Framework Snapshot

This folder is the public framework skeleton for QMS Lite.

It is intentionally smaller than the private working forks. The purpose is to let other builders follow the architecture and logic boundaries without exposing the entire local implementation.

## Included here

- local OpenClaw QMS profile example
- tool contract snapshot
- workspace behavior rules for:
  - `qm-review`
  - `qm-rca`
- logic-path summary for the deterministic chains

## Why this folder exists

This repository should not be only screenshots and rendered proof.

If somebody wants to follow the build, they should be able to see:

- how the runtime is shaped
- how the agents are scoped
- how tool contracts are defined
- how the strict 8D path differs from detective-style RCA

## Not included

- live secrets
- real local runtime config values
- full private forks
- complete Android private source
