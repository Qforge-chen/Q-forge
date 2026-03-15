# q-skill-8d

Q-Forge package for 8D report intake and audit.

## What It Does

- Reads Word-based 8D reports
- Validates critical sections with deterministic rules
- Flags missing containment, weak root cause logic, and incomplete closure conditions
- Produces review outputs that can be rendered into HTML

## Public Proof

- [Good input sample](../../examples/8d/input/8d-case-good.docx)
- [Bad input sample](../../examples/8d/input/8d-case-bad.docx)
- [Approved audit output](../../examples/8d/output/8d-review-approved.md)
- [Rendered HTML output](../../examples/8d/output/8d-review-rendered.html)

## Install

```bash
pip install -e .
```
