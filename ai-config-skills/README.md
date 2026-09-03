# ai-config-skills

基于 AI 代理（Codex Skill）的“配置表格维护/同步”技能集合。

## 技能列表

### [ai-config-table-editor](ai-config-table-editor/)

AI 编辑游戏/业务配置表格并同步到 Apollo 配置中心：

- 改表：先查表结构与依赖规则，Excel 未关闭时不做外部写入，改后校验；
- 导出：sheet `中文|English` → `Conf{English}.json`；
- 同步：按 JSON 文件名匹配同名 `Conf*` 命名空间，OpenAPI 更新 `content` 键；
- 边界：默认只提交（草稿），不自动调用 release；不新建/不改名命名空间。

本仓库（上传版）中技能标识为 `ai-config-table-editor`；你本机已安装的本地版仍保留 `apollo-config-sync`，两者内容一致，可按需使用。

## 安装到 Codex

把 `ai-config-table-editor` 目录放到个人技能目录：

```text
~/.agents/skills/ai-config-table-editor/
```

或在 Codex 会话中通过 skill-installer 安装本仓库。

## License

[MIT](LICENSE) © 2026 Yin Hao
