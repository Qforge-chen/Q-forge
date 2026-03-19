# Mobile Proof

This folder stores the public mobile proof set for the current OpenClaw quality-edition pass.

These captures come from the earlier QMS Lite mobile phase. They remain valid public proof, but they should be read as proof of the running workflows, not as a frozen statement of the latest internal agent names.

Current proof captured:

- `supplier-mobile-proof-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through the earlier review-agent layout
  - deterministic supplier analysis completed
  - full supplier report rendered to a local HTML artifact
- `8d-mobile-proof-good-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through the earlier review-agent layout
  - strict 8D audit path completed for a good-case sample
  - full 8D audit report rendered to a local HTML artifact
- `8d-mobile-proof-bad-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through the earlier review-agent layout
  - strict 8D audit path completed for a bad-case sample
  - rejection result rendered to a local HTML artifact
- `rca-mobile-proof-20260316.html`
  - generated from a real Android session connected to the local OpenClaw QMS Lite gateway
  - workflow executed through the earlier RCA-agent layout
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
- the earlier QMS Lite review path can execute the supplier workflow end to end
- the earlier QMS Lite review path can execute the 8D workflow end to end
- the earlier QMS Lite RCA path can execute a detective-style RCA workflow end to end
- local artifact generation works from a mobile-triggered run

Current status:

- mobile supplier proof: complete
- mobile 8D proof: complete
- mobile RCA proof: complete

Notes:

- this folder is meant to be publicly readable, not only locally staged
- the goal is to show start, reasoning, and conclusion without dumping full long chats
- no private runtime paths or customer data should be copied here without review
