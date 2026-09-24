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
- `PassTask.type` 含义（只记录含义，不做数值约束）：`1`=每日，`2`=每周，`3`=赛季。当前通行证任务已同时使用 1（每日）与 2（每周），3 暂未使用。
- `Task.desc` 占位符：`d%`=数字缺省，`b%`=羁绊 Sn 缺省。

## 已确认规则（2026-09-03）

1. **奖励组对齐**：`PassReward.rewardGroup` 必须被某期 `Pass.awardGroupId` 引用（当前 {1} ↔ {1}），双向一致。
2. **任务组对齐**：`PassTask.taskGroup` 必须被某期 `Pass.taskGroupId` 引用（当前 {1} ↔ {1}），双向一致。
3. 同一 `rewardGroup` 内 `level` 连续且唯一（当前 1~50）。
4. PassReward 的奖励 id（`low/highRewardID`，含 steam 变体）必须存在于 `Item.sn`（当前全部命中）。
5. **大奖对齐（dd 侧）**：PassReward 最高大奖档（当前 level=50）的 `highRewardID` 必须等于 `Pass.award`（当前均为 276）；steamAward 按全局规则只做 Item.sn 存在性校验。
6. `PassTask.taskID` 必须存在于 `Task.sn`；同一 `taskGroup` 内同 `type` 下，相同 `taskID` 的不同行**时间窗口不得重叠**（可按 startTime/endTime 配置多行用于每周轮换，如每周不同的“达成牌型”任务；type 不同互不影响）。校验按 `(taskGroup, type, taskID)` 分组后检查时间区间重叠；无时间列或时间为空时按整期处理。
7. `taskParams` 的参数个数必须等于 `Task.desc` 中占位符数量；`b%` 取值必须存在于 `Bond.sn`，`d%` 为数字。
   - 例：Task 4"达成 b%牌型 d%次"→ `taskParams=29,1`，其中 29 对应 `Bond.sn=29`（两个四条）。
8. steam 字段遵循全局规则（见 SKILL.md 通用安全边界），只做引用存在性检查。

9. 通行证奖励文本映射（2026-09-03 确认，用于设计稿 → PassReward）：金币=Item 255、糖果=1007、秀券=285、加分卡=10003、保分卡=10004、祝福刷新卡=10005、初始牌刷新卡=10006、竞技场1/2=40002/40003；数量拆分写入 `low/highRewardNum`；“表情N”暂用 20005 占位。

## 待确认 / 后续

- `low/highRewardID` 语义（2026-09-03 已随“通行证具体内容表”落地）：`lowRewardID`=普通（免费档）奖励，`highRewardID`=高级（付费档）奖励；50 级高级奖励特殊处理，保持手工配置（当前 276），不随批量更新改动。
- 表情奖励当前用 Item 20005（坏笑）占位，待替换为正式表情道具后再更新对应行。
- 50 级高级奖励（avatar）的最终道具 id 待业务最终确认。
