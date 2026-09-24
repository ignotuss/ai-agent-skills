# Card：GameEndReward ↔ GoldRoom

源文件与产物：

- `GameEndReward_对局结束奖励.xlsx`（sheet `对局结束奖励|GameEndReward`）→ `ConfGameEndReward.json`
- `GoldRoom_金币场.xlsx`（sheet `金币场|GoldRoom`）→ `ConfGoldRoom.json`

## 字段要点

- `GameEndReward`：`Power`（战斗力上限阈值，升序档位）、`Candy`（糖果奖励）、`ExtraGold`（金币桌金币，steam 端给糖果）、`GoldSn`（金币场 sn）。
- `GoldRoom`：`sn`、`Room`（Room 表 sn）、`Cost`（门票）、`RankGold`（名次金币数组）。

## 已确认规则（2026-09-17 用户确认，2026-09-17 数据验证）

1. **GameEndReward.GoldSn ⊆ GoldRoom.sn**
   - 当前 GameEndReward 10 档的 GoldSn 全为 1；GoldRoom.sn 当前为 {1}，全部命中。
   - 校验代码：`gameend-goldroom#1`（check_configs.py）。

## 备注

- `Power` 档位按升序排列，最高档为 99999999（无上限档）。
- `GoldRoom.Room → Room.sn` 仍是候选规则，尚未固化。
