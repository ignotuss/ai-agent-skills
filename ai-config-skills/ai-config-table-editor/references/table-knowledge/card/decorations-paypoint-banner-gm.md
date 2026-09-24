# Card：装饰物 / 支付点 / 排名 Banner / GM 配置

> 2026-09-23 用户确认，已固化进 `Card\Tool\_forAI\check_configs.py`。

## 一、装饰物名称 ↔ Item（decoration-item#1 / #2）

编号映射：

- `Item.sn` 在 **40001~40099** → 对应 `TableBackground.sn = Item.sn - 40000`（竞技场背景）
- `Item.sn` 在 **41001~41099** → 对应 `CardBackground.sn = Item.sn - 41000`（牌背）

规则：

- **#1** 对应的背景定义行必须存在；
- **#2** `Item.desc` 必须等于对应背景表的 `name`。

首跑（2026-09-23）发现 2 处既存不一致，**尚未处理，等用户定**：

| Item.sn | Item.desc | 对应行 | 问题 |
| --- | --- | --- | --- |
| 40002 | 夏日海滩 | TableBackground sn2 = 夏日沙滩 | 名称不一致（海滩 / 沙滩） |
| 40003 | 竞技场2 | TableBackground sn3 = 背景2 | 名称不一致（疑似占位数据） |

其余全部一致：40001 / 40014 / 40016、41001 / 41002 / 41003。

## 二、支付点 PayPoint（paypoint#1 / #2）

- **#1** `sn` 唯一；`payPoint` 非空且唯一。
- **#2** 各 `platform` 的 `Price` 档位集合必须一致。

背景：2026-09-23 本地支付点表一度只有 9 行（缺 68 元档 sn=10/11/12），而 Apollo 有 12 条；若盲目上传会删掉 3 个支付点。该规则可在上传前拦住这类"本地表缺行"的情况。

当前状态：platform 3 / 103 / 163 均为 6 / 18 / 30 / 68 四档，共 12 条。

## 三、排名活动 Banner（rankbanner#1 ~ #4）

- **#1** `sn` 唯一。
- **#2** 同一 `type` 内 `matchID` 唯一。
- **#3** `matchStartShowTime` 必须早于 `matchEndShowTime`。
- **#4** `type=3`（中秋）的 `matchID` 必须存在于 `MidAutumnActivity.sn`，且 `matchEndShowTime` 必须等于该活动的 `endTime` 或 `shopEndTime`。

背景：2026-09-23 之前中秋 banner 结束时间还是 `2026-12-31 10:00:00` 占位，与活动结束时间不一致；用户当天改为 `2026-10-05 23:59:59`（= 商店结束时间）。

注意：本表 `sn` 就是首页 banner 的展示顺序，重排 sn 属于**可见变更**。

## 四、GM 配置（gm#1）

- `sn` 唯一；`CMD` 非空且唯一；`Name` / `Desc` 非空。
- 整表列标记均为 `c`，属纯客户端配置，不产服务端 JSON、不进 Apollo。
