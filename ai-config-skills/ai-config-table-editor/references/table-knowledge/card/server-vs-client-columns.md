# Card：列标记（服务端 / 客户端）与回报约定

> 2026-09-23 用实际导出产物实证。这一页解决一个反复出现的问题：改了表，导出后服务端 JSON 一字不变，用户误以为已经生效。

## 标记语义

表头第 1 行是每列的类型标记，决定该列进不进服务端 JSON：

| 标记 | 含义 | 去向 |
| --- | --- | --- |
| `cs` | 服务端 + 客户端 | 进 `Tool\configs\json\ConfX.json`（上传 Apollo 用的那份），也进 `json\client\` |
| `s` | 仅服务端 | 只进服务端 JSON |
| `c` | 仅客户端 | **不进 Apollo**，只进客户端 JSON |

实证例子：

- `TableBackground_桌背景.xlsx` 第 1 行 = `cs cs cs cs c c c c c c`：服务端 JSON 只含 `sn / name / desc / img`；`tableImg / preImg / cardtableIcon / hexselectIcon / specialIcon1 / specialIcon2` 只在客户端。
- `PayPoint_支付点.xlsx` 第 1 行 = `cs cs s s s`：`Price` 双端，`chargeType / platform / payPoint` 仅服务端。
- `GM配置.xlsx` 第 1 行全为 `c`：整表不产服务端 JSON，Apollo 里没有也不应有 `ConfGM` 命名空间。

## 回报约定（2026-09-23 用户确认）

每次改表完成后，除了说明改了哪张表哪一格，**必须额外说明本次改动落在客户端列还是服务端列**：

- 全是服务端列：说明会同步到 Apollo 草稿；
- 含客户端列：明确指出"这几列不会进 Apollo，需要走客户端配置渠道"；
- 全是客户端列：明确说明"本次不产生 Apollo 变更"。

## 判断方法

导出后比对 `Tool\configs\json\ConfX.json` 是否变化即可；也可用 `work\compare_json_to_apollo.ps1` 逐命名空间比对本地导出与 Apollo 草稿。
