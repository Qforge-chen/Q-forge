# OpenClaw Quality Edition

QMS Lite is the quality-customized OpenClaw profile behind the latest Q-Forge migration pass.

It is not a generic assistant with a few domain prompts added on top. It is a local runtime profile designed around quality work.

The current direction has now hardened further into a clean-host overlay baseline. The host stays close to upstream OpenClaw, while the QMS-specific behavior lives in the overlay layer.

## Product role

- quality co-pilot
- not a digital clone of the quality engineer
- not an autonomous sign-off system
- focused on structured, repetitive, evidence-sensitive workflows

## Core v1 scope

- `8D`: report audit and D3-D7 logic lock
- `RCA`: detective-style root cause conversation, branch pruning, and conclusion report
- `Supplier`: spreadsheet triage with deterministic metrics
- `Reporter`: local HTML artifact generation
- `secretary -> qms`: front-door coordination and specialist handoff

## Why this exists

In quality work, the main problem is not only "how to call a model". The real problem is how to keep the runtime safe and the conclusions reviewable.

That means:

- local files should stay local by default
- mobile access should be reduced to a secure chat terminal
- agent scopes must be narrow
- tool paths must be deterministic
- the system must separate:
  - stable reference knowledge
  - daily incoming case material

## Runtime layers

- Android client: secure chat terminal
- OpenClaw gateway: sessions, pairing, TLS, routing
- QMS overlay: skills, deterministic runners, artifacts, audit rules, and agent boundaries
- LM Studio: local model backend
- local artifact root: generated HTML and audit traces

## Current validated baseline

The current private working baseline behind this public repo is:

- clean OpenClaw host kept close to upstream
- no OpenClaw core modifications for the QMS V1 layer
- local LM Studio inference
- `secretary` as the intake and coordination agent
- `qms` as the deep quality specialist
- live regression on real sessions
- validated `secretary -> qms` handoff

See [OpenClaw V1 Overlay Baseline](openclaw-v1-overlay-baseline.md) for the focused note on this milestone.

## Public vs private boundary

Public in this repository:

- architecture
- migration logic
- public framework snapshot
- sanitized mobile proof

Not public here:

- full private OpenClaw fork
- full private Android fork
- live tokens, IPs, or device secrets
- real runtime case files
