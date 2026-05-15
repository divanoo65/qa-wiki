# Pipeline 可靠性设计问答精粹

**日期**: 2026-05-15
**主题**: SOP Pipeline 架构设计、Evaluator、Guard、健康契约、LLM 边界

---

## Q1: evaluate 和 stage_guard 是冗余设计吗？

**问**: 每个 stage 背后有守卫检测该阶段是否正常，evaluate 也在做类似的事，这两个是不是冗余的？

**答**: 不冗余，两者正交，检测维度完全不同。

| | stage_guard | wiki-evaluate |
|--|-------------|---------------|
| **检测对象** | 进程是否活着 | 输出内容是否好 |
| **判断方式** | 看 git log 有没有 done commit | 规则检查 + Gemini 打分 |
| **回答的问题** | 这个 stage 有没有跑完？ | 跑完之后结果质量怎样？ |

guard 是 evaluate 的前提——guard 确认 stage 跑完了，evaluate 才有东西可以检查。两者保障不同维度：guard 保证流程完整，evaluate 保证结果质量。

---

## Q2: 评估器和重跑是否冗余？重跑能解决评分低的问题吗？

**问**: evaluate 打分低就触发 re-run wiki-build，这个设计有价值吗？

**答**: 盲目重跑是无效的，会白白消耗 token。

wiki-build 的输入没变，prompt 没变，LLM 温度低时输出高度相似，重跑大概率得到相同结果。更关键的问题是：**评分低的根源不一定在 wiki-build 这一层**。

| 症状 | 真正根源 | 重跑 wiki-build 有用吗 |
|------|---------|----------------------|
| 中文比例 < 5% | content-transform 没翻译 | **无用**，源头在上一层 |
| sources 引用文件不存在 | wiki-build 幻觉了路径 | 有限作用 |
| 语义评分低、机翻感强 | content-transform 翻译质量差 | **无用** |

正确做法是 **root cause routing**：诊断失败在哪一层，路由回正确的 stage，而不是一律重跑 wiki-build。但只有高置信度的诊断才自动处理，模糊症状直接告警人工。

---

## Q3: 不同 pipeline 应该有不同的评估规则吗？

**问**: web-wiki 和 youtube-wiki 的内容性质完全不同，能用同一套评估规则吗？

**答**: 不能，但规则不同的根本原因是**失败模式不同**，不只是内容类型不同。

| Pipeline | 最可能的失败模式 |
|----------|----------------|
| web-wiki（翻译） | content-transform 没翻译 → wiki 是英文 |
| youtube-wiki | NotebookLM 深度不够 → wiki 只有表面概念 |
| arxiv-wiki | LLM 误解公式/方法论 → 关键发现被篡改 |
| github-wiki | LLM 编造不存在的 API → sources 幻觉 |

评估规则不应该硬编码在脚本里，而应该写进每条 pipeline 的 `sop.yaml` 作为契约描述，evaluate 作为通用引擎读取并执行。

---

## Q4: pipeline-creator 创建新 pipeline 时会自动生成 guard 和 evaluate 配置吗？

**问**: 每次新建一条 pipeline，guard 参数和 evaluate 规则需要人工设计吗？

**答**: 目前是的，这是一个真实的设计缺口。

pipeline-creator 现在只生成 stages + triggers，不生成健康参数。每条新 pipeline 的 guard 超时、evaluate 规则都需要人工补充。

正确的设计是：pipeline-creator 在创建时必须回答四个问题：

```
Q1: 每个 stage 正常跑多久？      → timeout_minutes（guard 来源）
Q2: 产出内容什么语言/结构？      → min_chinese_ratio（evaluate 来源）
Q3: 语义上什么叫"好"？          → semantic_focus（evaluate 来源）
Q4: 最可能在哪里出错？           → failure_modes（路由来源）
```

这四个答案直接写进 `sop.yaml` 的 `health` 块，guard 和 evaluate 共用同一份数据源。

---

## Q5: 全新类型的 pipeline，failure_modes 能自动生成吗？

**问**: 已有的 pipeline 类型可以复用 failure_modes，但从没见过的新类型怎么办？

**答**: 可以生成，但第一版是猜测，不是事实。

| 情况 | 可靠性 |
|------|--------|
| 已有类型 | 复用已验证的规则，可靠 |
| 全新类型（首次运行） | LLM 推理生成草稿，标记 `draft: true` |
| 全新类型（跑过 N 次后） | 基于实际失败记录修正，越来越准 |

