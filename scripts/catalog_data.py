#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Product catalogue — the single source of truth for every quotable SKU.

Three consumers read this file:
  * scripts/sitegen.py      — builds the spec tables on the four category pages
  * scripts/configurator.py — fills the configurator's "start from a model" picker
  * scripts/sync_catalog.py — pushes it to Supabase (and seed.sql for a fresh project)

Rules that keep this honest, because a B2B buyer orders against these numbers:

  1. Rod rows are transcribed from factory-published parameter sheets. Nothing
     is rounded up or "improved".
  2. Line, lure and reel rows are NEUTRAL specification SKUs. No third-party
     brand names appear anywhere — components are bought in from component
     makers and ship under the customer's brand, a neutral pack, or a house
     brand we propose. Naming a maker here would also undo the
     de-branding decision already applied to every product photo.
  3. Prices stay null until a supplying line confirms them. An empty price
     renders as "quoted per build" on the site — never a guessed number.
  4. Where a value is an industry convention rather than a measured figure
     (PE-to-lb equivalence, for example) it carries a `note` saying so, and
     PENDING-BEFORE-PUBLISH.md carries the same item for confirmation.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# rods — transcribed from factory parameter sheets
# --------------------------------------------------------------------------
# Fields shared by every rod unless the row overrides them.
_ROD_BASE = dict(
    category="rod",
    brand_mode="customer",   # the rod always carries the customer's brand
    moq_oem=300,
    moq_custom=1,
    lead_time_oem_days=40,
    lead_time_custom_days=25,
    unit="pcs",
    paths=["oem", "custom"],
    status="active",
    source="Factory parameter sheet",
)


def rod(sku, model, sub, name, image, sort, **specs):
    r = dict(_ROD_BASE)
    r.update(sku=sku, model=model, subcategory=sub, name=name,
             image="assets/images/%s" % image, specs=specs, sort_order=sort)
    return r


