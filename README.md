# Q-Forge

**The Local AI Auditor for Manufacturing.**

> **"You must rely on yourself."**  
> Built by **Chen Zhongshun (Master Chen)** — Rebel Engineer. 20 years in Quality.

---

## 🎯 The Problem

**Traditional quality audits fail in the AI era:**

| Traditional Approach | The Reality |
|---------------------|-------------|
| Manual 8D review | Missed gaps, inconsistent standards |
| Excel-based supplier tracking | Reactive, not predictive |
| Tribal knowledge | Walks out the door when experts leave |

## 💡 The Q-Forge Solution

**Q-Forge transforms quality expertise into deployable AI skills.**

```
┌─────────────────────────────────────────────────────────────┐
│                        Q-Forge                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Logic Lock  │ →  │Golden Prompt│ →  │ Model Call  │     │
│  │ (Python)    │    │ (Knowledge) │    │ (LLM)       │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  Deterministic       Expert Rules      Reasoning Engine     │
│  Quality Gates       (MECE Format)     (GPT/GLM/Claude)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Three-Layer Philosophy

| Layer | What It Does | Why It Matters |
|-------|--------------|----------------|
| **Logic Lock** | Hardcoded business rules in Python | Never relies on LLM judgment for critical checks |
| **Golden Prompt** | Expert knowledge encoded as machine-readable rules | Your years of experience, now reusable |
| **Model Call** | Generic LLM for reasoning | Models are public, knowledge is yours |

> **"I don't build models. I build knowledge."**  
> — Chen Zhongshun

---

## 📦 Skill Packages (Continuous Update 🔄)

This repository is actively maintained and updated with new skills and logic gates.

| Skill | Description | Key Feature |
|-------|-------------|-------------|
| **q-skill-8d** | 8D Report Auditor | 4-location containment gate, D4 root cause validation |
| **q-skill-rootcause** | Root Cause Analyzer | Fault tree + elimination method |
| **q-skill-supplier** | Supplier Quality Monitor | PPM tracking, risk alerts |
| **q-skill-reporter** | Report Generator | Markdown/HTML output |

---

## 🛠️ Base System: Q-Forge Core

The base system of Q-Forge is a lightly customized version of [Goose](https://github.com/block/goose). 

> [!NOTE]
> The core `qforge` binary and customized Goose environment are **not** included in this repository to keep it lightweight. I will be sharing my specialized **System Prompts** and configuration files later in the `docs/` folder.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Qforge-chen/Q-forge.git
cd Q-forge

# Install a skill (e.g., 8D auditor)
cd skills/q-skill-8d
pip install -e .
```

---

## 🧠 Design Philosophy

> **"Models are public, knowledge is yours."**

The real barrier in AI for manufacturing is not the model — it's the **domain expertise**.

Q-Forge is a framework for **Knowledge Productization**:
- Consulting becomes a system
- Training becomes a rule engine  
- Experience becomes a reusable asset

---

## 👤 About the Author

**Chen Zhongshun (Master Chen)**  
**Rebel Engineer.** 20 years in Quality.  
Building Q-Forge (AI for Manufacturing) with $0 and 13 hours.  

- 𝕏 (Twitter): [@QForge_Builder](https://x.com/QForge_Builder)
- 📧 Email: [zhongshunchen1982@gmail.com](mailto:zhongshunchen1982@gmail.com)

*"You must rely on yourself."*  
*人一定要靠自己！*

---

## 📄 License

Apache License 2.0 — See [LICENSE](LICENSE) for details.

---

*Q-Forge: The Local AI Auditor for Manufacturing.*
