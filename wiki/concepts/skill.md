---
title: Skill
type: concept
tags: [Harness-Agent, Architecture, Workflow]
summary: Skill 是 Harness Agent 架构中的原子化工作流节点，封装了固定的执行逻辑，作为编排系统的最小执行单元。
sources: ["raw/notebooklm-analysis/harness-agent-architecture-qa.md"]
created: 2026-05-14
updated: 2026-05-14
layer: L1
confidence: high
reasoning: 直接从NotebookLM思维导图中提取的概念。
---

# Skill

## 概念定义
在 Harness Agent 架构中，**Skill** 被定义为原子化的、不可拆分的固定工作流节点。它是系统执行逻辑的最小封装单元，具备明确的输入（Input）与输出（Output）契约。Skill 的核心特征在于其逻辑的确定性与封闭性：它仅负责执行特定的任务，而不包含任何条件分支或决策逻辑。这种设计确保了 Skill 的高度可复用性与稳定性。在整个 Agent 系统中，Skill 充当了“执行者”的角色，而将复杂的决策与流程控制权完全交由上层的编排系统（如 Hermes Brain）负责。通过将逻辑封装在 Skill 内部，系统实现了执行层与决策层的解耦，使得底层操作的变更不会影响到上层的编排逻辑。

## 技术细节
- **原子性**：Skill 内部是固定流程，不涉及条件分支或复杂的业务决策。
- **接口标准化**：每个 Skill 必须具备标准的输入输出接口，以便于被编排引擎调用。
- **无状态执行**：Skill 专注于完成特定的原子操作，其执行过程不依赖于外部的动态决策，仅根据输入参数产生预期的输出结果。
- **编排无关性**：Skill 内部不包含编排逻辑，编排逻辑完全由外部的 [[Hermes LLM]] 或其他决策单元通过顺序或 DAG（有向无环图）方式进行组织。

## 应用场景
- **标准化任务执行**：将重复性的操作（如文件读取、API 调用、数据格式转换）封装为 Skill，供 Agent 在不同场景下调用。
- **复杂流程构建**：通过对多个原子 Skill 进行组合，构建出复杂的业务工作流，实现从简单指令到复杂任务的跨越。
- **系统解耦与扩展**：当底层执行环境发生变化时，只需更新或替换对应的 Skill 实现，而无需修改上层的编排逻辑，从而提升系统的可维护性与可扩展性。

## 相关链接
- [[Harness Agent 架构设计问答精粹]]
- [[编排]]
- [[Hermes LLM]]
- [[agent-brain-plugins]]