---
title: Pipeline 可靠性设计问答精粹
type: source
tags:
  - SOP
  - Pipeline
  - Reliability
  - Architecture
summary: 本文通过问答形式探讨了 SOP Pipeline 在可靠性设计中的核心挑战，重点分析了 stage_guard 与 evaluate 的正交关系、重跑机制的局限性，并提出了基于“健康契约”的统一配置架构方案。
sources:
  - raw/notebooklm-analysis/pipeline-reliability-design-qa.md
created: 2026-05-15
updated: 2026-05-15
layer: L1
run_id: gh-25899515768-1
---

# Pipeline 可靠性设计问答精粹

### 执行摘要
在构建自动化 SOP Pipeline 的过程中，可靠性保障机制（Guard、Evaluate、Retry）往往容易陷入碎片化配置的陷阱。本文通过对 Pipeline 架构设计的深度剖析，明确了“健康契约”作为统一配置源的重要性。核心结论指出：应将评估规则与失败模式定义从脚本中剥离，通过 `sop.yaml` 的 `health` 块进行声明式管理，并引入“代码自检”机制以减少对 LLM 的过度依赖，从而实现更高效、可预测的流程控制。

### 核心要点

1. **Guard 与 Evaluate 的正交性**：`stage_guard` 负责流程完整性（进程是否存活），而 `evaluate` 负责内容质量（输出是否达标）。两者互为前提，不可混淆。
2. **重跑机制的误区**：盲目触发重跑（Re-run）不仅消耗 Token，且无法解决根源问题。必须建立 **[[根因路由]]** 机制，根据失败症状将任务回溯至正确的 Stage，而非简单地在 `wiki-build` 层循环。
3. **健康契约（Health Contract）**：不同类型的 Pipeline（如 web-wiki 与 arxiv-wiki）具有不同的 **[[失败模式]]**。评估规则不应硬编码，而应作为“健康契约”写入 `sop.yaml`，由通用引擎统一执行。
4. **代码自检优先原则**：在涉及格式校验、引用检查等确定性任务时，应优先使用 Python 代码进行自检，仅在必要时调用 [[Gemini]] 等 LLM 进行语义评估。这种“代码化优先”的策略能显著提升系统的稳定性和响应速度。
5. **架构重构方向**：未来的 [[pipeline-creator]] 应在创建阶段强制定义健康参数（超时时间、质量阈值、失败模式），并通过 Reflection Agent 积累运行数据，实现从“声明式配置”向“经验式优化”的演进。

### 相关链接
- [[健康契约]]：定义 Pipeline 正常运行与质量标准的统一描述文件。
- [[代码自检]]：通过非 LLM 方式对产出物进行硬性规则校验的机制。
- [[pipeline-creator]]：负责初始化 Pipeline 架构与健康配置的工具。
- [[NotebookLM]]：在特定 Pipeline 中用于深度分析的辅助工具。