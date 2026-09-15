# SuperChameleon：Gift 与 Exchange

## Gift_礼包.xlsx（sheet `礼包|Gift`）

- `giftItem` 格式：`道具sn:数量,道具sn:数量`
- 已确认（2026-09-15）：`Gift.giftItem` 的 id 指向 **Item.sn**
  - `31:18` → Item 31（预言未来）
  - `32:60` → Item 32（辉耀守护）
  - 当前取值 {31,32}，全部命中 Item.sn。
- ⚠️ 与 Card 项目不同：Card 的 `Gift.giftItem` 指向 `ItemCard.sn`（体力/糖果），**禁止套用**。

## Exchange_兑换.xlsx（sheet `兑换|Exchange`）

- 已确认（2026-09-15）：`Exchange.id ⊆ Item.sn`，当前 6 条全部命中：
  - 1001→100秀券、1002→200秀券、1003→1000秀券、1004→2000秀券、1005→5000秀券、1006→10000秀券（Item.title 为对应名称）。
- 字段：`sn`（行序）、`id`（Item.sn）、`costs`（数值，业务含义待确认：兑换价或兑换数量）。
