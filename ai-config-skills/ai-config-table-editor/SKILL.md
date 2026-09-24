---
name: ai-config-table-editor
description: 将表格维护的配置同步到 Apollo 配置中心：按需求修改表格、生成 JSON、按 JSON 文件名匹配同名的 Conf* 命名空间并通过 OpenAPI 更新草稿。默认不自动发布、不新建或改名命名空间，适用于以 content 键存放 JSON 的 Conf* 命名空间。
---

# AI Config Table Editor

把“表格驱动的配置”同步到 Apollo 的流水线：改表 → 导出 JSON → 用 OpenAPI 把 JSON 更新到对应命名空间的 `content` 键。

默认停在“提交/草稿”，**不自动调用发布接口**；确需发布时必须由用户明确要求，并按项目权限流程执行。

## 目录

- 第 0 步（需求分析与方案确认）：见下文“第 0 步”章节
- 第 1 步（改表）：[references/step1-table-guide.md](references/step1-table-guide.md)
- 第 2 步（生成 JSON）：[references/step2-export.md](references/step2-export.md)
- 第 3 步（更新 Apollo）：[references/step3-apollo-openapi.md](references/step3-apollo-openapi.md)
- 表结构与依赖知识页：[references/table-knowledge/index.md](references/table-knowledge/index.md)
- 可复用脚本：[scripts/](scripts/)

## 第 0 步：需求分析与方案确认（改表前必经）

收到自然语言需求后，先分析与检索，不直接动手：

- 检索知识页与当前表数据，确定涉及哪张/哪几张表及具体改动方式；
- 识别跨表联动、奖励/道具映射、steam 等敏感字段、Apollo 现状与 Excel 占用状态；
- 输出“方案卡”并等待用户确认，确认后再进入第 1 步改表。

方案卡至少包含：目标表、改动明细（表/行/列/旧值→新值）、影响面（关联表、是否同步 Apollo、是否动敏感字段）、歧义点（附推荐默认）、后续动作（改表→校验→导出→同步）。

必须等待确认的场景：跨多张表、映射存在歧义、知识库未覆盖的新依赖、删除或覆盖已有数据、涉及特殊处理字段、任何需要额外权限的改动。

可直接执行（免确认）的场景：需求精确无歧义（如“某表某字段改为 N”），或用户明确说“直接改/不要问”。

## 第 1 步：按需求修改表格

执行前阅读 [step1-table-guide.md](references/step1-table-guide.md) 与知识页索引。

要点：

- 改表前先查依赖：确认目标表被谁引用、引用谁（见 `table-knowledge` 知识页）。
- 知识库按项目物理隔离（入口 `references/table-knowledge/index.md`）：例如 `table-knowledge/card/`、`table-knowledge/super-chameleon/`；**同名表不代表同规则，严禁跨项目套用**。
- **改表前统一预检 Excel 占用**：存在 `~$<表名>.xlsx` 锁文件说明该表正被 Excel 打开。此时外部写入会失败；更糟的是——Excel 内存里是打开那一刻的旧版本，用户之后一保存就会把你的修改覆盖回去。发现占用必须先请用户保存并关闭。（锁文件可能是崩溃残留，所以策略是“提示 + 尝试写入，失败则硬停”。）
- 源表被 Excel 打开时不能安全地外部写入：先保存并关闭，或经 Excel 自身会话修改。
- **改表后必须回报“列去向”**：表头第 1 行的标记决定列进不进服务端 JSON —— `cs` 双端、`s` 仅服务端、`c` 仅客户端。客户端列的改动导出后服务端 JSON 一字不变、不会进 Apollo，必须明确提示“不会进 Apollo，需走客户端配置渠道”，否则用户会误以为已生效。
- 修改后必须跑一致性校验，全部通过再进入第 2 步导出。
- 遇到知识库未覆盖的表或新依赖：先分析和用户确认，确认后再补录规则；不臆测。
- 如果一次修改未涉及任何已固化规则，必须输出提醒：当前表格修改未被依赖覆盖，建议手动检查准确性。
- **表格改动必须提交到配置仓库**：配置仓库通常是独立 git 子模块。改表 → 校验 → 导出 → 同步 Apollo 完成后，必须在仓库内 `git add` + `git commit` 对应 xlsx；未提交的表改动会被子模块更新/拉取覆盖（真实发生过两次）。
- **导出前必须把源表同步进暂存区**，且只同步流水线内的表。暂存区里放旧副本会导致导出结果与最新表不符，进而误判“表与 Apollo 不一致”。

## 第 2 步：由表格生成 JSON

执行前阅读 [step2-export.md](references/step2-export.md)。

要点：

