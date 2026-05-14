---
title: Hermes LLM
type: entity
tags:
  - LLM
  - Agent-Brain
  - Core-Component
summary: Hermes LLM 是 Harness Agent 架构中的核心大脑，负责意图理解、决策制定以及对 Skill 的动态编排。
sources:
  - "raw/notebooklm-analysis/harness-agent-architecture-qa.md"
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 基于 harness-agent-architecture-qa.md 中关于 Agent 架构的定义，Hermes LLM 被明确界定为负责意图识别与流程编排的核心智能单元。
---

# Hermes LLM

Hermes LLM 是 Harness Agent 架构中的核心智能中枢，被定义为系统的“大脑”。其核心职责在于处理复杂的逻辑决策与意图解析，而非直接执行具体的原子操作。在架构设计中，Hermes LLM 严格遵循解耦原则，将意图理解与具体执行逻辑分离：它负责根据用户指令进行意图识别，并基于预定义的 [[Skill]] 库进行动态编排，决定任务执行的顺序或构建有向无环图（DAG）。

与传统的基于关键词匹配的脚本逻辑不同，Hermes LLM 具备更强的语义理解能力，能够处理动态指令，避免了因硬编码逻辑导致的系统脆弱性。在工作流中，Hermes LLM 处于控制层，它通过调用 [[agent-brain-plugins]] 中注册的各类能力单元，将复杂的业务需求转化为有序的原子操作序列。这种设计确保了系统在面对复杂任务时，能够通过灵活的编排实现高效的自动化处理，同时保持底层 [[Skill]] 的原子性与稳定性。

## 在本视频中的角色
- **决策中枢**：负责对用户意图进行深度理解，并根据任务目标制定执行策略。
- **编排引擎**：在各个原子 [[Skill]] 之间进行逻辑调度，决定任务的执行顺序或 DAG 结构。
- **意图解析器**：替代了传统的 Python 关键词解析方案，通过 LLM 的语义能力实现更精准的指令识别。
- **架构协调者**：通过与 [[agent-brain-plugins]] 的交互，读取 SOP 与 Registry，确保 Agent 能够调用正确的工具完成任务。