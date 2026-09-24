# Card：海克斯表（Hextech）——注意 `isUsed` 其实是权重

> 2026-09-24 记录。这一页只讲一个坑，但它是"看字段名会理解反"的那种坑。

## 表结构

`Hextech_海克斯.xlsx`，sheet `海克斯|Hextech` → `ConfHextech.json`（43 行）。

字段：`sn / hexName / hexLevel / hexDescerption / hexType / round / param1 / param2 / param3 / smallIcon / bigIcon / isUsed`

## ⚠ 陷阱：最后一列的字段名 `isUsed`，含义是「权重」

表头第 3 行（中文注释）写的是 **权重**，但第 4 行字段名和第 1 行的列标记决定了它导出成 `isUsed`：

```json
{"sn":1001,"hexName":"应急护甲","hexLevel":1,"round":5,"isUsed":10, ...}
```

所以 `ConfHextech.json` 里的 `isUsed: 10` **不是"是否启用"的布尔值，而是权重**（实际取值 5 / 10 / 25 等）。

2026-09-17 的权重调整就是通过这一列完成的：`1 → 10`，其中「有序搜寻」「不计代价」改为 `5`。当时的脚本按列号 12（`isUsed`）写入，结果正确——说明这一列确实就是权重列。

**读这张表/这份 JSON 时不要把 `isUsed` 当开关。** 其他表里的 `isUsed`（如奇遇事件表）才是"是否启用"。

## 相关字段

- `round`：出现回合（当前值多为 5）。
- `hexType`：海克斯类型（数值含义未固化，遇到时先问用户）。
- `smallIcon / bigIcon`：资源名（如 `1001_1.png` / `1001_2.png`），不是完整 URL。

## 校验

目前**没有**针对 Hextech 的固化规则；`hextech#1`（权重 > 0、`hexName` 唯一、`round` 合法）在候选清单里，尚未落地。
