---
title: sop-wiki-build
type: entity
tags:
  - agent-pipeline
  - knowledge-graph
  - automation
summary: Harness Agent 架构中负责知识图谱构建的核心流水线阶段，将处理后的数据转化为结构化知识。
sources:
  - raw/notebooklm-analysis/harness-agent-architecture-qa.md
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 该实体是 Harness Agent 自动化工作流中的关键环节，负责将非结构化内容转化为知识图谱，在架构图中处于 Pipeline 的 Stage D 位置。
---

# sop-wiki-build

## 实体描述
`sop-wiki-build` 是 Harness Agent 架构中定义在 `sop.yaml` 流水线配置里的关键阶段（Stage D）。其核心职责是执行知识图谱的构建任务，将经过前序阶段（如 `sop-notebooklm-research` 的研究抓取和 `sop-content-transform` 的内容变换）处理后的数据，转化为符合知识图谱规范的结构化信息。该阶段通过自动化流程，确保从原始信息到知识库的平滑过渡，是实现系统知识沉淀与关联的核心引擎。在整个 Agent 运行周期中，`sop-wiki-build` 依赖于 `agent-brain-plugins` 进行持久化产出，确保构建的知识能够被后续的查询、推理或通知服务调用。

## 在本视频中的角色
在 Harness Agent 的整体工作流中，`sop-wiki-build` 扮演着“知识固化者”的角色。当 Intent Router Agent 完成意图识别并将任务路由至 Pipeline 后，该阶段负责接收处理后的中间产物，并将其转化为可供系统长期检索和利用的知识图谱格式。它是连接原始数据处理与最终信息分发（如 `sop-tg-notify`）的重要枢纽，确保了系统输出的知识具有高度的结构化与可追溯性。

## 相关链接
- [[Harness Agent 架构设计问答精粹]]
- [[sop-notebooklm-research]]
- [[sop-content-transform]]