RODS = [
    # ---- spinning -------------------------------------------------------
    rod("CRS721LXF", "CRS721LXF", "spinning",
        "7'2\" Light spinning rod — 4–10 lb", "spinning-rod-01.webp", 10,
        length_m=2.19, length_ft="7'2\"", closed_cm=219, sections=1, weight_g=100,
        power="Light", action="Fast", line_rating="4–10 lb", cast_weight_g="3–10",
        tip_mm=1.7, butt_mm=11.1, reel_type="Spinning reel", handle="Cork"),
    rod("CRS731MLF", "CRS731MLF", "spinning",
        "7'3\" Medium-Light spinning rod — 6–12 lb", "spinning-rod-02.webp", 11,
        length_m=2.21, length_ft="7'3\"", closed_cm=221, sections=1, weight_g=108,
        power="Medium-Light", action="Fast", line_rating="6–12 lb", cast_weight_g="5–14",
        tip_mm=1.8, butt_mm=11.5, reel_type="Spinning reel", handle="Cork"),
    rod("CRS741MF", "CRS741MF", "spinning",
        "7'4\" Medium spinning rod — 8–17 lb", "spinning-rod-03.webp", 12,
        length_m=2.23, length_ft="7'4\"", closed_cm=223, sections=1, weight_g=105,
        power="Medium", action="Fast", line_rating="8–17 lb", cast_weight_g="7–21",
        tip_mm=1.9, butt_mm=11.5, reel_type="Spinning reel", handle="Cork"),
    rod("CRS751MHF", "CRS751MHF", "spinning",
        "7'5\" Medium-Heavy spinning rod — 10–20 lb", "spinning-rod-04.webp", 13,
        length_m=2.26, length_ft="7'5\"", closed_cm=226, sections=1, weight_g=131,
        power="Medium-Heavy", action="Fast", line_rating="10–20 lb", cast_weight_g="10–28",
        tip_mm=1.8, butt_mm=12.0, reel_type="Spinning reel", handle="Cork"),
    # ---- casting --------------------------------------------------------
    rod("CRC721MF", "CRC721MF", "casting",
        "7'2\" Medium baitcasting rod — 8–14 lb", "spinning-rod-05.webp", 20,
        length_m=2.19, length_ft="7'2\"", closed_cm=219, sections=1, weight_g=119,
        power="Medium", action="Fast", line_rating="8–14 lb", cast_weight_g="7–21",
        tip_mm=1.7, butt_mm=11.6, reel_type="Baitcasting reel", handle="Cork"),
    rod("CRC741MHF", "CRC741MHF", "casting",
        "7'4\" Medium-Heavy baitcasting rod — 8–17 lb", "spinning-rod-06.webp", 21,
        length_m=2.23, length_ft="7'4\"", closed_cm=223, sections=1, weight_g=126,
        power="Medium-Heavy", action="Fast", line_rating="8–17 lb", cast_weight_g="10–28",
        tip_mm=1.8, butt_mm=12.0, reel_type="Baitcasting reel", handle="Cork"),
    rod("CRC761XH", "CRC761XH", "casting",
        "7'6\" Extra-Heavy baitcasting rod — 10–25 lb", "spinning-rod-02.webp", 22,
        length_m=2.29, length_ft="7'6\"", closed_cm=229, sections=1, weight_g=135,
        power="Extra-Heavy", action="Fast", line_rating="10–25 lb", cast_weight_g="14–42",
        tip_mm=2.3, butt_mm=12.7, reel_type="Baitcasting reel", handle="Cork"),
    # ---- carp -----------------------------------------------------------
    rod("PRC-9300", "PRC-9300", "carp",
        "9'0\" carp rod — 3.0 lb test curve", "carp-rod-01.webp", 30,
        length_m=2.70, length_ft="9'0\"", closed_cm=140, sections=2, weight_g=256,
        power="3.0 lb test curve", action="Progressive", line_rating="—",
        cast_weight_g="—", tip_mm=2.6, butt_mm=14.9, reel_type="Spinning reel",
        handle="Slim EVA + duplon"),
    rod("PRC-10300", "PRC-10300", "carp",
        "10'0\" carp rod — 3.0 lb test curve", "carp-rod-02.webp", 31,
        length_m=3.00, length_ft="10'0\"", closed_cm=156, sections=2, weight_g=315,
        power="3.0 lb test curve", action="Progressive", line_rating="—",
        cast_weight_g="—", tip_mm=2.7, butt_mm=16.0, reel_type="Spinning reel",
        handle="Slim EVA + duplon"),
    rod("PRC-12275", "PRC-12275", "carp",
        "12'0\" carp rod — 2.75 lb test curve", "carp-rod-03.webp", 32,
        length_m=3.60, length_ft="12'0\"", closed_cm=186, sections=2, weight_g=386,
        power="2.75 lb test curve", action="Progressive", line_rating="—",
        cast_weight_g="—", tip_mm=2.7, butt_mm=16.4, reel_type="Spinning reel",
        handle="Slim EVA + duplon"),
    rod("PRC-12300", "PRC-12300", "carp",
        "12'0\" carp rod — 3.0 lb test curve", "carp-rod-04.webp", 33,
        length_m=3.60, length_ft="12'0\"", closed_cm=186, sections=2, weight_g=421,
        power="3.0 lb test curve", action="Progressive", line_rating="—",
        cast_weight_g="—", tip_mm=2.7, butt_mm=16.8, reel_type="Spinning reel",
        handle="Slim EVA + duplon"),
    # ---- saltwater boat -------------------------------------------------
    rod("MPB66HC", "MPB66HC", "boat",
        "6'6\" boat rod — 20–50 lb class", "saltwater-rod-01.webp", 40,
        length_m=1.98, length_ft="6'6\"", closed_cm=198, sections=1, weight_g=444,
        power="Heavy", action="Moderate-Fast", line_rating="20–50 lb",
        cast_weight_g="50–150", tip_mm=3.0, butt_mm=12.0,
        reel_type="Conventional / overhead", handle="EVA"),
    rod("MPB66XHC", "MPB66XHC", "boat",
        "6'6\" boat rod — 60–100 lb class", "saltwater-rod-02.webp", 41,
        length_m=1.98, length_ft="6'6\"", closed_cm=198, sections=1, weight_g=465,
        power="Extra-Heavy", action="Moderate-Fast", line_rating="60–100 lb",
        cast_weight_g="80–200", tip_mm=3.3, butt_mm=12.7,
        reel_type="Conventional / overhead", handle="EVA"),
    rod("MPB66XXHC", "MPB66XXHC", "boat",
        "6'6\" boat rod — 80–200 lb class", "saltwater-rod-03.webp", 42,
        length_m=1.98, length_ft="6'6\"", closed_cm=198, sections=1, weight_g=508,
        power="Extra-Heavy", action="Moderate-Fast", line_rating="80–200 lb",
        cast_weight_g="120–300", tip_mm=3.7, butt_mm=13.7,
        reel_type="Conventional / overhead", handle="EVA"),
    # ---- saltwater jigging ----------------------------------------------
    rod("ASJS581-550", "ASJS581", "jigging",
        "5'8\" slow-pitch jigging rod — spinning, max 550 g", "saltwater-rod-04.webp", 50,
        length_m=1.73, length_ft="5'8\"", closed_cm=127, sections="1.5 (jointed)",
        weight_g=152, power="Heavy", action="Slow-pitch", line_rating="PE 2.5–4",
        cast_weight_g="max 550", tip_mm=2.7, butt_mm=12.7,
        reel_type="Spinning reel", handle="EVA"),
    rod("ASJS631-300", "ASJS631", "jigging",
        "6'3\" slow-pitch jigging rod — spinning, max 300 g", "saltwater-rod-05.webp", 51,
        length_m=1.91, length_ft="6'3\"", closed_cm=145, sections="1.5 (jointed)",
        weight_g=144, power="Medium-Heavy", action="Slow-pitch", line_rating="PE 1.5–2.5",
        cast_weight_g="max 300", tip_mm=2.1, butt_mm=11.5,
        reel_type="Spinning reel", handle="EVA"),
    rod("ASJS631-220", "ASJS631", "jigging",
        "6'3\" light jigging rod — spinning, max 220 g", "saltwater-rod-06.webp", 52,
        length_m=1.91, length_ft="6'3\"", closed_cm=145, sections="1.5 (jointed)",
        weight_g=131, power="Medium", action="Slow-pitch", line_rating="PE 1.0–2.0",
        cast_weight_g="max 220", tip_mm=1.9, butt_mm=11.5,
        reel_type="Spinning reel", handle="EVA",
        notes="Same model code as ASJS631-300 in the factory sheet but a lighter "
              "blank — confirm which one the customer means before quoting."),
    rod("ASJC581-550", "ASJC581", "jigging",
        "5'8\" slow-pitch jigging rod — casting, max 550 g", "saltwater-rod-07.webp", 53,
        length_m=1.73, length_ft="5'8\"", closed_cm=127, sections="1.5 (jointed)",
        weight_g=160, power="Heavy", action="Slow-pitch", line_rating="PE 2.5–4",
        cast_weight_g="max 550", tip_mm=2.7, butt_mm=12.5,
        reel_type="Baitcasting reel", handle="EVA"),
    rod("ASJC631-300", "ASJC631", "jigging",
        "6'3\" slow-pitch jigging rod — casting, max 300 g", "saltwater-rod-08.webp", 54,
        length_m=1.91, length_ft="6'3\"", closed_cm=145, sections="1.5 (jointed)",
        weight_g=152, power="Medium-Heavy", action="Slow-pitch", line_rating="PE 1.5–2.5",
        cast_weight_g="max 300", tip_mm=2.0, butt_mm=11.6,
        reel_type="Baitcasting reel", handle="EVA"),
    rod("ASJC631-120", "ASJC631", "jigging",
        "6'3\" light jigging rod — casting, max 120 g", "saltwater-rod-04.webp", 55,
        length_m=1.91, length_ft="6'3\"", closed_cm=145, sections="1.5 (jointed)",
        weight_g=138, power="Medium-Light", action="Slow-pitch", line_rating="PE 0.5–1.5",
        cast_weight_g="max 120", tip_mm=1.8, butt_mm=11.0,
        reel_type="Baitcasting reel", handle="EVA",
        notes="Same model code as ASJC631-300 in the factory sheet but a lighter "
              "blank — confirm which one the customer means before quoting."),
    # ---- rock & surf ----------------------------------------------------
    rod("AGSF4203", "AGSF4203", "surf",
        "13'9\" surf rod — 120–250 g cast", "rock-surf-rod-01.webp", 60,
        length_m=4.20, length_ft="13'9\"", closed_cm=148, sections="3 (plug-in)",
        weight_g=578, power="Heavy", action="Fast", line_rating="—",
        cast_weight_g="120–250", tip_mm=3.17, butt_mm=23.4,
        reel_type="Spinning reel", handle="Anti-slip EVA"),
    rod("AGSF4503", "AGSF4503", "surf",
        "14'9\" surf rod — 150–280 g cast", "rock-surf-rod-02.webp", 61,
        length_m=4.50, length_ft="14'9\"", closed_cm=158, sections="3 (plug-in)",
        weight_g=658, power="Heavy", action="Fast", line_rating="—",
        cast_weight_g="150–280", tip_mm=3.26, butt_mm=24.2,
        reel_type="Spinning reel", handle="Anti-slip EVA"),
]

