# 表格知识库（多项目，按项目隔离）

每个项目有独立的表结构、编号空间与依赖规则。**同名表不代表同规则，禁止跨项目套用。**

## 项目目录

| 项目 | 源表目录（示例） | 知识页 |
|---|---|---|
| Card | `Configs/Card` | [card/index.md](card/index.md) |
| SuperChameleon | `Configs/SuperChameleon` | [super-chameleon/index.md](super-chameleon/index.md) |

## 隔离原则

1. 引用关系只在同一项目内成立，校验脚本按项目各自维护。
2. 同名表/字段可能语义不同，例如 `Gift.giftItem`：Card 指向 `ItemCard.sn`；SuperChameleon 指向 `Item.sn`。
3. 新增规则先确认项目归属，写入对应项目子目录。
