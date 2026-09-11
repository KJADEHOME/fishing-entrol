# PENDING-BEFORE-PUBLISH — entrol-fishing.com

> 本站当前为**本地原型**（D://codex//fishing-growth-os//source//）。
> **硬约束：未完成本清单前，禁止 push 到 GitHub、禁止部署到任何线上环境。**

## 0. 当前状态（2026-09-11 更新）

| 环节 | 状态 |
|---|---|
| 三家工厂授权 — **已同意** | ✅ 润鼎 / 民盛 口头；**CRONY 经阿里国际站（有文字记录，强于口头）** |
| **CRONY 图包** | 🟡 已同意提供，尚未收到 —— 收到后替换现有 31 张，策略见 `image-pack-strategy.md` |
| 三家工厂授权 — **书面留档** | ❌ **未完成，当前唯一硬门槛**：CRONY 阿里对话截图 + 民盛/润鼎微信截图 |
| **图片去品牌化（Entrol 单一品牌呈现）** | ✅ 完成 —— 27 张，CRONY/Cross/Progress/Measplus/Remanso 标识已全部移除或换图；About 页已改为 brand-first 泛化表述（audited partner lines，不具名） |
| 每个类目页自拍 2–3 张（防撞图） | ❌ 未完成，建议在图包到位后一并做 |
| 域名注册 / 企业邮箱 | ❌ 未完成 |
| 部署 | ⛔ 被硬约束锁定，需另行授权 |

**"同意了"和"能举证"是两件事。** 口头同意没有证据力，必须走完
`docs/authorization/README.md` 里的截图归档（或盖章确认书）后，
才能把下面的状态改成 `GRANTED` 并考虑上线。

> **关于"图片都是公开的"**：公开可见 ≠ 放弃版权。真正给我们权利的
> 是**对方在阿里站内信里那句"可以给图包"**，不是图片本身。
> 所以那段对话的截图，比图包本身还重要 —— 见 `README.md` §2.3。


## 1. 工厂授权留档（最高优先级，全部未完成）

以下三家的"同意使用图片与资料"书面记录（微信/邮件回复截图）必须先拿到并归档到 `docs/authorization/`：

| 工厂 | 角色 | 口头 | 书面留档 | 需留档内容 | 话术/确认书 |
|---|---|---|---|---|---|
| Weihai CRONY Fishing Tackle | 4 个竿型页全部产品图来源（31 张） | ✅ **阿里站内信已同意并提供图包**（有文字记录，强于口头） | ❌ **待截图存档（最高优先）** | 阿里对话截图 + 图包到位后重跑图片脚本 | `README.md` §2.3 |
| 威海民盛体育用品 | About 页工厂图来源（2 张） | ✅ 已同意 | ❌ 待归档 | about-factory-01/02 两张图的授权 | `README.md` §2.1 微信话术 |
| 威海润鼎户外用品 | About 页背书工厂（仅用文字资质，0 张图） | ✅ 已同意 | ❌ 待归档 | 专利号 4 项 / 高新技术企业 / 出口权的展示授权 | `authorization-letter-CN.md` |

归档动作见 `docs/authorization/README.md`：
- 微信截图必须含**你的具体请求 + 对方明确答复 + 头像时间**
- 更稳的做法是盖章确认书拍照回传（`authorization-letter-CN.md` / `-EN.md`）
- 被授权主体一栏**尚未确定**，需你拍板（润鼎/元领进出口/潮若贸易）

## 2. 图片来源清单（每张必列，上线前逐条核对）

授权状态列 = `口头已同意 / 书面待归档`。**书面留档完成前不得上线。**

> 📦 **图包到位后**：本节每张图的"来源页面"要从官网 URL 改为 `Alibaba 图包（CRONY 提供）`，
> 并同步改 `scripts/product_images_manifest.json` 的 `source_page` 字段。
> 拿图时要问的 4 个问题 + 防撞图做法 + 替换重跑命令 → `docs/authorization/image-pack-strategy.md`



