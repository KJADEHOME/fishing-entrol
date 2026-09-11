"""Pass 4: deterministic text removal via median-diff mask + inpaint.
Targets fine lettering strokes; drops large structures (guides, hardware)."""
import os, sys, json, shutil
import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "images")
OUT = os.path.join(ROOT, "_raw", "erased4")
os.makedirs(OUT, exist_ok=True)

# file -> (median ksize, diff threshold, max component area)
JOBS = {
 "spinning-rod-04.webp": (41, 38, 30000),
 "carp-rod-06.webp":     (41, 34, 30000),
 "saltwater-rod-01.webp":(41, 34, 30000),
 "saltwater-rod-05.webp":(41, 36, 30000),
 "rock-surf-rod-03.webp":(41, 34, 30000),
}

for name, (ks, thr, max_area) in JOBS.items():
    p = os.path.join(IMG, name)
    img = cv2.imread(p)
    h, w = img.shape[:2]
    med = cv2.medianBlur(img, ks)
    diff = cv2.absdiff(img, med).max(axis=2)
    mask = (diff > thr).astype(np.uint8) * 255
    # drop large components (guides, reel seats, photo blocks) - keep fine strokes
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > max_area:
            mask[labels == i] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel, iterations=2)
    res = cv2.inpaint(img, mask, 4, cv2.INPAINT_TELEA)
    out = os.path.join(OUT, name.replace(".webp", ".png"))
    cv2.imwrite(out, res)
    print("ok", name, "mask_px=%d" % int((mask > 0).sum()))
print("PASS4 DONE")
