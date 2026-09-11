#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Static site generator for Entrol Fishing (entrol-fishing.com).

Idempotent: re-running rebuilds every page from the content definitions below.
All copy is ORIGINAL — never copied from other sites in the network (anti
template-spam rule). Technical facts (specs, factory credentials) come only
from factory-published sources recorded in scripts/product_images_manifest.json
and PENDING-BEFORE-PUBLISH.md.
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAIN = "https://www.entrol-fishing.com"
BRAND = "Entrol Fishing"
LEGAL = "Entrol Fishing — Weihai sourcing office"
EMAIL = "sales@entrol-fishing.com"
WA = "8615263130999"
WA_TEXT = "Hi%20Entrol%20Fishing%2C%20I%27d%20like%20a%20quote%20for%20OEM%20fishing%20rods."
WECHAT = "15263130999"
GTM_ID = "GTM-T3ZXMRHS"
FORM_ENDPOINT = "https://formsubmit.co/wangyan@entrol.com"
OG_IMAGE = DOMAIN + "/assets/images/spinning-rod-01.webp"
TODAY = "2026-09-11"

MANIFEST = json.load(open(os.path.join(ROOT, "scripts", "product_images_manifest.json"), encoding="utf-8"))

NAV = [
    ("index.html", "Home"),
    ("products.html", "Products"),
    ("configure.html", "Build Your Rod"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]
PRODUCT_NAV = [
    ("spinning-rods.html", "Spinning & Casting Rods"),
    ("carp-rods.html", "Carp Rods"),
    ("saltwater-rods.html", "Saltwater & Boat Rods"),
    ("rock-surf-rods.html", "Rock & Surf Rods"),
]
# category slug -> configurator preset key (read by script.js from ?rod=)
CFG_KEY = {
    "spinning-rod": "spinning",
    "carp-rod": "carp",
    "saltwater-rod": "boat",
    "rock-surf-rod": "surf",
}

LOGO_SVG = """<svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#0E6E8C"/><path d="M6 22c6-1 9-4 11-8 1.4-2.8 2.4-5.4 4.6-7.2.5-.4 1.2.2.9.8-1 2-1.4 4-1.2 6.2l3.4 1.5c.6.3.5 1.1-.1 1.3l-3.6 1c-1.3 3.4-4.3 6.9-9 7.6-2.3.4-4.6.2-6-.2-.6-.2-.6-1 0-1z" fill="#fff"/><circle cx="21.5" cy="9.5" r="1.4" fill="#0E6E8C"/></svg>"""


def wa_link(text=None):
    t = text or WA_TEXT
    return "https://wa.me/%s?text=%s" % (WA, t)


def gallery(slug):
    """Build the pg- gallery HTML for a category slug from the manifest."""
    items = []
    for m in MANIFEST.get(slug, []):
        items.append(
            '        <figure class="pg-item"><img src="%s" alt="%s" loading="lazy" decoding="async"></figure>'
            % (m["file"], m["alt_en"]))
    if not items:
        return ""
    return ('<div class="pg-grid" data-pg-gallery data-pg-caption="%s">\n%s\n      </div>'
            % (BRAND, "\n".join(items)))


# --------------------------------------------------------------------------
# spec data — transcribed from factory-published parameter sheets only
# --------------------------------------------------------------------------
SPIN_ROWS = [
    ["CRS721LXF", "2.19 m (7'2\")", "2.19 m", "1", "100 g", "Light / Fast", "1.7 / 11.1 mm", "4–10 lb", "Cork", "—"],
    ["CRS731MLF", "2.21 m (7'3\")", "2.21 m", "1", "108 g", "Medium-Light / Fast", "1.8 / 11.5 mm", "6–12 lb", "Cork", "—"],
    ["CRS741MF", "2.23 m (7'4\")", "2.23 m", "1", "105 g", "Medium / Fast", "1.9 / 11.5 mm", "8–17 lb", "Cork", "—"],
    ["CRS751MHF", "2.26 m (7'5\")", "2.26 m", "1", "131 g", "Medium-Heavy / Fast", "1.8 / 12.0 mm", "10–20 lb", "Cork", "—"],
    ["CRC721MF (cast)", "2.19 m (7'2\")", "2.19 m", "1", "119 g", "Medium / Fast", "1.7 / 11.6 mm", "8–14 lb", "Cork", "—"],
    ["CRC741MHF (cast)", "2.23 m (7'4\")", "2.23 m", "1", "126 g", "Medium-Heavy / Fast", "1.8 / 12.0 mm", "8–17 lb", "Cork", "—"],
    ["CRC761XH (cast)", "2.29 m (7'6\")", "2.29 m", "1", "135 g", "Extra-Heavy / Fast", "2.3 / 12.7 mm", "10–25 lb", "Cork", "—"],
]
SPIN_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Action / Power",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

CARP_ROWS = [
    ["PRC-9300", "2.70 m (9'0\")", "140 cm", "2", "256 g", "3.0 lb test curve", "2.6 / 14.9 mm", "—", "Slim EVA + duplon", "—"],
    ["PRC-10300", "3.00 m (10'0\")", "156 cm", "2", "315 g", "3.0 lb test curve", "2.7 / 16.0 mm", "—", "Slim EVA + duplon", "—"],
    ["PRC-12275", "3.60 m (12'0\")", "186 cm", "2", "386 g", "2.75 lb test curve", "2.7 / 16.4 mm", "—", "Slim EVA + duplon", "—"],
    ["PRC-12300", "3.60 m (12'0\")", "186 cm", "2", "421 g", "3.0 lb test curve", "2.7 / 16.8 mm", "—", "Slim EVA + duplon", "—"],
]
CARP_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Test Curve",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

BOAT_ROWS = [
    ["MPB66HC", "1.98 m (6'6\")", "1.98 m", "1", "444 g", "20–50 lb class", "3.0 / 12.0 mm", "20–50 lb", "EVA", "—"],
    ["MPB66XHC", "1.98 m (6'6\")", "1.98 m", "1", "465 g", "60–100 lb class", "3.3 / 12.7 mm", "60–100 lb", "EVA", "—"],
    ["MPB66XXHC", "1.98 m (6'6\")", "1.98 m", "1", "508 g", "80–200 lb class", "3.7 / 13.7 mm", "80–200 lb", "EVA", "—"],
]
BOAT_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Line Class",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

JIG_ROWS = [
    ["ASJS581 (spin)", "1.73 m (5'8\")", "127 cm", "1.5 (jointed)", "152 g", "MAX 550 g jig", "2.7 / 12.7 mm", "PE 2.5–4", "EVA", "—"],
    ["ASJS631 (spin)", "1.91 m (6'3\")", "145 cm", "1.5 (jointed)", "144 g", "MAX 300 g jig", "2.1 / 11.5 mm", "PE 1.5–2.5", "EVA", "—"],
    ["ASJS631 (spin)", "1.91 m (6'3\")", "145 cm", "1.5 (jointed)", "131 g", "MAX 220 g jig", "1.9 / 11.5 mm", "PE 1.0–2.0", "EVA", "—"],
    ["ASJC581 (cast)", "1.73 m (5'8\")", "127 cm", "1.5 (jointed)", "160 g", "MAX 550 g jig", "2.7 / 12.5 mm", "PE 2.5–4", "EVA", "—"],
    ["ASJC631 (cast)", "1.91 m (6'3\")", "145 cm", "1.5 (jointed)", "152 g", "MAX 300 g jig", "2.0 / 11.6 mm", "PE 1.5–2.5", "EVA", "—"],
    ["ASJC631 (cast)", "1.91 m (6'3\")", "145 cm", "1.5 (jointed)", "138 g", "MAX 120 g jig", "1.8 / 11.0 mm", "PE 0.5–1.5", "EVA", "—"],
]
JIG_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Jig Rating",
            "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

SURF_ROWS = [
    ["AGSF4203", "4.20 m (13'9\")", "148 cm", "3 (plug-in)", "578 g", "Fast", "3.17 / 23.4 mm", "120–250 g cast", "Anti-slip EVA", "—"],
    ["AGSF4503", "4.50 m (14'9\")", "158 cm", "3 (plug-in)", "658 g", "Fast", "3.26 / 24.2 mm", "150–280 g cast", "Anti-slip EVA", "—"],
]
SURF_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Action",
             "Tip / Butt Dia.", "Cast Weight", "Handle", "Carbon Grade"]

