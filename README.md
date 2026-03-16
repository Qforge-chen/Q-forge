# Q-Forge

Q-Forge is a quality-focused agent system for manufacturing workflows, not a generic chatbot.

This public repository is no longer only a proof page. It is now the public proof layer plus the migration blueprint for a local quality-specific OpenClaw runtime.

## 24-Hour Migration Result

Within roughly 24 hours, the four Q-Forge capabilities that had already been proven on Goose + MCP were migrated into a local OpenClaw quality runtime and a hardened Android chat client:

- `8D`
- `RCA`
- `Supplier`
- `Reporter`

The result is not a generic OpenClaw setup with extra prompts. It is a local quality runtime profile with:

- deterministic tool paths
- evidence-locked workflows
- local artifact generation
- mobile proof on Android

[![8D DOCX review demo](assets/8d-docx-review-demo-cover.jpg)](assets/8d-docx-review-demo-short.mp4)

Open the preview image to watch the 40-second 8D demo from the earlier Goose + MCP phase.

## What Is Public Here

- real public skill packages under [`skills/`](skills/)
- sanitized inputs, outputs, and rendered artifacts under [`examples/`](examples/) and [`docs/mobile-alpha-proof/`](docs/mobile-alpha-proof/)
- public QMS Lite design and migration documents under [`docs/`](docs/)
- a minimal framework snapshot under [`framework/`](framework/) so other builders can follow the architecture without needing the full private runtime

## Already Working Now

| Capability | Current working path | Public proof |
| --- | --- | --- |
| **8D** | strict 8D audit path, deterministic D3-D7 checks, local HTML artifact, Android-triggered proof | [good 8D HTML](docs/mobile-alpha-proof/8d-mobile-proof-good-20260316.html), [bad 8D HTML](docs/mobile-alpha-proof/8d-mobile-proof-bad-20260316.html), [good chat screenshot](docs/mobile-alpha-proof/8d-mobile-chat-proof-good-20260316.jpg), [bad chat screenshot](docs/mobile-alpha-proof/8d-mobile-chat-proof-bad-20260316.jpg) |
| **RCA** | detective-style branch-pruning chat, strongest cause-path conclusion, local HTML artifact, Android-triggered proof | [RCA HTML](docs/mobile-alpha-proof/rca-mobile-proof-20260316.html), [start screenshot](docs/mobile-alpha-proof/rca-mobile-chat-start-20260316.jpg), [pruning screenshot](docs/mobile-alpha-proof/rca-mobile-chat-pruning-20260316.jpg), [conclusion screenshot](docs/mobile-alpha-proof/rca-mobile-chat-conclusion-20260316.jpg) |
| **Supplier** | deterministic spreadsheet analysis, validation lock, local HTML artifact, Android-triggered proof | [supplier HTML](docs/mobile-alpha-proof/supplier-mobile-proof-20260316.html), [supplier screenshot](docs/mobile-alpha-proof/supplier-mobile-proof-20260316.jpg) |
| **Reporter** | deterministic markdown-to-HTML renderer used by all three flows above | [8D preview](assets/8d-rendered-report-preview.png), [RCA preview](assets/rootcause-rendered-report-preview.png) |

## Why Not Generic OpenClaw + Skills

Generic OpenClaw plus skills can add knowledge, but it does not automatically solve the runtime problem of quality work.

Quality-specific deployment needs:

- local data handling instead of casual cloud routing
- a reduced-permission mobile channel
- deterministic tool boundaries
- separate stable knowledge and daily work inputs
- logic-locked review paths instead of free-form model output
- rendered artifacts that can be reviewed and audited later

That is why QMS Lite is a runtime profile, not only a prompt pack.

## What Was Customized

### OpenClaw local quality edition

- OpenClaw was reduced into a QMS Lite runtime profile
- the local gateway was kept, but the work was narrowed to quality workflows
- `qm-review` and `qm-rca` were turned into skill-driven agents instead of generic assistants
- `8D`, `RCA`, `Supplier`, and `Reporter` were wired into deterministic local tool paths
- local data was split into:
  - `knowledge-base`
  - `work-inbox`
  - `artifacts`
  - `audit`

### Android secure chat edition

- the Android client was reduced from a general assistant into a secure chat terminal
- Firebase and update checks were removed
- cleartext traffic was disabled
- `FLAG_SECURE` and gateway-only behavior were enforced during the hardening pass
- the phone proof shown here was produced against the local OpenClaw QMS Lite gateway, not against a cloud runtime

## Follow The Build

### Public design docs

- [QMS Lite Overview](docs/qms-lite-overview.md)
- [24-Hour Migration Notes](docs/qms-lite-migration-24h.md)
- [QMS Lite Architecture](docs/qms-lite-architecture.md)
- [QMS Lite Android Hardening](docs/qms-lite-android.md)
- [Mobile Alpha Proof Index](docs/mobile-alpha-proof/README.md)

### Public framework snapshot

- [framework/README.md](framework/README.md)
- [OpenClaw QMS local profile example](framework/openclaw-qms-lite/openclaw.qms.local.example.jsonc)
- [Tool contract snapshot](framework/openclaw-qms-lite/tool-contracts.snapshot.ts)
- [qm-review workspace rules](framework/openclaw-qms-lite/qm-review.AGENTS.md)
- [qm-rca workspace rules](framework/openclaw-qms-lite/qm-rca.AGENTS.md)
- [Logic path summary](framework/openclaw-qms-lite/logic-paths.md)

## Earlier Public Examples

These remain useful as the original Goose + MCP proof layer:

- [8D good input](examples/8d/input/8d-case-good.docx)
- [8D bad input](examples/8d/input/8d-case-bad.docx)
- [8D audit markdown](examples/8d/output/8d-review-approved.md)
- [8D rendered HTML](examples/8d/output/8d-review-rendered.html)
- [RCA legacy markdown](examples/rootcause/output/rootcause-pm-ring.md)
- [RCA legacy rendered HTML](examples/rootcause/output/rootcause-pm-ring.html)

## Builder Update

- Q-Forge had already been proven on Goose + MCP before this migration pass started.
- The practical thesis was already validated: large models plus deterministic rules can produce useful quality outcomes.
- The current direction is now clearer: a local OpenClaw quality runtime plus Q-Forge-style skills is a better long-term base than staying on the old runtime.
- This repository now shows both:
  - what had already worked
  - how that working logic was migrated into a local OpenClaw quality edition

## Repository Layout

- `skills/`: public skill packages
- `examples/`: sanitized source examples from the earlier public proof layer
- `assets/`: demo media and report previews
- `docs/`: public migration, architecture, and proof documents
- `framework/`: minimal public code and config skeleton for QMS Lite

## Scope Note

- Included here:
  - proof artifacts
  - migration explanation
  - framework skeleton
  - public skill packages
- Intentionally excluded:
  - private project memory
  - private runtime configs and secrets
  - full local fork implementation
  - real customer data
  - full Android private implementation details

## Contact

- X: [@QForge_Builder](https://x.com/QForge_Builder)
- Email: [zhongshunchen1982@gmail.com](mailto:zhongshunchen1982@gmail.com)

## License

Apache License 2.0. See [LICENSE](LICENSE).
