# Android Secure Chat Client

The Android side of the OpenClaw quality edition was not treated as a consumer app. It was reduced into a quality-work chat terminal.

## What changed

- gateway-first flow
- pairing over TLS
- local-network use only for the current alpha
- no default raw document upload path

## Hardening decisions

- Firebase removed
- update checks removed
- cleartext traffic disabled
- main user-facing activities protected during the hardening pass
- manifest reduced to a smaller permission set
- general assistant paths reduced so the active runtime path is:
  - chat
  - settings

## Why this matters

The point of this fork was not to build a flashy assistant app. The point was to make the mobile side safe enough for a local quality runtime:

- less permission surface
- less unrelated system integration
- clearer gateway-only behavior

## Current public proof

This repository does not publish the full Android private implementation. Instead it publishes the proof that the hardened client is already working:

- supplier mobile proof
- 8D mobile proof
- RCA mobile proof

See [`mobile-proof/`](mobile-proof/).
