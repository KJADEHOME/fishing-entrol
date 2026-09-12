#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Local smoke test for the Entrol Fishing MVP site.

Serves the site root on 127.0.0.1 and verifies:
  1. every page + image returns 200
  2. every JSON-LD block parses with json.loads
  3. sitemap.xml parses with ElementTree and lists all pages
  4. WhatsApp float uses 8615263130999 everywhere
  5. no QQ email addresses in any page
"""
import http.server, socketserver, threading, os, sys, re, json, glob
import urllib.request
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8907

PAGES = ["index.html", "spinning-rods.html", "carp-rods.html", "saltwater-rods.html",
         "rock-surf-rods.html", "products.html", "oem-builder.html", "custom-rod.html",
         "capabilities.html", "process.html", "about.html", "faq.html", "contact.html",
         "blog.html", "australia-fishing-rod-oem-guide.html",
         "australian-surf-rod-specification-guide.html",
         "fishing-rod-oem-moq-sampling-guide.html", "carbon-fishing-rod-blank-guide.html",
         "styles.css", "script.js", "product-gallery.css", "product-gallery.js",
         "robots.txt", "assets/logo.svg"]
IMAGES = sorted(os.path.relpath(p, ROOT).replace("\\", "/")
                for p in glob.glob(os.path.join(ROOT, "assets", "images", "*.webp")))

ok = fail = 0
problems = []


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        problems.append("%s %s" % (label, detail))


def serve():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()


def get(path):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/%s" % (PORT, path), timeout=10) as r:
            return r.status, r.read()
    except Exception as e:
        return 0, str(e).encode()


threading.Thread(target=serve, daemon=True).start()
import time
time.sleep(1.0)

# 1. status codes
for p in PAGES + IMAGES:
    st, _ = get(p)
    check("[200]", st == 200, p)
print("status checks done: %d urls" % (len(PAGES) + len(IMAGES)))

# 2. JSON-LD parse
for p in PAGES:
    if not p.endswith(".html"):
        continue
    _, html = get(p)
    t = html.decode("utf-8", "replace")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    check("[jsonld]", len(blocks) >= 2, "%s has %d blocks" % (p, len(blocks)))
    for i, b in enumerate(blocks):
        try:
            json.loads(b.strip())
            ok += 1
        except Exception as e:
            fail += 1
            problems.append("[jsonld] %s block %d: %s" % (p, i, e))
print("jsonld checks done")

# 3. sitemap
_, sm = get("sitemap.xml")
try:
    tree = ET.fromstring(sm)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [e.text for e in tree.findall(".//s:url/s:loc", ns)]
    HTML_PAGES = [x for x in PAGES if x.endswith(".html")]
    check("[sitemap]", len(locs) == len(HTML_PAGES), "lists %d urls (expected %d)" % (len(locs), len(HTML_PAGES)))
    for p in HTML_PAGES:
        check("[sitemap]", any(l.endswith("/" + p) or (p == "index.html" and l.rstrip("/").endswith("fishing.entrol.com") or l.rstrip("/").endswith("/")) for l in locs), p)
except Exception as e:
    fail += 1
    problems.append("[sitemap] parse error: %s" % e)
print("sitemap checks done")

# 4/5. content rules
qq = re.compile(r"(qq\.com|\d{5,12}@qq)", re.I)
for p in [x for x in PAGES if x.endswith(".html")]:
    _, html = get(p)
    t = html.decode("utf-8", "replace")
    n_wa = len(re.findall(r"wa\.me/8615263130999", t))
    check("[whatsapp]", n_wa >= 1, "%s wa links: %d" % (p, n_wa))
    check("[no-qq]", not qq.search(t), p)
    check("[gtm]", "www.googletagmanager.com/gtm.js" in t and "GTM-T3ZXMRHS" in t, p)
    check("[canonical]", 'rel="canonical"' in t, p)
    check("[og]", 'property="og:image"' in t, p)
    if p.endswith("-guide.html"):
        check("[article]", '"@type": "Article"' in t, p)
        check("[guide-links]", 'href="oem-builder.html"' in t and 'href="contact.html"' in t, p)
# gallery image counts
for slug, fname in [("spinning-rod", "spinning-rods.html"), ("carp-rod", "carp-rods.html"),
                    ("saltwater-rod", "saltwater-rods.html"), ("rock-surf-rod", "rock-surf-rods.html")]:
    _, html = get(fname)
    t = html.decode("utf-8", "replace")
    n = len(re.findall(r'class="pg-item"', t))
    n_imgs = len(glob.glob(os.path.join(ROOT, "assets", "images", slug + "-*.webp")))
    check("[gallery]", n == n_imgs and n >= 6, "%s gallery=%d files=%d" % (fname, n, n_imgs))
    # spec table field coverage
    rows = len(re.findall(r"<tr><td>", t))
    cols = len(re.findall(r"<th>", t))
    check("[spec]", rows >= 2 and cols >= 10, "%s rows=%d cols=%d" % (fname, rows, cols))
# dead internal links
for p in [x for x in PAGES if x.endswith(".html")]:
    _, html = get(p)
    t = html.decode("utf-8", "replace")
    for href in set(re.findall(r'href="([^"#][^"]*)"', t)):
        href = href.split("?")[0]  # ignore query strings (?rod=carp)
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        local = os.path.normpath(os.path.join(ROOT, href))
        check("[link]", os.path.exists(local), "%s -> %s" % (p, href))
print("content checks done")

print("\n========== RESULT: %d passed, %d failed ==========" % (ok, fail))
if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("ALL GREEN")
