# Card：中秋活动（MidAutumnActivity / MidAutumnRank / MidAutumnShop）

源文件与产物：

- `MidAutumnActivity_中秋活动.xlsx`（sheet `中秋活动|MidAutumnActivity`）→ `ConfMidAutumnActivity.json`
- `MidAutumnRank_中秋活动排行奖励表.xlsx`（sheet `中秋活动排行|MidAutumnRank`）→ `ConfMidAutumnRank.json`
- `MidAutumnShop_中秋活动商店表.xlsx`（sheet `中秋活动商店|MidAutumnShop`）→ `ConfMidAutumnShop.json`

## 主从关系

```
MidAutumnActivity.shopGroupId → MidAutumnShop.shopGroupId
MidAutumnActivity.rankGroupId → MidAutumnRank.rankListRewardGroup
MidAutumnShop.rewardId        → Item.sn
```

## 已确认规则（2026-09-21 用户确认）

1. **midautumn#1**：`MidAutumnActivity.shopGroupId` 必须存在于 `MidAutumnShop.shopGroupId`。
2. **midautumn#2**：`MidAutumnActivity.rankGroupId` 必须存在于 `MidAutumnRank.rankListRewardGroup`。
3. **midautumn#3**：`MidAutumnShop.rewardId` 必须存在于 `Item.sn`。
4. **midautumn#4** 时间顺序：
   - `startTime <= endTime <= shopEndTime`
   - `rankAwardStartTime <= rankAwardEndTime`
   - `rankAwardStartTime >= endTime`
   - `rankAwardEndTime <= shopEndTime`

> 活动商店的名称不强制等于 Item 名称（如「中秋竞技场背景」对应 Item desc「月圆中秋」），只校验 rewardId 存在性。

## 当前配置（2026-09-21）

活动（sn=30001，名称：中秋活动）：

| 字段 | 值 |
|---|---|
| startTime | 2026-09-24 16:00:00 |
| endTime | 2026-10-01 23:59:59 |
| shopEndTime | 2026-10-05 23:59:59 |
| rankAwardStartTime | 2026-10-02 00:00:00 |
| rankAwardEndTime | 2026-10-05 23:59:59 |
| rankAward | 200,100,50,50（对局排名 1/2/3/4 名获得月饼） |
| dailyCount | 5（每日有效对局数） |
| rankCapacity | 100（排行榜容量/发奖名次） |

活动商店（shopGroupId=30001，价格单位为月饼）：

| rewardId | 名称 | 价格 | 限购 |
|---|---|---|---|
| 40014 | 中秋竞技场背景 | 1888 | 1 |
| 41003 | 中秋卡牌背景 | 1288 | 1 |
| 10003 | 加分卡 | 88 | 20 |
| 10004 | 保分卡 | 68 | 20 |
| 10005 | 祝福刷新卡 | 48 | 20 |
| 10006 | 初始牌刷新卡 | 48 | 20 |
| 1009 | 糖果*100 | 188 | 10 |
| 258 | 狼人杀加时卡 | 158 | 10 |
| 259 | 狼人杀抢身份卡 | 98 | 10 |
| 1008 | 糖果*10 | 28 | 999 |

新增 Item 捆绑行：`1008`（10糖果，num=10）、`1009`（100糖果，num=100），基于 Item 1007「糖果」同款字段。

排行奖励表：8 档覆盖 1–100 名（1 / 2-3 / 4-10 / 11-20 / 21-30 / 31-50 / 51-70 / 71-100），本轮保持原模板数值不变（文档未给出新数值）。

## 备注

- “仅消耗体力的对局可获得月饼、挂机判定无效（逻辑同糖果）”为服务端逻辑，三张表没有对应字段。
- 中秋竞技场背景 = Item 40014（TableBackground sn14）；中秋卡牌背景 = Item 41003（CardBackground sn3）。
