"""Q-Skill-Supplier: 供应商质量监控 MCP 技能包"""

import argparse
from .server import mcp


def main():
    """MCP 服务器入口点"""
    parser = argparse.ArgumentParser(description="Q-Skill-Supplier MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    args = parser.parse_args()
    
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
