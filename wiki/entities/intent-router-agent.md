---
title: "Intent Router Agent"
type: entity
tags:
  - agent
  - router
  - intent
  - pipeline
summary: "Intent Router Agent 是 Harness Agent 系统的核心决策组件，负责解析用户输入的意图并使用 Hermes LLM 理解意图，然后将请求路由到正确的 Pipeline 执行。"
sources:
  - "raw/notebooklm-analysis/harness-agent-architecture-qa.md"
created: "2025-01-01"
updated: "2025-01-01"
layer: L1
confidence: high
reasoning: "该实体在架构中作为关键路由节点，连接用户触发与下游 Pipeline，是系统智能入口，符合 L1 层实体的高置信度定义。"
---

## 实体描述

Intent Router Agent 是 Harness Agent 系统架构中的第一个主动处理节点，位于用户触发（webhook、Telegram 或 GitHub push）之后。它的核心职责是解析输入请求的意图，利用 Hermes LLM（大语言模型）理解用户想要执行的操作，然后根据解析结果将请求路由到正确的 Pipeline（流水线）。在实现上，Intent Router Agent 要求 **`parse_intent_actions()` 必须最先执行**，且 actions 作为必传参数，确保意图解析的优先级和可靠性。

该 Agent 的另一个关键特性是验收标准包含内容验证——当检测到翻译意图时，必须验证输出是否为中文。这种机制保证了意图理解的正确性，并防止错误路由浪费下游资源。Intent Router Agent 本身并不执行具体业务逻辑，而是作为智能调度器，将意图与预先定义的 sop.yaml 配置文件中的 Pipeline 进行匹配。例如，当用户请求“研究某个话题”时，它会路由到 sop-notebooklm-research Pipeline；如果是“构建知识图谱”，则路由到 sop-wiki-build Pipeline。

得益于 agent-brain-plugins 的持久化能力，Intent Router Agent 的决策过程可以被记录和分析，便于后续优化。在 Harness 系统中，该 Agent 扮演着“大脑入口”的角色，所有外部输入都必须经过它的意图理解与路由，才能触发后续的多阶段处理流程。它的高效性直接决定了整个系统的响应速度和准确性。

## 在本视频中的角色

在本次视频分析中，Intent Router Agent 被描述为 Harness Agent 系统的“智能总闸”。视频详细展示了用户触发后，该 Agent 如何通过 Hermes LLM 实时理解自然语言意图，并自动路由到对应的 Pipeline（如研究、内容变换、知识图谱或通知）。它体现了系统高度自动化和配置驱动的设计理念，是连接用户与复杂后端流程的关键桥梁。视频强调，如果没有 Intent Router Agent 的正确路由，后续的 Pipeline 将无法精准执行，因此它也是架构中最先被验证和测试的组件。

## 相关页面

- [[Harness Agent 架构设计问答精粹]]
- [[流水线]]