MOQ_NOTE = ("MOQ 300 pcs per model · Sample lead time 15–20 days · Production lead time 35–45 days "
            "after sample approval. Custom length, action, components and branding available on request.")


def spec_table(cols, rows, caption):
    th = "".join("<th>%s</th>" % c for c in cols)
    trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ('<div class="table-wrap"><table class="spec"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div><p class="table-note">%s</p>' % (th, trs, caption))


def jsonld(blocks):
    out = []
    for b in blocks:
        out.append('<script type="application/ld+json">\n%s\n  </script>' % json.dumps(b, ensure_ascii=False, indent=2))
    return "\n  ".join(out)


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": BRAND,
    "url": DOMAIN + "/",
    "logo": DOMAIN + "/assets/logo.svg",
    "description": "Overseas sales office for carbon fiber fishing rod factories in Weihai, Shandong, China. "
                   "OEM/ODM spinning, carp, saltwater and surf rods with low MOQs and full customization.",
    "email": EMAIL,
    "telephone": "+8615263130999",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Weihai",
        "addressRegion": "Shandong",
        "addressCountry": "CN",
    },
}


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + f}
            for i, (f, n) in enumerate(items)
        ],
    }


def webpage_ld(name, desc, path):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": desc,
        "url": DOMAIN + "/" + path,
        "isPartOf": {"@type": "WebSite", "name": BRAND, "url": DOMAIN + "/"},
    }


def head(title, desc, keywords, path, extra_ld=""):
    return """<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(t)s</title>
  <meta name="description" content="%(d)s">
  <meta name="keywords" content="%(k)s">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="%(domain)s/%(p)s">
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="%(t)s">
  <meta property="og:description" content="%(d)s">
  <meta property="og:url" content="%(domain)s/%(p)s">
  <meta property="og:image" content="%(og)s">
  <meta property="og:site_name" content="%(brand)s">
  <meta property="og:locale" content="en_US">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="%(t)s">
  <meta name="twitter:description" content="%(d)s">
  <meta name="twitter:image" content="%(og)s">
  <link rel="icon" type="image/svg+xml" href="assets/logo.svg">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="product-gallery.css">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','%(gtm)s');</script>
  <!-- End Google Tag Manager -->
  %(ld)s""" % {
        "t": title, "d": desc, "k": keywords, "domain": DOMAIN, "p": path,
        "og": OG_IMAGE, "brand": BRAND, "gtm": GTM_ID, "ld": extra_ld,
    }


GTM_NOSCRIPT = ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" '
                'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' % GTM_ID)


def nav_html(active):
    def link(f, label):
        cls = ' class="active"' if f == active else ""
        return '<a href="%s"%s>%s</a>' % (f, cls, label)
    prod_dd = (
        '<li class="nav-dropdown">%s<ul>%s</ul></li>'
        % (link("products.html", "Products"),
           "".join("<li>%s</li>" % link(f, l) for f, l in PRODUCT_NAV)))
    items = []
    for f, l in NAV:
        if f == "products.html":
            items.append(prod_dd)
        else:
            items.append("<li>%s</li>" % link(f, l))
    return "".join(items)


def footer_html():
    prod = "".join('<li><a href="%s">%s</a></li>' % (f, l) for f, l in PRODUCT_NAV)
    comp = "".join('<li><a href="%s">%s</a></li>' % (f, l) for f, l in NAV if f != "products.html")
    return """
<div class="container">
  <div class="footer-grid">
    <div class="footer-brand">
      <h4>%(brand)s</h4>
      <p>Overseas sales office for carbon fiber fishing rod factories in Weihai, Shandong —
         China's fishing tackle manufacturing capital. OEM and ODM programs for importers,
         brands and tackle retailers in Australia, Europe, Japan and Korea.</p>
    </div>
    <div>
      <h4>Rod Categories</h4>
      <ul>%(prod)s</ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>%(comp)s</ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul class="footer-contact">
        <li><strong>Email:</strong> <a href="mailto:%(email)s">%(email)s</a></li>
        <li><strong>WhatsApp:</strong> <a href="%(wa)s">+86 152 6313 0999</a></li>
        <li><strong>WeChat:</strong> %(wechat)s</li>
        <li><strong>Works:</strong> Weihai City, Shandong Province, China</li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 %(brand)s. All rights reserved.</span>
    <span>Carbon fishing rod OEM / ODM · Weihai, Shandong, China</span>
  </div>
</div>""" % {"brand": BRAND, "prod": prod, "comp": comp, "email": EMAIL,
             "wa": wa_link(), "wechat": WECHAT}


