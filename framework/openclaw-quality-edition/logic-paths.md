# Logic Paths

This is the minimum public description of the deterministic chains used in QMS Lite.

## 8D strict path

`qm_8d_review_strict -> reportMarkdown -> qm_report_render`

What this means:

- the model does not invent a new audit structure
- the strict 8D review becomes the canonical result
- the final HTML is rendered from canonical markdown

## Supplier path

`qm_supplier_analyze -> report generation -> qm_supplier_report_check -> qm_report_render`

What this means:

- the metrics come from the workbook
- the generated report is checked against the source numbers
- only then is the final HTML rendered

## RCA detective path

`qm_rca_detective_bootstrap -> detective chat -> qm_rca_detective_artifact`

What this means:

- RCA starts as a conversation, not as a report audit
- the agent narrows branches step by step
- only after convergence does it generate a conclusion report

## Why this matters

The project is not only "a model plus prompts". The important part is which layer is allowed to decide what:

- tools provide deterministic anchors
- the model reasons inside a bounded path
- the renderer only packages the final artifact
