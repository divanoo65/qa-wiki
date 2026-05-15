---
title: pipeline-creator
type: entity
tags: [pipeline, automation, architecture]
summary: pipeline-creator 是负责初始化自动化工作流的工具，目前主要负责生成 stages 和 triggers，但在健康监控与评估配置方面存在设计缺口。
sources: ["raw/notebooklm-analysis/pipeline-reliability-design-qa.md"]
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 该实体在 pipeline 可靠性设计中扮演核心初始化角色，其功能边界及改进方向在来源报告中有明确定义。
---

# pipeline-creator

### 实体描述
pipeline-creator 是自动化流水线构建的核心工具，其主要职责是根据预设逻辑生成 pipeline 的基础架构，包括定义各个阶段（stages）以及触发机制（triggers）。在当前的系统设计中，pipeline-creator 处于自动化流程的起点，但其功能尚不完善。根据最新的可靠性设计评估，该工具目前无法自动生成健康监控参数（guard）和评估规则（evaluate），导致开发者在新建 pipeline 时必须进行大量的人工补充工作。

为了提升系统的健壮性，pipeline-creator 的演进方向被定义为：在创建 pipeline 时，必须通过交互或配置引导用户回答关于运行超时（timeout_minutes）、语言结构要求（min_chinese_ratio）、语义质量标准（semantic_focus）以及潜在故障模式（failure_modes）的四个关键问题。这些信息将被统一写入 `sop.yaml` 的 `health` 块中，作为后续 [[健康契约]] 的核心数据源，从而实现 guard 和 evaluate 的自动化配置。

### 在本视频中的角色
在 pipeline 可靠性设计体系中，pipeline-creator 是导致当前“设计缺口”的关键环节。它目前仅负责流水线的骨架搭建，尚未实现与 [[失败模式]] 分析及自动化评估逻辑的深度集成。通过对其进行功能升级，使其能够自动生成符合契约要求的配置，是解决当前 pipeline 维护成本高、评估规则缺失问题的核心路径。

### 相关链接
- [[Pipeline 可靠性设计问答精粹]]
- [[健康契约]]
- [[失败模式]]