# RCA Detective Flow

This is the public summary of how RCA works in QMS Lite.

It is intentionally different from the 8D path.

## Why RCA is different

`8D` starts from an already written report and audits that report.

`RCA` starts from raw case notes and uses detective-style conversation to narrow
the cause path before a report exists.

That means RCA should not begin with:

- report validation
- final disposition
- "audit passed/failed"

It should begin with:

- the current reading of the case
- one active branch under investigation
- one next question

## Conversation model

### Step 1. Bootstrap the detective session

Tool:

`qm_rca_detective_bootstrap`

Purpose:

- load the raw case note from `work-inbox/rootcause/`
- confirm the case is a raw investigation input, not an old RCA report
- load process-map / fault-tree / retained experience context
- give the first focused question

Mobile output target:

- current reading
- status
- one next question

### Step 2. Narrow one branch at a time

The RCA agent should keep each turn short and strict:

- current branch
- current conclusion
- one next question

Typical branches:

- customer-side damage or handling
- compaction
- debinding
- sintering
- sizing / exposure window

## Branch pruning rules

The assistant should actively prune branches.

Examples:

- if the reject pattern is systematic, random customer damage becomes weak
- if process records are normal, that branch should be downgraded or pruned
- once a branch is ruled out, it should not be reopened without new evidence

This is the core detective behavior.

## What counts as progress

RCA is not only "more analysis text".

Progress means:

- more confirmed facts
- fewer plausible branches
- stronger mechanism anchor
- clearer evidence gap

## What the user should see

The user should be able to chat like this:

1. present a raw case
2. answer one focused question at a time
3. watch the branch tree narrow
4. stop when the strongest supported cause path is clear
5. request a final report

## When to generate the report

Only after convergence.

Tool:

`qm_rca_detective_artifact`

Its report should be a conclusion report, not an audit report.

## Required final report structure

- Executive Summary
- Confirmed Facts
- Strongest Supported Cause Path
- Root Cause Conclusion
- Evidence Basis
- Pruned Branches
- Remaining Evidence Gap
- Recommended Next Actions

## What must stay in the background

These are backend safety rails, not front-end report sections:

- evidence-chain gate internals
- tool raw JSON
- hidden context-loading notes
- prompt rules
- process-map/fault-tree loader traces

## Key design principle

RCA in QMS Lite is:

`chat first -> branch pruning -> strongest supported cause path -> final report`

not:

`old report in -> audit report out`
