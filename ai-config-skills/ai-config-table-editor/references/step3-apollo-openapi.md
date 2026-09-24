# 第 3 步：通过 OpenAPI 更新 Apollo 配置

## 环境与配置

通过环境变量注入，不在文档/代码中硬编码：

- `APOLLO_PORTAL_URL`：Portal/OpenAPI 根地址（如 `http://<apollo-host>:<port>`）
- `APOLLO_APP_ID`：目标 AppId
- `APOLLO_ENV`：环境（如 `DEV`）
- `APOLLO_CLUSTER`：集群（如 `default`）
- `APOLLO_OPERATOR`：门户中的真实用户名
- `APOLLO_TOKEN`：该 App 的 OpenAPI Token

命名空间通常采用 `properties` 格式，通常只有一个键 `content`，值为一段 JSON 文本。

非 `Conf*` 前缀的命名空间（如人工测试命名空间）不参与自动同步。

## 命名空间匹配规则

- 上传目标 = 生成 JSON 的文件名去掉 `.json`：`ConfShop.json` → 命名空间 `ConfShop`。
- 在目标 App 的环境/集群下查找同名命名空间：
  - 找到：更新该命名空间的 `content` 键（已有键用 PUT）。
  - 找不到：停下并向用户反馈缺失的命名空间，**不自动创建、不改名**。
- 原因：Apollo 不支持重命名命名空间，且命名空间被服务器配置引用，不能随意变更名称。

## 令牌

- 请求头：`Authorization: <token>`。
- 令牌在 Apollo 门户创建，作用域为单个 AppId。
- 不要把它写进 SKILL.md、代码或日志明文；优先从环境变量（例如 `APOLLO_TOKEN`）或受控本地文件读取。

## 发现与读取

1. 查看 App 的环境/集群：

   `GET /openapi/v1/apps/{appId}/envclusters`

2. 列出命名空间：

   `GET /openapi/v1/envs/{env}/apps/{appId}/clusters/{cluster}/namespaces`

3. 读取某个命名空间的条目：

   `GET /openapi/v1/envs/{env}/apps/{appId}/clusters/{cluster}/namespaces/{namespace}/items`

   返回分页对象；`total=0` 表示尚无条目。

## 写入

请求头均为 `Content-Type: application/json;charset=UTF-8`。

- 创建新键（命名空间为空或键不存在）：

  `POST .../namespaces/{namespace}/items`

  Body：`{"key":"content","value":"<json 文本>","comment":"<备注>","dataChangeCreatedBy":"<operator>"}`

- 更新已有键：

  `PUT .../namespaces/{namespace}/items/content`

  Body：`{"key":"content","value":"<json 文本>","comment":"<备注>","dataChangeLastModifiedBy":"<operator>"}`

### 常见坑

- 400 `key and dataChangeLastModifiedBy can not be empty`：Body 缺少操作者字段。
- 400 `user not exists for userName:xxx`：操作者必须是门户中的真实用户。
- 404 `item not found ... itemKey:content`：键不存在时不能用 PUT，应改用 POST 创建。

## 发布边界

- Apollo 存在 release 类接口（如 `POST .../releases`），本技能流程默认禁止调用。
- 保存条目不等于生效：客户端读取的是已发布版本。自动更新后必须停在发布前，由用户到门户检查并手动发布。
- 术语约定：用户说“发布到 Apollo / 同步到 Apollo”通常只是指“提交/更新条目”，不是调用 release。请求中出现“发布”字眼时仍默认按提交处理；只有用户明确要求“真正发布/调用发布接口/让配置生效”才调用发布接口。

## 发布状态核验（实测可用）

可用接口：

`GET /openapi/v1/envs/{env}/apps/{appId}/clusters/{cluster}/namespaces/{namespace}/releases/latest`

返回最新一次发布的 `id`（releaseId）、`name`、`comment`、发布人与 `configurations`（该次发布的内容快照）。

不可用的接口（不要浪费时间）：

- `GET .../namespaces/{namespace}/releases`（发布列表）通常返回 400 `Request method 'GET' not supported`；
- `.../items/{key}/commits`、`.../commits` 等提交历史接口返回 404；
- 门户页面接口需要登录态 cookie，OpenAPI Token 用不了。

**所以 OpenAPI 看不到历史，只能看到"最新一次发布"和条目的最后修改时间/修改人。** 需要历史只能靠门户的发布历史页或外部记录（操作日志）。

判断某个命名空间是否有“未发布的草稿改动”：

1. `GET .../namespaces/{namespace}/items`，取 `key=content` 的 `value`（草稿）；
2. `GET .../namespaces/{namespace}/releases/latest`，取 `configurations.content`（已发布快照）；
3. 逐字比较：完全相同 → 草稿已生效；不同 → 存在未发布改动；`releases/latest` 报错 → 该命名空间从未发布过。

注意点：

- 用 `releases/latest.id` 作为“发布 ID”写进日志，便于事后追溯；`release.name` 是发布时填写的备注名。
- `dataChangeCreatedTime` 是发布发生的时间；条目的 `dataChangeLastModifiedTime` / `dataChangeLastModifiedBy` 才是草稿最后一次修改的时间与人。两者要分开看。
- 操作者字段常是 OpenAPI 用的账号（如 `apollo`），**用它区分不出“是谁”**：门户界面操作会记录各自的用户名，接口/脚本操作则统一是 token 所属账号。

## 校验

- 修改前先 GET 记录原值，便于回滚。
- 写入后 GET 读回，比对 value 与提交内容完全一致再向用户报告。

## PowerShell 参考

```powershell
$headers = @{ Authorization = $env:APOLLO_TOKEN }
$base = "$env:APOLLO_PORTAL_URL/openapi/v1"
$appId = $env:APOLLO_APP_ID
$envName = $env:APOLLO_ENV
$cluster = $env:APOLLO_CLUSTER
$operator = $env:APOLLO_OPERATOR

# 已有 content 键时使用 PUT
$body = @{
  key                      = 'content'
  value                    = $contentText   # 从生成的服务端 JSON 读取
  comment                  = 'synced from xlsx'
  dataChangeLastModifiedBy = $operator
} | ConvertTo-Json

Invoke-RestMethod -Uri "$base/envs/$envName/apps/$appId/clusters/$cluster/namespaces/ConfShop/items/content" `
  -Headers $headers -Method Put -ContentType 'application/json;charset=UTF-8' -Body $body
```

更完整的可复用脚本见 `../scripts/update_namespace.ps1`。