### spinning-rod

| 文件 | 来源工厂 | 来源页面 | 授权状态 |
|---|---|---|---|
| spinning-rod-01.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/961.html | 口头✅ 书面❌ |
| spinning-rod-02.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/961.html | 口头✅ 书面❌ |
| spinning-rod-03.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/961.html | 口头✅ 书面❌ |
| spinning-rod-04.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/961.html | 口头✅ 书面❌ |
| spinning-rod-05.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/961.html | 口头✅ 书面❌ |
| spinning-rod-06.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/912.html | 口头✅ 书面❌ |
| spinning-rod-07.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/912.html | 口头✅ 书面❌ |
| spinning-rod-08.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/963.html | 口头✅ 书面❌ |

### carp-rod

| 文件 | 来源工厂 | 来源页面 | 授权状态 |
|---|---|---|---|
| carp-rod-01.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-02.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-03.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-04.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-05.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-06.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |
| carp-rod-07.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/944.html | 口头✅ 书面❌ |

### saltwater-rod

| 文件 | 来源工厂 | 来源页面 | 授权状态 |
|---|---|---|---|
| saltwater-rod-01.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/939.html | 口头✅ 书面❌ |
| saltwater-rod-02.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/939.html | 口头✅ 书面❌ |
| saltwater-rod-03.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/939.html | 口头✅ 书面❌ |
| saltwater-rod-04.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/939.html | 口头✅ 书面❌ |
| saltwater-rod-05.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/937.html | 口头✅ 书面❌ |
| saltwater-rod-06.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/937.html | 口头✅ 书面❌ |
| saltwater-rod-07.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/937.html | 口头✅ 书面❌ |
| saltwater-rod-08.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/938.html | 口头✅ 书面❌ |

### rock-surf-rod

| 文件 | 来源工厂 | 来源页面 | 授权状态 |
|---|---|---|---|
| rock-surf-rod-01.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/921.html | 口头✅ 书面❌ |
| rock-surf-rod-02.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/921.html | 口头✅ 书面❌ |
| rock-surf-rod-03.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/923.html | 口头✅ 书面❌ |
| rock-surf-rod-04.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/923.html | 口头✅ 书面❌ |
| rock-surf-rod-05.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/923.html | 口头✅ 书面❌ |
| rock-surf-rod-06.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/ | 口头✅ 书面❌ |
| rock-surf-rod-07.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/922.html | 口头✅ 书面❌ |
| rock-surf-rod-08.webp | Weihai CRONY Fishing Tackle | https://www.cronyfishing.com/Products/922.html | 口头✅ 书面❌ |

### about-factory

| 文件 | 来源工厂 | 来源页面 | 授权状态 |
|---|---|---|---|
| about-factory-01.webp | Weihai Minsheng Sporting Goods (news/article photo) | https://www.minshengfishing.cn/article.html | 口头✅ 书面❌ |
| about-factory-02.webp | Weihai Minsheng Sporting Goods (news/article photo) | https://www.minshengfishing.cn/article.html | 口头✅ 书面❌ |


## 3. 域名与邮箱（未完成）

- [ ] **确定签约主体**（渔具出口接单用哪个公司签）—— 授权确认书里的"被授权方"一栏卡在这，见 `docs/authorization/README.md` §4
- [ ] 注册 `entrol-fishing.com`（站点内 canonical/OG/sitemap 均已按此域名生成）
- [ ] 配置企业域名邮箱 `sales@entrol-fishing.com`（腾讯企业邮，参照 entrol.com 的 MX 配置）
- [ ] 表单收件箱确认：当前表单直投 `wangyan@entrol.com`（FormSubmit，已验证可用）

## 4. 统计与索引（上线后 48 小时内完成）