# --------------------------------------------------------------------------
# line / lure / reel — neutral specification SKUs, bought in from component makers
# --------------------------------------------------------------------------
_COMP_BASE = dict(
    brand_mode="neutral",
    moq_oem=500,          # components are bought in; the maker's own minimum applies
    moq_custom=1,
    lead_time_oem_days=45,
    lead_time_custom_days=20,
    unit="pcs",
    paths=["oem", "custom"],
    status="active",
    source="Component maker catalogue (neutral spec, no maker name published)",
)


def comp(category, sub, sku, name, sort, **specs):
    c = dict(_COMP_BASE)
    c.update(sku=sku, category=category, subcategory=sub, name=name,
             specs=specs, sort_order=sort, image=None)
    return c


def braid(pe, strand, metres, colour, sort):
    tag = ("%s" % pe).replace(".", "")
    return comp("line", "braid", "LINE-PE%s-%dS-%dM" % (tag, strand, metres),
                "PE %s braid — %d-strand, %d m, %s" % (pe, strand, metres, colour),
                sort, material="PE braid", pe_no=pe, strand=strand,
                length_m=metres, colour=colour)


def leader(lb, metres, sort):
    return comp("line", "leader", "LINE-FC%02d-%dM" % (lb, metres),
                "Fluorocarbon leader — %d lb, %d m" % (lb, metres), sort,
                material="Fluorocarbon", lb_test=lb, length_m=metres)


