# Skills

This folder contains the public Q-Forge skill packages.

Current public packages:

- `q-skill-8d`
- `q-skill-rootcause`
- `q-skill-supplier`
- `q-skill-reporter`

These packages are the public skill layer behind the proof, docs, and migration story shown in this repository.

In the current private validated baseline, the same capability families are carried forward inside a skillized QMS overlay with deterministic runners, artifacts, and regression checks. The public packages here remain the publishable skill-facing layer of that direction.

## Open tiers

| Package | Tier | Public focus |
| --- | --- | --- |
| `q-skill-reporter` | `full` | runnable renderer core, fixtures, tests, CLI |
| `q-skill-8d` | `lite-core` | public contract layer plus synthetic review fixture |
| `q-skill-supplier` | `lite-core` | public contract layer plus synthetic analysis fixture |
| `q-skill-rootcause` | `protocol-core` | protocol schema plus public evidence-chain fixture |

See [../docs/public-skill-open-tiers.md](../docs/public-skill-open-tiers.md) for the public/private boundary of each package.
