# 表格知识库（多项目，按项目隔离）

每个项目有独立的表结构、编号空间与依赖规则。**同名表不代表同规则，禁止跨项目套用。**

## 项目目录

| 项目 | 源表目录 | 知识页 |
|---|---|---|
| Card（牌类项目） | `Configs/Card` | [card/index.md](card/index.md) |
| SuperChameleon（变色龙项目） | `Configs/SuperChameleon` | [super-chameleon/index.md](super-chameleon/index.md) |

## 隔离原则（重要）

1. 引用关系只在**同一项目内**成立；校验脚本也按项目各自维护。
2. 同名表/同名字段可能语义不同，例如：
   - `Gift.giftItem`：Card 指向 `ItemCard.sn`；SuperChameleon 指向 `Item.sn`（31=预言未来、32=辉耀守护）。
   - `Item.sn` 编号空间完全不同（Card 含 ddCard 段；SuperChameleon 为 1~20006 等自有段）。
3. 新增规则时先确认项目归属，写入对应项目子目录。

## 校验脚本位置

| 项目 | 校验脚本 |
|---|---|
| Card | `Configs/Card/Tool/_forAI/check_configs.py` |
| SuperChameleon | 待建立（本页依赖规则可作为首版基础） |
