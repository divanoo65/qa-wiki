---
created: 2026-05-09
updated: 2026-05-09
type: guide
tags: [schema, wiki, knowledge-management, youtube-research]
---

## 0. 目标与边界

> 核心目标：将 YouTube 视频内容转化为**可复利、可游走、可审计**的知识图谱。
> 衡量标准：从任意一个节点出发，沿 wikilinks 至少可以游走 3 步不断链。

- `raw/` 是唯一事实来源，**只读不改**。
- 知识层维护仅在 `wiki/`、`index.md`、`log.md` 内进行。

---

## 1. 三层模型（强约束）

### L1 事实层
- 只写入可由 `raw/notebooklm-analysis/` 直接支持的事实。
- 每条关键断言必须能回溯到具体的 source 页。
- **禁止把推测写成事实。**

### L2 推断层
- 基于 2 个以上 L1 事实的归纳或跨视频综合。
- 必须标注：`confidence: high|medium|low` + `reasoning: 推理依据（一句话）`
- 典型场景：某个趋势在多个视频中反复出现，可以 L2 归纳。

### L3 问题层
- 记录尚未被现有视频回答的问题、假设、证据缺口。
- 指导下一轮视频选题，不作为既定事实。

---

## 2. 目录结构

| 目录 | 用途 | 命名规范 |
|------|------|--------|
| `raw/youtube-links/` | 输入的 YouTube 链接文件 | `{video-id}.md` |
| `raw/notebooklm-analysis/` | NotebookLM 生成的研究报告（只读）| `{中文标题}.md` |
| `raw/notebooklm-mindmaps/` | NotebookLM 生成的思维导图（只读）| `{中文标题}.json` |
| `wiki/sources/` | 每个视频的来源摘要页 | `{中文标题}.md` |
| `wiki/entities/` | 人物、产品、组织、AI 模型 | `{实体名}.md`（小写 slug）|
| `wiki/concepts/` | 技术方法、框架、行业趋势 | `{概念名}.md`（中文可直接用）|
| `wiki/comparisons/` | 两个或多个实体/方案的对比分析 | `{A}-vs-{B}.md` |
| `wiki/overview/` | 跨视频的主题综合分析 | `{主题名}.md` |
| `wiki/queries/` | 重要问答沉淀 | `{问题-slug}.md` |

---

## 3. Frontmatter 规范（必填字段）

```yaml
---
title: 页面标题（必填）
type: source|entity|concept|comparison|overview|query
tags: [tag1, tag2]
summary: 一句话核心内容
sources: [raw/notebooklm-analysis/xxx.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
layer: L1|L2|L3
confidence: high|medium|low  # L2/L3 必填
reasoning: 推理依据           # L2/L3 必填
---
```

**硬性约束：** `title/type/tags/summary/sources/layer` 缺一不可。

---

## 4. 五种页面类型规范

### 4.1 Source 页（`wiki/sources/`）
**每个视频必须有且仅有一个 source 页。**

必须包含：
- 视频元数据（标题、URL）— 直接从报告 frontmatter 的 `video_url` 字段读取
- 脑图引用（`mindmap` 字段 + 正文链接）— 从报告 frontmatter 的实际磁盘文件名获取
- 执行摘要（3-5 句，核心价值主张）
- 核心要点（5-10 条，具体而非泛泛）
- 关键引言（原话 + 背景分析）
- 关联实体：`[[实体名]]`（凡在视频中提到的关键实体）
- 关联概念：`[[概念名]]`（凡在视频中介绍的核心概念）

### 4.2 Entity 页（`wiki/entities/`）
**只为在本库视频中有实质性描述的实体创建页面。**

必须包含（每项都要实质内容，不允许空洞占位）：
- **基本定位**：一句话，包含开发者/来源/核心价值
- **核心特征/能力**：≥5 条，每条具体描述功能或技术实现，不是泛泛标签
- **应用场景**：列举 2-3 个在本库视频中提到的具体使用场景
- **关系网络**：与其他实体的关系（`[[wikilink]]`，≥2 条），说明关系类型（竞争/依赖/开发者等）
- **关键事件/里程碑**：如发布日期、重要更新、争议事件（如有）
- **出现的视频来源**：`[[source页标题]]`，≥1 条

### 4.3 Concept 页（`wiki/concepts/`）
**提取标准：每个视频至少提取4-5个概念，覆盖：核心架构概念、安全/安全模型名称、部署方案、交互机制、性能指标等维度。不只提取最显眼的概念，也要提取视频中有详细描述的技术细节概念。**

**⚠️ 禁止提炼通用行业常识型概念：**
以下类型的概念即使在视频中被提及，也**不得**创建独立页面，因其是行业公知，对本知识库无增量价值：
- 通用 AI/ML 术语：思维链（Chain of Thought）、检索增强生成（RAG）、微调（Fine-tuning）、向量数据库、注意力机制等
- 通用软件工程概念：API、Docker、Git、缓存、负载均衡等
- 泛泛的方法论词汇：最佳实践、迭代、模块化等

**只提炼视频中有独特视角、具体实现或新命名的概念。** 判断标准：如果这个概念在视频之外也能搜到完整定义且视频没有补充新内容，则不创建。

