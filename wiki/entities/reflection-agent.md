---
title: Reflection Agent
type: entity
tags:
  - agent
  - reflection
  - reliability
  - failure_modes
summary: Reflection Agent 是 Pipeline 可靠性系统中的后期组件，定期回顾运行记录、更新 failure_modes，融合声明式与经验式两类失效模式，需要 50+ 次运行数据后才具备实用价值。
sources:
  - raw/notebooklm-analysis/pipeline-reliability-design-qa.md
created: "2025-04-08"
updated: "2025-04-08"
layer: L1
confidence: high
reasoning: 该实体定义直接源于 pipeline-reliability-design-qa.md 中的 Q7 讨论，描述了明确的设计原则、触发条件和数据门槛，逻辑清晰且无歧义，因此给予高置信度。
---

## 实体描述

Reflection Agent 是 Pipeline 可靠性架构中的一个关键后期组件，其核心职责是**定期回顾运行记录，并根据实际执行情况动态更新 failure_modes**。在设计上，failure_modes 的来源被划分为两类：声明式（由 creator 在配置时生成，基于对可能出错点的预判）和经验式（根据实际运行中观察到的错误记录归纳）。这两种来源性质不同，前者偏重先验知识，后者偏重后验证据，而 Reflection Agent 正是扮演着两者融合与迭代的角色。

该组件的工作流程大致如下：当 Pipeline 积累了一定数量的运行日志后，Reflection Agent 会定期扫描这些记录，识别出新的、未在声明式 failure_modes 中覆盖的错误模式，将其转化为经验式 failure_modes；同时，它也会根据历史成功率对已有的声明式规则进行修正或淘汰。例如，一个在声明式中被标记为“可能超时”的 stage，如果实际运行中从未触发超时，Agent 可能会降低其权重或移除该规则；反之，一个声明中未预见的错误类型如果频繁出现，Agent 会将其补充到 failure_modes 列表中。

值得注意的是，Reflection Agent 的设计被**明确要求延迟构建**——只有在 Pipeline 运行超过 50 次之后，运行数据才具有统计意义，此时 Agent 的更新才会产生实质性价值。在数据不足时提前引入该组件，不仅会增加系统复杂度，还可能因为噪音数据导致规则劣化。这一原则体现了“LLM 只做 LLM 该做的事，其余全部代码化”的核心原则：Agent 本身可视为轻量级的代码逻辑（定时任务+规则引擎），而非依赖 LLM 推理的模块。

此外，Reflection Agent 与系统内的其他组件有着紧密的协作关系：它输出的更新后的 failure_modes 会直接影响 [[阶段守卫]]（Stage Guard）的 timeout 阈值设置和 [[评估引擎]]（Evaluation Engine）的质量评估标准，从而形成一条从“运行数据”到“健康契约”再到“执行策略”的闭环反馈链路。

## 在本视频中的角色

在本视频所讨论的 Pipeline 可靠性设计精粹中，Reflection Agent 被定位为整个架构的“自我进化中枢”。视频指出，系统中的 guard、evaluate、retry 三套配置本质上都是围绕同一个问题——“这条 pipeline 什么叫正常”——展开的，而 Reflection Agent 正是将这些分散的配置统一为一份“健康契约”的推动者。视频强调，Creator 无需提前设计该组件，而是应在 Pipeline 运行积累足够数据（50+ 次）后，再按需引入。这样一来，Reflection Agent 就能基于实际失败记录，自动修正 declaration 阶段的假设，避免“过度设计”和“配置冗余”两大陷阱。

## 相关页面

- [[Pipeline 可靠性设计问答精粹]]
- [[评估引擎]]