FLOAT_HTML = """
<a class="wa-float" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 3C9.4 3 4 8.3 4 14.9c0 2.6.8 5 2.3 7L4 29l7.3-2.3c1.9 1 4 1.6 6.2 1.6h.5c6.6 0 12-5.3 12-11.9C30 8.3 22.6 3 16 3zm7 17c-.3.8-1.7 1.6-2.4 1.7-.6.1-1.4.1-2.2-.1-.5-.2-1.2-.4-2-.8-3.5-1.5-5.8-5-6-5.3-.2-.2-1.4-1.9-1.4-3.6 0-1.7.9-2.6 1.2-2.9.3-.3.7-.4 1-.4h.7c.2 0 .5-.1.8.6.3.8 1 2.7 1.1 2.9.1.2.2.4 0 .7-.1.2-.2.4-.4.6l-.6.7c-.2.2-.4.4-.2.8.2.4 1 1.7 2.2 2.7 1.5 1.4 2.8 1.8 3.2 2 .4.2.6.2.9-.1.2-.3 1-1.2 1.3-1.6.3-.4.5-.3.9-.2.4.1 2.3 1.1 2.7 1.3.4.2.6.3.7.5.1.2.1 1-.2 1.8z"/></svg>
</a>
<button class="wc-float" aria-label="WeChat contact" title="WeChat: %(wechat)s">
  <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M11.5 4C6.3 4 2 7.6 2 12.1c0 2.6 1.4 4.9 3.6 6.4l-.9 2.8 3.2-1.7c.9.3 1.8.4 2.8.5-.2-.6-.3-1.3-.3-2 0-4.3 4.1-7.7 9.1-7.7h.6C19.3 7 15.8 4 11.5 4zM8.6 8.2c.6 0 1.1.5 1.1 1.1S9.2 10.4 8.6 10.4s-1.1-.5-1.1-1.1.5-1.1 1.1-1.1zm5.8 0c.6 0 1.1.5 1.1 1.1s-.5 1.1-1.1 1.1-1.1-.5-1.1-1.1.5-1.1 1.1-1.1zM20 11.5c-4.4 0-8 3-8 6.7s3.6 6.7 8 6.7c.9 0 1.7-.1 2.5-.4l2.8 1.5-.8-2.4c1.9-1.2 3.5-3.2 3.5-5.4 0-3.7-3.6-6.7-8-6.7zm-2.7 3.7c.5 0 .9.4.9.9s-.4.9-.9.9-.9-.4-.9-.9.4-.9.9-.9zm5.4 0c.5 0 .9.4.9.9s-.4.9-.9.9-.9-.4-.9-.9.4-.9.9-.9z"/></svg>
</button>
<div class="wc-modal" role="dialog" aria-modal="true" aria-label="WeChat contact">
  <div class="wc-modal-card">
    <button class="wc-close" aria-label="Close">&times;</button>
    <h3>Chat on WeChat</h3>
    <p class="form-hint">Add us on WeChat for fast answers on OEM rod programs (GMT+8).</p>
    <div class="wc-id">%(wechat)s</div>
    <p class="form-hint">Or email <a href="mailto:%(email)s">%(email)s</a></p>
  </div>
</div>""" % {"wa": wa_link(), "wechat": WECHAT, "email": EMAIL}


def page(fname, title, desc, keywords, body, ld_blocks, hero=None):
    path = fname if fname != "index.html" else ""
    crumbs = [("index.html", "Home")]
    if fname != "index.html":
        crumbs.append((fname, title.split("|")[0].strip()))
    head_html = head(title, desc, keywords, path, jsonld(ld_blocks))
    breadcrumb = "" if fname == "index.html" else (
        '<nav class="breadcrumb container" aria-label="Breadcrumb">%s</nav>'
        % " &rsaquo; ".join('<a href="%s">%s</a>' % (f, n) for f, n in crumbs[:-1])
        + ' &rsaquo; <span aria-current="page">%s</span>' % crumbs[-1][1])
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  %(head)s
</head>
<body>
%(ns)s
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="index.html">%(logo)s<span>%(brand)s<span class="logo-sub">Weihai &middot; Carbon Rod OEM</span></span></a>
    <button class="nav-toggle" aria-label="Toggle navigation"><span></span><span></span><span></span></button>
    <nav class="main-nav" aria-label="Main">
      <ul>%(nav)s</ul>
    </nav>
  </div>
</header>
<main>
%(crumb)s
%(body)s
</main>
<footer class="site-footer">%(footer)s</footer>
%(float)s
<script src="script.js"></script>
<script src="product-gallery.js"></script>
</body>
</html>""" % {
        "head": head_html, "ns": GTM_NOSCRIPT, "logo": LOGO_SVG, "brand": BRAND,
        "nav": nav_html(fname), "crumb": breadcrumb, "body": body,
        "footer": footer_html(), "float": FLOAT_HTML,
    }
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", fname, "(%d KB)" % (len(html.encode()) // 1024))


# ==========================================================================
# PAGE CONTENT (original copy — do not reuse on other sites)
# ==========================================================================

def build_index():
    title = "Carbon Fiber Fishing Rod Manufacturer | OEM From Weihai"
    assert len(title) <= 65
    desc = ("OEM/ODM carbon fiber rods from Weihai, China — spinning, carp, boat and surf rods. "
            "MOQ 300 pcs/model, samples in 15–20 days. Get a quote today.")
    assert len(desc) <= 160
    kw = ("carbon fiber fishing rod manufacturer, fishing rod OEM supplier China, custom fishing rod "
          "manufacturer, Weihai fishing rod factory, spinning rod OEM, carp rod manufacturer")
    body = """
