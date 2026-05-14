---
title: Harness Agent 架构设计问答精粹
type: source
tags:
  - HarnessAgent
  - 架构设计
  - LLM
  - 自动化
summary: 本文通过问答形式深度解析了 Harness Agent 的核心架构逻辑，重点阐述了通过虚拟化实现 Brain 与 Hands 解耦的机制，以及 Skill 编排、意图路由器设计与 agent-brain-plugins 的持久化规范。
sources:
  - raw/notebooklm-analysis/harness-agent-architecture-qa.md
created: 2026-05-14
updated: 2026-05-14
layer: L1
run_id: gh-25858551719-1
---

## 执行摘要

Harness Agent 系统的核心设计哲学在于“解耦”与“虚拟化”。通过将决策层（Hermes LLM）与执行层（Skill/Tool）分离，系统实现了类似操作系统的抽象能力。本文档详细探讨了如何通过原子化的 Skill 设计、基于意图的路由机制以及标准化的持久化方案（agent-brain-plugins），构建一个可扩展、易维护且具备高可靠性的自动化 Agent 系统。

## 核心要点

### 1. 架构的本质：解耦与虚拟化
Harness Agent 的核心价值在于通过虚拟化接口实现 Brain（决策）与 Hands（执行）的彻底解耦。这种设计类似于操作系统对硬件的抽象，使得上层逻辑无需关心底层执行环境（本地或云端沙盒）的差异，从而极大提升了系统的可扩展性与可替换性。

### 2. Skill 与编排的边界
Skill 被定义为不可拆分的原子工作流节点，封装了固定的输入输出逻辑。编排（Orchestration）则完全由 Hermes LLM 负责，它根据意图在 Skill 之间进行顺序或 DAG 决策。这种设计明确了“编排不在 Skill 内部”的原则，确保了每个 Skill 的纯粹性与复用性。

### 3. 意图驱动的路由设计
系统摒弃了脆弱的关键词匹配逻辑，转而采用“意图路由器”模式。由 Hermes LLM 负责语义层面的意图解析，Python 脚本仅负责执行原子操作。通过引入“意图契约”和“动作先解析”机制，确保了系统能够根据用户真实意图动态调度 Pipeline，而非仅仅进行简单的 URL 路由。

### 4. 持久化与规范化
`agent-brain-plugins` 项目作为系统的“大脑记忆库”，通过标准化的 `sop.yaml` 定义编排蓝图，通过 `SKILL.md` 和 `tools/` 目录管理能力单元。这种结构化存储方式不仅支持了 Meta-Agent 的能力发现，还通过 Git 版本控制实现了天然的隔离与回滚机制，确保新增 Pipeline 不会破坏现有业务逻辑。

### 5. 完整架构链路
系统从用户触发（Webhook/GitHub）开始，经由 Intent Router Agent 进行意图识别，随后进入由 SOP 定义的 Pipeline 阶段。每个阶段均配备 spawn 守卫与进度通知，最终产出物通过插件系统持久化，形成闭环的自动化生产链路。

---

## 相关链接
- [[Harness Agent]]
- [[Hermes LLM]]
- [[agent-brain-plugins]]
- [[Skill]]
- [[编排]]
- [[SOP]]
- [[意图路由器]]
- [[解耦]]