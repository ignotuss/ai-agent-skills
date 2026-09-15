# Bond / HandRanking / Audios

源文件与产物：

- `Bond_羁绊.xlsx`（`羁绊|Bond`）→ `ConfBond.json`
- `HandRanking_牌型.xlsx`（`牌型|HandRanking`）→ `ConfHandRanking.json`
- `Audios_音效.xlsx`（`音效信息|Audios`）→ `ConfAudios.json`

## 表定位

- `Audios`：全局音效/语音库，`sn` 为资源唯一 id；`type`：0=背景音乐、1=游戏音效、2=系统语音。
- `Bond`：牌型羁绊（31 行），`type` 表示牌型类别，`desc` 是细分牌型（如顺子5~8、葫芦3+2/4+2/4+3）。
- `HandRanking`：牌型战斗表现模板（14 行），`HandRanking` 是基础牌型名称。

## Bond ↔ HandRanking（唯一配置级关联，2026-09-03 确认）

`Bond.type` 与 `HandRanking.sn` 一一对应，取值集合都是 1~14；Bond 的多个细分条目共享同一个 `type`，即共享同一 HandRanking 表现行，属正常设计。

| Bond.type | HandRanking.sn | 牌型 | Bond.desc 细分 |
|---|---|---|---|
| 1 | 1 | 高牌 | 高牌 |
| 2 | 2 | 对子 | 对子、两对、三对、四对 |
| 3 | 3 | 三条 | 三条、两个三条 |
| 4 | 4 | 连对 | 三连对、四连对 |
| 5 | 5 | 顺子 | 顺子5~8 |
| 6 | 6 | 同花 | 同花5~8 |
| 7 | 7 | 连三条 | 连三条 |
| 8 | 8 | 葫芦 | 小葫芦3+2、中葫芦4+2、大葫芦4+3 |
| 9 | 9 | 四条 | 四条4、两个四条 |
| 10 | 10 | 五行 | 五行 |
| 11 | 11 | 连四条 | 连四条 |
| 12 | 12 | 同花顺 | 同花顺5~8 |
| 13 | 13 | 五条 | 五条 |
| 14 | 14 | 六条 | 六条 |

校验：`Bond.type` 必须存在于 `HandRanking.sn`（1~14）。

注意：`Bond.HandRankingSFX` 字段名容易误导，它指向的是 Audios 音效，不是 HandRanking。

## 已确认的音效引用规则（2026-09-03）

1. `Bond.HandRankingSFX` ⊆ `Audios.sn`（牌型语音，type=2；当前 50001~50017 全部命中）。
2. `HandRanking.AttackBulletSFX` / `HitSFX` ⊆ `Audios.sn`（弹道/受击音效，type=1；当前 40001~40020 全部命中）。
3. `Emotion.audiomale` / `audiofamale` ⊆ `Audios.sn`（表情男女声，type=2；当前 61001~61018 全部命中）。
4. `Rank.showSound` / `upgradeSound` / `disappearSound` ⊆ `Audios.sn`（段位音效）。
5. 通用：凡注释/字段名含"音效、语音、声音、SFX"的数值列，优先按 `Audios.sn` 校验。
