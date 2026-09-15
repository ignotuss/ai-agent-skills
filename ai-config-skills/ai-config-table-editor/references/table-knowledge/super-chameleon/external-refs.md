# SuperChameleon：外部引用与枚举（不做跨表校验）

> 状态：2026-09-15 用户确认**暂不处理**；仅记录，不建立校验规则。

## 外部平台引用（本地表中不存在对应行）

| 表.字段 | 当前值示例 | 说明 |
|---|---|---|
| ActivityItem.actId | 900684 | 备注标明“活动ID（平台Java给）”，来自外部平台 |
| ActivityItem.propId | 1053 | 备注标明“道具ID（平台Java给）”，来自外部平台 |
| ActivityItem.model | 101 | 外部模型 id，非本地 Model.sn（1–4） |
| ActivityItem.address | `/activities/...` | 外部活动地址 |

## 枚举/类型字段（仅记录含义，不做引用校验）

- `Map.mapType`：0 感染模式 / 1 常规模式
- `Map.lightType`：0 影响所有层级 / 1 只影响角色（客户端）
- `Map.hideTime / searchTime / maxCandyperMatch` 等：数值参数
- `Item.type`：1=口哨音效、2=猎人特效（其余取值按业务枚举）
- `Item.costType`：0/1/3（业务枚举）
- `Item.propType`：`chameleon` 等字符串类型标识
- `Model.model`：0/1；`Model.camp`：1/2（阵营）
- `Shop.type1/type2`：101 嘲讽音效 / 102 猎人特效
- `Shop.limitType / showType`、`Activity.takeEffect` 等：布尔或枚举
- `Audios.type`：0 背景音乐 / 1 游戏音效 / 2 系统语音

## 说明

以上字段不建立跨表引用规则；如后续业务确认某个字段实际指向本地表，再补录到对应知识页并加校验。
