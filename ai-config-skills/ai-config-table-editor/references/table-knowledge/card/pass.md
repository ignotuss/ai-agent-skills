# Pass 通行证体系（Pass / PassReward / PassTask）

通行证模块的三张表整合在一个页面维护：

- `Pass_通行证.xlsx`（sheet `通行证|Pass`）→ `ConfPass.json`：主表/上级表。
- `PassReward_通行证奖励表.xlsx`（sheet `通行证奖励|PassReward`）→ `ConfPassReward.json`：奖励明细。
- `PassTask_通行证任务表.xlsx`（sheet `通行证任务|PassTask`）→ `ConfPassTask.json`：任务明细。
- 关联基础表：`Item`（道具，奖励引用）、`Task`（任务模板，taskID 引用）、`Bond`（羁绊，任务参数 b% 引用）。

## 主从关系

Pass 是上级主表；PassReward、PassTask 通过组 ID 归属某期 Pass。校验以 Pass 为权威，明细侧向主表对齐。

## 字段要点

- `Pass`：`taskGroupId`（关联任务组）、`awardGroupId`（关联奖励组）、`award`（本期大奖奖励 sn）。
- `PassReward`：`rewardGroup`、`level`、`exp`、`bigReward`、`low/highRewardID`（点点奖励）及 steam 变体。
- `PassTask`：`taskGroup`、`type`、`taskID`、`taskParams`、`expNum` 及 steam 变体。
- `PassTask.type` 含义（只记录含义，不做数值约束）：`1`=每日，`2`=每周，`3`=赛季。当前数据全部为 2。
- `Task.desc` 占位符：`d%`=数字缺省，`b%`=羁绊 Sn 缺省。

## 已确认规则（2026-09-03）

1. **奖励组对齐**：`PassReward.rewardGroup` 必须被某期 `Pass.awardGroupId` 引用（当前 {1} ↔ {1}），双向一致。
2. **任务组对齐**：`PassTask.taskGroup` 必须被某期 `Pass.taskGroupId` 引用（当前 {1} ↔ {1}），双向一致。
3. 同一 `rewardGroup` 内 `level` 连续且唯一（当前 1~50）。
4. PassReward 的奖励 id（`low/highRewardID`，含 steam 变体）必须存在于 `Item.sn`（当前全部命中）。
5. **大奖对齐**：PassReward 最高大奖档（当前 level=50）的 `highRewardID` 必须等于 `Pass.award`（当前均=30006）。
6. `PassTask.taskID` 必须存在于 `Task.sn`，且同一 `taskGroup` 内同 `type` 下不重复（type 不同可重复，例如同一 Task 可分别配置每日/每周版；当前校验键为 `(taskGroup, type, taskID)`）。
7. `taskParams` 的参数个数必须等于 `Task.desc` 中占位符数量；`b%` 取值必须存在于 `Bond.sn`，`d%` 为数字。
   - 例：Task 4"达成 b%牌型 d%次"→ `taskParams=29,1`，其中 29 对应 `Bond.sn=29`（两个四条）。
8. steam 字段遵循全局规则（见 SKILL.md 通用安全边界），只做引用存在性检查。

## 待确认

- dd 侧每级发 `285`（秀券）×1 疑似占位/示例数据，是否为正式配置待业务确认。
- `low/highRewardID` 的具体语义（除 50 级外两者相同）待业务说明；在说明前只做存在性校验。
