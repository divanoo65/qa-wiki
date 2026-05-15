---
title: sop-notebooklm-research
type: entity
tags:
  - agent-pipeline
  - research-automation
  - harness-agent
summary: Harness Agent 架构中负责执行研究与数据抓取任务的核心流水线阶段。
sources:
  - "raw/notebooklm-analysis/harness-agent-architecture-qa.md"
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 该实体是 Harness Agent 自动化工作流中的关键执行单元，负责从原始输入到知识构建的初始数据获取环节。
---

# sop-notebooklm-research

### 实体描述
sop-notebooklm-research 是 Harness Agent 系统架构中定义的标准化流水线（Pipeline）阶段之一。该阶段的核心职责是执行研究任务与数据抓取工作，作为整个自动化处理流程的“感知层”或“输入层”。当 Intent Router Agent 解析用户意图并确定任务流向后，sop-notebooklm-research 会被激活，利用预定义的逻辑从外部源（如网页、文档或 API）获取原始信息。

该阶段的设计遵循模块化原则，通过 `sop.yaml` 配置文件进行定义与调度。它不仅负责数据的初步采集，还为后续的 [[sop-content-transform]] 和 [[sop-wiki-build]] 阶段提供高质量的原始语料。在执行过程中，该阶段集成了 spawn 守卫机制以确保任务的稳定性，并具备实时向 Telegram 发送进度通知的能力，从而实现对研究过程的透明化管理。

### 在本视频中的角色
在 [[Harness Agent 架构设计问答精粹]] 所描述的系统架构中，sop-notebooklm-research 处于 Pipeline 的 Stage B 位置。它是连接“意图识别”与“知识构建”的关键桥梁，确保了 [[Harness Agent]] 能够从非结构化的外部信息中提取出有价值的知识片段，是实现自动化知识库更新不可或缺的执行单元。