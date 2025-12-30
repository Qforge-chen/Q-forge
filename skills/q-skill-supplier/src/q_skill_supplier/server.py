"""
Q-Skill-Supplier: 供应商质量监控 MCP 服务器

功能：
- 读取供应商质量数据
- 计算供应商质量指标
- 供应商质量排名和预警
- 经验知识积累
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("q-skill-supplier")

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
    return "暂无预定义的分析逻辑，请先创建 golden_prompt.md 文件。"


# ============================================================
# MCP 工具
# ============================================================

@mcp.tool()
def read_supplier_data(file_path: str, sheet_name: str = None) -> dict:
    """
    读取供应商质量数据 Excel 文件
    
    Args:
        file_path: Excel 文件路径
        sheet_name: 工作表名称（可选）
    
    Returns:
        包含数据统计信息的字典
    """
    try:
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        return {
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(10).to_dict(orient='records'),
            "file_path": file_path
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def analyze_supplier_quality(file_path: str, date_column: str = "日期", 
                              supplier_column: str = "供应商",
                              qty_column: str = "检验数量",
                              defect_column: str = "不良数量") -> dict:
    """
    分析供应商质量指标
    
    Args:
        file_path: Excel 文件路径
        date_column: 日期列名
        supplier_column: 供应商列名
        qty_column: 检验数量列名
        defect_column: 不良数量列名
    
    Returns:
        供应商质量分析结果
    """
    try:
        df = pd.read_excel(file_path)
        
        # 按供应商分组统计
        supplier_stats = df.groupby(supplier_column).agg({
            qty_column: 'sum',
            defect_column: 'sum'
        }).reset_index()
        
        # 计算合格率和PPM
        supplier_stats['合格率'] = ((supplier_stats[qty_column] - supplier_stats[defect_column]) 
                                    / supplier_stats[qty_column] * 100).round(2)
        supplier_stats['PPM'] = (supplier_stats[defect_column] / supplier_stats[qty_column] * 1000000).round(0)
        
        # 按合格率排序
        supplier_stats = supplier_stats.sort_values('合格率', ascending=True)
        
        # 识别预警供应商（合格率 < 95%）
        warning_suppliers = supplier_stats[supplier_stats['合格率'] < 95][supplier_column].tolist()
        
        # 总体统计
        total_qty = df[qty_column].sum()
        total_defect = df[defect_column].sum()
        overall_rate = round((total_qty - total_defect) / total_qty * 100, 2)
        
        return {
            "status": "success",
            "overall": {
                "total_qty": int(total_qty),
                "total_defect": int(total_defect),
                "pass_rate": overall_rate,
                "ppm": round(total_defect / total_qty * 1000000)
            },
            "supplier_ranking": supplier_stats.to_dict(orient='records'),
            "warning_suppliers": warning_suppliers,
            "supplier_count": len(supplier_stats),
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def calculate_supplier_trend(file_path: str, supplier_name: str,
                              date_column: str = "日期",
                              supplier_column: str = "供应商",
                              qty_column: str = "检验数量",
                              defect_column: str = "不良数量") -> dict:
    """
    计算指定供应商的质量趋势
    
    Args:
        file_path: Excel 文件路径
        supplier_name: 供应商名称
        date_column: 日期列名
        supplier_column: 供应商列名
        qty_column: 检验数量列名
        defect_column: 不良数量列名
    
    Returns:
        供应商质量趋势数据
    """
    try:
        df = pd.read_excel(file_path)
        
        # 筛选指定供应商
        supplier_df = df[df[supplier_column] == supplier_name].copy()
        
        if len(supplier_df) == 0:
            return {"status": "error", "message": f"未找到供应商: {supplier_name}"}
        
        # 按日期分组
        supplier_df[date_column] = pd.to_datetime(supplier_df[date_column])
        trend = supplier_df.groupby(supplier_df[date_column].dt.strftime('%Y-%m-%d')).agg({
            qty_column: 'sum',
            defect_column: 'sum'
        }).reset_index()
        
        trend['合格率'] = ((trend[qty_column] - trend[defect_column]) 
                          / trend[qty_column] * 100).round(2)
        
        # 计算趋势方向
        if len(trend) >= 2:
            recent_rate = trend['合格率'].iloc[-1]
            previous_rate = trend['合格率'].iloc[-2]
            trend_direction = "上升" if recent_rate > previous_rate else ("下降" if recent_rate < previous_rate else "持平")
        else:
            trend_direction = "数据不足"
        
        return {
            "status": "success",
            "supplier": supplier_name,
            "trend_data": trend.to_dict(orient='records'),
            "trend_direction": trend_direction,
            "data_points": len(trend)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def get_experience(keyword: str = None) -> dict:
    """
    获取历史经验知识
    
    Args:
        keyword: 搜索关键词（可选）
    
    Returns:
        匹配的历史经验
    """
    experience = load_experience()
    
    if not experience:
        return {"status": "success", "experiences": [], "message": "暂无历史经验"}
    
    if keyword:
        filtered = {k: v for k, v in experience.items() if keyword in k or keyword in str(v)}
        return {"status": "success", "experiences": filtered, "count": len(filtered)}
    
    return {"status": "success", "experiences": experience, "count": len(experience)}


@mcp.tool()
def save_experience(key: str, summary: str, expert_note: str = None) -> dict:
    """
    保存分析经验到知识库
    
    Args:
        key: 经验标识（如 "1214_供应商A"）
        summary: 分析结论摘要
        expert_note: 专家补充说明（可选）
    
    Returns:
        保存结果
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
        "message": f"经验已保存: {key}",
        "total_experiences": len(experience)
    }


