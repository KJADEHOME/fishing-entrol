#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download CRONY images per category, build per-category contact sheets."""
import os, re, json, math, sys, time
import requests
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "_raw")
POOL = os.path.join(RAW, "crony_pool")
os.makedirs(POOL, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Referer": "https://www.cronyfishing.com/",
}

IDX = json.load(open(os.path.join(RAW, "crony_detail_imgs.json"), encoding="utf-8"))
# stable order: category then alt then url
items = sorted(IDX.items(), key=lambda kv: (kv[1]["cat"], kv[1]["alt"], kv[0]))


def download(u):
    try:
        r = requests.get(u, headers=HEADERS, timeout=30)
        if r.status_code == 200 and len(r.content) > 2000:
            return r.content
    except Exception:
        time.sleep(0.3)
    return None


def main():
    meta = []
    n = 0
    per_cat_counter = {}
    for u, v in items:
        data = download(u)
        if not data:
            continue
        try:
            im = Image.open(os.devnull)  # placeholder to fail fast if not image
        except Exception:
            pass
        fp = os.path.join(POOL, "tmp.bin")
        with open(fp, "wb") as f:
            f.write(data)
        try:
            im = Image.open(fp)
            im.load()
            w, h = im.size
        except Exception:
            os.remove(fp)
            continue
        if w < 300 or h < 300:
            os.remove(fp)
            continue
        if w > 3.5 * h or h > 3.5 * w:
            os.remove(fp)
            continue
        cat = v["cat"]
        per_cat_counter[cat] = per_cat_counter.get(cat, 0) + 1
        fmt = (im.format or "JPEG").lower()
        ext = "png" if fmt == "png" else "jpg"
        out = os.path.join(POOL, "%s-%02d.%s" % (cat, per_cat_counter[cat], ext))
        os.replace(fp, out)
        meta.append({"file": out, "w": w, "h": h, "bytes": len(data),
                     "url": u, "alt": v["alt"], "cat": cat, "src": v["src"]})
        n += 1

    json.dump(meta, open(os.path.join(RAW, "crony_pool_index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("KEPT", n, {c: per_cat_counter.get(c, 0) for c in set(m["cat"] for m in meta)})

    # contact sheets per category
    by = {}
    for m in meta:
        by.setdefault(m["cat"], []).append(m)
    cols, cell = 6, 240
    for cat, lst in by.items():
        rows = math.ceil(len(lst) / cols)
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 20)), "white")
        d = ImageDraw.Draw(sheet)
        for i, m in enumerate(lst):
            im = Image.open(m["file"]).convert("RGB")
            im.thumbnail((cell - 8, cell - 8))
            x = (i % cols) * cell + 4
            y = (i // cols) * (cell + 20) + 4
            sheet.paste(im, (x + (cell - 8 - im.width) // 2, y + (cell - 8 - im.height) // 2))
            d.text((x + 2, y + cell - 2), "%s-%02d %s" % (cat[:6], i + 1, m["alt"][:16]), fill="black")
        sp = os.path.join(RAW, "sheet_%s.jpg" % cat)
        sheet.save(sp, quality=82)
        print("sheet", cat, "->", sp)


if __name__ == "__main__":
    main()
