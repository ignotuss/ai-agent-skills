# 表格知识库索引

> 本目录规则仅适用于 Card 项目，不得与其它项目（如 SuperChameleon）混用。

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

## 全量扫描候选（注释+数值已核，尚未建页/按需确认）

- GoldRoom.Room → Room.sn
- GameEndReward.GoldSn → GoldRoom.sn
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