- [ ] 决定 GA4 资产：当前复用 GTM 容器 `GTM-T3ZXMRHS`，**建议为本站新建独立 GA4 property + GTM 容器**，避免与 entrol.com 数据混流；替换方法：改 `scripts/sitegen.py` 顶部 `GTM_ID` 后重跑
- [ ] GTM 后台确认容器内已挂 GA4 配置标签并发布（否则 GA4 报表为空）
- [ ] 转化事件已埋：`whatsapp_click` / `wechat_click` / `rfq_submit`（dataLayer），GTM 内需建对应标签
- [ ] GSC 添加资源 + 提交 `sitemap.xml` + 首页手动请求索引

## 5. 上线前内容核对

- [ ] **套装供应能力核实**：配置器 `kit_option` 提供 "rod + reel + line + lures" 套装选项，页面按
      "sourced from component makers to your brief" 表述（**已明确不把 Entrol 品牌打在轮/线/饵上**）。
      **上线前必须确认**：(a) 是否真有可供货的轮/线/饵供应商；(b) 整套出货的 HS 编码与目的国关税
      是否高于单竿（欧盟、澳洲对成品套装税率可能不同）；(c) 客户若选 "Our brand on everything"，
      轮厂/线厂是否接受 1,000 pcs 起做贴牌（**这条是报价承诺，先问到再上线**）；
      (d) 若暂时供不了，先在 `scripts/configurator.py` 里把该字段收窄为 Rod only
- [ ] **MOQ 三档已写进页面，需与工厂实际口径对齐**：竿 300 pcs/model / 竿+配套件 500 pcs /
      配套件也贴客户牌 1,000 pcs。目前数字是**按行业惯例预设的**，工厂确认前不要拿去对客报价
- [ ] **配置器真实提交测试**：在 `configure.html` 填一份完整规格提交，确认 wangyan@entrol.com 收到全部字段（现为 33 个 select，字段多，需确认 FormSubmit 邮件不截断）
- [ ] **GTM 后台建 `configurator_submit` 转化标签**（dataLayer 已埋，含 `options_selected` 与 `spec_summary`）；建议把「选了 ≥5 项」设为高质量询盘信号
- [ ] **兼容性预警规则复查**：13 条规则（轮型×竿型、竿长×饵重、线号×饵重、硬度×饵重、导环×前导、鱼种×前导等）为行业常识推断，**请让懂行的工厂技术或老客户过一遍**，特别是 PE 号数对应的安全抛投上限
- [ ] 联系三处一致（浮动按钮 / 页脚 / 表单页）：WhatsApp +8615263130999 / WeChat 15263130999 / sales@entrol-fishing.com
- [ ] CRONY 阿里对话截图已存进 `docs/authorization/weihai-crony/01-alibaba-reply.png`
- [ ] 图包已替换现有 31 张，并跑通 `build_product_images.py` → `sitegen.py` → `smoke_test.py`
- [ ] 4 个类目页各补 2–3 张自拍（头图 / 手持比例 / 细节特写），防撞图
- [ ] About 页三家工厂表述与书面授权范围一致（未授权的工厂不写"our factory"）
- [ ] 美国市场暂未做专门页面（301 关税），如后续主推美国需先做关税测算
- [ ] `python scripts/smoke_test.py` 全绿后再部署

## 5.1 产品库（Supabase）上线前必须补齐（2026-09-12 新增）

- [ ] **Supabase 项目还没建**：表结构已写好 `supabase/migrations/0001_product_catalog.sql`，
      种子数据 `supabase/seed.sql`（71 SKU）。需要提供 `SUPABASE_URL` + `SUPABASE_SERVICE_KEY`
      后跑 `python scripts/catalog.py push`。**不推也能上线**——站点构建只读本地
      `scripts/catalog_data.py`，Supabase 只是为了让人在后台表格里改产品
- [ ] **价格全部为空（`price_oem_usd` / `price_custom_usd` = null），这是故意的**。
      页面对空价格的渲染是 "quoted per build"，不会编数字。**拿到工厂/配套厂报价后再填**，
      填完重跑 `catalog.py json` + `sitegen.py`
