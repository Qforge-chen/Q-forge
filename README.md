# Q-Forge

Q-Forge is a quality-focused agent system for manufacturing workflows, not a generic chatbot.

This public repository is no longer only a proof page. It is now the public proof layer plus the migration blueprint for a local quality-specific OpenClaw runtime.

> In roughly 24 hours, Q-Forge moved from an already-proven Goose + MCP setup into a local OpenClaw quality edition with Android mobile proof.

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

### What changed in one fast migration pass

- the original Goose + MCP proof stack was not discarded; it was migrated
- the four working capability paths were re-established in a local OpenClaw quality runtime
- Android mobile proof was completed for `Supplier`, `8D`, and `RCA`
- the runtime was narrowed into a quality-specific profile instead of a generic assistant
- a public framework snapshot was added so other builders can follow the logic, not just the screenshots

### What this means

This repository now shows one concrete thing:

Q-Forge was already real before this pass, and after one focused 24-hour migration sprint it became a local OpenClaw quality edition with working mobile proof.

### Direct Running Proof

This repository contains direct running proof, not only design notes.

- the workflows shown here were executed end to end
- the proof set includes real local HTML artifacts
- the proof set includes real Android chat screenshots
- the public examples, rendered outputs, and mobile traces all come from actual runs

[![8D DOCX review demo](assets/8d-docx-review-demo-cover.jpg)](assets/8d-docx-review-demo-short.mp4)

Open the preview image to watch the 40-second 8D demo from the earlier Goose + MCP phase.

## Proof At A Glance

<table>
  <tr>
    <td align="center" width="33%">
      <img src="docs/mobile-proof/supplier-mobile-proof-20260316.jpg" alt="Supplier mobile proof" width="240" />
    </td>
    <td align="center" width="33%">
      <img src="docs/mobile-proof/8d-mobile-chat-proof-good-20260316.jpg" alt="8D mobile proof" width="240" />
    </td>
    <td align="center" width="33%">
      <img src="docs/mobile-proof/rca-mobile-chat-conclusion-20260316.jpg" alt="RCA mobile proof" width="240" />
    </td>
  </tr>
  <tr>
    <td align="center"><sub>Supplier mobile proof</sub></td>
    <td align="center"><sub>8D mobile proof</sub></td>
    <td align="center"><sub>RCA mobile proof</sub></td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <img src="assets/output-validation-stamp.png" alt="Validation stamp" width="240" />
    </td>
    <td align="center" width="33%">
      <img src="assets/8d-rendered-report-preview.png" alt="8D rendered report preview" width="240" />
    </td>
    <td align="center" width="33%">
      <img src="assets/rootcause-rendered-report-preview.png" alt="RCA rendered report preview" width="240" />
    </td>
  </tr>
  <tr>
    <td align="center"><sub>Validation lock</sub></td>
    <td align="center"><sub>8D report artifact</sub></td>
    <td align="center"><sub>RCA report artifact</sub></td>
  </tr>
</table>

## What Is Public Here

- real public skill packages under [`skills/`](skills/)
- sanitized inputs, outputs, and rendered artifacts under [`examples/`](examples/) and [`docs/mobile-proof/`](docs/mobile-proof/)
- public QMS Lite design and migration documents under [`docs/`](docs/)
- a minimal framework snapshot under [`framework/`](framework/) so other builders can follow the architecture without needing the full private runtime

## Already Working Now

| Capability | Current working path | Public proof |
| --- | --- | --- |
| **8D** | strict 8D audit path, deterministic D3-D7 checks, local HTML artifact, Android-triggered proof | [good 8D HTML](docs/mobile-proof/8d-mobile-proof-good-20260316.html), [bad 8D HTML](docs/mobile-proof/8d-mobile-proof-bad-20260316.html), [good chat screenshot](docs/mobile-proof/8d-mobile-chat-proof-good-20260316.jpg), [bad chat screenshot](docs/mobile-proof/8d-mobile-chat-proof-bad-20260316.jpg) |
| **RCA** | detective-style branch-pruning chat, strongest cause-path conclusion, local HTML artifact, Android-triggered proof | [RCA HTML](docs/mobile-proof/rca-mobile-proof-20260316.html), [start screenshot](docs/mobile-proof/rca-mobile-chat-start-20260316.jpg), [pruning screenshot](docs/mobile-proof/rca-mobile-chat-pruning-20260316.jpg), [conclusion screenshot](docs/mobile-proof/rca-mobile-chat-conclusion-20260316.jpg) |
| **Supplier** | deterministic spreadsheet analysis, validation lock, local HTML artifact, Android-triggered proof | [supplier HTML](docs/mobile-proof/supplier-mobile-proof-20260316.html), [supplier screenshot](docs/mobile-proof/supplier-mobile-proof-20260316.jpg) |
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

- [OpenClaw Quality Edition](docs/openclaw-quality-edition.md)
- [24-Hour OpenClaw Migration](docs/openclaw-migration-24h.md)
- [OpenClaw Quality Architecture](docs/openclaw-quality-architecture.md)
- [Android Secure Chat Client](docs/android-secure-chat-client.md)
- [Mobile Proof Index](docs/mobile-proof/README.md)
- [Project Roadmap](docs/openclaw-quality-roadmap.md)

### Public framework snapshot

- [framework/README.md](framework/README.md)
- [OpenClaw quality profile example](framework/openclaw-quality-edition/openclaw.qms.local.example.jsonc)
- [Tool contract snapshot](framework/openclaw-quality-edition/tool-contracts.snapshot.ts)
- [Bridge reference snapshot](framework/openclaw-quality-edition/qms_bridge_reference.py)
- [qm-review workspace rules](framework/openclaw-quality-edition/qm-review.AGENTS.md)
- [qm-rca workspace rules](framework/openclaw-quality-edition/qm-rca.AGENTS.md)
- [Logic path summary](framework/openclaw-quality-edition/logic-paths.md)
- [RCA detective flow](framework/openclaw-quality-edition/rca_detective_flow.md)
- [Mobile runtime boundary](framework/openclaw-quality-edition/mobile_runtime_boundary.md)

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
- Email: [zhongshunchen2004@gmail.com](mailto:zhongshunchen2004@gmail.com)

## License

Apache License 2.0. See [LICENSE](LICENSE).
