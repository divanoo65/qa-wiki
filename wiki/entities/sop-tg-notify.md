---
title: sop-tg-notify
type: entity
tags:
  - pipeline
  - automation
  - notification
summary: 一个负责处理 Telegram 通知发送的自动化组件，通过 Python 脚本实现逻辑解耦，不再依赖 LLM 进行格式化。
sources:
  - "raw/notebooklm-analysis/pipeline-reliability-design-qa.md"
created: 2024-05-22
updated: 2024-05-22
layer: L1
confidence: high
reasoning: 该实体是 pipeline 自动化流程中的关键通知模块，其设计原则体现了“LLM 只做 LLM 该做的事”的核心架构思想。
---

# sop-tg-notify

### 实体描述
sop-tg-notify 是 pipeline 自动化流水线中的核心通知组件，主要职责是将处理结果通过 Telegram 渠道推送给用户。在早期的架构设计中，该模块曾尝试调用 Hermes 服务进行内容处理，但在最新的可靠性优化方案中，sop-tg-notify 被重构为纯 Python 脚本实现。

该组件的设计遵循“代码化”原则，即通知内容的格式化与发送逻辑完全脱离 LLM 推理，直接读取 `pipeline-context.json` 模板进行格式化输出。这种设计不仅显著降低了对 LLM 的依赖，还提升了通知发送的响应速度与稳定性。此外，sop-tg-notify 在 `sop.yaml` 的健康检查配置中拥有独立的超时限制（3分钟）和完成模式（done_pattern: "stage-d done"），确保了整个 pipeline 在执行过程中的可观测性与故障预警能力。

### 在本视频中的角色
在本视频讨论的 pipeline 可靠性设计中，sop-tg-notify 扮演了“执行层”的角色。它与 [[代码自检]] 机制共同构成了 pipeline 的质量保障体系。通过将通知逻辑从 LLM 剥离，sop-tg-notify 确保了即使在 LLM 负载较高或出现推理偏差时，系统的通知反馈链路依然能够保持高可用性，是实现 [[Pipeline 可靠性设计问答精粹]] 中所提倡的“代码化执行”的关键一环。