<section class="hero">
  <div class="container">
    <span class="eyebrow">Weihai &middot; Shandong &middot; China</span>
    <h1>Carbon Fiber Fishing Rods, Built to Your Specification</h1>
    <p class="lead">You decide the rod: carbon grade, guide train, reel seat, handle shape,
    cosmetics and packaging. We build it in Weihai — the city that produces the majority of the
    world's fishing rods — from 300 pieces per model, under your own brand.</p>
    <div class="btn-row">
      <a class="btn btn-accent" href="configure.html">Build Your Rod &rarr;</a>
      <a class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,.7)" href="products.html">Browse Rod Categories</a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>MOQ 300</strong><span>pieces per model</span></div>
      <div class="hero-stat"><strong>15–20 days</strong><span>sample lead time</span></div>
      <div class="hero-stat"><strong>15–20 days</strong><span>sea freight to Australia</span></div>
      <div class="hero-stat"><strong>&lt;24 h</strong><span>inquiry response (GMT+8)</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">Rod Categories</span>
      <h2>Four Programs, One Supply Chain</h2>
      <p class="lead">Every category below is produced in Weihai on high-tonnage carbon blanks with
      full customization of length, action, components, cosmetics and packaging.</p>
    </div>
    <div class="grid grid-4" style="margin-top:38px">
      <div class="card cat-card">
        <img src="assets/images/spinning-rod-01.webp" alt="Spinning and casting rods — OEM carbon rod manufacturer" loading="lazy" decoding="async">
        <div class="cat-body"><span class="cat-tag">Australia &middot; Japan</span>
        <h3><a href="spinning-rods.html">Spinning &amp; Casting Rods</a></h3>
        <p>Bass, estuary and light inshore programs. Cork or EVA handles, 4–25 lb ratings.</p></div>
      </div>
      <div class="card cat-card">
        <img src="assets/images/carp-rod-01.webp" alt="Carp fishing rods — European style carbon carp rod manufacturer" loading="lazy" decoding="async">
        <div class="cat-body"><span class="cat-tag">UK &middot; Europe</span>
        <h3><a href="carp-rods.html">Carp Rods</a></h3>
        <p>9–12 ft two-piece carp rods, 2.75–3.0 lb test curves for European specimen anglers.</p></div>
      </div>
      <div class="card cat-card">
        <img src="assets/images/saltwater-rod-01.webp" alt="Saltwater and boat fishing rods — heavy tackle carbon rod manufacturer" loading="lazy" decoding="async">
        <div class="cat-body"><span class="cat-tag">Australia &middot; Coastal EU</span>
        <h3><a href="saltwater-rods.html">Saltwater &amp; Boat Rods</a></h3>
        <p>20–200 lb class boat sticks and slow jigging rods with corrosion-resistant components.</p></div>
      </div>
      <div class="card cat-card">
        <img src="assets/images/rock-surf-rod-01.webp" alt="Rock and surf casting rods — long cast carbon rod manufacturer" loading="lazy" decoding="async">
        <div class="cat-body"><span class="cat-tag">Japan &middot; Korea &middot; S. Europe</span>
        <h3><a href="rock-surf-rods.html">Rock &amp; Surf Rods</a></h3>
        <p>4.2–4.5 m long-cast surf rods and shore jigging sticks built for big water.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Why Source From Weihai</span>
      <h2>The World's Rod Factory Is a City, Not a Company</h2>
      <p class="lead">Nearly six in ten fishing rods sold worldwide are made in Weihai, Shandong.
      Working with %(brand)s puts you inside that cluster — blank rolling, component supply,
      painting and assembly within a single industrial base.</p>
      <ul class="feature-list">
        <li>High-tonnage carbon blanks (24T and above) with documented material sourcing</li>
        <li>Full OEM/ODM: length, action, guides, reel seats, grip, cosmetics, packaging</li>
        <li>Zero tariff on fishing tackle into Australia under the China–Australia FTA</li>
        <li>15–20 day sea freight to Australian ports, smaller time-zone gap than Europe</li>
        <li>One contact in your time zone for quotes, samples, QC and shipment documents</li>
      </ul>
    </div>
    <div class="card" style="padding:0;overflow:hidden">
      <img src="assets/images/about-factory-01.webp" alt="Carbon rod production line in Weihai, Shandong — OEM carbon rod manufacturer" loading="lazy" decoding="async">
      <div style="padding:20px 22px"><p class="form-hint">Rod rolling and assembly line at a partner
      factory in Weihai, Shandong, China.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">How We Work</span>
      <h2>From Spec Sheet to Shipment</h2>
    </div>
    <div class="grid grid-4" style="margin-top:36px">
      <div class="card"><h3>1 &middot; Specification</h3><p>Send a reference rod, a spec table or just
      your target fish and price point. We translate it into a buildable blank spec.</p></div>
      <div class="card"><h3>2 &middot; Sample</h3><p>Pre-production sample in 15–20 days. Test it on
      the water before you commit to volume.</p></div>
      <div class="card"><h3>3 &middot; Production</h3><p>35–45 days after sample approval, with
      in-line QC and photo reports at each milestone.</p></div>
      <div class="card"><h3>4 &middot; Delivery</h3><p>Consolidated sea or air freight, full export
      documentation, and after-shipment support.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">OEM Configurator</span>
      <h2>Build the Rod You Sell — Component by Component</h2>
      <p class="lead">Nothing here is fixed. Pick the components your market actually asks for and
      we quote the rod that comes out the other end.</p>
    </div>
    <div class="cfg-why" style="margin-top:32px">
      <div class="card"><h4>Carbon grade</h4><p>24T to 46T cloth, mixed layups or glass composite —
      you set the balance of weight, sensitivity and cost that your price point needs.</p></div>
      <div class="card"><h4>Guide train</h4><p>Single-foot, double-foot, KW anti-tangle or micro
      guides, in Alconite, SiC or Torzite, on stainless or titanium frames.</p></div>
      <div class="card"><h4>Reel seat &amp; handle</h4><p>Fuji VSS, ECS, ACS or TCS; split or full
      grip; cork, EVA or carbon; trigger or straight — matched to spinning or baitcasting reels.</p></div>
      <div class="card"><h4>Your brand, your pack</h4><p>Silk-screen, laser or hydro-dip logo, plus
      rod bag, tube or printed retail box. You sell it under your name.</p></div>
    </div>
    <div class="center" style="margin-top:30px">
      <a class="btn btn-accent" href="configure.html">Open the Configurator &rarr;</a>
      <p class="form-hint" style="margin-top:12px">About two minutes. Skip anything you are unsure
      about — we will advise on the rest.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Rather Just Talk to Someone?</h2>
      <p>Send a photo or a link to a rod you like and we will reverse-engineer the specification, or
      simply tell us your market and target price. Quotation within one business day.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Request a Quote</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp Us Now</a>
      </div>
    </div>
  </div>
</section>""" % {"brand": BRAND, "wa": wa_link()}

    ld = [ORG_LD, webpage_ld(title, desc, ""),
          breadcrumb_ld([("index.html", "Home")])]
    page("index.html", title, desc, kw, body, ld)


def cat_page(fname, slug, title, h1, desc, kw, intro_html, cols, rows, table_note,
             custom_html, ld_extra):
    crumbs = [("index.html", "Home"), ("products.html", "Products"), (fname, h1)]
    crumb_ld = breadcrumb_ld(crumbs)
    product_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": h1,
        "description": desc,
        "image": [DOMAIN + "/" + m["file"] for m in MANIFEST.get(slug, [])][:6],
        "brand": {"@type": "Brand", "name": BRAND},
        "manufacturer": {"@type": "Organization", "name": BRAND, "url": DOMAIN + "/"},
        "category": h1,
        "material": "Carbon fiber composite",
    }
    body = """
%(breadcrumb)s
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Weihai &middot; Shandong &middot; China</span>
    <h1>%(h1)s</h1>
    %(intro)s
    <div class="btn-row">
      <a class="btn btn-primary" href="contact.html">Request a Quote</a>
      <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp +86 152 6313 0999</a>
    </div>
  </div>
</section>
<section class="section section-alt pg-section">
  <div class="container">
    <div class="pg-head">
      <p class="pg-eyebrow">Factory Reference Gallery</p>
      <h2 class="pg-title">%(h1)s — Production Reference</h2>
      <p class="pg-sub">Product, detail and application photos from our Weihai partner factory floor.
      Click any image to enlarge.</p>
    </div>
    %(gallery)s
    <div class="pg-cta">
      <p>Need a different length, action, guide train or private-label finish? Every rod below can be re-specced.</p>
      <div class="pg-cta-btns">
        <a class="btn btn-primary" href="contact.html">Request a Quote</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <span class="eyebrow">Specifications</span>
    <h2>Reference Specification Table</h2>
    <p class="lead">Real production data from current Weihai tooling. Any model can be customized —
    treat these as the starting point of your own program.</p>
    %(table)s
  </div>
</section>
<section class="section section-alt">
  <div class="container grid grid-2">
    %(custom)s
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>Configure Your %(h1short)s Specification</h2>
      <p>%(moq)s Choose carbon grade, guide train, reel seat, handle and packaging in the
      configurator — you will have a quotable specification in about two minutes.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="configure.html?rod=%(cfgkey)s">Open the Rod Configurator</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp Us</a>
      </div>
    </div>
  </div>