@mcp.tool()
def get_golden_prompt() -> dict:
    """
    获取供应商分析的黄金 Prompt（预定义分析逻辑）
    
    Returns:
        黄金 Prompt 内容
    """
    content = load_golden_prompt()
    return {
        "status": "success",
        "golden_prompt": content
    }



@mcp.tool()
def apply_quality_gate(pass_rate: float, trend_direction: str = None) -> dict:
    """
    【逻辑锁】应用供应商质量判定闸门
    
    Args:
        pass_rate: 合格率 (0-100)
        trend_direction: 趋势方向 (上升/下降/持平/数据不足)，可选
        
    Returns:
        逻辑判定结果 (CRITICAL/WARNING/PASS/EXCELLENT) 及说明
    """
    # 强制逻辑
    gates = {
        "critical_fail": pass_rate < 95,
        "warning": 95 <= pass_rate < 99,
        "excellent": pass_rate >= 99,
        "trend_alert": trend_direction == "下降" if trend_direction else False
    }
    
    verdict = "PASS"
    comment = "质量达标"
    level_icon = "✅"
    
    if gates["critical_fail"]:
        verdict = "CRITICAL"
        comment = "合格率未达标 (<95%)，触发严重预警"
        level_icon = "🔴"
    elif gates["warning"]:
        verdict = "WARNING"
        comment = "合格率需提升 (95%-99%)"
        level_icon = "🟡"
        # 警告区 + 趋势下降 = 风险提升（虽然不到 Critical，但需要标记）
        if gates["trend_alert"]:
             comment += "，且趋势下降，需密切关注"
    elif gates["excellent"]:
        verdict = "EXCELLENT"
        comment = "质量优秀 (>=99%)"
        level_icon = "🟢"
        
    return {
        "verdict": verdict,
        "level_icon": level_icon,
        "pass_rate": pass_rate,
        "trend": trend_direction,
        "comment": comment,
        "gates": gates
    }


