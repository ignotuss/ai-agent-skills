# SuperChameleon：Shop → Item → Whistle / SpecialHunt（+ Audios）

## 依赖链

```
Shop.rewardId → Item.sn
                 └─ Item.id → Whistle.sn      （Shop.type1/type2 = 101 嘲讽音效）
                 └─ Item.id → SpecialHunt.sn  （Shop.type1/type2 = 102 猎人特效）
Whistle.soundId → Audios.sn
```

## 已确认规则（2026-09-15 数据验证）

1. **Shop.rewardId ⊆ Item.sn**：当前 11 条全部命中。
2. **Shop.type1 = 101（嘲讽音效）**：对应 `Item.type = 1`，且 `Item.id → Whistle.sn`，名称一致：
   - `Shop.name == Item.title == Whistle.name`
   - 对应关系：Item 10001(id2)→Whistle sn2、10002(id3)→sn3、10003(id4)→sn4、10004(id5)→sn5、10005(id6)→sn6（Whistle sn1 默认音效不上架）。
3. **Shop.type1 = 102（猎人特效）**：对应 `Item.type = 2`，且 `Item.id → SpecialHunt.sn`，名称一致：
   - Item 20001(id2)→SpecialHunt sn2 绽放莲花、20002(id3)→sn3 燃烧烈焰、20003(id4)→sn4 电闪雷鸣、20004(id5)→sn5 氤氲之气、20005(id6)→sn6 动感地带、20006(id7)→sn7 万众瞩目（SpecialHunt sn1 默认形象不上架）。
4. **Whistle.soundId ⊆ Audios.sn**：取值 10007、10010–10014，全部命中 Audios.sn（10001–10014、20000、20001）。

## 字段要点

- `Shop.type1` / `Shop.type2`：101=嘲讽音效、102=猎人特效（二级类别当前与一级一致）。
- `Item.propType = chameleon`：本项目的售卖道具类型标识。
- `Item.type`：1=口哨音效、2=猎人特效（与 Shop.type1/type2 的末两位对应）。

## 注意

- 与 Card 项目的 `Item.id → Emotion/Avatar` 规则**无关**，禁止混用。