必须包含（内容要有深度，不允许空洞定义）：
- **定义**：精确，不超过 3 句，包含关键技术细节
- **在本库的具体例子**：必须引用具体视频/实体/代码路径/数据
  - ✅ `在 [[hermes-agent]] 中，程序化知识存储在 ~/.hermes/skills/ 目录下，通过 skill_manage 工具管理`
  - ❌ `该概念在多个视频中均有体现`（太泛泛，不合格）
- **技术实现细节**：如何实现/工作原理的 1-2 个关键细节
- **与近似概念的边界**：区分此概念与容易混淆的相邻概念
- **关联概念**：`[[xxx]]`（≥2 条）
- **关联实体**：`[[xxx]]`（≥1 条）

### 4.4 Comparison 页（`wiki/comparisons/`）
**触发条件：同一视频或不同视频中，两个实体被直接对比时，必须创建。**

必须包含：
- 对比维度表格（维度 | A | B）
- 核心差异分析
- 适用场景结论
- 双向链接到被比较的 entity 页：`[[实体A]]` `[[实体B]]`

### 4.5 Overview 页（`wiki/overview/`）
**触发条件：同一主题的 source 页达到 2 个或以上时，必须创建或更新。**

必须包含：
- 主题范围与边界
- 跨视频综合发现（L2 推断，附 reasoning）
- 开放问题/L3（指导后续视频选题）
- 引用所有相关 source 页：`[[source1]]` `[[source2]]`

---

## 5. 链接健康规则（硬性约束，每次构建必须执行）

1. **死链检测**：扫描所有 `[[wikilink]]`，确认目标文件存在。
   - 目标文件不存在 → 立即创建该页面，或删除该链接
   - **禁止带死链提交**

2. **孤立页检测**：每个 wiki 页面至少被 1 个其他页面引用。
   - 孤立页在 log 中记录，下次构建时处理。

3. **Sources 字段验证**：`sources:` 列出的文件必须真实存在于 `raw/`。

4. **脑图关联验证**：source 页的 `mindmap` 字段指向的 `.json` 文件必须存在于 `raw/notebooklm-mindmaps/`。

---

## 5.5 脑图（Mindmap）利用规范

每个分析报告对应一个 mindmap.json，包含结构化的知识关系（节点 + 边）。**Stage C 应主动利用脑图数据**，而不只是存文件引用。

**如何利用脑图：**
1. 读取 `raw/notebooklm-mindmaps/{同名}.json`，提取节点列表和边（关系）
2. 在对应 source 页的正文中，增加"脑图核心节点"小节，列出脑图的一级节点
3. 在 entity 页中，如果脑图中有该实体相关的关系边，补充"知识图谱关系"小节
4. 新发现的概念节点（脑图中有但正文没有涵盖的）可以补充创建 concept 页

**脑图 JSON 格式参考（notebooklm 输出的典型结构）：**
```json
{
  "title": "...",
  "nodes": [{"id": "n1", "label": "核心概念"}],
  "edges": [{"source": "n1", "target": "n2", "label": "包含"}]
}
```

---

## 6. 增量构建工作流（执行顺序不可调换）

**Step 1 — 定向阅读**
```
读 TheSchema.md → 读 index.md → 读 log.md（最近 10 条）
```

**Step 2 — 处理每个新报告**
1. 创建/更新 source 页（每视频一个，唯一）
2. 创建/更新 entity 页（查 index 确认是否已存在，存在则更新不重建）
3. 创建/更新 concept 页（同上）
4. **检查 comparison 触发**：本视频是否有两个实体直接对比？→ 创建 comparison 页
5. **检查 overview 触发**：同主题 source 页是否已有 2+ 个？→ 创建或更新 overview 页

**Step 3 — 链接健康检查**
扫描所有新建/修改页面的 wikilinks，修复死链。

**Step 4 — 更新 index.md 和 log.md**
- index.md：按 type 分类，字母序，每条带 summary，更新 Last updated 和总页数
- log.md：追加本次运行记录（run_id、新增文件列表）

**Step 5 — 质量核查（必须全部通过再提交）**
- [ ] 每个新页面 frontmatter 6 个必填字段齐全
- [ ] 每个新页面至少 2 个有效出链 wikilinks（目标文件存在）
- [ ] source 页内容 ≥ 400 字
- [ ] entity/concept 页内容 ≥ 200 字
- [ ] sources 字段文件存在于 raw/
- [ ] 无死链

**Step 6 — 提交**
```bash
git add wiki/ index.md log.md logs/
git commit -m "chore: update llm wiki graph [run:{run_id}]"
git push origin main
```

---

## 7. 命名规范

- **raw 分析文件**：直接用中文语义标题，不加 video_id 前缀
  - ✅ `零成本本地AI-Agent部署指南.md`
  - ❌ `Kh8tGD5liwo-零成本本地AI-Agent部署指南.md`
- **wiki 文件**：同上，语义化中文名
- **内链**：`[[文件名（不含扩展名）]]` 或 `[[文件名|显示文字]]`
- 所有内容使用**中文**，frontmatter 字段名用英文

---

## 8. Telegram 通知格式（Stage C 成功 push 后发送）

```
[YOUTUBE-WIKI-RUN]
run_id: {run_id}
新增 source: {n} 个 — {标题列表}
新增 entity: {n} 个 — {名称列表}
新增 concept: {n} 个 — {名称列表}
新增 comparison: {n} 个（如有）
新增 overview: {n} 个（如有）
commit: {hash}
log: logs/webhook-runs/{run_id}.md
```
