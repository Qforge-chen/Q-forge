# Q-Skill-Supplier

供应商质量监控 MCP 技能包 - Q-Forge 专用

## 功能

- 读取供应商质量数据（Excel）
- 计算供应商质量指标（合格率、PPM、趋势）
- 供应商质量排名和预警
- 经验知识积累

## 安装

```bash
pip install -e .
```

## 在 qforge 中使用

```bash
qforge configure
# 添加扩展：
# Type: SSE
# Command: python -m q_skill_supplier
```
