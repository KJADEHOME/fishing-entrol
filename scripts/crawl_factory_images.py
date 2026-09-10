#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Crawl allowed Weihai factory sites for rod product images (LOCAL PROTOTYPE ONLY).

Rules from the project prompt:
  - Allowed: factory official sites / 1688 / Alibaba listings of the partner factories.
  - FORBIDDEN: Guangwei (guangwei.com / en.gwfishing.com) and any other big-brand site.
  - Output: _raw/image_index.json  -> [{url, source_page, alt, factory}]
Every downloaded file keeps its source URL + authorization status so it can be
listed in PENDING-BEFORE-PUBLISH.md.
"""
import os, re, json, hashlib, time, sys
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "_raw")
os.makedirs(RAW, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.minshengfishing.cn/",
}

SEEDS = {
    "minsheng": [
        "https://www.minshengfishing.cn/",
        "https://www.minshengfishing.cn/product.html",
        "https://www.minshengfishing.cn/product-200000.html",
        "https://www.minshengfishing.cn/product-200001.html",
        "https://www.minshengfishing.cn/p-about.html",
        "https://www.minshengfishing.cn/p-1.html",
        "https://www.minshengfishing.cn/p-contact.html",
        "https://www.minshengfishing.cn/article.html",
    ],
}

# junk images that are UI chrome, not product photos
JUNK = re.compile(
    r"(logo|icon|icp|cs\.png|vip|years|static/txys|lang|qrcode|weixin|wechat|"
    r"arrow|banner_bg|background|placeholder)", re.I)

IMG_RE = re.compile(r"https?://[^\"'\s)\\<>]+?\.(?:jpg|jpeg|png|webp)", re.I)
NAME_RE = re.compile(r"(?:title|alt)=[\"']([^\"']{2,60})[\"']")


def fetch(url, tries=2):
    for i in range(tries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=25)
            if r.status_code == 200:
                return r
        except Exception as e:
            sys.stderr.write("  ! %s %s\n" % (url, e))
            time.sleep(1)
    return None


def clean(u):
    # strip sizing query but remember we can upscale
    return re.sub(r"\?.*$", "", u)


def main():
    index = {}
    for factory, urls in SEEDS.items():
        for page in urls:
            sys.stderr.write("[page] %s\n" % page)
            r = fetch(page)
            if not r:
                continue
            try:
                html = r.content.decode("utf-8")
            except UnicodeDecodeError:
                html = r.content.decode("gb18030", "replace")
            for m in IMG_RE.finditer(html):
                u = m.group(0)
                if JUNK.search(u):
                    continue
                base = clean(u)
                ctx = html[max(0, m.start() - 400): m.end() + 400]
                nm = NAME_RE.findall(ctx)
                alt = ""
                for cand in nm:
                    cand = cand.strip()
                    if cand and not cand.lower().endswith((".png", ".jpg", ".jpeg")):
                        alt = cand
                        break
                key = base
                if key not in index:
                    index[key] = {
                        "url": base,
                        "orig": u,
                        "factory": factory,
                        "source_page": page,
                        "alt": alt,
                    }
                elif not index[key]["alt"] and alt:
                    index[key]["alt"] = alt

    items = list(index.values())
    out = os.path.join(RAW, "image_index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print("total unique images: %d -> %s" % (len(items), out))
    for it in items:
        print("  %s | %s | %s" % (it["factory"], it["alt"], it["url"]))


if __name__ == "__main__":
    main()
