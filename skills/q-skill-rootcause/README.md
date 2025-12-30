# q-skill-rootcause

**Q-Forge 探因分析智能体 (Detective Agent)**

这是一个交互式的根因分析工具，像侦探一样通过多轮对话协助用户排查问题。

## 🎯 核心能力 (Detective Mode)

1.  **交互式排查**：不直接给出结论，而是基于逻辑树一步步引导用户检查。
2.  **排除法逻辑**：自顶向下，通过特征排除（Exclusion）缩小嫌疑范围。
3.  **终极界面检查**：当单点问题都排除后，强制触发"衔接点/接口"检查。
4.  **经验自进化**：排查成功的案例会自动存入经验库，下次直接调用。

## 📂 知识库架构

启动时会自动加载以下三个文件：

1.  **工艺原理 (`src/q_skill_rootcause/data/process_map.md`)**
    *   描述物理/化学过程原理。
    *   定义关键输入变量 (KPIV) 和输出变量 (KPOV)。

2.  **故障树 (`src/q_skill_rootcause/data/fault_tree.md`)**
    *   结构化的"现象-原因"逻辑树。
    *   系统依据此树进行推理和提问。

3.  **过往经验 (`src/q_skill_rootcause/knowledge/experience.json`)**
    *   AI 自动记录的成功排查案例。

## 🚀 使用方法

**安装**

```bash
pip install -e .
```

**在 MCP 中使用**

配置到 Q-Forge (Goose) 后，直接对话：

> "请帮我排查一下现在的同心度超差问题，现象是..."

系统会启动侦探模式，引导你进行排查。
