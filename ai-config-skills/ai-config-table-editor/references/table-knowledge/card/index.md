# Card 表格知识库索引（项目：Configs/Card）

> 本目录规则仅适用于 Card 项目（`Configs\Card`），不得与 SuperChameleon（`Configs\SuperChameleon`）混用。

记录表字段语义与表间依赖。维护方式：按实际需求增量收录；每条规则必须经用户确认，标注确认日期与依据，不臆测。

## 通用检查规则（2026-09-03 用户确认）

- 阅读配置表时关注资源类字段：`icon`、`img`、`url`、`avatar`、`banner` 等链接字段。
- 同一资源 URL 出现在不同条目（同表不同 sn，或跨表）时，必须提醒用户；多数是临时占位资源，但也存在正常复用（同一商品的不同时长/数量变体共用图标），需结合条目语义判断，不直接当错误。
- 已知占位（2026-09-03 全表扫描）：
  - `TableBackground`：13 个背景行全部共用 `default.jpg`。
  - `Item` ddCard 段：竞技场/牌背（sn 40001~41003）共用坏笑 emoji 图，占位。
  - `CardBackground`：13 行与 `Emotion` 图片完全同源，属占位/冗余数据，真源以 `Emotion` 为准。

## 已收录

- [conf-item-shop.md](conf-item-shop.md)：Item（道具表）↔ Shop（商城表），2026-09-03 确认。
- [itemcard-gift.md](itemcard-gift.md)：ItemCard（棋牌道具）与 Gift 礼包内容物引用，2026-09-03 确认。
- [pass.md](pass.md)：通行证体系 Pass / PassReward / PassTask，2026-09-03 确认。
- [bond-handranking-audios.md](bond-handranking-audios.md)：Bond ↔ HandRanking（type↔sn）与音效引用 Audios，2026-09-03 确认。
- [gameend-goldroom.md](gameend-goldroom.md)：GameEndReward.GoldSn → GoldRoom.sn，2026-09-17 确认。
- [oss-assets.md](oss-assets.md)：图片/资源上传到 OSS 的路径约定与上传规则，2026-09-18 用户确认。
- [midautumn-event.md](midautumn-event.md)：中秋活动三表（活动/排行奖励/活动商店）依赖与配置，2026-09-21 确认。
- [server-vs-client-columns.md](server-vs-client-columns.md)：列标记 `cs` / `s` / `c` 的语义，以及"改表后必须回报客户端列"的约定，2026-09-23 用户确认。
- [decorations-paypoint-banner-gm.md](decorations-paypoint-banner-gm.md)：装饰物名称↔Item、支付点档位一致性、排名活动 Banner 时间校验、GM 配置唯一性，2026-09-23 用户确认。
- [activity-id-system.md](activity-id-system.md)：活动/赛事编号体系（1000n/2000n/3000n）、RankActivity 与 Banner 的引用关系、rankactivity#1 与 rankbanner#5，2026-09-24 确认。
- [item-sn-segments.md](item-sn-segments.md)：Item.sn 分段约定、Item.type 与装饰物表的对应、sn 作为展示顺序的语义，2026-09-24 确认。
- [hextech.md](hextech.md)：海克斯表的 `isUsed` 其实是「权重」这一字段陷阱，2026-09-24 记录。

## 全量扫描候选（注释+数值已核，尚未建页/按需确认）

- GoldRoom.Room → Room.sn
- PassTask.taskID → Task.sn
- Match.rankRewardGroup → MatchRankReward.rankListRewardGroup
- Match.activeRewardGroup → MatchActiveReward.activeRewardGroup
- RankActivity.rankListRewardGroup → RankActivityRewardGroup.rankListRewardGroup
- 各奖励表 rewardID / steamRewardID → Item.sn（含赛事活跃、赛事排名、排行活动奖励组、通行证奖励）
- Match 的 5 个 *Text 字段 → Str.sn（文本表）
- Pass.awardGroupId → PassReward.rewardGroup；Pass.taskGroupId → PassTask.taskGroup
- Pass.award / steamAward → Item.sn

## 待确认（遇到时先问用户）

- RankActivityBanner.matchID 的活动段（type=1）
- RankActivity.activitySn 与 Activity/Match 的关系
- PassTask.steamtaskID 是否指向本地 Task 表
