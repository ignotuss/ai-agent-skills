# SuperChameleon：Map / Born / MapRes / MapRandom

## 表定位

- `Map_地图表.xlsx`（sheet `地图表|Map`）：地图主表，`sn` 为主键（当前 2、3、4）。
- `Born_出生表.xlsx`（sheet `出生表|Born`）：各地图出生点，`mapId` 指向地图。
- `MapRes_地图资源表.xlsx`（sheet `地图资源表|MapRes`）：地图内可交互资源/道具。
- `MapRandom_地图随机生成表.xlsx`（sheet `地图随机生成表|MapRandom`）：随机生成组配置。

## 已确认规则（2026-09-15 数据验证）

1. **Born.mapId ⊆ Map.sn**
   - Born.mapId 取值 {2,3,4}，Map.sn 当前 {2,3,4}，全部命中。
2. **MapRes.mapId ⊆ Map.sn**
   - MapRes.mapId 取值 {2,3}，全部命中 Map.sn。

## 待确认（2026-09-15 用户确认暂不处理）

3. `Map.mapRandomGroup` 预期指向 `MapRandom.mapId`（地图道具随机关联组，0 表示没有随机）。
   - 当前 Map.mapRandomGroup 数据只有 0；MapRandom.mapId 取值为 1、2，缺少非 0 样本，暂不固化。
4. `MapRandom.item`（100,200,…,1000）不是 `MapRes.sn`（100–125）的引用，疑似“道具类型”枚举；待业务说明。

## 其他字段说明

- `Map.mapType`：0 感染模式 / 1 常规模式（枚举）
- `Map.lightType`：0 影响所有层级 / 1 只影响角色（客户端，枚举）
- `Map.hideTime / searchTime`：躲藏/寻找时间
- `MapRes.sn`：资源唯一 id（100–125），供地图内资源引用
