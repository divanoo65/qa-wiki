# Harness Agent 架构设计问答精粹

**日期**: 2026-05-14
**主题**: Harness Agent 架构设计、Skill 编排、解耦原则

---

## Q1: Harness Agent 的本质是什么？

**问**: Harness Agent 就是 Agent 编排，这个理解对吗？

**答**: 方向对，但少了核心一层。Harness 的本质不只是编排，是**解耦**：

```
机制：虚拟化（标准化接口）
  ↓ 实现了
结果：解耦（Brain 和 Hands 互不依赖）
  ↓ 带来了
价值：可替换、可扩展、可靠性
```

类比操作系统：OS 对硬件虚拟化 → `read()` 命令不知道底层是磁带还是 SSD。Harness 对执行环境虚拟化 → Brain 不知道底层是本地还是云端沙盒。

---

## Q2: Skill 是什么？它和编排的关系是什么？

**问**: Skill 是固定原子流程节点，不可拆分，编排是对 Skill 的编排，这个理解对吗？

**答**: 完全正确。

- **Skill** = 原子固定工作流节点，封装固定逻辑，有输入有输出
- **编排** = Hermes Brain 在 Skill 之间做决策（顺序 or DAG）
- **编排不在 Skill 内部** —— Skill 内部是固定流程，不做条件分支决策

```
Brain（Hermes LLM）
  ↓ 编排
Skill A → Skill B → Skill C
  每个 Skill 是原子操作，Brain 决定顺序
```

---

## Q3: agent-brain-plugins 这个项目的定位是什么？

**问**: agent-brain-plugins 是为了持久化 Hermes Brain 产出的核心 SOP、Skill、结果？

**答**: 对，这正是它的定位：

| 持久化内容 | 说明 |
|-----------|------|
| SOP（sop.yaml） | Pipeline 流程定义，Brain 的编排蓝图 |
| Skill（SKILL.md + scripts） | Brain 可调用的能力单元 |
| Tool（tools/\*.py） | Skill 使用的原子数据获取函数 |
| Registry（registry.yaml） | 所有能力的目录，Meta-Agent 的"菜单" |

---

## Q4: 意图理解应该由谁负责？

**问**: Python 脚本用关键词解析意图，还是 Hermes LLM 理解意图？

**答**: **Hermes LLM 负责理解，Python 脚本负责执行。**

错误设计：
```python
# Python 用关键词匹配 → 脆弱，新指令必须改代码
if "翻译" in intent: action = "translate"
```

正确设计（SKILL.md 描述给 Hermes）：
```
你来分析 intent，判断用户要做什么：
- 想翻译 → 调 transform.py --action translate
- 想总结 → 调 transform.py --action summarize
- 想提炼核心 → 调 transform.py --action extract_key_points
```

Hermes 理解语义，Python 执行原子操作。

---

## Q5: 如何保证新增 Pipeline 不影响旧 Pipeline？

**问**: 每次新增 SOP，旧的 pipeline 是否绝对不受影响？

**答**: 是的，天然隔离，前提是：

1. 新 SOP 使用独立触发目录（`raw/github-links/` vs `raw/youtube-links/`）
2. Skill 只做加法，不修改现有 Skill 代码
3. Tool 是新文件，不修改现有 Tool

回滚机制：所有变更通过 git commit，出问题 `git revert` 即可。

---

## Q6: 为什么说关键词匹配是根本性错误？

**根本原因**：系统被设计成「URL 路由器」而非「意图路由器」。

设计的坏味道：
- `parse_intent_actions()` 接受 `intent` 参数但内部完全不用它
- `build_content()` 函数签名有 `intent` 但逻辑忽略它
- 测试只验证"pipeline 是否触发"，不验证"内容是否符合意图"

三个防范机制：
1. **意图契约**：每个处理意图的函数必须声明支持哪些动作
2. **动作先解析**：`parse_intent_actions()` 必须最先执行，actions 作为必传参数
3. **验收标准包含内容验证**：翻译意图 → 验证输出是中文

---

## Q7: Harness Agent 系统的完整架构是什么？

```
用户触发（webhook / TG / GitHub push）
  ↓
路由注册（Hermes webhook routes）
  ↓
Intent Router Agent
  → 理解意图（Hermes LLM）
  → 路由到正确 Pipeline
  ↓
Pipeline（sop.yaml 定义）
  Stage B: 研究/抓取（sop-notebooklm-research）
  Stage C: 内容变换（sop-content-transform）可选
  Stage D: 知识图谱构建（sop-wiki-build）
  Stage E: TG 汇总通知（sop-tg-notify）
  ↓
每个 Agent 自带：spawn 守卫 + TG 进度通知
  ↓
agent-brain-plugins 持久化产出
```