failure_modes 有两种来源，性质不同：
- **声明式**（creator 生成）："我认为它会在这里出错"
- **经验式**（运行后观察）："它确实在这里出错了"

完整设计需要一个 **Reflection Agent** 定期回顾运行记录、更新 failure_modes。但这个组件需要 50+ 次运行数据才有意义，应该在积累足够数据后再建，不要提前过度设计。

---

## Q6: 系统整体架构的核心问题是什么？

**问**: guard、evaluate、retry 策略都是 per-pipeline 的，越来越多的配置需要 creator 维护，是不是冗余了？

**答**: 对，这是在用三个独立机制解决同一个问题："pipeline 没达到预期怎么办"。

真正需要的是一份**统一的 pipeline 健康契约**，从一个问题自然推导出所有参数：

```
"这条 pipeline，什么叫正常？"
    ↓
每个 stage 跑多久算正常    → guard timeout
产出什么质量算合格          → evaluate profile
哪层出了问题回哪层          → failure_modes routing
```

三套配置变成一份描述，creator 只推理一次。

---

## Q7: 完整的技术重构方案是什么？

**问**: 针对上述所有问题，给出可执行的技术方案。

**答**:

### 核心原则

LLM 只做 LLM 该做的事，其余全部代码化。

| 操作类型 | 执行方 |
|---------|--------|
| 下载/抓取内容、git 操作、格式转换、发 TG 通知 | Python 脚本（代码） |
| 理解用户意图、翻译/总结内容、生成 wiki、语义质量判断 | LLM |

### 改动一：sop-tg-notify 改为纯 Python

删掉 Hermes 调用，直接读 `pipeline-context.json` 模板化格式化后发送。通知格式化不需要 LLM 推理。

### 改动二：wiki-build 加代码自检

```
生成页面
  → 代码自检（无 LLM）：
      ✓ 必填 frontmatter 字段存在
      ✓ sources 引用文件真实存在
      ✓ wikilink >= 2
      ✓ 中文比例 >= 健康契约阈值
  → 通过 → commit
  → 不通过 → LLM 修正 → 再检（最多 2 轮）
  → 仍不通过 → commit 并标记 self_check: failed
```

### 改动三：sop.yaml 增加 health 块

```yaml
health:
  stages:
    wiki-build:
      timeout_minutes: 25
      done_pattern: "stage-c done"
    tg-notify:
      timeout_minutes: 3
      done_pattern: "stage-d done"
  evaluate:
    min_chinese_ratio: 0.30
    min_score: 0.65
    semantic_focus: "翻译质量、中文流畅性、核心概念覆盖"
    failure_modes:
      - symptom: self_check_failed
        confidence: high
        action: alert
      - symptom: semantic_score < 0.5
        confidence: low
        action: alert
```

guard 读 `health.stages` 的 timeout，evaluate 读 `health.evaluate` 的规则，统一数据源。

### 改动四：evaluate 变为通用语义引擎

从 webhook payload 读 `health.evaluate` 配置，不再硬编码任何业务逻辑。检查 `self_check: failed` 后只做语义判断，语义问题一律告警人工（不自动 re-trigger，语义根源太模糊）。

### 改动五：pipeline-creator 生成健康契约

SKILL.md 增加推理步骤：创建新 pipeline 时必须回答四个问题（见 Q4），生成完整 `health` 块写入 sop.yaml，failure_modes 初始标记 `draft: true`。

### 明确不做的事

| 不做 | 原因 |
|------|------|
| Reflection Agent | 需要 50+ 次运行数据，现在建是空转 |
| failure_modes 自动学习 | 依赖 Reflection Agent，一起推迟 |
| 语义失败自动 re-trigger | 根源模糊，自动重跑大概率浪费 token |

### 实现顺序

```
第一步（1-2天）  sop-tg-notify 改纯 Python
第二步（3-4天）  wiki-build 加代码自检 + sop.yaml health 块 schema
第三步（1-2天）  evaluate 重构为通用语义引擎 + guard 读 health 配置
第四步（1天）    pipeline-creator 加健康契约推理步骤
```

---

**核心判断**：方向正确，但建设顺序反了。应该先让基础 pipeline 的每一步足够可靠，再往上加智能层。现在是智能层已经三层了，基础还在靠补丁维持。Reflection Agent 等数据成熟再建，不要为未来的学习需求提前建基础设施。
