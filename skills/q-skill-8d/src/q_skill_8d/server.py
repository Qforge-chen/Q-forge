"""
Q-Skill-8D: 8D 报告审核 MCP 服务器

功能：
- 读取 Word 格式的 8D 报告
- 按 D3-D8 各环节进行严格审核
- 识别不合格环节并给出驳回意见
- 经验知识积累
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("q-skill-8d")

# 知识库路径
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
EXPERIENCE_FILE = KNOWLEDGE_DIR / "experience.json"
GOLDEN_PROMPT_FILE = KNOWLEDGE_DIR / "golden_prompt.md"


# ============================================================
# 工具函数
# ============================================================

def load_experience() -> dict:
    """加载经验知识库"""
    if EXPERIENCE_FILE.exists():
        with open(EXPERIENCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_experience_data(data: dict) -> None:
    """保存经验知识库"""
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    with open(EXPERIENCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_golden_prompt() -> str:
    """加载黄金 Prompt"""
    if GOLDEN_PROMPT_FILE.exists():
        with open(GOLDEN_PROMPT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return "暂无预定义的审核逻辑。"


def extract_evidence_snippet(text: str, max_len: int = 160, preferred_keywords: Optional[List[str]] = None) -> str:
    if not text or not text.strip():
        return "Not Found"

    raw_lines = [re.sub(r"\s+", " ", ln.strip()) for ln in text.splitlines() if ln.strip()]
    if not raw_lines:
        return "Not Found"

    def is_heading_like(line: str) -> bool:
        if len(line) < 18:
            return True
        if re.fullmatch(r"[A-Z0-9\s\-\(\)\[\]#:·•]+", line):
            return True
        heading_markers = ["(ICA)", "(PCA)", "Interim Containment", "Permanent Corrective", "Validation of", "System/Process Controls"]
        if any(m.lower() in line.lower() for m in heading_markers) and len(re.findall(r"\d", line)) == 0:
            return True
        if line.endswith(":") and len(re.findall(r"\d", line)) == 0:
            return True
        return False

    candidates = [ln for ln in raw_lines if not is_heading_like(ln)]
    if not candidates:
        candidates = raw_lines

    def score(line: str) -> int:
        s = 0
        if preferred_keywords:
            hits = sum(1 for kw in preferred_keywords if kw and kw.lower() in line.lower())
            if hits:
                s += 5 + min(hits, 3)
        if re.search(r"\d", line):
            s += 3
        if any(u.lower() in line.lower() for u in ["%", "mpa", "pcs", "lot", "0/", "sop", "coa", "cpk", "ppm"]):
            s += 2
        if any(v.lower() in line.lower() for v in ["screen", "sort", "inspect", "segreg", "hold", "stop ship", "lock", "verify", "update", "train", "recipe"]):
            s += 2
        if len(line) >= 40:
            s += 1
        return s

    snippet = max(candidates, key=score)
    if not snippet or not snippet.strip():
        return "Not Found"
    if len(snippet) > max_len:
        snippet = snippet[: max_len - 3].rstrip() + "..."
    return snippet


def extract_8d_sections(doc_text: str) -> dict:
    """从文档文本中提取 8D 各章节内容"""
    sections = {
        "D1": "", "D2": "", "D3": "", "D4": "",
        "D5": "", "D6": "", "D7": "", "D8": ""
    }
    
    # 使用正则表达式匹配 D1-D8 章节
    patterns = [
        (r'D1[\.、:：\s]*(.*?)(?=D2[\.、:：\s]|$)', "D1"),
        (r'D2[\.、:：\s]*(.*?)(?=D3[\.、:：\s]|$)', "D2"),
        (r'D3[\.、:：\s]*(.*?)(?=D4[\.、:：\s]|$)', "D3"),
        (r'D4[\.、:：\s]*(.*?)(?=D5[\.、:：\s]|$)', "D4"),
        (r'D5[\.、:：\s]*(.*?)(?=D6[\.、:：\s]|$)', "D5"),
        (r'D6[\.、:：\s]*(.*?)(?=D7[\.、:：\s]|$)', "D6"),
        (r'D7[\.、:：\s]*(.*?)(?=D8[\.、:：\s]|$)', "D7"),
        (r'D8[\.、:：\s]*(.*?)$', "D8"),
    ]
    
    for pattern, section in patterns:
        match = re.search(pattern, doc_text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(1).strip()
    
    return sections


# ============================================================
# 审核逻辑
# ============================================================

def review_d3(content: str) -> dict:
    """Review D3 Interim Actions - Must check 5 locations"""
    keywords = {
        "WIP": ["在制", "正在生产", "生产中", "在产", "WIP", "production", "in-process"],
        "In-transit": ["在途", "运输中", "物流", "发运", "transit", "shipping", "shipment"],
        "Customer Site": ["客户现场", "客户处", "客户端", "现场", "customer site", "on-site", "onsite"],
        "Customer Stock": ["客户库存", "客户仓库", "客户处库存", "customer stock", "customer warehouse"],
        "Internal Stock": ["我司", "本司", "公司", "仓库", "产线", "车间", "internal stock", "internal inventory", "warehouse", "stock", "inventory"]
    }
    
    found = {}
    missing = []
    
    for location, kws in keywords.items():
        found[location] = any(kw.lower() in content.lower() for kw in kws)
        if not found[location]:
            missing.append(location)
    
    passed = len(missing) == 0
    
    return {
        "passed": passed,
        "found_locations": [k for k, v in found.items() if v],
        "missing_locations": missing,
        "comment": "Pass" if passed else f"Missing containment for: {', '.join(missing)}"
    }


def review_d4(content: str) -> dict:
    """Review D4 Root Cause - Must include Mechanism, Root Cause, Escape Point"""
    checks = {
        "Mechanism": ["发生机制", "怎么发生", "发生过程", "发生原因", "机理", "mechanism", "how it happened", "occurrence"],
        "Root Cause": ["产生原因", "根本原因", "工艺原因", "真因", "根因", "为什么产生", "root cause", "why it happened"],
        "Escape Point": ["流出原因", "流出", "未检出", "未拦截", "漏检", "为什么流出", "escape", "detection failure", "why it was not detected"]
    }
    
    found = {}
    missing = []
    
    for check_type, kws in checks.items():
        found[check_type] = any(kw.lower() in content.lower() for kw in kws)
        if not found[check_type]:
            missing.append(check_type)
    
    # Check for Systemic Root Cause (Bonus)
    system_keywords = ["系统原因", "管理原因", "制度", "流程缺陷", "系统性", "system", "management", "procedure", "policy"]
    has_system_analysis = any(kw.lower() in content.lower() for kw in system_keywords)
    
    passed = len(missing) == 0
    
    comment = "Pass"
    if not passed:
        comment = f"Missing analysis for: {', '.join(missing)}"
    elif has_system_analysis:
        comment = "Pass (Bonus: Systemic analysis included)"
    
    return {
        "passed": passed,
        "found_analysis": [k for k, v in found.items() if v],
        "missing_analysis": missing,
        "has_system_analysis": has_system_analysis,
        "comment": comment
    }


def review_d5(content: str, d4_content: str) -> dict:
    """Review D5 Permanent Actions - Must align with D4"""
    # Check for actions
    measure_keywords = ["措施", "改善", "对策", "纠正", "改进", "整改", "action", "measure", "correction", "fix"]
    has_measures = any(kw.lower() in content.lower() for kw in measure_keywords)
    
    # Check for owner and date
    has_owner = any(kw.lower() in content.lower() for kw in ["责任人", "负责人", "执行人", "担当", "owner", "responsible", "person", "lead"])
    has_deadline = any(kw.lower() in content.lower() for kw in ["完成时间", "期限", "日期", "月", "日", "date", "deadline", "due", "time"])
    
    issues = []
    if not has_measures:
        issues.append("No specific actions described")
    if not has_owner:
        issues.append("Missing owner")
    if not has_deadline:
        issues.append("Missing deadline")
    
    passed = len(issues) == 0
    
    return {
        "passed": passed,
        "has_measures": has_measures,
        "has_owner": has_owner,
        "has_deadline": has_deadline,
        "issues": issues,
        "comment": "Pass" if passed else f"Issues: {'; '.join(issues)}"
    }


def review_d6(content: str) -> dict:
    """Review D6 Validation - Must have data"""
    # Check validation type
    production_keywords = ["生产验证", "批量验证", "量产", "生产数据", "良率", "production", "run", "batch", "manufacturing"]
    experiment_keywords = ["实验验证", "测试", "试验", "CPK", "数据", "合格率", "experiment", "test", "trial", "lab"]
    
    has_production = any(kw.lower() in content.lower() for kw in production_keywords)
    has_experiment = any(kw.lower() in content.lower() for kw in experiment_keywords)
    
    # Check for data
    has_data = bool(re.search(r'\d+\.?\d*\s*[%％]', content)) or \
               any(kw.lower() in content.lower() for kw in ["OK", "合格", "通过", "达标", "pass", "accepted", "good"])
    
    passed = (has_production or has_experiment) and has_data
    
    issues = []
    if not (has_production or has_experiment):
        issues.append("Validation method not specified (Production or Experiment)")
    if not has_data:
        issues.append("No validation data provided")
    
    return {
        "passed": passed,
        "has_production_verification": has_production,
        "has_experiment_verification": has_experiment,
        "has_data": has_data,
        "issues": issues,
        "comment": "Pass" if passed else f"Issues: {'; '.join(issues)}"
    }


def review_d7(content: str) -> dict:
    """Review D7 Prevention - Must have document revision and training"""
    # Check docs
    doc_keywords = ["文件", "标准", "规范", "SOP", "作业指导书", "检验标准", "修订", "更新", "document", "standard", "procedure", "instruction", "revise", "update"]
    has_doc_revision = any(kw.lower() in content.lower() for kw in doc_keywords)
    
    # Check training
    training_keywords = ["培训", "学习", "教育", "宣贯", "培训记录", "train", "educate", "lesson", "teach"]
    has_training = any(kw.lower() in content.lower() for kw in training_keywords)
    
    passed = has_doc_revision and has_training
    
    issues = []
    if not has_doc_revision:
        issues.append("Missing document revision")
    if not has_training:
        issues.append("Missing training")
    
    return {
        "passed": passed,
        "has_doc_revision": has_doc_revision,
        "has_training": has_training,
        "issues": issues,
        "comment": "Pass" if passed else f"Issues: {'; '.join(issues)}"
    }


def review_d8(content: str) -> dict:
    """Review D8 Recognition"""
    summary_keywords = ["总结", "经验", "教训", "心得", "感谢", "表彰", "关闭", "summary", "lesson", "thank", "recognize", "close", "team"]
    has_summary = any(kw.lower() in content.lower() for kw in summary_keywords)
    
    return {
        "passed": True,  # D8 is not critical for failure
        "has_summary": has_summary,
        "comment": "Pass" if has_summary else "Suggestion: Add team recognition or lessons learned"
    }


# ============================================================
# MCP Tools
# ============================================================

@mcp.tool()
def read_8d_report(file_path: str) -> dict:
    """
    Read Word format 8D report
    
    Args:
        file_path: Word document path (.docx)
    
    Returns:
        Dictionary containing content and sections
    """
    try:
        doc = Document(file_path)

        parts: List[str] = []

        def norm(s: str) -> str:
            return re.sub(r"\s+", " ", (s or "").strip())

        body_elm = doc.element.body
        for child in body_elm.iterchildren():
            if isinstance(child, CT_P):
                p = Paragraph(child, doc)
                t = norm(p.text)
                if t:
                    parts.append(t)
            elif isinstance(child, CT_Tbl):
                tbl = Table(child, doc)
                for row in tbl.rows:
                    cells = [norm(cell.text) for cell in row.cells]
                    if not any(cells):
                        continue
                    parts.append(" | ".join([c for c in cells if c]))

        full_text = "\n".join(parts)
        
        # Extract sections
        sections = extract_8d_sections(full_text)
        
        return {
            "status": "success",
            "file_path": file_path,
            "full_text": full_text,
            "sections": sections,
            "paragraph_count": len(doc.paragraphs)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def review_8d_report(file_path: str) -> dict:
    """
    Comprehensive 8D Report Review (D3-D8)
    
    Args:
        file_path: Word document path (.docx)
    
    Returns:
        Full review results
    """
    # Read doc
    doc_result = read_8d_report(file_path)
    
    if doc_result["status"] == "error":
        return doc_result
    
    sections = doc_result["sections"]
    
    # Execute reviews
    reviews = {
        "D3": review_d3(sections["D3"]),
        "D4": review_d4(sections["D4"]),
        "D5": review_d5(sections["D5"], sections["D4"]),
        "D6": review_d6(sections["D6"]),
        "D7": review_d7(sections["D7"]),
        "D8": review_d8(sections["D8"]),
    }
    
    # Verdict
    critical_sections = ["D3", "D4", "D5", "D6", "D7"]
    failed_sections = [s for s in critical_sections if not reviews[s]["passed"]]
    overall_passed = len(failed_sections) == 0
    
    # Verdict text
    if overall_passed:
        verdict = "✅ 8D Report APPROVED"
    else:
        verdict = "❌ 8D Report REJECTED"
    
    return {
        "status": "success",
        "file_path": file_path,
        "verdict": verdict,
        "overall_passed": overall_passed,
        "failed_sections": failed_sections,
        "reviews": reviews,
        "review_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@mcp.tool()
def prepare_logic_audit_packet(file_path: str) -> dict:
    """Prepare the source-of-truth packet for LLM logic audit (D3–D7 only)."""
    doc_result = read_8d_report(file_path)
    if doc_result.get("status") != "success":
        return doc_result

    gate_result = review_8d_report(file_path)
    if gate_result.get("status") != "success":
        return gate_result

    sections = doc_result.get("sections", {})
    d3_d7 = {k: sections.get(k, "") for k in ["D3", "D4", "D5", "D6", "D7"]}

    instructions = """You are performing Stage-2 LOGIC AUDIT (Risk Flags ONLY).\n\nRules (must follow):\n- Use ONLY the provided D3–D7 source text.\n- Do NOT invent any content/actions. If the evidence is missing, write: Evidence: Not Found.\n- Every claim MUST include a short verbatim quote from the source text (Evidence).\n- Do NOT provide SLA/time estimates unless explicitly stated in the source text.\n- Do NOT introduce ANY new numbers/timeframes/targets/durations (e.g., \"6 months\", \"0.3%\"). If not explicitly present in the source text, write the suggestion without numbers or use TBD.\n- Output must be concise and demo-friendly.\n\nConsistency risk meaning:\n- Low = alignment/completeness is good (no meaningful gap).\n- Medium = some uncertainty or minor gap.\n- High = clear misalignment or major gap.\n\nHard constraint for consistency checks:\n- If you write that alignment is good / properly addressed, the risk MUST be Low (do not output High).\n\nOutput format (Markdown):\n## IV. LLM Logic Audit (Risk Flags Only — does not affect Pass/Fail)\n\n### 1) Key Risk Flags\n- [Major/Minor] <risk>\n  - Evidence: \"<verbatim quote>\" OR Evidence: Not Found\n  - Why it matters: <1 line>\n  - Suggested fix: <1 line> (no new numbers unless quoted)\n\n### 2) Consistency Checks (quick)\n- D4→D5 alignment risk: <Low/Medium/High>\n  - Evidence: \"...\" OR Evidence: Not Found\n- D5→D6 validation sufficiency risk: <Low/Medium/High>\n  - Evidence: \"...\" OR Evidence: Not Found\n- D7 prevention completeness risk: <Low/Medium/High>\n  - Evidence: \"...\" OR Evidence: Not Found\n"""

    return {
        "status": "success",
        "file_path": file_path,
        "critical_sections_definition": "D3–D7 (5 sections)",
        "gate_result": {
            "overall_passed": gate_result.get("overall_passed"),
            "failed_sections": gate_result.get("failed_sections", []),
            "reviews": gate_result.get("reviews", {}),
            "review_date": gate_result.get("review_date"),
        },
        "source_sections": d3_d7,
        "logic_audit_instructions": instructions,
    }


@mcp.tool()
def generate_review_report(file_path: str, report_title: str = "8D Report Review") -> str:
    """
    Generate 8D Review Report (Markdown)
    
    Args:
        file_path: Word document path (.docx)
        report_title: Title of the report
    
    Returns:
        Markdown content
    """
    result = review_8d_report(file_path)
    
    if result["status"] == "error":
        return f"**Error**: {result['message']}"
    
    reviews = result["reviews"]
    doc_result = read_8d_report(file_path)
    sections = doc_result.get("sections", {}) if doc_result.get("status") == "success" else {}
    d3 = reviews["D3"]
    d4 = reviews["D4"]
    d5 = reviews["D5"]
    d6 = reviews["D6"]
    d7 = reviews["D7"]
    d8 = reviews["D8"]
    
    failed_count = len(result["failed_sections"])
    passed_count = 5 - failed_count
    critical_sections = ["D3", "D4", "D5", "D6", "D7"]
    passed_critical_sections = [s for s in critical_sections if reviews.get(s, {}).get("passed")]
    failed_critical_sections = [s for s in critical_sections if not reviews.get(s, {}).get("passed")]
    
    # Generate Header
    report = f"""# {report_title}

> 📅 **Date**: {result["review_date"]}  
> 📁 **File**: `{file_path}`  
> 📊 **Result**: {"APPROVED" if result["overall_passed"] else "REJECTED"} ({passed_count}/5 Critical Sections Passed)  
> 🔎 **Critical sections definition**: D3–D7 (5 sections)  
> ✅ **Critical sections passed**: {len(passed_critical_sections)}/5 ({', '.join(passed_critical_sections) if passed_critical_sections else 'None'})  
> ❌ **Critical sections failed**: {len(failed_critical_sections)}/5 ({', '.join(failed_critical_sections) if failed_critical_sections else 'None'})

---

## I. Executive Summary

### {result["verdict"]}

"""
    
    if not result["overall_passed"]:
        report += f"""| Status | Detail |
|--------|--------|
| **Rejected Sections** | {', '.join(result["failed_sections"])} |
| **Issues Found** | {failed_count} Critical Issues |
| **Action** | Please revise and resubmit. |

"""
    else:
        # Highlights
        highlights = []
        
        if d3["passed"]:
            found_count = len(d3["found_locations"])
            if found_count == 5:
                highlights.append("D3: Covered all 5 containment locations (WIP, In-transit, Customer Site, Customer Stock, Internal Stock).")
        
        if d4["passed"]:
            if d4["has_system_analysis"]:
                highlights.append("D4: Included systemic root cause analysis.")
            else:
                highlights.append("D4: Covered Mechanism, Root Cause, and Escape Point.")
        
        if d5["passed"]:
            highlights.append("D5: Actions have clear owners and deadlines.")
        
        if d6["passed"]:
            if d6["has_production_verification"] and d6["has_experiment_verification"]:
                highlights.append("D6: Verified by both Production and Experiment data.")
            else:
                highlights.append("D6: Verified with quantitative data.")
        
        if d7["passed"]:
            highlights.append("D7: Preventive actions include document updates and training.")
        
        if d8["has_summary"]:
            highlights.append("D8: Team recognition included.")
        
        report += """| Status | Detail |
|--------|--------|
| **Result** | All critical sections passed. |
| **Action** | Closure after confirming all corrective/preventive actions are completed (see Logic Audit). |

### ✨ Highlights

"""
        for h in highlights:
            report += f"- {h}\n"
        report += "\n"


    report += """---

## II. Detailed Audit

"""
    
    # D3
    d3 = reviews["D3"]
    status_icon = "✅" if d3["passed"] else "❌"
    d3_text = sections.get('D3', '')
    d3_ev_customer_stock = extract_evidence_snippet(
        d3_text,
        max_len=140,
        preferred_keywords=["customer warehouse", "customer stock", "customer warehouse sorting", "warehouse", "客户仓库", "客户库存"],
    )
    d3_ev_in_transit = extract_evidence_snippet(
        d3_text,
        max_len=140,
        preferred_keywords=["in-transit", "in transit", "shipment", "shipping", "returned", "return", "在途", "运输", "发运", "退回"],
    )
    d3_ev_wip_internal = extract_evidence_snippet(
        d3_text,
        max_len=140,
        preferred_keywords=["wip", "in-process", "stop production", "quarantine", "segreg", "hold", "internal stock", "inventory", "在制", "停产", "隔离", "我司", "本司", "内部库存"],
    )

    d3_evidence_lines = []
    if d3_ev_customer_stock != "Not Found":
        d3_evidence_lines.append(f"- Customer Stock: \"{d3_ev_customer_stock}\"")
    if d3_ev_in_transit != "Not Found":
        d3_evidence_lines.append(f"- In-transit: \"{d3_ev_in_transit}\"")
    if d3_ev_wip_internal != "Not Found":
        d3_evidence_lines.append(f"- WIP/Internal: \"{d3_ev_wip_internal}\"")

    d3_evidence_block = "Not Found" if not d3_evidence_lines else "\n".join(d3_evidence_lines)
    report += f"""### D3 Interim Containment {status_icon}

**Standard**: Must contain product in 5 locations:
- WIP (In-process)
- In-transit
- Customer Site
- Customer Stock
- Internal Stock

**Evidence**: {d3_evidence_block}

**Findings**:

| Location | Status |
|----------|--------|
| WIP | {"✅ Checked" if "WIP" in d3["found_locations"] else "❌ Not Checked"} |
| In-transit | {"✅ Checked" if "In-transit" in d3["found_locations"] else "❌ Not Checked"} |
| Customer Site | {"✅ Checked" if "Customer Site" in d3["found_locations"] else "❌ Not Checked"} |
| Customer Stock | {"✅ Checked" if "Customer Stock" in d3["found_locations"] else "❌ Not Checked"} |
| Internal Stock | {"✅ Checked" if "Internal Stock" in d3["found_locations"] else "❌ Not Checked"} |

"""
    if not d3["passed"]:
        report += f"""**❌ Rejection Reason**: Missing containment for {', '.join(d3['missing_locations'])}

**Required Actions**:
1. Confirm status of parts in missing locations.
2. Provide quantity and method of screening.

"""
    
    # D4
    d4 = reviews["D4"]
    status_icon = "✅" if d4["passed"] else "❌"
    report += f"""### D4 Root Cause Analysis {status_icon}

**Standard**: Must analyze:
- **Mechanism**: How it happened physically.
- **Root Cause**: Why it happened (Process/Method).
- **Escape Point**: Why it wasn't detected.

**Evidence**: {('"' + extract_evidence_snippet(sections.get('D4', '')) + '"') if extract_evidence_snippet(sections.get('D4', '')) != 'Not Found' else 'Not Found'}

**Findings**:

| Dimension | Status |
|-----------|--------|
| Mechanism | {"✅ Analyzed" if "Mechanism" in d4["found_analysis"] else "❌ Missing"} |
| Root Cause | {"✅ Analyzed" if "Root Cause" in d4["found_analysis"] else "❌ Missing"} |
| Escape Point | {"✅ Analyzed" if "Escape Point" in d4["found_analysis"] else "❌ Missing"} |
| Systemic | {"✨ Bonus" if d4["has_system_analysis"] else "⚪ N/A"} |

"""
    if not d4["passed"]:
        report += f"""**❌ Rejection Reason**: Missing analysis for {', '.join(d4['missing_analysis'])}

**Required Actions**:
1. Use 5-Why or Fishbone.
2. Drill down to process parameters or design features.
3. Explain why current controls failed to detect the defect.

"""
    elif d4["has_system_analysis"]:
        report += """**✨ Bonus**: Good job identifying systemic/management issues.

"""
    
    # D5
    d5 = reviews["D5"]
    status_icon = "✅" if d5["passed"] else "❌"
    report += f"""### D5 Permanent Actions {status_icon}

**Standard**:
- Actions must match Root Causes.
- Must have Owner and Deadline.

**Evidence**: {('"' + extract_evidence_snippet(sections.get('D5', '')) + '"') if extract_evidence_snippet(sections.get('D5', '')) != 'Not Found' else 'Not Found'}

**Findings**:

| Item | Status |
|------|--------|
| Action Description | {"✅ Present" if d5["has_measures"] else "❌ Missing"} |
| Owner | {"✅ Present" if d5["has_owner"] else "❌ Missing"} |
| Deadline | {"✅ Present" if d5["has_deadline"] else "❌ Missing"} |

"""
    if not d5["passed"]:
        issues_str = ", ".join(d5["issues"])
        required_actions = []
        if not d5.get("has_measures"):
            required_actions.append("Define specific actions.")
        if not d5.get("has_owner"):
            required_actions.append("Assign specific owners.")
        if not d5.get("has_deadline"):
            required_actions.append("Add deadlines/due dates.")
        if not required_actions:
            required_actions.append("Clarify missing information.")
        required_actions_md = "\n".join([f"{i}. {a}" for i, a in enumerate(required_actions, start=1)])

        report += f"""**❌ Rejection Reason**: {issues_str}

**Required Actions**:
{required_actions_md}

"""
    
    # D6
    d6 = reviews["D6"]
    status_icon = "✅" if d6["passed"] else "❌"
    report += f"""### D6 Validation {status_icon}

**Standard**:
- Must verify with Data (Production or Experiment).

**Evidence**: {('"' + extract_evidence_snippet(sections.get('D6', '')) + '"') if extract_evidence_snippet(sections.get('D6', '')) != 'Not Found' else 'Not Found'}

**Findings**:

| Item | Status |
|------|--------|
| Production Run | {"✅ Present" if d6["has_production_verification"] else "❌ Missing"} |
| Experiment/Test | {"✅ Present" if d6["has_experiment_verification"] else "❌ Missing"} |
| Data Support | {"✅ Present" if d6["has_data"] else "❌ Missing"} |

"""
    if not d6["passed"]:
        issues_str = ", ".join(d6["issues"])
        report += f"""**❌ Rejection Reason**: {issues_str}

**Required Actions**:
1. Provide quantitative data (e.g., Defect rate 0%).
2. Compare Before vs. After.

"""
    
    # D7
    d7 = reviews["D7"]
    status_icon = "✅" if d7["passed"] else "❌"
    report += f"""### D7 Prevention {status_icon}

**Standard**:
- Update Documents (SOP/Control Plan).
- Conduct Training.

**Evidence**: {('"' + extract_evidence_snippet(sections.get('D7', '')) + '"') if extract_evidence_snippet(sections.get('D7', '')) != 'Not Found' else 'Not Found'}

**Findings**:

| Item | Status |
|------|--------|
| Document Update | {"✅ Present" if d7["has_doc_revision"] else "❌ Missing"} |
| Training | {"✅ Present" if d7["has_training"] else "❌ Missing"} |

"""
    if not d7["passed"]:
        issues_str = ", ".join(d7["issues"])
        report += f"""**❌ Rejection Reason**: {issues_str}

**Required Actions**:
1. Update SOP/Work Instructions.
2. Train operators and keep records.

"""
    
    # D8
    d8 = reviews["D8"]
    report += f"""### D8 Recognition {"✅" if d8["has_summary"] else "💡 Suggestion"}

**Standard**: Team recognition and lessons learned.

- Recognition: {"✅ Present" if d8["has_summary"] else "❌ Missing"}

"""
    if not d8["has_summary"]:
        report += """**Suggestion**: Add team recognition or summarize lessons learned.

"""
    
    # Summary Table
    if not result["overall_passed"]:
        report += """---

## III. Action Items

Please address the following issues:

| # | Section | Requirement |
|---|---------|-------------|
"""
        idx = 1
        for section in result["failed_sections"]:
            r = reviews[section]
            if section == "D3" and r["missing_locations"]:
                report += f"| {idx} | D3 | Check {', '.join(r['missing_locations'])} |\n"
            elif section == "D4" and r["missing_analysis"]:
                report += f"| {idx} | D4 | Analyze {', '.join(r['missing_analysis'])} |\n"
            elif section == "D5":
                report += f"| {idx} | D5 | {', '.join(r['issues'])} |\n"
            elif section == "D6":
                report += f"| {idx} | D6 | {', '.join(r['issues'])} |\n"
            elif section == "D7":
                report += f"| {idx} | D7 | {', '.join(r['issues'])} |\n"
            idx += 1
    
    report += """
---

*Generated by Q-Forge Quality Intelligence*
"""
    
    return report


@mcp.tool()
def get_experience(keyword: str = None) -> dict:
    """
    Get 8D review experience history
    
    Args:
        keyword: Search keyword (optional)
    
    Returns:
        Matching history
    """
    experience = load_experience()
    
    if not experience:
        return {"status": "success", "experiences": [], "message": "No history found"}
    
    if keyword:
        filtered = {k: v for k, v in experience.items() if keyword.lower() in k.lower() or keyword.lower() in str(v).lower()}
        return {"status": "success", "experiences": filtered, "count": len(filtered)}
    
    return {"status": "success", "experiences": experience, "count": len(experience)}


@mcp.tool()
def save_experience(key: str, summary: str, expert_note: str = None) -> dict:
    """
    Save 8D review experience to knowledge base
    
    Args:
        key: Experience ID (e.g. "1214_8D_ProductA")
        summary: Review conclusion summary
        expert_note: Expert note (optional)
    
    Returns:
        Save result
    """
    experience = load_experience()
    
    experience[key] = {
        "summary": summary,
        "expert_note": expert_note,
        "timestamp": datetime.now().isoformat()
    }
    
    save_experience_data(experience)
    
    return {
        "status": "success",
        "message": f"Experience saved: {key}",
        "total_experiences": len(experience)
    }


@mcp.tool()
def get_golden_prompt() -> dict:
    """
    Get 8D Review Golden Prompt
    
    Returns:
        Golden Prompt content
    """
    content = load_golden_prompt()
    return {
        "status": "success",
        "golden_prompt": content
    }


@mcp.tool()
def save_review_report(file_path: str, report_title: str = "8D Report Review", logic_review_md: Optional[str] = None, require_logic_audit: bool = True) -> dict:
    """
    [Save File] Save 8D Review Report as Markdown file
    
    Function: Generates the full review report and saves it to the same directory as the source file.
    
    IMPORTANT: This is the ONLY way to save the review report to disk! Must be called after review!
    
    Args:
        file_path: Original Word document path (.docx)
        report_title: Title of the review report
        logic_review_md: Optional Stage-2 LLM logic audit Markdown (risk flags only). Will be appended to the deterministic report.
        require_logic_audit: If true (default), Stage-2 logic audit is required before saving. If missing, returns a packet for the agent to complete.
    
    Returns:
        Dictionary with saved_path
    """
    try:
        if require_logic_audit and not (logic_review_md and str(logic_review_md).strip()):
            packet = prepare_logic_audit_packet(file_path)
            if packet.get("status") != "success":
                return packet
            return {
                "status": "needs_logic_audit",
                "message": "Stage-2 Logic Audit is required. Use logic_audit_packet to generate logic_review_md (verbatim Evidence quotes; Not Found if missing), then call save_review_report again with logic_review_md.",
                "logic_audit_packet": packet,
            }

        # Generate report
        report = generate_review_report(file_path, report_title)
        
        if report.startswith("**Error**"):
            return {"status": "error", "message": report}
        
        # Get directory
        doc_path = Path(file_path)
        output_dir = doc_path.parent
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"8D_Review_{timestamp}.md"
        report_path = output_dir / report_filename
        
        # Append optional LLM logic audit
        logic_included = False
        if logic_review_md and str(logic_review_md).strip():
            logic_block = str(logic_review_md).strip()
            insert_marker = "\n*Generated by Q-Forge Quality Intelligence*\n"
            if insert_marker in report:
                head, tail = report.split(insert_marker, 1)
                report = head.rstrip() + "\n\n---\n\n" + logic_block + "\n\n" + insert_marker + tail.lstrip("\n")
            else:
                report = report.rstrip() + "\n\n---\n\n" + logic_block + "\n"
            logic_included = True

        # Save file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            "status": "success",
            "message": "Review report saved",
            "saved_path": str(report_path),
            "filename": report_filename,
            "logic_review_included": logic_included,
            "report_content": report
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================
# MCP Prompts
# ============================================================

@mcp.prompt()
def review_8d_prompt() -> str:
    """8D Report Review Prompt"""
    golden = load_golden_prompt()
    experience = load_experience()
    
    exp_summary = ""
    if experience:
        recent = list(experience.items())[-3:]
        exp_summary = "\n".join([f"- {k}: {v['summary']}" for k, v in recent])
    
    return f"""# 8D Report Review Guide

{golden}

## Review History
{exp_summary if exp_summary else "No history available"}

## Review Process
1. Use `read_8d_report` to read the Word document.
2. Use `review_8d_report` to perform strict validation.
3. Use `prepare_logic_audit_packet` to get D3–D7 source text and gate results.
4. Write a short Stage-2 Logic Audit using `logic_audit_instructions` (Risk Flags ONLY, must include verbatim Evidence quotes; if missing, write Not Found).
5. Use `save_review_report(file_path, report_title, logic_review_md=...)` to append Stage-2 audit and save (Critical!).
   - If `save_review_report` returns `status: needs_logic_audit`, generate the Stage-2 audit from the returned `logic_audit_packet` and call `save_review_report` again with `logic_review_md`.
6. Use `save_experience` to save key learnings.
"""


if __name__ == "__main__":
    mcp.run()