</section>""" % {
        "breadcrumb": "", "h1": h1, "h1short": h1.split(" — ")[0], "intro": intro_html,
        "wa": wa_link(), "cfgkey": CFG_KEY.get(slug, "spinning"),
        "gallery": gallery(slug), "table": spec_table(cols, rows, table_note),
        "custom": custom_html, "moq": MOQ_NOTE,
    }
    page(fname, title, desc, kw, body, [ORG_LD, webpage_ld(title, desc, fname), crumb_ld, product_ld])


def build_spinning():
    title = "Spinning Rod OEM & ODM | Carbon Bass Rods | Entrol Fishing"
    desc = ("Custom spinning and casting rods from Weihai, China. 2.13–2.29 m carbon blanks, cork "
            "handles, 4–25 lb. MOQ 300/model, samples 15–20 days. Request a quotation.")
    kw = ("spinning rod OEM, spinning rod manufacturer China, custom bass rod, carbon casting rod "
          "supplier, Weihai fishing rod factory, lure rod ODM")
    intro = """
    <p class="lead">Spinning and casting rods are the volume workhorse of every tackle program — and
    the category where Weihai's supply chain is deepest. Our partner lines roll 24T+ carbon blanks
    for freshwater bass and perch fishing, estuary flathead and bream work, and light inshore
    species. Australian and Japanese buyers account for the largest share of this program, and the
    blanks below are proven in those markets.</p>
    <p class="lead">Who fishes them: weekend bass anglers on lakes and rivers, estuary anglers
    targeting flathead and bream with soft plastics, and light-tackle inshore anglers chasing
    jacks and small trevally. One-piece blanks with fast tapers for sensitivity; casting variants
    with reinforced reel seats for baitcasting reels.</p>"""
    custom = """
    <div>
      <span class="eyebrow">Customization</span>
      <h2>Make It Your Program</h2>
      <ul class="feature-list">
        <li><strong>Length &amp; power:</strong> 1.98–2.59 m, Ultra-Light to Extra-Heavy, action tuned per blank</li>
        <li><strong>Carbon:</strong> 24T / 30T / 40T layups; X-wrap or standard carbon cloth</li>
        <li><strong>Guides:</strong> stainless or Fuji Alconite / SiC trains, single-foot or double-foot</li>
        <li><strong>Reel seat:</strong> graphite or aluminum, Fuji VSS style available</li>
        <li><strong>Handle:</strong> Portuguese cork, EVA, split-grip or full grip</li>
        <li><strong>Cosmetics &amp; packaging:</strong> your logo, color wrap, rod sock, tube and retail box</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">Market Fit</span>
      <h2>Built for AU &amp; JP Retail Programs</h2>
      <p class="lead">Under the China–Australia FTA, fishing tackle enters Australia duty-free, and
      sea freight from Weihai to major Australian ports runs 15–20 days. For Japanese buyers we
      build tighter-taper JDM-style blanks with lighter guide trains. MOQ 300 pieces per model
      keeps first programs manageable; mixed-model containers are welcome.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Discuss a Spinning Program</a></div>
    </div>"""
    cat_page("spinning-rods.html", "spinning-rod", title,
             "Spinning & Casting Rods — Carbon Bass Rod Manufacturer",
             desc, kw, intro, SPIN_COLS, SPIN_ROWS,
             MOQ_NOTE, custom, None)


def build_carp():
    title = "Carp Rod Manufacturer Europe | 12ft OEM Carp Rods | Entrol Fishing"
    desc = ("European-style carp rods made in Weihai, China: 9–12 ft two-piece blanks, 2.75–3.0 lb "
            "test curves, EVA handles. MOQ 300/model, REACH-aware finishes. Get a quote today.")
    kw = ("carp fishing rod manufacturer, 12ft carp rod OEM, European carp rod supplier, custom carp "
          "rod China, specimen rod manufacturer, Weihai carp rod factory")
    intro = """
    <p class="lead">Carp angling is the backbone of the European tackle market, and it is the most
    margin-rich rod category we build. The blanks below follow the European convention: two-piece
    construction, 2.75–3.0 lb test curves, slim diameters and subdued cosmetics that UK and
    continental anglers expect. If your range needs 10 ft stalking rods or 13 ft spod and marker
    rods, those are built on the same tooling.</p>
    <p class="lead">Who fishes them: specimen carp anglers fishing lakes, rivers and commercials
    across the UK, France, Germany, the Netherlands and Italy — anglers who cast 100 m+ with heavy
    leads and PVA bags and who judge a rod by its recovery rate and blank recovery speed.</p>"""
    custom = """
    <div>
      <span class="eyebrow">Customization</span>
      <h2>Spec It Like a European Brand</h2>
      <ul class="feature-list">
        <li><strong>Length:</strong> 9 ft stalking, 10 ft, 12 ft standard, 13 ft spod / marker</li>
        <li><strong>Test curve:</strong> 2.5 lb, 2.75 lb, 3.0 lb, 3.25 lb, 3.5 lb — verified per blank</li>
        <li><strong>Handle:</strong> slim duplon, shrink wrap, cork;Japanese-style abbreviated handles</li>
        <li><strong>Guides:</strong> 50 mm butt rings available; anti-friction SIC options</li>
        <li><strong>Cosmetics:</strong> matte "continental" finishes, stealth black, custom logo placement</li>
        <li><strong>Compliance:</strong> REACH-aware coating choices; UKCA documentation discussed per order</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">Market Fit</span>
      <h2>UK &amp; Europe First</h2>
      <p class="lead">Europe is where carp fishing earns its premium. We quote EU-bound programs with
      documentation your compliance team can review — material declarations and coating compliance
      discussed before contract, not after. Sea freight to northern European ports via Weihai runs
      roughly 30–35 days; plan sampling accordingly.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Discuss a Carp Program</a></div>
    </div>"""
    cat_page("carp-rods.html", "carp-rod", title,
             "Carp Rods — 9–12 ft Carbon Carp Rod Manufacturer for Europe",
             desc, kw, intro, CARP_COLS, CARP_ROWS, MOQ_NOTE, custom, None)


def build_saltwater():
    title = "Boat Rod Manufacturer | 20–200 lb Saltwater Rods OEM | Entrol Fishing"
    desc = ("Saltwater boat rods and slow jigging rods from Weihai, China. 20–200 lb class blanks, "
            "corrosion-resistant components, MOQ 300/model. Samples in 15–20 days.")
    kw = ("boat rod manufacturer, saltwater fishing rod OEM, slow jigging rod supplier, deep sea rod "
          "China, 200 lb game rod manufacturer, Weihai boat rod factory")
    intro = """
    <p class="lead">Australia's coastline makes saltwater the highest-repeat category for local
    tackle retailers. This program covers two distinct builds: stand-up boat rods rated 20–200 lb
    for reef, bottom and light game work, and short jointed jigging rods rated by jig weight (MAX
    120–550 g) for slow-pitch and high-pitch techniques. Both are built around corrosion
    resistance — reinforced ceramic guides, metal reel seats and baked finishes that survive
    salt, sun and rod holders.</p>
    <p class="lead">Who fishes them: trailer-boat anglers bottom fishing reef species, kayak and
    inshore anglers working metal jigs, and charter operators who need durable sticks that survive
    heavy daily use. Buyers in coastal Europe and the Gulf add this program for charter fleets.</p>"""
    custom = """
    <div>
      <span class="eyebrow">Customization</span>
      <h2>Spec for Salt, Not the Showroom</h2>
      <ul class="feature-list">
        <li><strong>Line class:</strong> 20–50, 60–100, 80–200 lb — butt and tip dia. tuned per rating</li>
        <li><strong>Jig ratings:</strong> MAX 120 g to MAX 550 g, spin or cast configurations</li>
        <li><strong>Guides:</strong> reinforced ceramic ring guides; Fuji SIC trains on premium builds</li>
        <li><strong>Reel seat:</strong> graphite or aluminum with extended hoods for heavy drags</li>
        <li><strong>Finish:</strong> corrosion-resistant baked paint;gimbal butt options on 80 lb+ sticks</li>
        <li><strong>Branding:</strong> charter-quantity pricing for fleet programs</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">Market Fit</span>
      <h2>Australia Leads, Europe Follows</h2>
      <p class="lead">Duty-free entry into Australia under ChAFTA plus 15–20 day sea freight makes
      replenishing boat-rod stock predictable ahead of the southern spring season. European charter
      and Baltic sea programs typically order after the Australian season proves the spec.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Discuss a Boat Rod Program</a></div>
    </div>"""
    intro_tables = spec_table(JIG_COLS, JIG_ROWS, MOQ_NOTE)
    custom = custom + intro_tables  # second table appended inside grid second column
    cat_page("saltwater-rods.html", "saltwater-rod", title,
             "Saltwater & Boat Rods — 20–200 lb Carbon Rods + Slow Jigging",
             desc, kw, intro, BOAT_COLS, BOAT_ROWS, MOQ_NOTE, custom, None)


def build_rocksurf():
    title = "Surf Rod Manufacturer | 4.2–4.5m Long Cast Rods OEM | Entrol Fishing"
    desc = ("Long-cast surf and rock rods from Weihai, China. 4.2–4.5 m three-piece plug-in blanks, "
            "120–280 g cast weights, corrosion-resistant finishes. MOQ 300/model. Get a quote.")
    kw = ("surf fishing rod manufacturer, long cast rod OEM, rock fishing rod supplier, shore jigging "
          "rod China, 4.5m surf rod factory, Weihai surf rod manufacturer")
    intro = """
    <p class="lead">Long-cast surf rods are a Weihai specialty — the tapered high-modulus blanks and
    large-coil guide trains needed to throw 150–280 g leads beyond 150 m are exactly what the
    city's tooling was built for. The program below includes three-piece plug-in beach rods and
    telescopic travel variants, plus shore-jigging sticks for rock anglers working jigs off
    breakwalls and headlands.</p>
    <p class="lead">Who fishes them: beach anglers casting whole baits and weighted rigs for
    mulloway, salmon and flathead in Australia; rock and breakwall anglers in Japan and Korea
    working shore jigs for yellowtail and bluefish; Mediterranean surf anglers targeting
    seabass and bream on sandy beaches in southern Europe.</p>"""
    custom = """
    <div>
      <span class="eyebrow">Customization</span>
      <h2>Distance Is a Spec, Not Luck</h2>
      <ul class="feature-list">
        <li><strong>Length:</strong> 3.9 m, 4.2 m, 4.5 m, 4.7 m beach rods; 2.7–3.3 m rock / shore jig models</li>
        <li><strong>Construction:</strong> 3-piece plug-in or telescopic; travel-friendly closed lengths</li>
        <li><strong>Cast weight:</strong> 100–150 g, 120–250 g, 150–280 g ratings</li>
        <li><strong>Guides:</strong> large-coil low-rider trains; reinforced ceramic tip rings</li>
        <li><strong>Handle:</strong> anti-slip EVA, extended butt for two-handed casting</li>
        <li><strong>Finish:</strong> corrosion-resistant baked paint in matte or metallic; custom wraps</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">Market Fit</span>
      <h2>Japan, Korea &amp; Southern Europe</h2>
      <p class="lead">Shore-based fishing dominates in Japan and Korea, and Weihai's proximity means
      samples arrive in days, not weeks. For southern European beach programs we quote mixed-model
      containers with both surf and boat rods, timed to arrive ahead of the summer season.</p>
      <div class="btn-row"><a class="btn btn-primary" href="contact.html">Discuss a Surf Program</a></div>
    </div>"""
    cat_page("rock-surf-rods.html", "rock-surf-rod", title,
             "Rock & Surf Rods — 4.2–4.5 m Long-Cast Carbon Rod Manufacturer",
             desc, kw, intro, SURF_COLS, SURF_ROWS, MOQ_NOTE, custom, None)


def build_products():
    title = "Fishing Rod Product Range | OEM Carbon Rods | Entrol Fishing"
    desc = ("All carbon fishing rod categories from Entrol Fishing: spinning & casting, carp, "
            "saltwater & boat, rock & surf. OEM/ODM from Weihai, China. MOQ 300 pcs/model.")
    kw = ("fishing rod product range, OEM fishing rods China, carbon rod categories, wholesale fishing "
          "rods, Weihai rod supplier")
    items = "".join("""
      <div class="card cat-card">
        <img src="%(img)s" alt="%(alt)s" loading="lazy" decoding="async">
        <div class="cat-body"><span class="cat-tag">%(tag)s</span>
        <h3><a href="%(href)s">%(name)s</a></h3>
        <p>%(blurb)s</p>
        <a class="card-link" href="%(href)s">View category &rarr;</a></div>
      </div>""" % {
        "img": MANIFEST[slug][0]["file"], "alt": MANIFEST[slug][0]["alt_en"],
        "tag": tag, "href": href, "name": name, "blurb": blurb,
    } for slug, href, name, tag, blurb in [
        ("spinning-rod", "spinning-rods.html", "Spinning & Casting Rods", "AU · JP",
         "Bass, estuary and light inshore blanks, 4–25 lb, cork or EVA handles."),
        ("carp-rod", "carp-rods.html", "Carp Rods", "UK · EU",
         "9–12 ft two-piece carp blanks, 2.75–3.0 lb test curves, continental cosmetics."),
        ("saltwater-rod", "saltwater-rods.html", "Saltwater & Boat Rods", "AU · Coastal EU",
         "20–200 lb boat sticks and slow jigging rods, corrosion-resistant builds."),
        ("rock-surf-rod", "rock-surf-rods.html", "Rock & Surf Rods", "JP · KR · S. EU",
         "4.2–4.5 m long-cast beach rods and shore jigging sticks."),
    ])
    item_list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Fishing rod categories — Entrol Fishing OEM program",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "url": DOMAIN + "/" + f}
            for i, (f, n) in enumerate(PRODUCT_NAV)
        ],
    }
    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Product Range</span>
    <h1>Fishing Rod Categories We Manufacture</h1>
    <p class="lead">Four rod programs cover the volume segments of the B2B tackle market. Every
    category ships from Weihai, Shandong with MOQ 300 pieces per model, 15–20 day sampling and
    full OEM customization — blanks, components, cosmetics and packaging.</p>
    <div class="grid grid-2" style="margin-top:38px">%(items)s</div>
    <div class="cta-band" style="margin-top:46px">
      <h2>Not Sure Which Blank Fits Your Market?</h2>
      <p>Send us your target species, price point and market. We'll spec two or three options with
      quotes — no obligation.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Request a Quote</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp Us</a>
      </div>
    </div>
  </div>
</section>""" % {"items": items, "wa": wa_link()}
    page("products.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "products.html"),
          breadcrumb_ld([("index.html", "Home"), ("products.html", "Products")]), item_list_ld])


