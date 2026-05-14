---
title: SOP
type: concept
tags:
  - AgentArchitecture
  - Workflow
  - Orchestration
summary: SOP（Standard Operating Procedure）在 Agent 架构中作为 Pipeline 流程定义，是 Brain 进行任务编排的蓝图，用于规范化原子操作的执行顺序。
sources:
  - "raw/notebooklm-analysis/harness-agent-architecture-qa.md"
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 直接从NotebookLM思维导图中提取的概念。
---

# SOP (Standard Operating Procedure)

## 概念定义
在 Agent 架构体系中，SOP（标准作业程序）被定义为一种结构化的 Pipeline 流程蓝图。它不仅是任务执行的逻辑框架，更是连接 Brain（如 Hermes LLM）与具体执行单元（Skill）的桥梁。SOP 的核心价值在于将复杂的业务逻辑拆解为一系列可预测、可复用的原子操作序列。通过将这些流程显式地定义在 `sop.yaml` 等配置文件中，系统实现了逻辑与执行的解耦：Brain 负责根据意图进行高层级的编排决策，而 SOP 则确保了这些决策能够按照预设的路径稳定执行，避免了在执行过程中引入不必要的条件分支决策，从而提升了系统的可维护性与执行效率。

## 技术细节
- **存储形式**：通常以 `sop.yaml` 格式持久化存储于 `agent-brain-plugins` 项目中，作为系统配置的一部分。
- **编排逻辑**：SOP 定义了 Skill 的调用链（例如：Skill A → Skill B → Skill C）。在这种架构下，Brain 并不直接编写执行代码，而是通过读取 SOP 定义的蓝图，决定当前任务流的执行顺序。
- **与 Skill 的关系**：SOP 是 Skill 的“剧本”。Skill 是原子化的能力单元，而 SOP 负责将这些原子单元串联成完整的业务流程。
- **执行约束**：SOP 强调流程的确定性，通过预定义的 Pipeline 结构，减少了 LLM 在运行时进行复杂逻辑判断的负担，降低了因模型幻觉导致的执行偏差。

## 应用场景
- **自动化工作流编排**：在处理复杂任务（如数据清洗、分析、报告生成）时，通过 SOP 定义标准化的处理步骤，确保每次执行的逻辑一致性。
- **系统能力扩展**：当需要增加新的业务流程时，无需修改核心代码，只需在 `agent-brain-plugins` 中更新或新增 SOP 定义，即可实现功能的快速迭代。
- **任务标准化**：在多 Agent 协作场景中，SOP 作为统一的执行协议，确保不同组件对任务流程的理解保持高度一致。

## 相关链接
- [[Skill]]
- [[编排]]
- [[agent-brain-plugins]]
- [[Hermes LLM]]