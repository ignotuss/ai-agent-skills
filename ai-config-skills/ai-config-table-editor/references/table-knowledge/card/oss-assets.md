# Card：图片/资源上传到 OSS 的路径约定

> 2026-09-18 用户确认：以后上传图片时，**本地路径由用户提供，目标 OSS 路径由助手自行判断**。

## 默认桶与根路径

- 桶：`u3d-onlinetest`（北京，`oss-cn-beijing.aliyuncs.com`）
- 公网访问前缀：`https://u3d-onlinetest.oss-cn-beijing.aliyuncs.com/`
- Card 项目资源根目录：`CardGame/`
  - 未额外说明时，目标路径默认在 `oss://u3d-onlinetest/CardGame/` 下，大概率位于其中的 `Pic/`

## 常用子目录（按内容类型判断）

| 资源类型 | OSS 路径 | 对应配置 |
|---|---|---|
| 桌背景 / 竞技场（small/big/全图/cardtable/hex） | `CardGame/Pic/decoration/background/` | TableBackground、Item、Shop |
| 牌背 | `CardGame/Pic/decoration/cardback/` | CardBackground、Item、Shop |
| 表情 | `CardGame/Pic/emoji/` | Emotion、Item、Shop |
| 公告图 | `CardGame/Pic/announcement/` | Announcement |
| 海克斯图标 | `CardGame/Pic/hextech/` | Hextech |
| 通用道具图标 | `CardGame/Pic/item/` | Item、Shop |
| 商店图标 | `CardGame/Pic/store/` | Item、Shop |
| 装扮/头像图标 | `CardGame/AvatarIcon/` | Item、Avatar、Shop |
| 头像背景 | `CardGame/AvatarBG/` | 头像相关 |
| 桌面背景（旧/通用） | `CardGame/TableBg/` | TableBackground（占位） |
| 音效 | `CardGame/Audio/` | Audios（Url 存文件名） |
| 活动素材 | `CardGame/Pic/activity/` | Activity / ActivityItem |

## 上传规则

1. 本地路径由用户提供且视为准确；目标路径由助手按上表推断。
2. 上传工具：本机 `ossutil`（配置在 `%USERPROFILE%\.ossutilconfig`；不得在日志/文档中输出密钥）。
3. 上传前先列目标目录，形成「文件清单 + 目标路径」确认；遇到同名文件默认**先汇报、不覆盖**。
4. 上传后做 HEAD 校验（200 + 图片 Content-Type）；需要时把新 URL 配回表并走「导出 JSON → Apollo 提交 → Configs 子模块提交」。
5. 路径无法判断时：先 `ossutil ls` 列出候选目录再询问，不猜。