- 产物命名由 sheet 名决定：sheet 名 `中文|English` → 生成 `Conf{English}.json`，与文件名无关。
- 表头固定 4 行（类型标记/字段类型/中文注释/字段名），第 5 行起为数据。
- 先把改过的表同步进导出暂存区（同名覆盖），再运行导出工具；不要使用带 `pause` 的批处理（会卡住自动化）。
- 上传 Apollo 使用服务端 JSON（如有 client 副本，用途另见项目约定）。

## 第 3 步：更新 Apollo

执行前阅读 [step3-apollo-openapi.md](references/step3-apollo-openapi.md)。

要点：

- 先发现环境/集群/命名空间，确认目标存在且为空或已含 `content` 键。
- 目标命名空间 = 生成的 JSON 文件名去掉 `.json`；在 Apollo 中找不到同名命名空间时停下并反馈，不创建、不改名。
- 空命名空间用 POST 创建键；已有键用 PUT 修改。
- 操作者字段必须是门户中的真实用户名。
- 写入后读回校验 value 与提交内容一致。
- 默认只保存草稿，不调用发布接口；更新完停在此处，提示用户到门户确认并手动发布。
- 需要核对“到底发布了没有”时用 `GET .../namespaces/{ns}/releases/latest`（列表接口 `.../releases` 通常不可用），把草稿内容与发布快照逐字比较；详见 step3 的“发布状态核验”。

> 非 `Conf*` 前缀的命名空间（如人工测试命名空间）不参与自动同步；如出现无同名命名空间的产物，按“找不到即反馈”处理。

## 校验、守护与巡检

### 一致性校验

每个项目维护自己的校验脚本，规则与知识页同步。运行前建议确认“规则签名”存在——这类脚本被外部回退过，回退后校验会静默变空，产生“0 失败”的假象。

### 未提交改动守护

校验收尾时检查顶层 xlsx 是否有未提交的 git 改动，有则报 FAIL 并列出文件名。检查路径要**只匹配顶层表**（例如 `:(glob)<项目>/*.xlsx`），否则会把导出暂存区里的副本也算进来、天天误报。

### 漂移巡检

“表格里写的”和“Apollo 里跑的”是否一致。只读，见 `scripts/drift_check.py`：

```powershell
python scripts/drift_check.py --released --json-dir <服务端 JSON 目录>
```

- 默认比对本地导出的 `Conf*.json` 与 Apollo 草稿内容；`--released` 额外报告“草稿是否已发布”。
- 有漂移时退出码为 1，可直接用于流程判断。
- 常见漂移来源：有人在 Apollo 直接改没回写表格、表格被回退/覆盖、表格缺行、服务端多出占位数据、表格改了没同步。
- **前提**：只能查到流水线清单内的表；表不在清单里就查不到，问题会长期潜伏。
- 建议节奏：每天首次任务时跑一次，或发布前跑。

## 日志与发布状态

每次任务写一条日志（建议存项目本地、按天一个 `YYYY-MM-DD.jsonl`）：

- 字段建议：`logId / ts / operator / request / requestSummary / planCard / confirmResult / tableChanges / checks / export(含 sha256) / apollo(含 release 状态) / notUploaded / vcs / backups / status / pendingNotes`。
- 多段展开、如实记录；一条需求一条记录。
- 提交节奏：每天第一次任务结束后，把**昨天及更早**的日志提交一次；当天的日志留到次日（当天还会持续追加）。

发布状态三级：`confirmed`（有实证或用户确认已发布）、`assumedReleased`（无反馈推定）、`requested`（本流程真的调用了发布接口）。

**自动回填**：见 `scripts/backfill_release_status.py`。它读取所有未确认记录涉及的命名空间，用 `releases/latest` 比较草稿与线上版本：相同则回填 `confirmed=true` + `releaseId` + 证据，不同则保持待发布——不必再逐条问用户“发布了没有”。

## 通用安全边界

- 令牌不硬编码、不写入 SKILL.md 或日志；从环境变量（如 `APOLLO_TOKEN`）或受控本地文件读取。
- “发布/同步到 Apollo”的默认含义 = 提交（更新条目，停在草稿/未发布状态），绝不调用 release 发布接口；即使请求词是“发布”，只要未明确说“真正发布/调用发布接口/让配置生效”，都按提交处理并提示用户手动发布。真正发布只允许在用户明确要求时执行，且涉及非 DEV 环境前先确认权限与影响面。
- 修改前记录原值，便于回滚。
- 涉及展示资源（icon/avatar/banner 等 URL）、steam 等敏感业务字段时，遵循项目约定：默认只做引用存在性检查，不臆测业务内容、不主动修改。
- 本地表格可能落后于 Apollo（有人直接在 Apollo 上改过）。**同步前先比对现状**，不要把本地值盲目覆盖到线上；发现分叉先报告，由用户决定方向。
