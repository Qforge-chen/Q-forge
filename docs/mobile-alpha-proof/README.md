# Mobile Alpha Proof

This folder stores local staging evidence for the first mobile alpha milestone of QMS Lite.

Current proof captured:

- `supplier-mobile-proof-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through `qm-review`
  - deterministic supplier analysis completed
  - full supplier report rendered to a local HTML artifact
- `8d-mobile-proof-good-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through `qm-review`
  - strict 8D audit path completed for a good-case sample
  - full 8D audit report rendered to a local HTML artifact
- `8d-mobile-proof-bad-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through `qm-review`
  - strict 8D audit path completed for a bad-case sample
  - rejection result rendered to a local HTML artifact
- `rca-mobile-proof-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through `qm-rca`
  - detective-style RCA conversation converged to a supported cause path
  - final RCA conclusion report rendered to a local HTML artifact

Screenshot proof captured:

- `supplier-mobile-proof-20260316.jpg`
- `8d-mobile-chat-proof-good-20260316.jpg`
- `8d-mobile-chat-proof-bad-20260316.jpg`
- `rca-mobile-chat-start-20260316.jpg`
- `rca-mobile-chat-pruning-20260316.jpg`
- `rca-mobile-chat-conclusion-20260316.jpg`

What this proves:

- Android client pairing works
- local gateway routing works
- `qm-review` can execute the supplier workflow end to end
- `qm-review` can execute the 8D workflow end to end
- `qm-rca` can execute a detective-style RCA workflow end to end
- local artifact generation works from a mobile-triggered run

Current status:

- mobile supplier proof: complete
- mobile 8D proof: complete
- mobile RCA proof: complete

Notes:

- this is a staging folder inside the public repo working copy
- screenshots from the phone UI should be added later as separate proof assets
- no private runtime paths or customer data should be copied here without review
