# Public Skill Open Tiers

This note defines how Q-Forge skill code is opened in public without collapsing the private product core into the repository.

The principle is simple:

- do not publish pure prompt text alone
- do publish runnable engineering slices
- keep the private overlay, regression corpus, and dense specialist logic out of the public repo

## Current tiers

### `q-skill-reporter`

**Tier:** `full`

Public here:

- CLI and library core
- HTML rendering logic
- schemas
- fixtures
- tests

Kept private:

- any private runtime styling or customer-specific presentation rules

### `q-skill-8d`

**Tier:** `lite-core`

Public here:

- contract schema
- synthetic review-result fixture
- smoke test
- public MCP-era package reference

Kept private:

- full hard-gate density
- private experience and audit language
- live regression corpus
- overlay handoff behavior

### `q-skill-supplier`

**Tier:** `lite-core`

Public here:

- analysis summary schema
- synthetic ranking fixture
- smoke test
- public MCP-era package reference

Kept private:

- true threshold tuning
- customer mapping rules
- dense trend heuristics
- private regression data

### `q-skill-rootcause`

**Tier:** `protocol-core`

Public here:

- evidence-chain schema
- synthetic protocol fixture
- smoke test
- public MCP-era package reference

Kept private:

- branch-pruning engine density
- specialist heuristics
- private knowledge base
- full reasoning contract

## Why this tiering exists

Q-Forge is being built as a long-term career and product asset.

That means the public repository should prove:

- the system is real
- the engineering is deliberate
- the code is runnable

It should not donate the entire product core in one pass.
