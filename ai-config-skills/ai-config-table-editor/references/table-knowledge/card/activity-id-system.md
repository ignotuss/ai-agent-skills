# Card：活动 / 赛事编号体系

> 2026-09-24 用户确认。这一页解决的问题：某天发现 `RankActivity.activitySn=10004/10005` 在两台 Apollo 上对不上、也说不清归属。

## 编号规则

| 前缀 | 指向的表 | 换算 | 例子 |
| --- | --- | --- | --- |
| `1000n` | `Activity_活动.xlsx`（活动表） | `Activity.sn = n` | `10001` → 活动 1 |
| `2000n` | `Match_赛事表.xlsx`（赛事表） | `Match.sn = 2000n`（赛事表本身就用这个号） | `20001` → 赛事 20001 |
| `3000n` | `MidAutumnActivity_中秋活动.xlsx` | `MidAutumnActivity.sn = 3000n` | `30001` → 中秋活动 |

## 引用关系

```
RankActivity.activitySn ──► Activity.sn（1000n）或 Match.sn（2000n）
RankActivity.sn         =   activitySn（同值，见 2026-03 与 2026-09 数据）
RankActivity.rankListRewardGroup ──► RankActivityRewardGroup.rankListRewardGroup

RankActivityBanner.type=1.matchID ──► 同一个活动号（必须 == RankActivity.activitySn）
RankActivityBanner.type=2.matchID ──► Match.sn
RankActivityBanner.type=3.matchID ──► MidAutumnActivity.sn
```

## 已固化校验

- `rankactivity#1`：`RankActivity.activitySn` 必须落在已知编号段，且指向的活动/赛事真实存在。
- `rankbanner#4`：`type=3` 的 `matchID` 必须存在于 `MidAutumnActivity.sn`，且结束展示时间等于该活动的 `endTime` 或 `shopEndTime`。
- `rankbanner#5`：`type=1` 的 `matchID` 必须与 `RankActivity.activitySn` 一致。

## 已知未解问题（2026-09-24）

`RankActivity.activitySn = 10004` 指向 `Activity.sn = 4`，但**活动表里只有 sn=1、sn=2**。

- 三方已统一为 10004（本地 Apollo、目标 Apollo、`RankActivity_排行活动.xlsx`），但源头依据仍然缺失；
- `rankactivity#1` 因此**会持续报 FAIL**，这不是脚本误报，而是真实缺口；
- 需要配这个活动的人确认：是活动表缺行（应补 Activity sn=4），还是号本身写错了。

## 历史坑（避免重蹈）

`RankActivityBanner` 的 `matchID` 轨迹，两次跳号都没有留下原因：

| 时间 | 提交人 | 提交说明 | matchID |
| --- | --- | --- | --- |
| 2026-03-06 | Yanan LI | 表上传 | 10001 |
| 2026-05-28 | FengYMa | 赛事表更新 | **10002** |
| 2026-09-21 | shaoyikun-sQzze | **「1」** | **10005** |

2026-09-24 做跨实例全量复制时，本地是 10005、目标端是 10004，两边各自自洽但互不相同；导入把目标端改成 10005 后，10:12 又被人单点改回 10004。
**教训：改活动号必须在提交说明里写清依据**，否则事后无法追溯。