def build_about():
    title = "About Entrol Fishing | Carbon Rod OEM Program Management from Weihai"
    desc = ("Entrol Fishing manages carbon fishing rod OEM/ODM programs from Weihai, China — "
            "audited partner production lines, milestone QC reports, one contact from spec to shipment.")
    kw = ("Weihai fishing rod factory, Entrol Fishing, carbon rod OEM China, fishing rod program "
          "management, fishing tackle supply Weihai")
    crumbs = [("index.html", "Home"), ("about.html", "About Us")]
    body = """
<section class="section" style="padding-top:34px">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Who We Are</span>
      <h1>OEM &amp; ODM Rod Programs, Managed from Weihai</h1>
      <p class="lead">%(brand)s is an OEM and export-management office based in Weihai, Shandong
      Province — the Chinese city that manufactures close to sixty percent of the world's fishing
      rods. You specify the rod; we get it built, inspected and shipped. Production runs on audited
      partner lines while we handle quotations, specifications, sampling, QC reports, documents and
      communication in your working hours.</p>
      <p class="lead">Almost everything we build leaves under the buyer's own brand — your logo,
      your colours, your packaging — because for an importer the brand on the rod is the asset, not
      ours. We are not locked to one factory either: for every category we keep qualified
      alternatives and place your program on the line whose strengths genuinely fit it.</p>
    </div>
    <div class="card" style="padding:0;overflow:hidden">
      <img src="assets/images/about-factory-01.webp" alt="Rod manufacturing facility in Weihai, Shandong, China — OEM carbon rod manufacturer" loading="lazy" decoding="async">
      <div style="padding:18px 22px"><p class="form-hint">A partner production line in Weihai, Shandong.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">The Supply Base</span>
    <h2>Who Actually Builds Your Rods</h2>
    <p class="lead">Weihai's rod industry is a cluster of specialized factories, and no single line
    is best at everything. We qualify multiple production lines per category and place each program
    where it genuinely fits best.</p>
    <div class="grid grid-3" style="margin-top:32px">
      <div class="card">
        <h3>Carbon Blank Engineering</h3>
        <p>Partner lines working with 24T–40T carbon prepreg, with published utility-model patents
        on blank structures, butt systems and handle mechanisms. High-tech enterprise recognition
        and in-house R&amp;D teams on the lines we use for custom programs.</p>
      </div>
      <div class="card">
        <h3>OEM Volume Capacity</h3>
        <p>Dedicated OEM lines producing on the order of hundreds of thousands of rods per year,
        with dust-controlled workshops and full customization of action, cosmetics and packaging —
        the backbone for repeating container programs.</p>
      </div>
      <div class="card">
        <h3>Export Compliance</h3>
        <p>Lines holding ISO 9001-certified processes and export rights, accustomed to FOB Qingdao
        documentation, third-party inspection and market-specific compliance conversations
        (REACH for the EU, UKCA review for the UK).</p>
      </div>
    </div>
    <div class="grid grid-2" style="margin-top:28px">
      <div class="card">
        <h3>How We Qualify a Production Line</h3>
        <ul class="feature-list">
          <li>On-site audit: workshop, capacity, QC stations, dust control</li>
          <li>Sample teardown and field testing before any program is placed</li>
          <li>Compliance document review for the destination market</li>
          <li>Requalification every season — underperforming lines are rotated out</li>
        </ul>
      </div>
      <div>
        <h3>Why Buyers Choose This Model</h3>
        <ul class="feature-list">
          <li>One contract, one contact — but factory-direct pricing, not trader margin</li>
          <li>Category matched to the line that is genuinely best at it — today, not on paper</li>
          <li>QC photo reports at rolling, assembly and packing milestones</li>
          <li>Consolidated shipments across categories from one industrial base</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Working Hours</span>
      <h2>Australia-Friendly Response Times</h2>
      <p class="lead">Weihai is GMT+8 — only two to three hours ahead of Australian Eastern time.
      Inquiries sent during Australian business hours are typically answered the same day, and
      always within one business day. European inquiries are answered each morning CET.</p>
      <ul class="feature-list">
        <li>Quotation within 1 business day</li>
        <li>Sample proposal within 3 business days of spec confirmation</li>
        <li>Production updates every milestone, with photos</li>
      </ul>
    </div>
    <div class="cta-band" style="align-self:start">
      <h2>Talk to the Sales Office</h2>
      <p>Email %(email)s or message us on WhatsApp — tell us your market and target price, and we'll
      come back with a spec and a number.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Contact Us</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp</a>
      </div>
    </div>
  </div>
</section>""" % {"brand": BRAND, "email": EMAIL, "wa": wa_link()}
    page("about.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "about.html"), breadcrumb_ld(crumbs)])


FAQS = [
    ("What is your MOQ for OEM fishing rods?",
     "MOQ is 300 pieces per model. Mixed-model containers are welcome for first orders, and "
     "charter or fleet programs can be quoted at different volumes."),
    ("How long does a sample take?",
     "Pre-production samples take 15–20 days from specification confirmation, depending on blank "
     "tooling and component availability. Bulk production takes 35–45 days after sample approval."),
    ("Can you build rods to my own specification?",
     "Yes — that is the core of our business. Send a reference rod, a competitor spec, or simply "
     "your target species and price point. We engineer the blank, guide train, reel seat, handle, "
     "cosmetics and packaging to match, and confirm the spec in writing before sampling."),
    ("Do you provide private-label branding?",
     "Yes. Logo placement, custom paint, wraps, rod socks, tubes and retail-ready boxes are all "
     "produced by our partner lines. Artwork requirements are provided with the quotation."),
    ("What are the shipping terms and freight times?",
     "We quote FOB Qingdao as standard; CIF and EXW available. Sea freight from Weihai/Qingdao to "
     "Australian ports runs 15–20 days, and to northern Europe roughly 30–35 days. Fishing tackle "
     "enters Australia duty-free under the China–Australia FTA."),
    ("Which certifications and compliance documents can you support?",
     "Our audited partner lines hold ISO 9001 certification and national high-tech enterprise status, "
     "and published rod patents. For EU-bound programs we discuss REACH-aware material and coating "
     "choices before contract; UKCA documentation can be reviewed for UK orders. Request the "
     "specific document set you need with your quotation."),
    ("How do you control quality?",
     "In-line inspection at blank rolling, assembly and packing milestones, with photo reports at "
     "each stage. Sample approval is a formal gate: bulk production starts only after you sign off "
     "the sample or an approved third-party inspection report."),
    ("Can I visit the factory?",
     "Yes — factory visits in Weihai are welcome. We coordinate the visit schedule, interpretation "
     "and follow-up. Video factory tours can be arranged before you commit to travel."),
]


def build_faq():
    title = "Fishing Rod OEM FAQ | MOQ, Samples, Lead Times | Entrol Fishing"
    desc = ("Answers on fishing rod OEM: MOQ 300 pcs/model, 15–20 day samples, 35–45 day production, "
            "private label, freight times to Australia and Europe, QC and factory visits.")
    kw = ("fishing rod OEM FAQ, fishing rod MOQ, fishing rod sample lead time, private label fishing "
          "rods, fishing rod factory China questions")
    crumbs = [("index.html", "Home"), ("faq.html", "FAQ")]
    qa_html = "".join("""
      <div class="card" style="margin-bottom:14px">
        <h3>%d. %s</h3>
        <p>%s</p>
      </div>""" % (i + 1, q, a) for i, (q, a) in enumerate(FAQS))
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
        ],
    }
    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">FAQ</span>
    <h1>Fishing Rod OEM — Questions Buyers Ask First</h1>
    <p class="lead">Straight answers on MOQ, sampling, lead times, compliance and logistics. If your
    question isn't here, ask us directly — it usually gets a same-day reply.</p>
    <div style="margin-top:30px">%(qa)s</div>
    <div class="cta-band" style="margin-top:36px">
      <h2>Still Have a Question?</h2>
      <p>Ask it on WhatsApp or by email — you'll be talking to the people who run the programs, not a call center.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Contact Us</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp Us</a>
      </div>
    </div>
  </div>