- [ ] **轮/线/饵是中性规格 SKU，没有品牌名**（`LINE-PE08-8S-150M`、`LURE-HARD-MINNOW-110` 这类）。
      这是刻意遵守"全站去工厂品牌"的既定策略。若后续拿到配套厂目录且对方书面同意，
      再补 `brand` 列；**补之前不要在页面上写任何第三方品牌名**
- [ ] **轮的参数只有型号尺寸（1000–6000 / Baitcaster 100–200），没有齿比、刹车力、自重**。
      这些我手上没有可核实数据，宁缺勿编。让配套厂发规格表后补进 `specs` jsonb
- [ ] **两个同型号不同调性的竿需要工厂确认**：`ASJS631`（MAX 300 g / MAX 220 g）和
      `ASJC631`（MAX 300 g / MAX 120 g）在工厂参数表里是同一个型号出现两次。
      我拆成了 4 个 SKU（`-220` / `-300` / `-120` 后缀）并在 `notes` 里标注，
      **报价前必须问清客户要的是哪一个**
- [ ] **单支定制（custom path）的商务条款是我按行业惯例写的，需你确认**：
      1 支起订 / 20–25 天 / 50% 定金 / 刻字后不可退换 / 运费按目的地另报。
      尤其是"不可退换"和"50% 定金"两条是对客承诺，改文案在
      `script.js` 的 `renderMoq()` custom 分支
- [ ] **单支定制真接单前要算清物流**：单竿空运/快递到欧美的运费可能接近竿价，
      建议先问 2–3 家货代拿 1.3–1.6 m 硬管的门到门报价，再决定这个路径要不要对外开放
- [ ] 产品库字段如后续要加（例如交货港口、装箱数、HS 编码），
      改 `catalog_data.py` → 跑 `catalog.py seed` 重新生成 seed.sql，**不要手改 seed.sql**

## 5.2 配置器双路径 + 数量逻辑（2026-09-12 定稿，详见 `docs/configurator-paths.md`）

**已定死的边界（后续改动不许越线）：**
- [ ] **不零售、不标价、不在线支付**。全站无价格、无购物车、无结账。一律询价。
      产品库 `price_*` 全为 null，空价格渲染成 "quoted per build"
- [ ] **不做"寄样品给达人/买家试用"**——定制竿逐支生产，做出来就是订单本身，没有余量可寄
- [ ] **不写第三方品牌名**（线/饵/轮中性规格 SKU）
- [ ] **个人定制不可退换**（刻字+按身材做=无法二次销售），页面已明示，发货前拍照留档
- [ ] 隐藏的那半路径会被 `disabled`，不会进询盘（已有测试守着）

**数量在两条路径里是两个概念（已实现）：**
- OEM = 生产批量：`quantity`（每型号支数）+ `model_count`（几个型号）+ `annual_volume` + `ship_window`
- Personal = 件数明细：`quantity_custom`（竿几根，主场景 1–2 支）+ 配件清单
  （轮/线/饵各可加多行，每行独立选型号+填数量，汇总进隐藏字段 `kit_lines`）

**OEM 新增商务字段（已上线）：** `model_count` / `target_price`（目标零售价，最能决定配置）/
`annual_volume` / `ship_window` / `compliance` / `trade_terms` / `sample_plan`
**Personal 新增：** `budget` / `urgency` / `spool_service` / 配件清单

- [ ] **上面对客文案里有 3 处是商业承诺，需你确认**：
      ① "20–25 天出货" ② "50% 定金" ③ "刻字后不可退换"。改文案在 `script.js` 的 `renderMoq()`
- [ ] FAQ 已新增一问 "Can I buy just one rod for myself?"，明确**无库存、无购物车、按订单生产**

## 6. 已知限制（MVP 范围外，不要在原型阶段补）

- 无博客、无多语言、无国家落地页（按 prompt 第二节要求砍掉）
- 鲤鱼竿页产品图全部来自 CRONY 单一系列（Progress Carp），SKU 丰富度需工厂确认后扩充
- 第二阶段再补：飞钓竿 / 冰钓竿 / 便携竿类目页
