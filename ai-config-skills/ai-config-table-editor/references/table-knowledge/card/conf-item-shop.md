# Item（道具表）↔ Shop（商城表）

源文件与产物：

- `Item_道具.xlsx`（sheet `道具|Item`）→ `ConfItem.json`
- `shop_商城.xlsx`（sheet `商城|Shop`）→ `ConfShop.json`

## 字段要点

- `Item.sn`：全局唯一道具 ID（道具表主键），396 行无重复。
- `Item.id`：非唯一（id=1 有 17 行），语义复杂且历史遗留（用户确认不可考），不做唯一性校验。
- `Item.title`：分类名（如"表情""时装"），不是具体商品名。
- `Item.desc`：具体商品名（如"坏笑""像素女孩"）。
- `Shop.sn`：行序号，唯一。
- `Shop.rewardId`：允许重复（同一奖励可拆成多个销售条目，如 10001 两条）。
- `Shop.name`：商品名，应与 `Item.desc` 一致。

## 已确认规则（2026-09-03 数据验证 + 用户确认）

1. `Shop.rewardId` 必须存在于 `Item.sn`（61 条全命中）。
2. `Shop.name` 必须等于 `Item.desc` 或 `Item.title` 其中之一（2026-09-11 更新：卡类商品名放在 `Item.title`、详细说明放在 `Item.desc`；表情/时装/装扮/竞技场类则名称放在 `Item.desc`，`Item.title` 为分类名）。
3. type1=7（表情）：`Item.id` → `Emotion.sn`，且 `Item.desc` == `Emotion.desc` == `Shop.name`（9/9 通过）。
4. type1=8（时装）：`Item.id` → `Avatar.sn`，且名称一致（42/42 通过）。
5. 新增商城商品时不得直接发明 rewardId：必须先建 `Item.sn` 行，再在 Shop 中引用。

## 业务说明（2026-09-03 用户确认）

- type1=10（牌背）、type1=11（竞技场）：展示资源在 `icon` 链接路径下，目前是占位资源；不需要本地配置表存在对应行，也不做目录行校验。
- `CardBackground` 当前是占位数据；表情类配置以 `Emotion` 为真源。
- `Item.type` 的数字含义不可考（历史遗留代码），遇到具体取值时先根据实际情况给用户建议，由用户决定后再固化。
- `Shop.type2` 没有配套备注表（用户确认当前不存在）；只记录 0 = 无类别，其余枚举不猜测。
