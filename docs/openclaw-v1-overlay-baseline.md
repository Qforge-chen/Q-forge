# OpenClaw V1 Overlay Baseline

This note explains the current validated baseline behind the latest Q-Forge direction.

It is not a claim that the whole product is finished. It is a statement that the current OpenClaw-based QMS overlay has crossed from idea into repeatable engineering.

## What Is Validated

As of March 19, 2026, the working baseline is:

- a clean OpenClaw host kept close to upstream
- no OpenClaw core modifications for the QMS V1 layer
- local LM Studio inference
- `secretary` as the intake and coordination agent
- `qms` as the deep quality specialist
- skillized QMS protocols for `8D`, `RCA`, `Supplier`, and `Reporter`
- deterministic runner scripts behind those skill protocols
- live regression against real sessions
- real `secretary -> qms` handoff validation

## Why This Matters

The hard part is not only getting a model to say something plausible.

The hard part is building a local runtime where:

- specialist responsibilities are separated
- deterministic steps are not left to model improvisation
- artifacts and audit traces are saved
- the host can still be upgraded without carrying a pile of private core patches

That is why this baseline is shaped as a clean host plus overlay.

## How The Overlay Is Shaped

The current direction separates the system into three layers:

1. Clean OpenClaw host
   - close to upstream
   - not rewritten into a private fork

2. QMS overlay
   - quality-specific workspaces
   - skill protocols
   - deterministic runners
   - artifact and audit rules

3. Runtime
   - local LM Studio model backend
   - local state and work directories
   - live regression and handoff checks

## Why Not "Just Ask OpenClaw To Create Skills"

That approach is useful for quick prototypes.

It is not enough for a manufacturing workflow that needs:

- repeatable gates
- saved evidence
- deterministic calculations
- specialist handoff
- rerunnable regression after host changes

The current Q-Forge direction treats skills as the protocol layer, not as a magic shortcut. Deterministic engineering is what makes those skills stable enough to reuse.

## What Has Been Proved In This Baseline

- `8D` can run a strict audit path with deterministic blocking logic
- `RCA` can keep evidence-chain discipline instead of collapsing into free-form certainty
- `Supplier` can keep the numbers deterministic
- `Reporter` can turn validated outputs into reviewable HTML artifacts
- `secretary` can delegate a formal quality task to `qms` and return the specialist result instead of faking expertise

## What This Public Repo Shows

This public repository does not expose the full private runtime.

It does expose:

- the public proof layer
- the migration story
- the public skill packages
- the framework skeleton
- the reasoning behind the clean-host overlay model

## What Comes Next

The next layers after this baseline are expected to be:

- channel integrations such as Feishu or other secure messaging clients
- tighter sandbox rules
- more specialist agents

Those are next steps, not prerequisites for the current proof.
