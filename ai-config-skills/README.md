# ai-config-skills

基于 AI 代理（Codex Skill）的“配置表格维护/同步”技能集合。

## 技能列表

### [ai-config-table-editor](ai-config-table-editor/)

AI 编辑游戏/业务配置表格并同步到 Apollo 配置中心：

- 改表：先查表结构与依赖规则；改表前检查 `~$` 锁文件（Excel 打开时外部写入会被覆盖）；改后校验并回报"改动落在服务端列还是客户端列"；
- 导出：sheet `中文|English` → `Conf{English}.json`；导出前先把源表同步进暂存区，避免用旧副本导出；
- 同步：按 JSON 文件名匹配同名 `Conf*` 命名空间，OpenAPI 更新 `content` 键；
- 边界：默认只提交（草稿），不自动调用 release；不新建/不改名命名空间；同步前先比对现状，不盲目用本地值覆盖线上；
- 校验与守护：一致性校验（表间依赖）、未提交改动守护（表改了没 git 提交会 FAIL）、漂移巡检（本地导出 vs Apollo 实际内容）、发布状态自动回填；
- 知识库：按项目隔离（`card/`、`super-chameleon/` 等子目录），同名表规则不可跨项目混用。

本仓库（上传版）中技能标识为 `ai-config-table-editor`；你本机已安装的本地版仍保留 `apollo-config-sync`，两者内容一致，可按需使用。

## 工作流

0. 需求分析与方案确认：先检索知识页与当前数据，输出“改哪张表、怎么改”的方案卡，用户确认后再执行。
1. 改表：先查 `references/table-knowledge/` 中的依赖规则；文件被 Excel 打开时不能安全写入；改完做一致性校验。
2. 导出：sheet 名形如 `中文|English` 时产物为 `Conf{English}.json`。
3. 更新 Apollo：按 JSON 文件名匹配同名 `Conf*` 命名空间，OpenAPI 更新 `content` 键（默认只提交不发布）。
4. 收尾：提交表格改动到配置仓库、写操作日志、跑漂移巡检确认本地与 Apollo 一致。

## 安装到 Codex

把 `ai-config-table-editor` 目录放到个人技能目录：

```text
~/.agents/skills/ai-config-table-editor/
```

或在 Codex 会话中通过 skill-installer 安装本仓库。

## License

[MIT](LICENSE) © 2026 Yin Hao