@mcp.tool()
def generate_supplier_report(file_path: str, report_title: str = "供应商质量监控报告") -> str:
    """
    生成供应商质量监控 Markdown 报告
    
    Args:
        file_path: Excel 文件路径
        report_title: 报告标题
    
    Returns:
        Markdown 格式的报告
    """
    # 先执行分析
    analysis = analyze_supplier_quality(file_path)
    
    if analysis["status"] == "error":
        return f"**错误**: {analysis['message']}"
    
    overall = analysis["overall"]
    ranking = analysis["supplier_ranking"]
    warnings = analysis["warning_suppliers"]
    
    # 1. 应用总体质量闸门
    overall_gate = apply_quality_gate(overall['pass_rate'])
    quality_level = f"{overall_gate['level_icon']} {overall_gate['verdict']}"
    quality_comment = overall_gate['comment']
    
    # 找出最佳和最差供应商
    best_supplier = ranking[-1] if ranking else None
    worst_supplier = ranking[0] if ranking else None
    
    # 生成报告
    report = f"""# {report_title}

> 📅 **生成时间**: {analysis["analysis_date"]}  
> 📁 **数据来源**: `{file_path}`  
> 📊 **供应商数量**: {analysis["supplier_count"]}家

---

## 一、总体质量概况

| 指标 | 数值 | 说明 |
|------|------|------|
| 总检验数 | **{overall['total_qty']:,}** 件 | - |
| 总不良数 | **{overall['total_defect']:,}** 件 | - |
| 综合合格率 | **{overall['pass_rate']}%** | {quality_level} |
| 综合 PPM | **{overall['ppm']:,}** | 百万分之不良数 |

**质量评价**: {quality_comment}

---

## 二、供应商质量排名

> 按合格率从低到高排序，预警线：95%

| 排名 | 供应商 | 检验数 | 不良数 | 合格率 | PPM | 状态 |
|:----:|--------|-------:|-------:|-------:|----:|:----:|
"""
    
    for i, row in enumerate(ranking, 1):
        supplier = row.get('供应商', row.get('Supplier', 'N/A'))
        qty = row.get('检验数量', row.get('Qty', 0))
        defect = row.get('不良数量', row.get('Defect', 0))
        rate = row.get('合格率', 0)
        ppm = row.get('PPM', 0)
        
        # 应用单体供应商闸门
        gate = apply_quality_gate(rate)
        status = f"{gate['level_icon']} {gate['verdict']}"
        
        report += f"| {i} | {supplier} | {qty:,} | {defect:,} | {rate}% | {ppm:,.0f} | {status} |\n"
    
    # 最佳/最差供应商对比
    if best_supplier and worst_supplier:
        best_name = best_supplier.get('供应商', 'N/A')
        best_rate = best_supplier.get('合格率', 0)
        worst_name = worst_supplier.get('供应商', 'N/A')
        worst_rate = worst_supplier.get('合格率', 0)
        gap = round(best_rate - worst_rate, 2)
        
        report += f"""
### 📊 供应商对比

| 对比项 | 最佳供应商 | 最差供应商 | 差距 |
|--------|-----------|-----------|------|
| 供应商 | **{best_name}** | **{worst_name}** | - |
| 合格率 | {best_rate}% | {worst_rate}% | **{gap}%** |

"""

    if warnings:
        report += f"""
---

## 三、⚠️ 预警供应商（需重点关注）

以下 **{len(warnings)}** 家供应商合格率低于 95%，建议立即采取行动：

"""
        for w in warnings:
            # 找到该供应商的详细数据
            w_data = next((r for r in ranking if r.get('供应商') == w), None)
            if w_data:
                w_rate = w_data.get('合格率', 0)
                w_ppm = w_data.get('PPM', 0)
                
                # 再次应用闸门获取详细评价
                gate = apply_quality_gate(w_rate)
                
                report += f"### {gate['level_icon']} {w}\n"
                report += f"- 合格率：**{w_rate}%**\n"
                report += f"- 状态判定：{gate['comment']}\n"
                report += f"- PPM：**{w_ppm:,.0f}**\n"
                report += f"- 建议措施：暂停新订单、开展专项审核、增加检验频次\n\n"
            else:
                report += f"- ⚠️ **{w}**\n"
    
    report += """
---

## 四、改进建议

### 🚨 立即行动（本周内）
1. **约谈预警供应商**：要求提交改善计划及时间表
2. **加严检验**：对预警供应商来料实施 100% 检验
3. **根因分析**：识别主要不良类型，定位问题根源

### 📈 持续改进（本月内）
1. **供应商评级**：建立月度质量评分机制
2. **趋势监控**：跟踪供应商质量变化趋势
3. **能力辅导**：对有潜力的供应商提供技术支持

### 🎯 长期策略（季度规划）
1. **供应商优化**：考虑淘汰持续不达标供应商
2. **多元供应**：培养备选供应商降低风险
3. **质量前移**：推动供应商过程质量控制

---

## 五、附录

### 质量等级标准 (逻辑锁)

| 等级 | 合格率范围 | 说明 |
|------|-----------|------|
| 🟢 EXCELLENT | ≥ 99% | 质量优秀 |
| 🟡 WARNING | 95% - 99% | 质量达标但需提升 |
| 🔴 CRITICAL | < 95% | 严重预警，必须整改 |

---

*本报告由 Q-Forge 质量智能助手自动生成*  
*如有问题，请联系质量管理部门*
"""
    
    return report



@mcp.tool()
def save_supplier_report(file_path: str, report_title: str = "供应商质量监控报告") -> dict:
    """
    生成供应商质量报告并自动保存到与 Excel 相同目录
    
    Args:
        file_path: Excel 文件路径（报告将保存到同一目录）
        report_title: 报告标题
    
    Returns:
        包含报告内容和保存路径的字典
    """
    try:
        # 生成报告
        report = generate_supplier_report(file_path, report_title)
        
        if report.startswith("**错误**"):
            return {"status": "error", "message": report}
        
        # 获取 Excel 文件所在目录
        excel_path = Path(file_path)
        output_dir = excel_path.parent
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"分析报告_{timestamp}.md"
        report_path = output_dir / report_filename
        
        # 保存报告
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return {
            "status": "success",
            "message": f"报告已保存",
            "saved_path": str(report_path),
            "filename": report_filename,
            "report_content": report
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================
# MCP 提示词
# ============================================================

@mcp.prompt()
def supplier_analysis_prompt() -> str:
    """供应商质量分析提示词"""
    golden = load_golden_prompt()
    experience = load_experience()
    
    exp_summary = ""
    if experience:
        recent = list(experience.items())[-3:]  # 最近3条经验
        exp_summary = "\n".join([f"- {k}: {v['summary']}" for k, v in recent])
    
    return f"""# 供应商质量分析指南

{golden}

## 历史经验参考
{exp_summary if exp_summary else "暂无历史经验"}

## 分析流程
1. 使用 read_supplier_data 读取数据
2. 使用 analyze_supplier_quality 计算指标
3. 对预警供应商使用 calculate_supplier_trend 分析趋势
4. 使用 generate_supplier_report 生成报告
5. 使用 save_experience 保存分析结论
"""


if __name__ == "__main__":
    mcp.run()
