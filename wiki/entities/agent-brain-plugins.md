---
title: agent-brain-plugins
type: entity
tags:
  - architecture
  - infrastructure
  - agent-system
summary: agent-brain-plugins 是 Harness Agent 架构中用于持久化存储核心逻辑、能力单元及执行蓝图的配置与资源库，是实现 Brain 与 Skill 解耦的关键基础设施。
sources:
  - "raw/notebooklm-analysis/harness-agent-architecture-qa.md"
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 该实体作为架构中的持久化层，承载了 SOP、Skill 和 Tool 的定义，是连接 LLM 决策与底层执行的桥梁。
---

# agent-brain-plugins

### 实体描述
agent-brain-plugins 是 Harness Agent 架构中的核心配置与资源管理模块，其主要定位是作为 [[Hermes LLM]] 产出成果的持久化载体。该模块通过结构化的文件系统，将 Agent 的运行逻辑从代码逻辑中剥离出来，实现了“配置即能力”的设计哲学。

在具体实现上，agent-brain-plugins 包含以下核心组件：
1. **SOP (sop.yaml)**：定义了 [[SOP]] 的 Pipeline 流程，作为 Brain 进行任务[[编排]]的蓝图。
2. **Skill (SKILL.md + scripts)**：封装了 Brain 可调用的原子能力单元，通过 Markdown 描述与脚本实现，确保了能力的标准化。
3. **Tool (tools/*.py)**：存放 Skill 执行过程中所需的原子数据获取函数，确保了执行层面的原子性。
4. **Registry (registry.yaml)**：作为所有能力的集中目录，充当 Meta-Agent 的“菜单”，使得系统能够动态发现并调用可用资源。

通过这种设计，系统避免了在 Python 脚本中硬编码逻辑的脆弱性，确保了意图理解由 LLM 负责，而执行逻辑由插件化脚本负责，极大地提升了系统的可维护性与扩展性。

### 在本视频中的角色
在 [[Harness Agent 架构设计问答精粹]] 中，agent-brain-plugins 被明确定义为架构的“持久化中心”。它不仅存储了 Agent 的执行蓝图，还通过 Registry 机制为 Brain 提供了可调用的能力清单。它在架构中起到了承上启下的作用：向上为 Brain 提供决策依据（通过 SKILL.md 描述），向下为执行层提供标准化的工具函数，是实现 [[解耦原则]] 的关键基础设施。