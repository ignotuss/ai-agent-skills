# ItemCard（棋牌道具）与 Gift.giftItem

源文件与产物：

- `ItemCard_棋牌道具.xlsx`（sheet `棋牌道具|ItemCard`）→ `ConfItemCard.json`
- `Gift_礼包.xlsx`（sheet `礼包|Gift`）→ `ConfGift.json`

## ItemCard 现状

- 只有 2 行，是棋牌模块（dd成王）的基础货币/道具目录：
  - `sn=31`：体力（道具）
  - `sn=32`：糖果（货币）
- 字段注释缺失，仅 `sn/title/icon/type/desc`。

## 已确认规则（2026-09-03 用户确认）

1. `Gift.giftItem` 的表述格式为 `sn:数量`，多个内容用英文逗号分隔；其中的 `sn` 指 `ItemCard.sn`。
   - 例：`31:18,32:60` = 体力 ×18、糖果 ×60。
2. 校验规则：解析 `giftItem` 每段 `sn:数量`，`sn` 必须存在于 `ItemCard.sn`，数量为正数。当前 3 条礼包全部命中。

## 关联说明（棋牌语境）

- Item 的 ddCard 行中，`Item.id` 可能对应 ItemCard 等目录表的 `sn`（例：Item `sn=1007` 糖果的 `id=32` ↔ ItemCard `sn=32`）。
- 校验 `Item.id` 时必须限定 `propType=ddCard` 等棋牌语境，否则会与狼人杀等其他项目的同名 id 误报。
- ItemCard 有行不代表 Item 必须有行：`sn=31` 体力在 Item 中无对应条目，属正常（体力只作为礼包内容物出现）。