</section>""" % {"qa": qa_html, "wa": wa_link()}
    page("faq.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "faq.html"), breadcrumb_ld(crumbs), faq_ld])


def build_configurator():
    import configurator as C
    crumbs = [("index.html", "Home"), ("configure.html", "Build Your Rod")]
    body = C.render_body(wa_link(), FORM_ENDPOINT)
    page("configure.html", C.TITLE, C.DESC, C.KEYWORDS, body,
         [ORG_LD, webpage_ld(C.TITLE, C.DESC, "configure.html"), breadcrumb_ld(crumbs)])


def build_contact():
    title = "Request a Quote | Fishing Rod OEM Inquiry | Entrol Fishing"
    desc = ("Request a fishing rod OEM quotation from Weihai, China. MOQ 300 pcs/model, samples in "
            "15–20 days. Reply within one business day, or WhatsApp +86 152 6313 0999.")
    kw = ("fishing rod quote, fishing rod OEM inquiry, contact fishing rod manufacturer, Weihai rod "
          "factory contact, custom rod quotation")
    crumbs = [("index.html", "Home"), ("contact.html", "Contact")]
    body = """
<section class="section" style="padding-top:34px">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Contact</span>
      <h1>Request a Quote</h1>
      <p class="lead">Tell us what you're sourcing — a rod category, a reference spec, or just your
      target species and market. You'll get a quotation with MOQ, sample cost and freight estimate
      within one business day (GMT+8).</p>
      <ul class="feature-list" style="margin-top:22px">
        <li>Email: <strong>%(email)s</strong></li>
        <li>WhatsApp: <strong>+86 152 6313 0999</strong> (fastest response)</li>
        <li>WeChat: <strong>%(wechat)s</strong></li>
        <li>Sales office &amp; factory visits: Weihai City, Shandong Province, China</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-accent" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Chat on WhatsApp</a>
      </div>
    </div>
    <div class="card">
      <form id="rfq-form" action="%(form)s" method="POST">
        <!-- honeypot -->
        <div class="hp-field" aria-hidden="true">
          <label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>
        </div>
        <input type="hidden" name="_subject" value="New fishing rod OEM inquiry — entrol-fishing.com">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <div class="form-grid">
          <div class="form-field">
            <label for="f-name">Full name <span>*</span></label>
            <input id="f-name" name="name" type="text" required placeholder="Jane Smith">
          </div>
          <div class="form-field">
            <label for="f-email">Work email <span>*</span></label>
            <input id="f-email" name="email" type="email" required placeholder="jane@company.com">
          </div>
          <div class="form-field">
            <label for="f-company">Company</label>
            <input id="f-company" name="company" type="text" placeholder="Company / brand">
          </div>
          <div class="form-field">
            <label for="f-market">Target market</label>
            <select id="f-market" name="target_market">
              <option value="">Select market…</option>
              <option>Australia</option>
              <option>United Kingdom</option>
              <option>Europe (EU)</option>
              <option>Japan</option>
              <option>South Korea</option>
              <option>United States</option>
              <option>Other</option>
            </select>
          </div>
          <div class="form-field">
            <label for="f-category">Rod category</label>
            <select id="f-category" name="rod_category">
              <option value="">Select category…</option>
              <option>Spinning / casting rods</option>
              <option>Carp rods</option>
              <option>Saltwater / boat rods</option>
              <option>Rock / surf rods</option>
              <option>Mixed / not sure yet</option>
            </select>
          </div>
          <div class="form-field">
            <label for="f-quantity">Estimated quantity</label>
            <input id="f-quantity" name="quantity" type="text" placeholder="e.g. 300–1000 pcs/model">
          </div>
          <div class="form-field full">
            <label for="f-message">Project details <span>*</span></label>
            <textarea id="f-message" name="message" rows="5" required
              placeholder="Target species, preferred lengths/actions, reference products, price point, timeline…"></textarea>
          </div>
          <div class="form-field full">
            <button class="btn btn-primary" type="submit" style="width:100%%">Send Inquiry</button>
            <p class="form-hint">We reply within one business day. Your details are used only to
            answer this inquiry.</p>
          </div>
        </div>
      </form>
      <div class="form-status" role="status"></div>
    </div>
  </div>
