"""Write erased (brand-removed) images back into the source pools, then rebuild.

1. Backs up original source files to _raw/crony_pool_backup/
2. Copies _raw/erased/<name>.png over the matching source pool file
3. Crops the parameter table off CarpRods-05 (keep white-background rod shot)
4. Wipes assets/images and lets build_product_images.py rebuild from pools
"""
import os, shutil, sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "_raw")
ERASED = os.path.join(RAW, "erased")
CRONY = os.path.join(RAW, "crony_pool")
MSPOOL = os.path.join(RAW, "pool")
BACKUP = os.path.join(RAW, "crony_pool_backup")
os.makedirs(BACKUP, exist_ok=True)

MAP = {
 "spinning-rod-01.png": "BassPerchRods-01.jpg",
 "spinning-rod-04.png": "BassPerchRods-04.jpg",
 "spinning-rod-05.png": "BassPerchRods-06.jpg",
 "spinning-rod-07.png": "BassPerchRods-19.jpg",
 "carp-rod-01.png": "CarpRods-01.jpg",
 "carp-rod-02.png": "CarpRods-02.jpg",
 "carp-rod-03.png": "CarpRods-03.jpg",
 "carp-rod-06.png": "CarpRods-07.jpg",
 "carp-rod-07.png": "CarpRods-08.jpg",
 "saltwater-rod-01.png": "BoatRods-01.jpg",
 "rock-surf-rod-01.png": "SurfRods-01.jpg",
 "rock-surf-rod-02.png": "SurfRods-02.jpg",
 "rock-surf-rod-03.png": "SurfRods-08.jpg",
 "rock-surf-rod-05.png": "SurfRods-16.jpg",
 "rock-surf-rod-06.png": "SurfRods-17.jpg",
 "about-factory-01.png": os.path.join("..", "pool", "cand_59.jpg"),
}

def src_path(rel):
    return os.path.normpath(os.path.join(CRONY, rel))

done = missed = 0
for erased, src_rel in MAP.items():
    e = os.path.join(ERASED, erased)
    s = src_path(src_rel)
    if not os.path.exists(e):
        print("!! erased missing:", erased); missed += 1; continue
    if not os.path.exists(s):
        print("!! source missing:", s); missed += 1; continue
    bak = os.path.join(BACKUP, os.path.basename(src_rel))
    if not os.path.exists(bak):
        shutil.copyfile(s, bak)
    im = Image.open(e).convert("RGB")
    im.save(s, "JPEG", quality=92)
    print("ok", erased, "->", os.path.basename(src_rel))
    done += 1

# crop parameter table off CarpRods-05 (keep lower white-background rod shot)
s = os.path.join(CRONY, "CarpRods-05.jpg")
bak = os.path.join(BACKUP, "CarpRods-05.jpg")
if not os.path.exists(bak):
    shutil.copyfile(s, bak)
im = Image.open(bak).convert("RGB")
w, h = im.size
im.crop((0, int(h * 0.47), w, h)).save(s, "JPEG", quality=92)
print("ok CarpRods-05 cropped ->", (w, h - int(h * 0.47)))

print("DONE applied=%d missed=%d" % (done, missed))
