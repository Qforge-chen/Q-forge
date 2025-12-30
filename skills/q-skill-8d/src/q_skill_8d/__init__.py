"""Q-Skill-8D: 8D 报告审核 MCP 技能包"""

import argparse
from .server import mcp


def main():
    """MCP 服务器入口点"""
    parser = argparse.ArgumentParser(description="Q-Skill-8D MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    args = parser.parse_args()
    
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
