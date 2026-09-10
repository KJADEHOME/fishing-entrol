#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download candidate factory images, filter UI junk, build a contact sheet."""
import os, re, json, math, sys, time
import requests
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "_raw")
POOL = os.path.join(RAW, "pool")
os.makedirs(POOL, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.minshengfishing.cn/",
}

IDX = json.load(open(os.path.join(HERE, "_raw", "image_index.json"), encoding="utf-8"))


def variants(u):
    """Try to get the biggest version available."""
    base = re.sub(r"\?.*$", "", u)
    return [base + "?w=1600", base + "?w=1200", base]


def download(u):
    for v in variants(u):
        try:
            r = requests.get(v, headers=HEADERS, timeout=30)
            if r.status_code == 200 and len(r.content) > 3000:
                return r.content
        except Exception:
            time.sleep(0.4)
    return None


def main():
    kept = []
    for i, it in enumerate(IDX):
        data = download(it["url"])
        if not data:
            continue
        fp = os.path.join(POOL, "cand_%02d.img" % i)
        with open(fp, "wb") as f:
            f.write(data)
        try:
            im = Image.open(fp)
            im.load()
            w, h = im.size
        except Exception:
            continue
        if w < 380 or h < 200:
            continue
        if w > 4 * h or h > 4 * w:      # banners / strips
            continue
        ext = (im.format or "JPEG").lower()
        out = os.path.join(POOL, "cand_%02d.%s" % (i, "png" if ext == "png" else "jpg"))
        os.replace(fp, out)
        kept.append({
            "i": i, "file": out, "w": w, "h": h, "bytes": len(data),
            "url": it["url"], "alt": it["alt"], "factory": it["factory"],
            "source_page": it["source_page"],
        })
        print("keep %02d %4dx%-4d %6dB  %s" % (i, w, h, len(data), it["alt"][:40]))

    kept.sort(key=lambda k: -k["w"] * k["h"])
    json.dump(kept, open(os.path.join(RAW, "pool_index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\nKEPT %d / %d" % (len(kept), len(IDX)))

    # ---- contact sheet ----
    cols, cell = 6, 260
    rows = math.ceil(len(kept) / cols)
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), "white")
    d = ImageDraw.Draw(sheet)
    for n, k in enumerate(kept):
        im = Image.open(k["file"]).convert("RGB")
        im.thumbnail((cell - 8, cell - 8))
        x = (n % cols) * cell + 4
        y = (n // cols) * (cell + 22) + 4
        sheet.paste(im, (x + (cell - 8 - im.width) // 2, y + (cell - 8 - im.height) // 2))
        d.text((x + 4, y + cell - 4), "#%02d %s" % (k["i"], k["alt"][:22]), fill="black")
    sp = os.path.join(RAW, "contact_sheet.jpg")
    sheet.save(sp, quality=85)
    print("sheet ->", sp, sheet.size)


if __name__ == "__main__":
    main()
