export type QmsToolContract = {
  name: string;
  scene: "root-cause-analysis" | "report-review" | "shared";
  description: string;
  optional: boolean;
  recommendedAgents: string[];
  implementationNotes: string[];
};

export const qmRcaDetectiveBootstrapContract: QmsToolContract = {
  name: "qm_rca_detective_bootstrap",
  scene: "root-cause-analysis",
  description: "Bootstrap a detective-style RCA session from a raw local case note before any final report is generated.",
  optional: true,
  recommendedAgents: ["qm-rca"],
  implementationNotes: [
    "Use this first for live RCA chat sessions.",
    "It should return one focused next question, not a final report.",
  ],
};

export const qmRcaDetectiveArtifactContract: QmsToolContract = {
  name: "qm_rca_detective_artifact",
  scene: "root-cause-analysis",
  description: "Generate the final local RCA conclusion artifact from the detective session state.",
  optional: true,
  recommendedAgents: ["qm-rca"],
  implementationNotes: [
    "This is a conclusion report path, not an audit report path.",
    "It should preserve pruned branches and remaining evidence gaps.",
  ],
};

export const qm8dAuditArtifactContract: QmsToolContract = {
  name: "qm_8d_audit_artifact",
  scene: "report-review",
  description: "Run the retained strict 8D audit and render the canonical markdown into a local HTML artifact.",
  optional: true,
  recommendedAgents: ["qm-review"],
  implementationNotes: [
    "Locks the chain to strict review -> canonical markdown -> local renderer.",
  ],
};

export const qmSupplierAnalyzeContract: QmsToolContract = {
  name: "qm_supplier_analyze",
  scene: "report-review",
  description: "Analyze a supplier workbook and return deterministic grouped risk signals.",
  optional: true,
  recommendedAgents: ["qm-review"],
  implementationNotes: [
    "Numbers stay tool-driven so the model explains instead of inventing.",
  ],
};

export const qmReportRenderContract: QmsToolContract = {
  name: "qm_report_render",
  scene: "shared",
  description: "Render markdown or a source artifact into a local HTML report.",
  optional: true,
  recommendedAgents: ["qm-review", "qm-rca"],
  implementationNotes: [
    "Reporter is a deterministic artifact renderer, not a separate chat agent.",
  ],
};