def mono(lb, metres, sort):
    return comp("line", "mono", "LINE-NY%02d-%dM" % (lb, metres),
                "Nylon monofilament — %d lb, %d m" % (lb, metres), sort,
                material="Nylon", lb_test=lb, length_m=metres)


def lure(sub, slug, name, weight_g, length_mm, colour, sort, **extra):
    s = dict(lure_type=sub, weight_g=weight_g, length_mm=length_mm, colour=colour)
    s.update(extra)
    return comp("lure", sub, "LURE-%s" % slug, name, sort, **s)


def reel(sub, size, sort, **extra):
    s = dict(reel_type=sub, size=size)
    s.update(extra)
    return comp("reel", sub, "REEL-%s-%d" % (sub[:4].upper(), size),
                "%s reel — size %d" % (sub.capitalize(), size), sort, **s)


def terminal(sub, slug, name, sort, **specs):
    """Neutral terminal-tackle reference.

    These rows make a complete personal set specifiable. They are reference
    combinations until a supplying line confirms stock, packing and MOQ.
    """
    specs.setdefault("verification", "supplier confirmation required")
    item = comp("accessory", sub, "TERM-%s" % slug, name, sort, **specs)
    item.update(status="draft", moq_oem=None, moq_custom=None,
                lead_time_oem_days=None, lead_time_custom_days=None,
                unit="packs", source="Internal reference specification")
    return item


