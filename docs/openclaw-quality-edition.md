# OpenClaw Quality Edition

QMS Lite is the quality-customized OpenClaw profile behind the latest Q-Forge migration pass.

It is not a generic assistant with a few domain prompts added on top. It is a local runtime profile designed around quality work.

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
- QMS tools: deterministic 8D, RCA, supplier, reporter paths
- LM Studio: local model backend
- local artifact root: generated HTML and audit traces

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
