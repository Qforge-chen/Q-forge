from mcp.server.fastmcp import FastMCP
from pathlib import Path
from datetime import datetime

# 初始化 MCP 服务器
mcp = FastMCP("q-skill-reporter")

# 默认数据目录
DEFAULT_DATA_DIR = r"C:\Users\chen\Desktop\Qcli\Q-FORGE-V1\data"


@mcp.tool()
def list_md_files(directory: str = DEFAULT_DATA_DIR) -> dict:
    """
    【查找报告】列出指定目录下的所有 Markdown 报告文件
    
    功能：
    扫描目录，返回所有 .md 文件的列表，帮助用户选择要转换的报告。
    
    Args:
        directory: 要扫描的目录路径，默认为 Q-FORGE-V1/data
    
    Returns:
        包含文件列表的字典
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"status": "error", "message": f"目录不存在: {directory}"}
        
        md_files = list(dir_path.glob("*.md"))
        
        file_info = []
        for f in md_files:
            stat = f.stat()
            file_info.append({
                "filename": f.name,
                "path": str(f),
                "size_kb": round(stat.st_size / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            })
        
        file_info.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "status": "success",
            "count": len(file_info),
            "files": file_info,
            "message": f"找到 {len(file_info)} 个 Markdown 文件"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def read_md_for_html(md_file_path: str) -> dict:
    """
    【读取报告】读取 Markdown 文件内容，并返回 HTML 生成指南
    
    功能：
    读取指定的 MD 文件内容，同时返回专业的 HTML 设计指南。
    AI 将根据这些指南创造性地生成漂亮的 HTML 网页。
    
    重要：读取后，请根据返回的设计指南，创造性地生成完整的 HTML 代码！
    
    Args:
        md_file_path: Markdown 文件的完整路径
    
    Returns:
        包含 MD 内容和 HTML 设计指南的字典
    """
    try:
        md_path = Path(md_file_path)
        if not md_path.exists():
            return {"status": "error", "message": f"文件不存在: {md_file_path}"}
        
        md_content = md_path.read_text(encoding="utf-8")
        
        return {
            "status": "success",
            "filename": md_path.name,
            "md_content": md_content,
            "html_design_guide": get_html_design_guide(),
            "instruction": "请根据上述 Markdown 内容和设计指南，创造性地生成一个完整的、专业精美的 HTML 网页。生成后使用 save_html_report 工具保存。"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def save_html_report(html_content: str, original_md_path: str, report_title: str = "Q-Forge 质量报告") -> dict:
    """
    【保存HTML】将 AI 生成的 HTML 内容保存为文件
    
    功能：
    将完整的 HTML 代码保存到与原 MD 文件相同的目录。
    
    重要：html_content 必须是完整的 HTML 代码，包含 <!DOCTYPE html> 开头！
    
    Args:
        html_content: 完整的 HTML 代码（由 AI 生成）
        original_md_path: 原始 MD 文件的路径（用于确定保存位置）
        report_title: 报告标题
    
    Returns:
        包含保存路径的字典
    """
    try:
        md_path = Path(original_md_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"{md_path.stem}_{timestamp}.html"
        html_path = md_path.parent / html_filename
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            "status": "success",
            "message": "✅ HTML 报告已保存！",
            "html_path": str(html_path),
            "html_filename": html_filename,
            "open_hint": f"请在浏览器中打开: {html_path}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_html_design_guide() -> str:
    """返回 HTML 设计指南"""
    return """
# HTML 设计指南 - 请严格遵循！

## 1. 整体风格
- **现代质感**：使用渐变背景、圆角卡片、柔和阴影
- **配色方案**：主色调用蓝色系(#2563eb)，成功用绿色(#10b981)，警告用橙色(#f59e0b)，错误用红色(#ef4444)
- **字体**：使用系统字体栈（-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei'）

## 2. 布局结构
- 页面背景用柔和的渐变色
- 主内容区域用白色卡片，带圆角(16px)和阴影
- 顶部有一个渐变色的标题栏
- 底部有 Q-Forge 品牌 footer

## 3. 组件样式
- **表格**：表头深色背景，奇偶行交替颜色，悬停高亮
- **代码块**：深色背景(#1f2937)，浅色字体
- **引用块**：左边框强调，浅灰背景
- **列表**：适当的间距和缩进

## 4. 响应式
- 移动端友好
- 打印优化（去掉背景色和阴影）

## 5. 必须包含
- `<!DOCTYPE html>` 声明
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- 所有样式内嵌在 `<style>` 标签中
- Footer 文字："由 Q-Forge 质量智能助手自动生成"

## 6. 创意发挥
- 可以根据报告内容添加合适的图标（用 emoji 或 Unicode）
- 可以为不同等级的标题设计不同的视觉效果
- 可以为表格数据添加颜色编码（如合格=绿色，不合格=红色）
"""


@mcp.prompt()
def html_generator_prompt() -> str:
    """HTML 报告生成器的系统指令"""
    return f"""# Q-Forge HTML 报告生成器

你是一名专业的网页设计师，擅长将 Markdown 报告转换为精美的 HTML 网页。

## 工作流程

1. **使用 `list_md_files`** 列出可用的 MD 报告
2. 用户选择后，**使用 `read_md_for_html`** 读取内容和获取设计指南
3. 根据设计指南，**创造性地生成完整的 HTML 代码**
4. **使用 `save_html_report`** 保存生成的 HTML

## 重要提醒

- 你生成的 HTML 必须是**完整的网页**，从 `<!DOCTYPE html>` 开始
- 所有 CSS 必须**内嵌**在 `<style>` 标签中
- 尽情发挥创意，让每次生成的网页都有独特的设计细节！
- 保持专业感的同时，也要有视觉吸引力

{get_html_design_guide()}
"""


if __name__ == "__main__":
    mcp.run()
