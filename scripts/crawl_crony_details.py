#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pass 2: crawl CRONY product detail pages, index all product photos per category."""
import os, re, json, sys, time
import requests

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "_raw")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Referer": "https://www.cronyfishing.com/",
}
CATS = ["CarpRods", "BoatRods", "SurfRods", "JiggingRods", "RockfishRods", "BassPerchRods", "FeederRods"]


def get(url):
    for _ in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                return r.content.decode("utf-8", "replace")
        except Exception:
            time.sleep(0.5)
    return ""


def main():
    index = {}   # url -> {cat, alt}
    for cat in CATS:
        lp = os.path.join(RAW, "crony_%s.html" % cat)
        if not os.path.exists(lp):
            continue
        t = open(lp, encoding="utf-8", errors="replace").read()
        links = sorted(set(re.findall(r'href="(/Products/\d+\.html)"', t)))
        print("%s: %d detail pages" % (cat, len(links)))
        for lk in links:
            html = get("https://www.cronyfishing.com" + lk)
            if not html:
                continue
            title = re.findall(r"<title>(.*?)[_｜-]", html, re.S)
            name = title[0].strip() if title else ""
            imgs = re.findall(
                r'https?://public\.miloweb\.cn/[^"\'\s)]*?/allimg/[^"\'\s)]+?\.(?:jpg|jpeg|png|webp)',
                html, re.I)
            for u in dict.fromkeys(imgs):
                if u not in index:
                    index[u] = {"cat": cat, "alt": name, "src": lk}
            time.sleep(0.2)
        print("  cum images: %d" % len(index))

    json.dump(index, open(os.path.join(RAW, "crony_detail_imgs.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("TOTAL", len(index))
    by = {}
    for u, v in index.items():
        by.setdefault(v["cat"], []).append((v["alt"], u))
    for c, lst in by.items():
        print("\n== %s (%d)" % (c, len(lst)))
        for a, u in lst[:40]:
            print("  ", a[:36], "|", u[-42:])


if __name__ == "__main__":
    main()
