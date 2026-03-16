"""
Public reference snapshot for the QMS Lite bridge.

This file is intentionally smaller than the private runtime bridge. It shows
the core orchestration ideas that make the local OpenClaw quality edition work:

- deterministic tool entry points
- strict 8D audit path
- detective-style RCA path
- supplier validation lock
- local HTML artifact rendering

It is a teaching/reference file, not the private production bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Roots:
    knowledge_root: Path
    inbox_root: Path
    artifact_root: Path
    audit_root: Path


def load_roots() -> Roots:
    """
    The real bridge reads these from environment variables and local runtime
    config. The public snapshot keeps the boundary visible without exposing
    private runtime values.
    """
    runtime_root = Path("qms-runtime")
    return Roots(
        knowledge_root=runtime_root / "knowledge-base",
        inbox_root=runtime_root / "work-inbox",
        artifact_root=runtime_root / "artifacts",
        audit_root=runtime_root / "audit",
    )


ROOTS = load_roots()


def resolve_case(ref: str, bucket: str, suffixes: tuple[str, ...]) -> Path:
    """
    Resolve a referenced case from the local work inbox.
    Example buckets:
    - 8d
    - rootcause
    - supplier
    """
    candidate = ROOTS.inbox_root / bucket / ref
    if candidate.exists():
        return candidate
    for suffix in suffixes:
        fallback = ROOTS.inbox_root / bucket / f"{ref}{suffix}"
        if fallback.exists():
            return fallback
    raise FileNotFoundError(f"Case not found: {bucket}/{ref}")


def tool_8d_review_strict(params: dict[str, Any]) -> dict[str, Any]:
    """
    Canonical 8D gate.

    The private bridge loads the Q-Forge 8D skill and returns a structured
    result anchored to deterministic D3-D7 checks.
    """
    file_ref = params["fileRef"]
    case_path = resolve_case(file_ref, "8d", (".docx", ".md"))

    # Private runtime:
    # - parse the report
    # - compare against strict template
    # - run claim-versus-evidence checks
    # - emit canonical markdown audit report
    return {
        "fileRef": case_path.name,
        "overallDisposition": "APPROVED",
        "unsupportedClaimsCount": 0,
        "highestPriorityFinding": "None - all critical sections passed",
        "reportMarkdown": "# 8D Audit Review\n\n...",
    }


def tool_8d_audit_artifact(params: dict[str, Any]) -> dict[str, Any]:
    """
    Enforced 8D artifact path:

    qm_8d_review_strict -> canonical reportMarkdown -> qm_report_render
    """
    strict_result = tool_8d_review_strict(params)
    render_result = tool_report_render(
        {
            "title": "8D Audit Review",
            "artifactName": f"8d-audit-{Path(strict_result['fileRef']).stem}",
            "markdown": strict_result["reportMarkdown"],
            "sourceRef": strict_result["fileRef"],
        }
    )
    return {
        "summary": {
            "overallDisposition": strict_result["overallDisposition"],
            "unsupportedClaimsCount": strict_result["unsupportedClaimsCount"],
            "highestPriorityFinding": strict_result["highestPriorityFinding"],
        },
        "artifact": render_result,
    }


def tool_rca_detective_bootstrap(params: dict[str, Any]) -> dict[str, Any]:
    """
    Start RCA as detective chat, not as audit.

    The private bridge loads:
    - raw case notes
    - process map context
    - fault-tree context
    - detective prompt
    - prior retained experience
    """
    case_ref = params["caseRef"]
    case_path = resolve_case(case_ref, "rootcause", (".md", ".txt"))

    return {
        "caseRef": case_path.name,
        "inputMode": "raw-case",
        "alignmentStatus": "READY",
        "mobileStarterLines": [
            "Current Reading: PM Support Ring End-Face Cracking - Raw Case Notes",
            "Status: READY - detective RCA can begin",
            "Next Question: Where was the crack first detected in the process flow, and after which exact process step?",
        ],
    }


def tool_rca_detective_strict(params: dict[str, Any]) -> dict[str, Any]:
    """
    Convert the detective session into a bounded RCA conclusion state.

    Important distinction:
    - this is not an RCA audit
    - this is not a generic model summary
    - it is a controlled conclusion state with explicit evidence gaps
    """
    case_ref = params["caseRef"]
    case_path = resolve_case(case_ref, "rootcause", (".md", ".txt"))

    # Private runtime:
    # - collects detective chat state
    # - prunes ruled-out branches
    # - keeps facts / hypotheses / strongest cause path separate
    # - blocks "confirmed root cause" when evidence gate is not passed
    return {
        "caseRef": case_path.name,
        "executiveSummary": (
            "PM Support Ring end-face cracking was first detected after customer assembly, "
            "but the strongest supported upstream cause path is elevated compaction pressure."
        ),
        "rootCauseConclusion": (
            "The strongest supported cause path is elevated compaction pressure in batch "
            "20240910, which likely introduced density-gradient-driven stress concentration "
            "and end-face microcrack initiation."
        ),
        "evidenceBasis": [
            "30% compaction pressure deviation for the affected batch",
            "50% batch reject pattern points to systematic process issue",
            "Metallography shows density gradient and micro-crack indicators",
        ],
        "prunedBranches": [
            "Random customer-side handling damage",
            "Debinding abnormality",
            "Sintering abnormality",
            "Sizing as the primary crack-creation step",
        ],
        "remainingEvidenceGap": [
            "Formal reproduction or stronger comparative verification is still missing.",
        ],
        "reportMarkdown": "# Root Cause Conclusion Report\n\n...",
    }


def tool_rca_detective_artifact(params: dict[str, Any]) -> dict[str, Any]:
    """
    Enforced RCA artifact path:

    qm_rca_detective_strict -> conclusion markdown -> qm_report_render
    """
    strict_result = tool_rca_detective_strict(params)
    render_result = tool_report_render(
        {
            "title": "Root Cause Conclusion Report",
            "artifactName": f"rca-detective-{Path(strict_result['caseRef']).stem}",
            "markdown": strict_result["reportMarkdown"],
            "sourceRef": strict_result["caseRef"],
        }
    )
    return {
        "summary": {
            "executiveSummary": strict_result["executiveSummary"],
            "rootCauseConclusion": strict_result["rootCauseConclusion"],
            "evidenceBasis": strict_result["evidenceBasis"],
            "prunedBranches": strict_result["prunedBranches"],
        },
        "artifact": render_result,
    }


def tool_supplier_analyze(params: dict[str, Any]) -> dict[str, Any]:
    """
    Deterministic supplier analysis.

    The private runtime reads the workbook, calculates supplier metrics, and
    returns the ranked result before any free-form report is generated.
    """
    file_ref = params["fileRef"]
    workbook_path = resolve_case(file_ref, "supplier", (".xlsx", ".xls", ".csv"))
    return {
        "fileRef": workbook_path.name,
        "supplierCount": 4,
        "topSupplier": "Alpha Electronics",
        "highestRiskSupplier": "Gamma Components",
        "ppmRanking": ["Alpha Electronics", "Beta Materials", "Delta Tech", "Gamma Components"],
    }


def tool_supplier_report_check(params: dict[str, Any]) -> dict[str, Any]:
    """
    Final supplier lock.

    The private implementation validates:
    - required report sections
    - key metrics copied from the workbook
    - supplier ranking order
    """
    deterministic_result = tool_supplier_analyze({"fileRef": params["fileRef"]})
    return {
        "passed": True,
        "failedChecks": 0,
        "expectedTopSupplier": deterministic_result["topSupplier"],
    }


def tool_report_render(params: dict[str, Any]) -> dict[str, Any]:
    """
    Shared local renderer.

    The private renderer normalizes markdown, adds report metadata, writes a
    local HTML artifact, and returns its relative path.
    """
    artifact_name = params["artifactName"]
    return {
        "artifactId": f"{artifact_name}-20260316-000000",
        "relativePath": f"qms-runtime/artifacts/{artifact_name}-20260316-000000.html",
    }


TOOLS = {
    "qm_8d_review_strict": tool_8d_review_strict,
    "qm_8d_audit_artifact": tool_8d_audit_artifact,
    "qm_rca_detective_bootstrap": tool_rca_detective_bootstrap,
    "qm_rca_detective_strict": tool_rca_detective_strict,
    "qm_rca_detective_artifact": tool_rca_detective_artifact,
    "qm_supplier_analyze": tool_supplier_analyze,
    "qm_supplier_report_check": tool_supplier_report_check,
    "qm_report_render": tool_report_render,
}
