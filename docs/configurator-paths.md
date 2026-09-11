# 配置器两条路径设计说明

更新日期：2026-09-12
适用范围：`oem-builder.html`（OEM 量产路径）与 `custom-rod.html`（个人定制路径），由 `scripts/configurator.py` 按 `path` 渲染 + `script.js` 驱动

---

## 1. 为什么分成两条路径

同一个配置器过去只做一件事：让客人填抽象规格（30T 碳布、SiC 导环、软木握把）。
但两类买家的决策方式完全不同，共用一张表必然有一边别扭：

| | OEM / 品牌方 | 个人发烧友 |
|---|---|---|
| 他来干什么 | **定义一款要上架卖的商品** | **给自己做一支用着顺手的竿** |
| 决策起点 | 目标零售价 → 反推配置 | 在哪钓、钓什么鱼 → 正推配置 |
| 他怕什么 | 报价超预算、交期赶不上渔季、复购做不出同一支 | 买回来不好用、花了钱没手感、坏了没人管 |
| 他要的结果 | 报价单 + 打样 + 量产 | 一支（或两支）能下水的竿 |
| 不该问他 | 刻什么字、缠线什么颜色 | MOQ、贸易条款、认证 |

**结论：不是"一个表单加几个分支"，而是两条决策链。**

---

## 2. 「数量」在两条路径里是两个概念

这是最容易搞混的地方，代码里也是分开实现的：

### OEM：数量 = 生产批量
- `quantity` 每型号多少支：300 / 500 / 1,000 / 3,000 / 5,000+
- `model_count` 本次几个型号：1 / 2–3 / 4–6 / 7+（每型号一副模具、一次印刷，所以 MOQ 按型号算）
- `annual_volume` 12 个月预计量（决定报一次性价还是项目价，以及值不值开专用模具）
- `ship_window` 目标出货窗口（渔季倒推）
- 配套件不选型号，只选"要不要配套件"和"贴谁的牌"（`kit_option` / `kit_brand`）

### Personal：数量 = 件数明细
- `quantity_custom` 竿几根：1 / 2 / … / 6–10 / 10+（**主场景是 1–2 支**）
- 配件清单（`#kit-lines`）：轮 / 线 / 饵 **各可加多行，每行独立选型号 + 填数量**
  - 轮：型号 ▼ × ___ 套（可"再加一款"，例如 2500 一套 + 水滴轮一套）
  - 线：型号 ▼ × ___ 卷
  - 饵：型号 ▼ × ___ 包
- 汇总进隐藏字段 `kit_lines`（如 `Rods: 2 rods | Reels: REEL-SPIN-2500 ×2, REEL-BAIT-200 ×1 | Line: LINE-PE08-8S-150M ×3`）
- 右侧 "In the box" 面板实时显示清单与件数合计

---

## 3. 字段清单

### 两条路径共用（竿本体规格）
`base_model`（从现有型号起步，自动预填）· `rod_type` · `length` · `sections` · `power` · `action` ·
`lure_weight` · `line_rating` · `carbon_grade` · `carbon_cloth` · `blank_finish` · `blank_color` ·
`target_species` · `fishing_method` · `lure_type` · `main_line` · `leader` · `lure_colour` ·
`reel_type` · `reel_size` · `guide_type` · `guide_ring` · `guide_frame` · `guide_count` ·
`reel_seat` · `handle_material` · `handle_style` · `butt_cap` · `target_market` · `name` ·
`email` · `notes`

### OEM 独有
`logo_method` · `packaging` · `hook_keeper` · `kit_option` · `kit_brand` ·
`quantity` · `model_count` · `target_price` · `annual_volume` · `ship_window` ·
`compliance` · `trade_terms` · `sample_plan` · `company`

### Personal 独有
`engraving`（刻字）· `thread_colour`（缠线配色）· `custom_pack`（出货包装）·
`kit_option_custom` · `spool_service`（是否帮忙上线）· `ship_to`（收货国家）·
`budget` · `urgency` · `quantity_custom` · 配件清单 `kit_lines`

**所有字段的选项值都来自产品库**（`scripts/catalog_data.py`），不再是硬编码常量 —— 产品库改了，选项自动跟着变。

---

## 4. 已定死的边界（不要越线）

1. **不零售、不标价。** 全站没有价格、没有购物车、没有在线支付。所有价格一律"询价"。
   - 产品库 `price_oem_usd` / `price_custom_usd` 目前**全为 null**，页面对空价格的渲染是 "quoted per build"。
   - 拿到工厂/配套厂真实报价后再填，禁止编数字 —— B2B 站填假参数，客户会按参数下单索赔。
2. **不做"寄样品给达人/买家试用"。** 定制竿是逐支做的，做出来就是订单本身，没有余量可寄。
3. **不写第三方品牌名。** 线/饵/轮一律中性规格 SKU（`LINE-PE08-8S-150M` 这类）。
   理由：① 遵守"全站去工厂品牌"既定策略；② 列 YGK / Daiwa 有商标风险。
4. **个人定制不可退换**（刻字 + 按身材做 = 无法二次销售），页面已明示，发货前拍照留档。
5. **隐藏的那半不会进询盘。** 路径切换时隐藏字段会被 `disabled`，FormData 直接跳过 —— 有测试守着。

---

## 5. 数据来源与可信度

| 数据 | 来源 | 状态 |
|---|---|---|
| 22 支竿参数 | 工厂公开参数表逐条转录 | 已核对，与原站点表格逐字节一致 |
| 线 / 饵 / 轮 | 中性规格 SKU（行业通用规格，非某品牌型号） | **待配套厂目录补充品牌与齿比/刹车力/自重** |
| 价格 | 无 | **全空，待报价** |
| MOQ 300 / 500 / 1,000 | 行业惯例预设 | **待工厂确认后才能对客报价** |

产品库真源：`scripts/catalog_data.py`（71 SKU）
Supabase：`supabase/migrations/0001_product_catalog.sql` + `supabase/seed.sql`
同步：`python scripts/catalog.py check|seed|json|push|pull`
**构建只读本地文件，Supabase 挂了也能出包。**

---

## 6. 待确认事项

见 `PENDING-BEFORE-PUBLISH.md` 第 5.1 节。最关键的三条：
1. Supabase 项目还没建（需 URL + service key 才能 `push`）
2. 价格全空、MOQ 数字未与工厂对齐 —— 报价前必须补齐
3. 单竿空运到欧美运费可能接近竿价，先问货代再决定 personal 路径是否对外开放