LINES = (
    # 8-strand: smoother, quieter through the guides, the default for jigging
    [braid(p, 8, m, "Dark green", 100 + i)
     for i, (p, m) in enumerate([("0.6", 150), ("0.8", 150), ("1.0", 150),
                                 ("1.2", 150), ("1.5", 200), ("2.0", 200),
                                 ("3.0", 300), ("4.0", 300)])]
    # 4-strand: the value option for volume programs
    + [braid(p, 4, m, "Multi-colour", 120 + i)
       for i, (p, m) in enumerate([("0.8", 150), ("1.0", 150), ("1.5", 200),
                                   ("2.0", 200), ("3.0", 300)])]
    + [leader(lb, m, 140 + i)
       for i, (lb, m) in enumerate([(6, 30), (10, 30), (16, 50), (20, 50),
                                    (30, 50), (40, 50)])]
    + [mono(lb, m, 160 + i)
       for i, (lb, m) in enumerate([(8, 150), (12, 150), (17, 200), (25, 200)])]
)

LURES = [
    # soft plastics
    lure("soft", "SOFT-GRUB-3", "Curly tail grub — 3\", 5 g", 5, 76, "Mixed natural", 200,
         rig="Jig head rig"),
    lure("soft", "SOFT-SHAD-4", "Paddle tail shad — 4\", 10 g", 10, 100, "Mixed natural", 201,
         rig="Jig head rig"),
    lure("soft", "SOFT-WORM-5", "Straight worm / stick bait — 5\", 8 g", 8, 127,
         "Mixed natural", 202, rig="Texas / Carolina rig"),
    lure("soft", "SOFT-CRAW-35", "Creature / craw — 3.5\", 12 g", 12, 89, "Dark", 203,
         rig="Texas / Carolina rig"),
    # hard lures
    lure("hard", "HARD-MINNOW-110", "Minnow — 110 mm, 15 g", 15, 110, "Mixed", 210,
         action="Floating"),
    lure("hard", "HARD-CRANK-60", "Crankbait — 60 mm, 12 g", 12, 60, "Mixed", 211,
         action="Diving"),
    lure("hard", "HARD-VIB-70", "Vibration / lipless — 70 mm, 18 g", 18, 70, "Mixed", 212,
         action="Sinking"),
    lure("hard", "HARD-PENCIL-120", "Pencil / stickbait — 120 mm, 25 g", 25, 120, "Mixed", 213,
         action="Sinking"),
    lure("hard", "HARD-POPPER-90", "Popper — 90 mm, 20 g", 20, 90, "Mixed", 214,
         action="Topwater"),
    # metal
    lure("metal", "METAL-SLOW-100", "Slow-pitch metal jig — 100 g", 100, 120, "Mixed", 220,
         action="Sinking"),
    lure("metal", "METAL-SLOW-150", "Slow-pitch metal jig — 150 g", 150, 140, "Mixed", 221,
         action="Sinking"),
    lure("metal", "METAL-SHORE-40", "Shore casting metal jig — 40 g", 40, 90, "Mixed", 222,
         action="Sinking"),
    lure("metal", "METAL-SHORE-60", "Shore casting metal jig — 60 g", 60, 100, "Mixed", 223,
         action="Sinking"),
    # spoon & spinner
    lure("spoon", "SPOON-20", "Casting spoon — 20 g", 20, 70, "Mixed", 230,
         action="Sinking"),
    lure("spoon", "SPINNER-15", "Inline spinner — 15 g", 15, 60, "Mixed", 231,
         action="Sinking"),
    # glow / UV
    lure("glow", "GLOW-EGI-30", "Glow squid jig (egi) — size 3.0", 18, 90, "Glow / UV", 240,
         action="Sinking"),
]

REELS = [
    reel("spinning", 1000, 300),
    reel("spinning", 2000, 301),
    reel("spinning", 2500, 302),
    reel("spinning", 3000, 303),
    reel("spinning", 4000, 304),
    reel("spinning", 5000, 305),
    reel("spinning", 6000, 306),
    reel("baitcasting", 100, 310),
    reel("baitcasting", 200, 311),
    reel("conventional", 30, 320),
]

