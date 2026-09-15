---
name: ai-config-table-editor
description: 将表格维护的配置同步到 Apollo 配置中心：按需求修改表格、生成 JSON、按 JSON 文件名匹配同名的 Conf* 命名空间并通过 OpenAPI 更新草稿。默认不自动发布、不新建或改名命名空间，适用于以 content 键存放 JSON 的 Conf* 命名空间。
---

# Apollo Config Sync

把“表格驱动的配置”同步到 Apollo 的流水线：改表 → 导出 JSON → 用 OpenAPI 把 JSON 更新到对应命名空间的 `content` 键。

默认停在“提交/草稿”，**不自动调用发布接口**；确需发布时必须由用户明确要求，并按项目权限流程执行。

## 目录

- 第 0 步（需求分析与方案确认）：见下文“第 0 步”章节
- 第 1 步（改表）：[references/step1-table-guide.md](references/step1-table-guide.md)
- 第 2 步（生成 JSON）：[references/step2-export.md](references/step2-export.md)
- 第 3 步（更新 Apollo）：[references/step3-apollo-openapi.md](references/step3-apollo-openapi.md)
- 表结构与依赖知识页：[references/table-knowledge/index.md](references/table-knowledge/index.md)

## 第 0 步：需求分析与方案确认（改表前必经）

收到自然语言需求后，先分析与检索，不直接动手：

- 检索知识页与当前表数据，确定涉及哪张/哪几张表及具体改动方式；
- 识别跨表联动、奖励/道具映射、导出与 Apollo 同步范围、源文件占用状态；
- 输出“方案卡”并等待用户确认，确认后再进入第 1 步改表。

方案卡至少包含：目标表、改动明细（表/行/列/旧值→新值）、影响面（关联表、是否同步 Apollo）、歧义点（附推荐默认）、后续动作（改表→校验→导出→同步）。

必须等待确认的场景：跨多张表、映射存在歧义、知识库未覆盖的新依赖、删除或覆盖已有数据、涉及特殊处理字段、任何需要额外权限的改动。

可直接执行（免确认）的场景：需求精确无歧义（如“某表某字段改为 N”），或用户明确说“直接改/不要问”。

## 第 1 步：按需求修改表格

执行前阅读 [step1-table-guide.md](references/step1-table-guide.md) 与知识页索引。

要点：

- 改表前先查依赖：确认目标表被谁引用、引用谁（见 `table-knowledge` 知识页）。
- 知识库按项目物理隔离（入口 `references/table-knowledge/index.md`）：Card 在 `table-knowledge/card/`，SuperChameleon 在 `table-knowledge/super-chameleon/`；**同名表不代表同规则，严禁跨项目套用**。
- 源表被 Excel 打开时不能安全地外部写入：先保存并关闭，或经 Excel 自身会话修改。
- 修改后必须跑一致性校验，全部通过再进入第 2 步导出。
- 遇到知识库未覆盖的表或新依赖：先分析和用户确认，确认后再补录规则；不臆测。

## 第 2 步：由表格生成 JSON

执行前阅读 [step2-export.md](references/step2-export.md)。

要点：

- 产物命名由 sheet 名决定：sheet 名 `中文|English` → 生成 `Conf{English}.json`，与文件名无关。
- 表头固定 4 行（类型标记/字段类型/中文注释/字段名），第 5 行起为数据。
- 修改后的表放入导出暂存区，再运行导出工具；不要使用带 `pause` 的批处理（会卡住自动化）。
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

> 测试命名空间等非 `Conf*` 前缀产物不参与自动同步；如出现无同名命名空间的产物，按“找不到即反馈”处理。

## 通用安全边界

- 令牌不硬编码、不写入 SKILL.md 或日志；从环境变量（如 `APOLLO_TOKEN`）或受控本地文件读取。
- “发布/同步到 Apollo”的默认含义 = 提交（更新条目，停在草稿/未发布状态），绝不调用 release 发布接口；即使请求词是“发布”，只要未明确说“真正发布/调用发布接口/让配置生效”，都按提交处理并提示用户手动发布。真正发布只允许在用户明确要求时执行，且涉及非 DEV 环境前先确认权限与影响面。
- 修改前记录原值，便于回滚。
- 涉及展示资源（icon/avatar/banner 等 URL）、steam 等敏感业务字段时，遵循项目约定：默认只做引用存在性检查，不臆测业务内容、不主动修改。
- 如果一次表格修改未涉及任何已固化的依赖规则，必须输出提醒：当前表格修改未被依赖覆盖，建议手动检查准确性。
