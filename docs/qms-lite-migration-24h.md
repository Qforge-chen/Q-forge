# QMS Lite Migration In About 24 Hours

This document explains what changed in the first fast migration pass from the earlier Goose + MCP runtime into the current local OpenClaw quality runtime.

## Starting point

Before this pass, Q-Forge was already proven on the earlier runtime with four core capability packages:

- `8D`
- `RCA`
- `Supplier`
- `Reporter`

So the question was not whether the idea worked. The question was whether those working paths could be moved into a more suitable long-term runtime.

## Migration objective

Move the already working quality logic into:

- a local OpenClaw quality runtime
- a hardened Android chat client
- a local model backend

without turning the project into a generic assistant.

## What was migrated

### 8D

- migrated into a strict audit path
- local HTML artifact path locked to:
  - strict review
  - canonical markdown
  - local render

### RCA

- migrated into a detective-style chat path
- moved away from report-audit mode
- rebuilt as:
  - branch pruning
  - evidence-aware narrowing
  - final conclusion report only after convergence

### Supplier

- migrated as a lightweight deterministic spreadsheet path
- numbers remain tool-driven, not invented by the model
- final supplier report is checked before render

### Reporter

- reused as a deterministic local renderer
- became the final artifact layer for all three flows

## Why OpenClaw was a better fit

OpenClaw provided the shape needed for the next stage:

- local gateway
- multi-agent structure
- mobile pairing
- TLS
- local tool orchestration

But the default OpenClaw runtime was still too broad for quality work. That is why the migration was not "install OpenClaw and stop". It required a quality-specific runtime profile.

## Result of this pass

At the end of the migration sprint:

- the four capabilities were running in the local OpenClaw runtime
- Android mobile alpha proof was produced for supplier, 8D, and RCA
- the project moved from:
  - proof of concept on an earlier runtime
  - to a local OpenClaw quality edition with mobile proof

## What this repository now documents

- the original public proof layer
- the OpenClaw migration direction
- the public framework skeleton needed to follow the architecture