</section>""" % {"email": EMAIL, "wechat": WECHAT, "wa": wa_link(), "form": FORM_ENDPOINT}
    page("contact.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "contact.html"), breadcrumb_ld(crumbs)])


def build_assets():
    logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 48" width="240" height="48">
  <rect width="48" height="48" rx="10" fill="#0E6E8C"/>
  <path d="M9 33c9-1.5 13.5-6 16.5-12 2.1-4.2 3.6-8.1 6.9-10.8.8-.6 1.8.3 1.4 1.2-1.5 3-2.1 6-1.8 9.3l5.1 2.2c.9.4.8 1.7-.2 2l-5.4 1.5C30 31.5 25.5 36.6 18.5 37.6c-3.4.6-6.9.3-9-.3-.9-.3-.9-1.5 0-1.7z" fill="#fff"/>
  <text x="60" y="30" font-family="Arial, sans-serif" font-size="21" font-weight="800" fill="#12242C">Entrol Fishing</text>
  <text x="61" y="42" font-family="Arial, sans-serif" font-size="8.5" letter-spacing="2.6" fill="#48626D">WEIHAI · CARBON ROD OEM</text>
</svg>"""
    with open(os.path.join(ROOT, "assets", "logo.svg"), "w", encoding="utf-8") as f:
        f.write(logo)
    print("wrote assets/logo.svg")

    sitemap_urls = ["", "spinning-rods.html", "carp-rods.html", "saltwater-rods.html",
                    "rock-surf-rods.html", "products.html", "configure.html", "about.html",
                    "faq.html", "contact.html"]
    urls = "".join("""
  <url>
    <loc>%s/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>""" % (DOMAIN, u, TODAY,
               "1.0" if u in ("", "configure.html", "spinning-rods.html", "carp-rods.html") else "0.8")
        for u in sitemap_urls)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s\n</urlset>\n' % urls
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap)
    print("wrote sitemap.xml")

    robots = """User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % DOMAIN
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(robots)
    print("wrote robots.txt")


if __name__ == "__main__":
    build_assets()
    build_index()
    build_spinning()
    build_carp()
    build_saltwater()
    build_rocksurf()
    build_products()
    build_configurator()
    build_about()
    build_faq()
    build_contact()
    print("\nAll pages generated.")
