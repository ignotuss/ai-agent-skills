# Apollo Config Sync

一个可复用的 Codex Skill：把“表格驱动的配置”同步到 Apollo 配置中心。

流程：按需求修改表格 → 生成 `Conf*.json` → 按 JSON 文件名匹配同名 `Conf*` 命名空间，通过 Apollo OpenAPI 更新 `content` 键。

默认边界（重要）：**只提交、不发布**。不会自动调用 release 类接口，也不会新建或改名命名空间。

## 目录结构

```text
ai-config-table-editor/
├── SKILL.md                        # 技能入口（Codex 加载说明）
├── README.md                       # 本说明
├── .gitignore                      # 忽略本地机密/日志/备份
├── agents/
│   └── openai.yaml                 # 展示用元数据
├── references/
│   ├── step1-table-guide.md        # 第 1 步：改表
│   ├── step2-export.md             # 第 2 步：生成 JSON
│   ├── step3-apollo-openapi.md     # 第 3 步：OpenAPI 更新 Apollo
│   └── table-knowledge/            # 多项目知识库：card/、super-chameleon/ 等，按项目隔离
└── scripts/
    └── update_namespace.ps1        # OpenAPI 更新脚本模板（不含发布）
```

## 工作流

0. 需求分析与方案确认：先检索知识页与当前数据，输出“改哪张表、怎么改”的方案卡，用户确认后再执行。
1. 改表：先查 `references/table-knowledge/` 中的依赖规则；文件被 Excel 打开时不能安全写入；改完做一致性校验。
2. 导出：sheet 名形如 `中文|English` 时产物为 `Conf{English}.json`；把改过的 xlsx 放入导出暂存区并运行导出工具。
3. 更新 Apollo：目标命名空间 = JSON 文件名去掉 `.json`；找不到同名命名空间时停下反馈，不自动创建、不改名。

## 配置

通过环境变量注入运行参数，令牌等机密不要写入仓库：

| 环境变量 | 说明 | 示例 |
|---|---|---|
| `APOLLO_PORTAL_URL` | Apollo Portal/OpenAPI 根地址 | `http://apollo.example.com:8080` |
| `APOLLO_APP_ID` | 目标 AppId | `my-server` |
| `APOLLO_ENV` | Apollo 环境 | `DEV` |
| `APOLLO_CLUSTER` | Apollo 集群 | `default` |
| `APOLLO_OPERATOR` | 门户中的真实用户名 | `apollo` |
| `APOLLO_TOKEN` | 该 App 的 OpenAPI Token | 不提交 |

本地表格路径请按项目实际替换（见 `references/step2-export.md`），本仓库统一使用占位符 `$CONFIG_XLSX_DIR` / `$EXPORT_STAGING_DIR` / `$EXPORT_GEN_DIR`。

## 在 Codex 中安装

- 放到个人技能目录：`~/.agents/skills/ai-config-table-editor`（Windows 为 `C:\Users\<you>\.agents\skills\ai-config-table-editor`），或
- 在 Codex 会话中通过 skill-installer 从本仓库路径安装。

## 发布边界

Apollo 中“保存条目”不等于生效，客户端读取的是已发布版本。因此：

- 用户说“发布/同步/提交到 Apollo”时，默认理解为**更新条目（提交草稿）**，不调用 release；
- 只有用户明确要求“真正发布 / 调用发布接口 / 让配置生效”时，才允许调用发布接口；
- 涉及非 DEV 环境前，先确认权限与影响面。

## 项目特定内容

`references/table-knowledge/` 中沉淀了本项目（游戏配置表）的表结构、依赖与已确认规则。若把本仓库用于其它项目或公开分发，请替换为自己的规则，或删除该目录并维护自己的知识页。

## License

MIT License，见仓库根目录 [LICENSE](../LICENSE)。
