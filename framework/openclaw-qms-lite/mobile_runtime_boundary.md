# Mobile Runtime Boundary

This file explains what the Android client is and what it is not.

## Product role

The Android side is a secure chat terminal for QMS Lite.

It is not meant to be:

- a general phone assistant
- a system automation controller
- a place where raw sensitive manufacturing files are casually uploaded

## Runtime shape

The working model is:

`Android chat client -> OpenClaw gateway -> QMS agents -> local bridge -> local artifacts`

## What the phone should do

- connect to the local or private-network gateway
- start `qm-review` or `qm-rca` sessions
- send short instructions and case references
- receive compact summaries
- receive local artifact file names

## What the phone should not do

- store or expose full private runtime config
- upload arbitrary sensitive files by default
- act as the place where final artifacts live
- become the only source of record

## Why the boundary matters

The point of QMS Lite is not only "use a local model".

It is also:

- keep runtime boundaries clear
- keep high-sensitivity data local
- separate conversation from artifact storage
- prevent the mobile layer from becoming the uncontrolled data plane

## Data separation

QMS Lite separates:

- stable knowledge:
  - standards
  - SOPs
  - templates
  - retained experience
- daily work inputs:
  - new 8D reports
  - raw RCA case notes
  - supplier workbooks
- generated outputs:
  - HTML artifacts
  - rendered reports
  - audit traces

The Android client should mainly reference these things, not absorb them all.

## What is local

In the private runtime, local data is organized like this:

- `qms-runtime/knowledge-base`
- `qms-runtime/work-inbox`
- `qms-runtime/artifacts`
- `qms-runtime/audit`

These paths are intentionally shown as a public pattern, not as a secret-bearing config dump.

## Agent boundary

### `qm-review`

Used for:

- 8D audit
- supplier analysis
- local artifact generation through the renderer

### `qm-rca`

Used for:

- detective-style RCA chat
- branch pruning
- strongest cause-path convergence
- final RCA conclusion artifact

## Security posture in plain language

The hardening idea is simple:

- the phone is the front door
- the gateway is the router
- the logic lock stays in local tools
- the final artifact stays local

That is why QMS Lite is not just "generic OpenClaw with prompts".
