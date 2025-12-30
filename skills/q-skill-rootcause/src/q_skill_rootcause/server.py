from mcp.server.fastmcp import FastMCP
from pathlib import Path
import json
from datetime import datetime

# 初始化 MCP 服务器
mcp = FastMCP("q-skill-rootcause")

# 路径配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"

def load_file_content(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

def load_json_content(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except:
            return {}
    return {}

@mcp.tool()
def load_rootcause_context() -> dict:
    """
    【核心工具】加载探因分析所需的所有上下文知识
    
    功能：
    一次性读取工艺解析(process)、故障树(fault tree)和经验库(experience)。
    这是启动"侦探模式"的第一步，必须在对话开始时调用。
    
    Returns:
        包含三个知识库内容的字典
    """
    process_map = load_file_content(DATA_DIR / "process_map.md")
    fault_tree = load_file_content(DATA_DIR / "fault_tree.md")
    experience = load_json_content(KNOWLEDGE_DIR / "experience.json")
    
    # 构建经验摘要字符串
    exp_summary = ""
    if experience:
        redacted = {}
        for k, v in experience.items():
            redacted[k] = {
                "symptom": v.get("symptom", ""),
                "solution": v.get("solution", ""),
                "timestamp": v.get("timestamp", "")
            }
        exp_summary = json.dumps(redacted, ensure_ascii=False, indent=2)
    else:
        exp_summary = "暂无历史经验"

    return {
        "process_map": process_map,
        "fault_tree": fault_tree,
        "experience": exp_summary,
        "detective_mode_prompt": detective_mode_prompt(),
        "message": "✅ 已加载三大知识库：工艺解析、故障树、过往经验。请开始侦探排查模式。"
    }

@mcp.tool()
def save_rca_case(symptom: str, root_cause: str, solution: str, key_tag: str = None) -> dict:
    """
    【保存经验】将成功的排查案例保存到经验库
    
    功能：
    当找到根本原因后，将"现象-原因-对策"保存下来的工具。
    让智能体越用越聪明。
    
    Args:
        symptom: 故障现象描述
        root_cause: 确定的根本原因
        solution: 解决方案/纠正措施
        key_tag: (可选) 案例的唯一标识标签，如 "同心度_夹具_01"，不填则自动生成
    """
    experience_path = KNOWLEDGE_DIR / "experience.json"
    data = load_json_content(experience_path)
    
    if not key_tag:
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        key_tag = f"Case_{timestamp}"
    
    data[key_tag] = {
        "symptom": symptom,
        "root_cause": root_cause,
        "solution": solution,
        "timestamp": datetime.now().isoformat()
    }
    
    # 确保目录存在
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(experience_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return {
        "status": "success",
        "message": f"✅ 已成功保存案例 [{key_tag}] 到经验库",
        "total_cases": len(data)
    }


@mcp.tool()
def get_experience(keyword: str, limit: int = 3) -> dict:
    data = load_json_content(KNOWLEDGE_DIR / "experience.json")
    if not data:
        return {"status": "empty", "items": []}

    kw = (keyword or "").strip()
    if not kw:
        return {"status": "error", "message": "keyword is required", "items": []}

    matches = []
    for k, v in data.items():
        symptom = str(v.get("symptom", ""))
        root_cause = str(v.get("root_cause", ""))
        solution = str(v.get("solution", ""))

        haystack = f"{k}\n{symptom}\n{root_cause}\n{solution}".lower()
        if kw.lower() in haystack:
            matches.append(
                {
                    "key_tag": k,
                    "symptom": symptom,
                    "solution": solution,
                    "root_cause": "[REDACTED]"
                }
            )

    matches = matches[-max(int(limit), 1):]
    return {"status": "success", "keyword": kw, "items": matches}



@mcp.tool()
def validate_evidence_chain(suspected_cause: str, evidence_list: list[str]) -> dict:
    """
    【证据验证】验证根本原因的证据链是否完整（逻辑锁）
    
    功能：
    在确认根本原因之前，必须调用此工具验证证据是否充分。
    防止"我觉得是..."的主观推测。
    
    Args:
        suspected_cause: 怀疑的根本原因
        evidence_list: 提供的证据列表（字符串数组）
    
    Returns:
        验证判定结果
    """
    # 关键词定义
    keywords = {
        "mechanism": ["金相", "断口", "截面", "SEM", "显微镜", "机理", "微观", "microstructure"],
        "data": ["数据", "CPK", "趋势", "DOE", "对比", "统计", "测量", "记录", "data", "chart"],
        "verification": ["复现", "验证", "实验", "试做", "改善", "回归", "verify", "reproduce"]
    }
    
    found_types = set()
    details = {}
    
    combined_text = " ".join(evidence_list).lower()
    
    for k, words in keywords.items():
        if any(w in combined_text for w in words):
            found_types.add(k)
            details[k] = True
        else:
            details[k] = False
            
    # 判定逻辑：必须有机理(Mechanism) + (数据(Data) 或 验证(Verification))
    has_mechanism = "mechanism" in found_types
    has_hard_proof = "data" in found_types or "verification" in found_types
    
    passed = has_mechanism and has_hard_proof
    
    if passed:
        verdict = "VERIFIED"
        comment = "证据链完整（包含机理和实证）"
        icon = "✅"
    else:
        verdict = "UNVERIFIED"
        missing = []
        if not has_mechanism: missing.append("机理证据 (如金相/SEM)")
        if not has_hard_proof: missing.append("实证证据 (如数据统计/复现实验)")
        comment = f"证据不足，缺少: {', '.join(missing)}"
        icon = "❌"
        
    return {
        "verdict": verdict,
        "status_icon": icon,
        "suspected_cause": suspected_cause,
        "passed": passed,
        "found_types": list(found_types),
        "comment": comment,
        "next_step": "可以直接下结论" if passed else "请补充缺失的证据实验"
    }


# 默认报告输出目录（相对于项目根目录）
DEFAULT_REPORT_DIR = BASE_DIR.parent.parent.parent.parent / "data"


@mcp.tool()
def save_rca_report(report_content: str, save_dir: str = None, report_title: str = "RCA分析报告") -> dict:
    """
    【保存报告】将完整的根因分析报告保存为 Markdown 文件
    
    功能：
    将完整的分析报告保存到指定目录（默认为 Q-FORGE-V1/data）。
    
    重要：这是保存报告到本地文件的唯一方法！分析完成后必须调用此工具！
    
    Args:
        report_content: 报告的完整内容（Markdown 格式）
        save_dir: 保存目录路径（可选，默认为项目 data 目录）
        report_title: 报告标题
    
    Returns:
        包含保存路径的字典
    """
    try:
        # 使用相对路径作为默认值
        if save_dir is None:
            save_path = DEFAULT_REPORT_DIR
        else:
            save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"根因分析_{timestamp}.md"
        file_path = save_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {report_title}\n\n")
            f.write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(report_content)
            f.write("\n\n---\n*由 Q-Forge 探因分析智能体自动生成*")
        
        return {
            "status": "success",
            "message": f"✅ 报告已保存",
            "saved_path": str(file_path),
            "filename": filename
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.prompt()
def detective_mode_prompt() -> str:
    """启动探因侦探模式的系统指令（自动加载知识库）"""
    prompt_path = BASE_DIR / "prompt" / "detective_prompt.md"
    base_prompt = load_file_content(prompt_path)
    
    # 自动加载知识库并嵌入
    process_map = load_file_content(DATA_DIR / "process_map.md")
    fault_tree = load_file_content(DATA_DIR / "fault_tree.md")
    experience = load_json_content(KNOWLEDGE_DIR / "experience.json")
    
    # 构建经验摘要
    exp_summary = ""
    if experience:
        recent = list(experience.items())[-3:]  # 最近3条
        exp_summary = "\n".join([f"- **{k}**: {v['symptom']}" for k, v in recent])
    else:
        exp_summary = "暂无历史经验"
    
    # 组合完整的 Prompt
    full_prompt = f"""{base_prompt}

---

## 📚 已加载的知识库

### 工艺解析
{process_map}

### 故障树
{fault_tree}

### 历史经验（最近3条）
{exp_summary}

---

**现在开始，严格按照上方的排查流程，一步一步引导用户排查问题！**
"""
    return full_prompt


@mcp.tool()
def get_detective_mode_prompt() -> str:
    return detective_mode_prompt()


if __name__ == "__main__":
    mcp.run()