TERMINAL = [
    terminal("jig-head", "JIG-1-0-7G", "Jig head — 1/0 hook, 7 g", 400,
             hook_size="1/0", weight_g=7, finish="Black nickel"),
    terminal("jig-head", "JIG-2-0-14G", "Jig head — 2/0 hook, 14 g", 401,
             hook_size="2/0", weight_g=14, finish="Black nickel"),
    terminal("worm-hook", "EWG-2-0", "EWG worm hook — size 2/0", 410,
             hook_size="2/0", barb="Barbed", finish="Black nickel"),
    terminal("worm-hook", "EWG-3-0", "EWG worm hook — size 3/0", 411,
             hook_size="3/0", barb="Barbed", finish="Black nickel"),
    terminal("assist-hook", "ASSIST-2-0", "Jigging assist hook — size 2/0", 420,
             hook_size="2/0", rig="Single assist"),
    terminal("swivel", "SWIVEL-30LB", "Rolling swivel — 30 lb", 430,
             strength_lb=30),
    terminal("snap", "SNAP-30LB", "Lure snap — 30 lb", 431,
             strength_lb=30),
    terminal("sinker", "SINKER-MIX-5-20G", "Sinker assortment — 5–20 g", 440,
             weight_g="5–20", pack="Mixed reference pack"),
]

PRODUCTS = sorted(RODS + LINES + LURES + REELS + TERMINAL,
                  key=lambda p: (p["sort_order"], p["sku"]))


# --------------------------------------------------------------------------
# helpers used by the page builders
# --------------------------------------------------------------------------
def by_category(cat):
    return [p for p in PRODUCTS if p["category"] == cat]


def rods_by_sub(sub):
    return [p for p in RODS if p["subcategory"] == sub]


def sku(code):
    for p in PRODUCTS:
        if p["sku"] == code:
            return p
    return None


# --------------------------------------------------------------------------
# spec-table rows for the four category pages
# --------------------------------------------------------------------------
import re  # noqa: E402


def _closed(p):
    s = p["specs"]
    return "%.2f m" % s["length_m"] if s["sections"] == 1 else "%d cm" % s["closed_cm"]


def _dia(p):
    s = p["specs"]
    return "%s / %s mm" % (s["tip_mm"], s["butt_mm"])


# Each category page numbers and labels the two middle columns differently —
# a carp page shows a test curve where a boat page shows a line class — so the
# row shape lives here rather than being transcribed by hand per page.
PAGE_KINDS = {
    "spinning": dict(subs=("spinning", "casting"),
                     c6=lambda s: "%s / %s" % (s["power"], s["action"]),
                     c8=lambda s: s["line_rating"]),
    "carp": dict(subs=("carp",),
                 c6=lambda s: s["power"],
                 c8=lambda s: s["line_rating"]),
    "boat": dict(subs=("boat",),
                 c6=lambda s: "%s class" % s["line_rating"],
                 c8=lambda s: s["line_rating"]),
    "jig": dict(subs=("jigging",),
                c6=lambda s: "MAX %s g jig" % re.sub(r"\D", "", str(s["cast_weight_g"])),
                c8=lambda s: s["line_rating"]),
    "surf": dict(subs=("surf",),
                 c6=lambda s: s["action"],
                 c8=lambda s: "%s g cast" % s["cast_weight_g"]),
}


def spec_rows(kind):
    k = PAGE_KINDS[kind]
    out = []
    for sub in k["subs"]:
        for p in sorted(rods_by_sub(sub), key=lambda r: r["specs"]["length_m"]):
            s = p["specs"]
            if sub == "casting":
                mark = " (cast)"
            elif sub == "jigging":
                mark = " (spin)" if "Spinning" in s["reel_type"] else " (cast)"
            else:
                mark = ""
            out.append([
                p["model"] + mark,
                "%.2f m (%s)" % (s["length_m"], s["length_ft"]),
                _closed(p),
                s["sections"],
                "%d g" % s["weight_g"],
                k["c6"](s),
                _dia(p),
                k["c8"](s),
                s["handle"],
                "—",
            ])
    return out


def as_json():
    return json.dumps(PRODUCTS, ensure_ascii=False, indent=1, sort_keys=True)


if __name__ == "__main__":
    print("products: %d (rods %d, line %d, lure %d, reel %d, terminal %d)"
          % (len(PRODUCTS), len(RODS), len(LINES), len(LURES), len(REELS),
             len(TERMINAL)))
