#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build final WebP product images for the Entrol Fishing site.

Reads from  _raw/crony_pool/  and  _raw/pool/  (crawl output)
Writes to   assets/images/    as <slug>-NN.webp (max side 1200px, quality 82)
and a manifest  scripts/product_images_manifest.json  recording every image's
source URL + authorization status for PENDING-BEFORE-PUBLISH.md.

Idempotent: re-running just rebuilds the same outputs.
"""
import os, json, sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "_raw")
CRONY = os.path.join(RAW, "crony_pool")
MSPOOL = os.path.join(RAW, "pool")
OUT = os.path.join(ROOT, "assets", "images")
os.makedirs(OUT, exist_ok=True)

MAX_SIDE = 1200
QUALITY = 82

SRC_URL = "https://www.cronyfishing.com"
MS_URL = "https://www.minshengfishing.cn"

# slug -> [(source file, source url, source page, alt text)]
MAP = {
    "spinning-rod": [
        ("BassPerchRods-01.jpg", "Galaxy series spinning rod — full rod view — OEM carbon rod manufacturer"),
        ("BassPerchRods-02.jpg", "Spinning rod guide wrap detail — stainless steel frames — OEM carbon rod manufacturer"),
        ("BassPerchRods-03.jpg", "Spinning rod cork handle and reel seat — custom handle options — OEM carbon rod manufacturer"),
        ("BassPerchRods-04.jpg", "Spinning rod reel seat close-up — Fuji-compatible seats — OEM carbon rod manufacturer"),
        ("BassPerchRods-06.jpg", "Full cork handle spinning rod — 2.13–2.29 m, 4–20 lb — OEM carbon rod manufacturer"),
        ("BassPerchRods-11.jpg", "Bass spinning rods in action — freshwater scene — OEM carbon rod manufacturer"),
        ("BassPerchRods-19.jpg", "Master Supreme spinning rod — Toray carbon blank — OEM carbon rod manufacturer"),
        ("BassPerchRods-42.jpg", "More Catch spinning rod — cork handle detail — OEM carbon rod manufacturer"),
    ],
    "carp-rod": [
        ("CarpRods-01.jpg", "Carp rod — Progress Carp full rod — 2.7–3.6 m 2-piece — OEM carbon rod manufacturer"),
        ("CarpRods-02.jpg", "Carp rod blank and guides — slim carbon blank — OEM carbon rod manufacturer"),
        ("CarpRods-03.jpg", "Carp rod reel seat detail — EVA handle — OEM carbon rod manufacturer"),
        ("CarpRods-04.jpg", "Carp rod stainless guide ring — 3 lb test curve — OEM carbon rod manufacturer"),
        ("CarpRods-05.jpg", "Carp rod full profile — 3.6 m 2-piece carp rod — OEM carbon rod manufacturer"),
        ("CarpRods-07.jpg", "Carp rod butt section — reinforced reel seat — OEM carbon rod manufacturer"),
        ("CarpRods-08.jpg", "Carp rod EVA handle — comfortable fish-fighting grip — OEM carbon rod manufacturer"),
    ],
    "saltwater-rod": [
        ("BoatRods-01.jpg", "Boat rod — Measplus series full rod — 20–200 lb — OEM carbon rod manufacturer"),
        ("BoatRods-02.jpg", "Boat rod guide and tip detail — corrosion resistant — OEM carbon rod manufacturer"),
        ("BoatRods-03.jpg", "Boat rod EVA handle and metal wheel seat — OEM carbon rod manufacturer"),
        ("BoatRods-06.jpg", "Boat rod high-strength guide ring — tangle-free design — OEM carbon rod manufacturer"),
        ("BoatRods-09.jpg", "Inshore boat rod — More Catch series — orange baked finish — OEM carbon rod manufacturer"),
        ("BoatRods-13.jpg", "Boat rod split grip handle — graphite reel seat — OEM carbon rod manufacturer"),
        ("BoatRods-15.jpg", "Boat rod reinforced reel seat — heavy duty aluminum — OEM carbon rod manufacturer"),
        ("BoatRods-20.jpg", "Offshore boat rod — full rod with wrapped cork grip — OEM carbon rod manufacturer"),
    ],
    "rock-surf-rod": [
        ("SurfRods-01.jpg", "Surf casting rod — Agress series 4.2 m / 4.5 m — OEM carbon rod manufacturer"),
        ("SurfRods-02.jpg", "Surf rod — telescopic long cast design — OEM carbon rod manufacturer"),
        ("SurfRods-08.jpg", "Surf rod family lineup — multiple lengths and powers — OEM carbon rod manufacturer"),
        ("SurfRods-13.jpg", "Surf fishing scene — anglers landing fish on long cast rods — OEM carbon rod manufacturer"),
        ("SurfRods-16.jpg", "Surf rod test curve chart — blank action reference — OEM carbon rod manufacturer"),
        ("SurfRods-17.jpg", "Surf rod guide and blank detail — reinforced ceramic rings — OEM carbon rod manufacturer"),
        ("SurfRods-20.jpg", "Telescopic surf rod — plug-in joint full view — OEM carbon rod manufacturer"),
        ("SurfRods-25.jpg", "Surf rod extended handle — long casting distance — OEM carbon rod manufacturer"),
    ],
    "about-factory": [
        ("cand_59.jpg", "Carbon rod production line in Weihai, Shandong — OEM carbon rod manufacturer", MS_URL + "/article.html"),
        ("cand_46.jpg", "Automated rod rolling workshop in Weihai, Shandong — OEM carbon rod manufacturer", MS_URL + "/article.html"),
    ],
}

# the two About images live in _raw/pool/ instead of crony_pool
POOL_FILES = {"cand_59.jpg", "cand_46.jpg"}

# source URL lookup for crony images (from crawl index)
crony_idx = json.load(open(os.path.join(RAW, "crony_detail_imgs.json"), encoding="utf-8"))
# map pool filename back to URL via crony_pool_index.json
pool_idx = json.load(open(os.path.join(RAW, "crony_pool_index.json"), encoding="utf-8"))
file2url = {os.path.basename(m["file"]): m["url"] for m in pool_idx}
file2src = {os.path.basename(m["file"]): m["src"] for m in pool_idx}
file2alt = {os.path.basename(m["file"]): m["alt"] for m in pool_idx}


def convert(src_path, dst_path):
    im = Image.open(src_path)
    im = im.convert("RGB")
    w, h = im.size
    scale = min(1.0, MAX_SIDE / max(w, h))
    if scale < 1.0:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.save(dst_path, "WEBP", quality=QUALITY, method=6)
    return im.size


def main():
    manifest = {}
    total = 0
    for slug, entries in MAP.items():
        manifest[slug] = []
        for n, (fname, alt, *rest) in enumerate(entries, 1):
            src_dir = MSPOOL if fname in POOL_FILES else CRONY
            src = None
            for ext in (".jpg", ".png", ".webp", ".jpeg"):
                cand = os.path.join(src_dir, os.path.splitext(fname)[0] + ext)
                if os.path.exists(cand):
                    src = cand
                    break
            if src is None:
                print("!! missing", os.path.join(src_dir, fname))
                continue
            dst = os.path.join(OUT, "%s-%02d.webp" % (slug, n))
            w, h = convert(src, dst)
            if fname in POOL_FILES:
                url = MS_URL + "/article.html"
                page = MS_URL + "/article.html"
                factory = "Weihai Minsheng Sporting Goods (news/article photo)"
            else:
                url = file2url.get(fname, SRC_URL)
                page = SRC_URL + file2src.get(fname, "/")
                factory = "Weihai CRONY Fishing Tackle"
            manifest[slug].append({
                "file": "assets/images/%s-%02d.webp" % (slug, n),
                "source_url": url,
                "source_page": page,
                "factory": factory,
                "alt_en": alt,
                "size": [w, h],
                "bytes": os.path.getsize(dst),
                "authorization": "PENDING — local prototype use only; written factory approval required before publish",
            })
            total += 1
            print("ok %-22s %4dx%-4d %6.1fKB" % ("%s-%02d" % (slug, n), w, h,
                                                 os.path.getsize(dst) / 1024))

    out = os.path.join(HERE, "product_images_manifest.json")
    json.dump(manifest, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    size_mb = sum(i["bytes"] for v in manifest.values() for i in v) / 1048576
    print("\nTOTAL %d images, %.2f MB -> %s" % (total, size_mb, out))


if __name__ == "__main__":
    main()
