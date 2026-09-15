# SuperChameleon 表格知识库（项目：Configs/SuperChameleon）

源表目录：`Configs/SuperChameleon`（21 张表）

> 与 Card 项目**物理隔离**：本目录规则不得用于 Card 表，Card 规则也不得套用到本项目。

## 已确认依赖（2026-09-15 用户确认，共 8 条）

1. `Born.mapId` ⊆ `Map.sn`（见 [map.md](map.md)）
2. `MapRes.mapId` ⊆ `Map.sn`（见 [map.md](map.md)）
3. `Shop.rewardId` ⊆ `Item.sn`（见 [shop-item-effects.md](shop-item-effects.md)）
4. `Shop.type1/type2=101` → `Item.type=1` → `Item.id` → `Whistle.sn`（见 [shop-item-effects.md](shop-item-effects.md)）
5. `Shop.type1/type2=102` → `Item.type=2` → `Item.id` → `SpecialHunt.sn`（见 [shop-item-effects.md](shop-item-effects.md)）
6. `Whistle.soundId` ⊆ `Audios.sn`（见 [shop-item-effects.md](shop-item-effects.md)）
7. `Gift.giftItem` 的 id → `Item.sn`（见 [gift-exchange.md](gift-exchange.md)）
8. `Exchange.id` ⊆ `Item.sn`（见 [gift-exchange.md](gift-exchange.md)）

## 无跨表依赖 / 外部引用（待后续补充确认）

- 独立表：Activity、CandyCalc、Param、PayPoint、Scene、Str、WaitBorn、GM、Model
- 外部平台引用：[external-refs.md](external-refs.md)（ActivityItem 的 actId/propId/model 等）

## 待确认（按用户 2026-09-15 指示：暂不处理）

- `Map.mapRandomGroup` → `MapRandom.mapId`（0=无随机；当前数据只有 0，无样本可验证）
- `MapRandom.item`（取值 100、200…1000）与 `MapRes.sn`（100–125）不构成包含关系，疑似枚举/类型字段
- `Item.goodUuid` 形如 `22_1_10000002` 的复合串语义
- ActivityItem 的 actId/propId/model 等外部引用与各类枚举字段（见 [external-refs.md](external-refs.md)）
