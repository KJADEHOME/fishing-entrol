#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Static site generator for Entrol Fishing (fishing.entrol.com).

Idempotent: re-running rebuilds every page from the content definitions below.
All copy is ORIGINAL — never copied from other sites in the network (anti
template-spam rule). Technical facts (specs, factory credentials) come only
from factory-published sources recorded in scripts/product_images_manifest.json
and PENDING-BEFORE-PUBLISH.md.
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import catalog_data as cat  # noqa: E402  (product catalogue — single source of truth)

DOMAIN = "https://fishing.entrol.com"
BRAND = "Entrol Fishing"
LEGAL = "Entrol Fishing — Weihai sourcing office"
EMAIL = "wangyan@entrol.com"
WA = "8615263130999"
WA_TEXT = "Hi%20Entrol%20Fishing%2C%20I%27d%20like%20a%20quote%20for%20OEM%20fishing%20rods."
WECHAT = "15263130999"
GTM_ID = "GTM-T3ZXMRHS"
GA4_ID = "G-5QK21JJ0G4"
FORM_ENDPOINT = "#"
OG_IMAGE = DOMAIN + "/assets/images/spinning-rod-01.webp"
TODAY = "2026-09-11"

MANIFEST = json.load(open(os.path.join(ROOT, "scripts", "product_images_manifest.json"), encoding="utf-8"))
# Ready-made rods from a partner production line that we are authorised to
# distribute. Kept apart from the OEM rod list: these are the maker's own
# published models, sold as-is, not an anonymous pattern we re-brand for a buyer.
STOCK = json.load(open(os.path.join(ROOT, "scripts", "stock_catalog.json"), encoding="utf-8"))
# Ready-made reels and lures from the same authorised partner. Same trade-integration
# position as the ready-ship rods: existing models, our SKU prefix, no maker branding.
RL = json.load(open(os.path.join(ROOT, "scripts", "reels_lures_site.json"), encoding="utf-8"))

PRODUCT_NAV = [
    ("spinning-rods.html", "Spinning & Casting Rods"),
    ("carp-rods.html", "Carp Rods"),
    ("saltwater-rods.html", "Saltwater & Boat Rods"),
    ("rock-surf-rods.html", "Rock & Surf Rods"),
    ("products.html", "Ready-Ship Rods"),
    ("reels.html", "Ready-Ship Reels"),
    ("lures.html", "Ready-Ship Lures"),
]
CAPABILITY_NAV = [
    ("capabilities.html", "Manufacturing Capability"),
    ("process.html", "How We Work — Quote to Shipment"),
]
COMPANY_NAV = [
    ("about.html", "About Us"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]
BLOG_NAV = [
    ("blog.html", "All Guides"),
    ("australia-fishing-rod-oem-guide.html", "Australia OEM Buying Guide"),
    ("australian-surf-rod-specification-guide.html", "Australian Surf Rod Guide"),
    ("fishing-rod-oem-moq-sampling-guide.html", "MOQ & Sampling Guide"),
    ("carbon-fishing-rod-blank-guide.html", "Carbon Blank Guide"),
]
# (file, label, submenu) — submenu files also mark the parent as active
NAV = [
    ("index.html", "Home", []),
    ("products.html", "Products", PRODUCT_NAV),
    ("capabilities.html", "Capabilities", CAPABILITY_NAV),
    ("oem-builder.html", "OEM Builder", []),
    ("custom-rod.html", "Custom Rod", []),
    ("blog.html", "Guides", BLOG_NAV),
    ("about.html", "About", COMPANY_NAV),
]
# Every URL the site publishes — sitemap and internal-link checks come from here.
ALL_PAGES = [
    ("", "1.0"),
    ("spinning-rods.html", "0.9"),
    ("carp-rods.html", "0.9"),
    ("saltwater-rods.html", "0.9"),
    ("rock-surf-rods.html", "0.9"),
    ("products.html", "0.8"),
    ("reels.html", "0.8"),
    ("lures.html", "0.8"),
    ("products.html", "0.9"),
    ("capabilities.html", "0.8"),
    ("process.html", "0.8"),
    ("oem-builder.html", "1.0"),
    ("custom-rod.html", "0.9"),
    ("about.html", "0.7"),
    ("faq.html", "0.7"),
    ("contact.html", "0.8"),
    ("blog.html", "0.8"),
    ("australia-fishing-rod-oem-guide.html", "0.8"),
    ("australian-surf-rod-specification-guide.html", "0.8"),
    ("fishing-rod-oem-moq-sampling-guide.html", "0.8"),
    ("carbon-fishing-rod-blank-guide.html", "0.8"),
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
# Rows come from the product catalogue (scripts/catalog_data.py) so the spec
# tables, the configurator picker and the compatibility engine can never drift.
SPIN_ROWS = cat.spec_rows("spinning")
SPIN_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Action / Power",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

CARP_ROWS = cat.spec_rows("carp")
CARP_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Test Curve",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

BOAT_ROWS = cat.spec_rows("boat")
BOAT_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Line Class",
             "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

JIG_ROWS = cat.spec_rows("jig")
JIG_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Jig Rating",
            "Tip / Butt Dia.", "Line Rating", "Handle", "Carbon Grade"]

SURF_ROWS = cat.spec_rows("surf")
SURF_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Action",
             "Tip / Butt Dia.", "Cast Weight", "Handle", "Carbon Grade"]

MOQ_NOTE = ("MOQ 300 pcs per model (500 for kits) · Sample lead time 20 days · Production "
            "lead time 45 days after sample approval. Custom length, action, components and "
            "branding available on request.")


def spec_table(cols, rows, caption):
    th = "".join("<th>%s</th>" % c for c in cols)
    trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ('<div class="table-wrap"><table class="spec"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div><p class="table-note">%s</p>' % (th, trs, caption))


CARD_KINDS = {
    "spinning-rod": ("spinning",),
    "carp-rod": ("carp",),
    "saltwater-rod": ("boat", "jig"),
    "rock-surf-rod": ("surf",),
}


def rod_cards(kinds):
    """Model cards for a category page, generated from the product catalogue.

    Each card is an anchor target (#<sku>) and links into the OEM builder with
    the model preselected, so a buyer can start from a real rod instead of
    filling 30 abstract fields from scratch.
    """
    if isinstance(kinds, str):
        kinds = (kinds,)
    cards = []
    for kind in kinds:
        k = cat.PAGE_KINDS[kind]
        for sub in k["subs"]:
            for p in sorted(cat.rods_by_sub(sub), key=lambda r: r["specs"]["length_m"]):
                s = p["specs"]
                if sub == "casting":
                    mark = " (cast)"
                elif sub == "jigging":
                    mark = " (spin)" if "Spinning" in s.get("reel_type", "") else " (cast)"
                else:
                    mark = ""
                rows = [("Length", "%.2f m (%s)" % (s["length_m"], s["length_ft"]))]
                if kind == "carp":
                    rows.append(("Test curve", s["power"]))
                else:
                    rows.append(("Power / action", "%s / %s" % (s.get("power", "—"),
                                                                s.get("action", "—"))))
                rows.append(("Line rating", s.get("line_rating", "—")))
                if s.get("cast_weight_g"):
                    rows.append(("Cast weight", "%s g" % s["cast_weight_g"]))
                rows += [("Rod weight", "%d g" % s["weight_g"]),
                         ("Sections", s["sections"]),
                         ("Handle", s.get("handle", "—")),
                         ("Reel type", s.get("reel_type", "—"))]
                dl = "".join("<div class=\"rod-spec\"><span>%s</span><strong>%s</strong></div>"
                             % (lab, val) for lab, val in rows)
                cards.append("""
      <article class="card rod-card" id="%(sku)s">
        <img src="%(img)s" alt="%(alt)s" loading="lazy" decoding="async">
        <div class="rod-body">
          <h3>%(model)s%(mark)s</h3>
          <p class="rod-name">%(name)s</p>
          <div class="rod-specs">%(specs)s</div>
          <div class="rod-actions">
            <a class="card-link" href="oem-builder.html?model=%(sku)s">Start an OEM program from this rod &rarr;</a>
            <a class="card-link" href="custom-rod.html?model=%(sku)s">Or build one for yourself</a>
          </div>
        </div>
      </article>""" % {"sku": p["sku"], "img": p["image"], "model": p["model"], "mark": mark,
                       "name": p["name"], "specs": dl,
                       "alt": p["model"] + " carbon fishing rod — OEM specification"})
    return ('<div class="grid grid-3 rod-grid">%s</div>' % "".join(cards))


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
    "description": "OEM and export-management office for carbon fishing rod programs in Weihai, Shandong, China. "
                   "We plan, sample, quality-control and ship spinning, carp, saltwater and surf rods under your brand.",
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
  <!-- Entrol Fishing Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=%(ga4)s"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','%(ga4)s');</script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','%(gtm)s');</script>
  <!-- End Google Tag Manager -->
  %(ld)s""" % {
        "t": title, "d": desc, "k": keywords, "domain": DOMAIN, "p": path,
        "og": OG_IMAGE, "brand": BRAND, "gtm": GTM_ID, "ga4": GA4_ID, "ld": extra_ld,
    }


GTM_NOSCRIPT = ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" '
                'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' % GTM_ID)


def nav_html(active):
    def link(f, label):
        cls = ' class="active"' if f == active else ""
        return '<a href="%s"%s>%s</a>' % (f, cls, label)

    def dropdown(f, label, sub):
        here = f == active or any(sf == active for sf, _ in sub)
        cls = ' class="active"' if here else ""
        items = "".join("<li>%s</li>" % link(sf, sl) for sf, sl in sub)
        return ('<li class="nav-dropdown"><a href="%s"%s>%s</a><ul>%s</ul></li>'
                % (f, cls, label, items))

    out = []
    for f, label, sub in NAV:
        out.append(dropdown(f, label, sub) if sub else "<li>%s</li>" % link(f, label))
    return "".join(out)


def footer_html():
    prod = "".join('<li><a href="%s">%s</a></li>' % (f, l) for f, l in PRODUCT_NAV)
    prog = "".join('<li><a href="%s">%s</a></li>' % (f, l) for f, l in [
        ("oem-builder.html", "OEM Rod Program"),
        ("custom-rod.html", "One Custom Rod"),
        ("blog.html", "Buyer Guides"),
        ("capabilities.html", "Manufacturing Capability"),
        ("process.html", "How We Work"),
        ("about.html", "About Us"),
        ("faq.html", "FAQ"),
    ])
    return """
<div class="container">
  <div class="footer-grid">
    <div class="footer-brand">
      <h4>%(brand)s</h4>
      <p>An OEM and export-management office for carbon fishing rod programs in Weihai, Shandong —
         China's fishing tackle manufacturing capital. We plan, sample, quality-control and ship
         rods under your brand for importers, brands and tackle retailers in Australia, Europe,
         Japan and Korea.</p>
    </div>
    <div>
      <h4>Rod Categories</h4>
      <ul>%(prod)s</ul>
    </div>
    <div>
      <h4>Programs &amp; Company</h4>
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
</div>""" % {"brand": BRAND, "prod": prod, "comp": prog, "email": EMAIL,
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
    if fname in {f for f, _ in PRODUCT_NAV}:
        crumbs.append(("products.html", "Products"))
    if fname != "index.html":
        crumbs.append((fname, title.split("|")[0].strip()))
    head_html = head(title, desc, keywords, path, jsonld(ld_blocks))
    if fname == "index.html":
        breadcrumb = ""
    else:
        _inner = " &rsaquo; ".join('<a href="%s">%s</a>' % (f, n) for f, n in crumbs[:-1])
        _inner += ' &rsaquo; <span aria-current="page">%s</span>' % crumbs[-1][1]
        breadcrumb = ('<nav class="breadcrumb container" aria-label="Breadcrumb">%s</nav>'
                      % _inner)
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
            "MOQ 300 pcs/model, samples in 20 days. Get a quote today.")
    assert len(desc) <= 160
    kw = ("carbon fiber fishing rod manufacturer, fishing rod OEM supplier China, custom fishing rod "
          "manufacturer, Weihai fishing rod factory, spinning rod OEM, carp rod manufacturer")
    body = """
<section class="hero">
  <div class="container">
    <span class="eyebrow">Weihai &middot; Shandong &middot; China</span>
    <h1>Carbon Fiber Fishing Rods, Built to Your Specification</h1>
    <p class="lead">Tell us the market, target retail price and quantity. We turn that brief into
    a buildable rod or complete retail kit, coordinate the supplying lines in Weihai, and quote it
    under your own brand.</p>
    <div class="btn-row">
      <a class="btn btn-accent" href="oem-builder.html">Build Your Rod &rarr;</a>
      <a class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,.7)" href="products.html">Browse Rod Categories</a>
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>OEM first</strong><span>private-label programs</span></div>
      <div class="hero-stat"><strong>3 positions</strong><span>value · balanced · performance</span></div>
      <div class="hero-stat"><strong>One brief</strong><span>rod, components and packaging</span></div>
      <div class="hero-stat"><strong>One reference</strong><span>for quote, sample and reorder</span></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="center">
      <span class="eyebrow">Choose Your Starting Point</span>
      <h2>Start With the Business Decision — Not a Wall of Components</h2>
      <p class="lead">You can begin with a target price, an existing product, a new private-label
      idea or a complete retail kit. Technical choices come after the commercial brief.</p>
    </div>
    <div class="path-row">
      <a class="path-card" href="oem-builder.html">
        <span class="path-eyebrow">Primary · B2B</span><h3>Build an OEM Product Program</h3>
        <p>For brands, importers, distributors, tackle stores and online sellers.</p>
        <ul class="path-meta"><li>Start from a target retail price</li><li>Modify a proven base model</li>
        <li>Quote a rod or a complete retail kit</li></ul><strong>Open OEM Builder →</strong>
      </a>
      <a class="path-card" href="custom-rod.html">
        <span class="path-eyebrow">Secondary · Angler</span><h3>Configure One Professional Set-up</h3>
        <p>For an angler who wants a rod, reel, line, lures and terminal tackle matched together.</p>
        <ul class="path-meta"><li>Build around species and fishing method</li><li>Add each component by quantity</li>
        <li>Receive one combined quotation</li></ul><strong>Build My Set-up →</strong>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center"><span class="eyebrow">Three Product Positions</span>
      <h2>Give Buyers a Useful Starting Point</h2>
      <p class="lead">These are design directions, not fixed prices. The final specification is
      checked against the target market, order quantity and supplier availability.</p></div>
    <div class="grid grid-3" style="margin-top:34px">
      <div class="card"><h3>Value</h3><p>Durability and sell-through first. Spend where the angler
      feels it; keep decoration and component cost controlled.</p><a class="card-link" href="oem-builder.html">Brief a value program →</a></div>
      <div class="card"><h3>Balanced</h3><p>The default for an independent brand: reliable blank,
      credible components, practical packaging and room for retail margin.</p><a class="card-link" href="oem-builder.html">Brief a balanced program →</a></div>
      <div class="card"><h3>Performance</h3><p>Lower weight, upgraded component train and finish,
      developed around a buyer who can explain the difference.</p><a class="card-link" href="oem-builder.html">Brief a performance program →</a></div>
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
      <p class="lead">Weihai brings blank rolling, component supply, painting and assembly into
      one established fishing-tackle cluster. Working with %(brand)s gives you one project contact
      across those specialist supplying lines.</p>
      <ul class="feature-list">
        <li>Carbon and composite options confirmed against the selected supplying line</li>
        <li>Full OEM/ODM: length, action, guides, reel seats, grip, cosmetics, packaging</li>
        <li>Product-specific tariff and origin documentation reviewed before shipment</li>
        <li>Freight route and lead time quoted against the destination and sailing</li>
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
      <div class="card"><h3>2 &middot; Sample</h3><p>Pre-production sample in 20 days. Test it on
      the water before you commit to volume.</p></div>
      <div class="card"><h3>3 &middot; Production</h3><p>45 days after sample approval, with
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
      <a class="btn btn-accent" href="oem-builder.html">Open the Configurator &rarr;</a>
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
    <span class="eyebrow">Models</span>
    <h2>Every Model in This Category</h2>
    <p class="lead">These are the rods currently tooled on our Weihai lines. Pick one and the
    builder opens with its real measurements already filled in — length, power, line rating, reel
    type and handle — and you change only what you want to change.</p>
    %(cards)s
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">Specifications</span>
    <h2>Reference Specification Table</h2>
    <p class="lead">Real production data from current Weihai tooling. Any model can be customized —
    treat these as the starting point of your own program.</p>
    %(table)s
  </div>
</section>
<section class="section">
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
        <a class="btn btn-accent" href="oem-builder.html?rod=%(cfgkey)s">Open the OEM Rod Builder</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp Us</a>
      </div>
    </div>
  </div>
</section>""" % {
        "breadcrumb": "", "h1": h1, "h1short": h1.split(" — ")[0], "intro": intro_html,
        "wa": wa_link(), "cfgkey": CFG_KEY.get(slug, "spinning"),
        "gallery": gallery(slug), "table": spec_table(cols, rows, table_note),
        "cards": rod_cards(CARD_KINDS.get(slug, ("spinning",))),
        "custom": custom_html, "moq": MOQ_NOTE,
    }
    page(fname, title, desc, kw, body, [ORG_LD, webpage_ld(title, desc, fname), crumb_ld, product_ld])


def build_spinning():
    title = "Spinning Rod OEM & ODM | Carbon Bass Rods | Entrol Fishing"
    desc = ("Custom spinning and casting rods from Weihai, China. 2.13–2.29 m carbon blanks, cork "
            "handles, 4–25 lb. MOQ 300/model, samples 20 days. Request a quotation.")
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
            "corrosion-resistant components, MOQ 300/model. Samples in 20 days.")
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


LIB_COLS = ["Model", "Length", "Closed Length", "Sections", "Weight", "Power / Rating",
            "Tip / Butt Dia.", "Line Rating", "Handle", "Reel Type"]


def library_rows(kind):
    """Spec rows for the full-model library — same data as the category pages,
    plus the reel type so the table stands on its own."""
    k = cat.PAGE_KINDS[kind]
    out = []
    for sub in k["subs"]:
        for p in sorted(cat.rods_by_sub(sub), key=lambda r: r["specs"]["length_m"]):
            s = p["specs"]
            if sub == "casting":
                mark = " (cast)"
            elif sub == "jigging":
                mark = " (spin)" if "Spinning" in s.get("reel_type", "") else " (cast)"
            else:
                mark = ""
            out.append([p["model"] + mark,
                        "%.2f m (%s)" % (s["length_m"], s["length_ft"]),
                        cat._closed(p), s["sections"], "%d g" % s["weight_g"],
                        k["c6"](s), cat._dia(p), k["c8"](s),
                        s.get("handle", "—"), s.get("reel_type", "—")])
    return out


def comp_rows(items):
    out = []
    for p in items:
        bits = []
        for key, val in p["specs"].items():
            if val in (None, "", "—"):
                continue
            bits.append("%s %s" % (str(key).replace("_", " ").title(), val))
        out.append([p["sku"], p["name"], ", ".join(bits)])
    return out


COMP_COLS = ["SKU", "Description", "Specification"]


def _ready_card(s):
    """One ready-ship series: photo, published spec summary and its full model table."""
    rows = [("Rod weight", ("%s g" % s["weight_g"]) if s["weight_g"] else "—"),
            ("Material", s["material"] or "—"),
            ("Action", s["action"] or "—"),
            ("Sections", s["sections"] or "—")]
    dl = "".join('<div class="rod-spec"><span>%s</span><strong>%s</strong></div>'
                 % (lab, val) for lab, val in rows)
    if s["variants"]:
        vrows = [[v["sku"], v["code"], v["reel"] or "—",
                  "%.2f m (%s)" % (v["length_m"], v["length_ft"]),
                  v["power"] or "—",
                  ("%s g" % v["lure_g"]) if v.get("lure_g") else "—"] for v in s["variants"]]
        table = spec_table(["Our SKU", "Model", "Type", "Length", "Power", "Lure"], vrows,
                           "Order by our SKU. The model code next to it is the maker's "
                           "own reference for the same rod. Lure range shown where the "
                           "maker publishes it — ask us for the full model sheet.")
    else:
        table = ('<p class="table-note">The maker publishes the variant list for this '
                 'series on its own store page — ask us for the current model sheet.</p>')
    flag = ("<p class=\"rod-name\"><em>Source: the maker's own store listing.</em></p>"
            if s["official_store"] else
            "<p class=\"rod-name\"><em>Source: authorised retailer listing.</em></p>")
    img = ('<figure class="pg-item"><img src="%s" alt="%s" loading="lazy" decoding="async"></figure>' %
           (s["image"], s["series"] + " carbon lure rod")) if s["image"] else ""
    thumbs = ""
    if s.get("gallery"):
        tfigs = "".join(
            '<figure class="pg-item rod-thumb"><img src="%s" alt="%s detail view %d" '
            'loading="lazy" decoding="async"></figure>' % (g, s["series"], i + 1)
            for i, g in enumerate(s["gallery"]))
        thumbs = '<div class="rod-thumbs">%s</div>' % tfigs
    return """
      <article class="card rod-card" id="series-%(slug)s" data-pg-gallery data-pg-caption="%(name)s">
        %(img)s
        %(thumbs)s
        <div class="rod-body">
          <h3>%(name)s</h3>
          <p class="rod-name">%(blurb)s</p>
          <div class="rod-specs">%(specs)s</div>
          %(flag)s
          %(table)s
        </div>
      </article>""" % {"slug": s["slug"].lower(), "img": img, "thumbs": thumbs,
                       "name": s["name_en"],
                       "blurb": s["blurb"], "specs": dl, "flag": flag, "table": table}


def build_ready_ship_rods():
    title = "Ready-to-Ship Carbon Lure Rods | Wholesale from Weihai | Entrol Fishing"
    desc = ("Ready-to-ship carbon lure rods from a Weihai partner line: F30 long-cast, "
            "X20 / X30 / X40 finesse, T30 travel, R30 ajing and G30 big-bait. "
            "57–128 g carbon blanks, 1.8–3.35 m, 52 models. Wholesale and OEM enquiries welcome.")
    kw = ("ready to ship fishing rods, carbon lure rod supplier China, Weihai lure rod factory, "
          "finesse rod wholesale, lure rod distributor, ajing rod supplier")
    series = STOCK["series"]
    total = sum(len(s["variants"]) for s in series)
    cards = "".join(_ready_card(s) for s in series)
    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Weihai &middot; Shandong &middot; China</span>
    <h1>Ready-Ship Lure Rod Series</h1>
    <p class="lead">Ready-made rods from one of Weihai's carbon-rod lines, which we are
    authorised to distribute. No tooling, no sampling cycle — you pick a model code and
    we ship. Or take the same pattern and build it under your own brand.</p>
    <p class="lead">Every figure below is transcribed from the maker's own published
    product data: blank weight, material, action, section count and the full model
    list. All models are available for immediate shipment — tell us your model mix
    and quantity and we will come back with a quotation within one business day.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="contact.html">Request Wholesale Pricing</a>
      <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp +86 152 6313 0999</a>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">The Range</span>
    <h2>%(n)d Published Models Across %(k)d Series</h2>
    <p class="lead">Spinning and casting versions, 1.8 m finesse rods up to 3.35 m
    long-cast rods. Model codes are the maker's own, so you can order by code.</p>
    <div class="grid grid-2 rod-grid">%(cards)s</div>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Buy it as it is</span>
      <h2>Resale &amp; Distribution</h2>
      <ul class="feature-list">
        <li><strong>Ready to sell:</strong> existing models with retail packaging — no tooling and no sampling cycle</li>
        <li><strong>Shipped from stock:</strong> ask us for current availability and the minimum order</li>
        <li><strong>Order by our SKU:</strong> every model carries an RS code, so nothing traces back to the maker</li>
        <li><strong>Export handling:</strong> consolidated cartons, documentation and freight from Weihai</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">Or build it as yours</span>
      <h2>OEM Version of the Same Pattern</h2>
      <p class="lead">Because we work with the same production line, any model on this
      page can be the starting point of your own program — same blank and taper, your
      cosmetics, your model codes, from 300 pieces per model.</p>
      <div class="btn-row"><a class="btn btn-outline" href="oem-builder.html">Open the OEM Rod Builder</a></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>Ask for the Ready-Ship Price List</h2>
      <p>Tell us which series and which model codes you want and we will come back with
      wholesale pricing, carton quantities and a landed-cost estimate for your port.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Request a Quotation</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>""" % {"wa": wa_link(), "cards": cards, "n": total, "k": len(series)}
    crumbs = [("index.html", "Home"), ("products.html", "Products"),
              ("products.html", "Ready-Ship Rods")]
    page("products.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "products.html"), breadcrumb_ld(crumbs)])


def _rl_card(e, unit):
    """Ready-ship reel or lure card: photo, spec summary, variant table, gallery."""
    dl = "".join('<div class="rod-spec"><span>%s</span><strong>%s</strong></div>'
                 % (k, v) for k, v in e["specs"].items())
    vrows = [[v["sku"], v["model"]] for v in e["variants"]]
    table = spec_table(["Our SKU", "Model / Option"], vrows,
                       "Order by our SKU. Tell us the SKU mix and quantity and we "
                       "quote within one business day.")
    img = ('<figure class="pg-item"><img src="%s" alt="%s" loading="lazy" decoding="async"></figure>'
           % (e["image"], e["name_en"])) if e.get("image") else ""
    thumbs = ""
    if e.get("gallery"):
        tfigs = "".join(
            '<figure class="pg-item rod-thumb"><img src="%s" alt="%s detail view %d" '
            'loading="lazy" decoding="async"></figure>' % (g, e["name_en"], i + 1)
            for i, g in enumerate(e["gallery"]))
        thumbs = '<div class="rod-thumbs">%s</div>' % tfigs
    return """
      <article class="card rod-card" id="item-%(slug)s" data-pg-gallery data-pg-caption="%(name)s">
        %(img)s
        %(thumbs)s
        <div class="rod-body">
          <h3>%(name)s</h3>
          <p class="rod-name">%(blurb)s</p>
          <div class="rod-specs">%(specs)s</div>
          %(table)s
        </div>
      </article>""" % {"slug": e["slug"].lower(), "img": img, "thumbs": thumbs,
                       "name": e["name_en"], "blurb": e["blurb"], "specs": dl, "table": table}


_RL_HERO = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Weihai &middot; Shandong &middot; China</span>
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <p class="lead">Every specification below is transcribed from the maker's published
    product data. All items are available for immediate shipment - tell us your SKU mix
    and quantity and we will come back with a quotation within one business day.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="contact.html">Request Wholesale Pricing</a>
      <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">WhatsApp +86 152 6313 0999</a>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">The Range</span>
    <h2>%(n)d Items, %(k)d Product Lines</h2>
    <div class="grid grid-2 rod-grid">%(cards)s</div>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2">
    <div>
      <span class="eyebrow">Buy it as it is</span>
      <h2>Resale &amp; Distribution</h2>
      <ul class="feature-list">
        <li><strong>Ready to sell:</strong> existing models with retail packaging - no tooling, no sampling cycle</li>
        <li><strong>Shipped from stock:</strong> ask us for current availability and the minimum order</li>
        <li><strong>Order by our SKU:</strong> every variant carries an RS code, so nothing traces back to the maker</li>
        <li><strong>Export handling:</strong> consolidated cartons, documentation and freight from Weihai</li>
      </ul>
    </div>
    <div>
      <span class="eyebrow">One more thing</span>
      <h2>Matched Rod Programs</h2>
      <p class="lead">These %(unit)s come from the same partner network as our Ready-Ship
      rod series, so we can put together matched rod + %(unit)s packages for your market -
      one shipment, one set of export documents.</p>
      <div class="btn-row"><a class="btn btn-outline" href="products.html">See the Ready-Ship Rods</a></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="cta-band">
      <h2>Ask for the %(unit)s Price List</h2>
      <p>Tell us which SKUs you want and we will come back with wholesale pricing,
      carton quantities and a landed-cost estimate for your port.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Request a Quotation</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""


def build_ready_ship_reels():
    title = "Ready-to-Ship Fishing Reels | Spinning & Baitcasting | Entrol Fishing"
    desc = ("Ready-to-ship fishing reels from our Weihai partner network: Galaxy and "
            "Hummingbird spinning reels, J-20, Venom and Cyber baitcasters. Wholesale "
            "and matched rod-and-reel programs.")
    kw = ("ready to ship fishing reels, spinning reel wholesale China, baitcasting reel "
          "supplier, fishing reel distributor, finesse reel wholesale, fishing reel exporter")
    items = RL["reels"]
    cards = "".join(_rl_card(e, "reel") for e in items)
    body = _RL_HERO % {
        "h1": "Ready-Ship Spinning &amp; Baitcasting Reels",
        "lead": "Five reel lines from our Weihai partner network, sold as finished goods "
                "under our own RS codes: two spinning reels for finesse and all-round use, "
                "three baitcasters from 7.2:1 up to a high-speed 8.0:1.",
        "wa": wa_link(), "cards": cards, "n": sum(len(e["variants"]) for e in items),
        "k": len(items), "unit": "reel",
    }
    crumbs = [("index.html", "Home"), ("products.html", "Products"),
              ("reels.html", "Ready-Ship Reels")]
    page("reels.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "reels.html"), breadcrumb_ld(crumbs)])


def build_ready_ship_lures():
    title = "Ready-to-Ship Lures & Rigs | Spinnerbaits & Micro Rigs | Entrol Fishing"
    desc = ("Ready-to-ship lures and pre-tied rigs from our Weihai partner network: "
            "crescent-blade spinnerbait sets in three weights and micro spoon fly-hook "
            "rigs. Mixed-SKU cartons welcome.")
    kw = ("ready to ship fishing lures, spinnerbait wholesale China, fishing lure supplier, "
          "micro lure rig wholesale, fishing lure distributor, terminal tackle exporter")
    items = RL["lures"]
    cards = "".join(_rl_card(e, "lure") for e in items)
    body = _RL_HERO % {
        "h1": "Ready-Ship Lures &amp; Rigs",
        "lead": "Two lure lines that pair with our micro-rod programs: the "
                "crescent-blade spinnerbait set in 7.5 / 11 / 15 g and a pre-tied micro "
                "spoon rig. Low unit weight makes these easy to consolidate with a rod order.",
        "wa": wa_link(), "cards": cards, "n": sum(len(e["variants"]) for e in items),
        "k": len(items), "unit": "lure",
    }
    crumbs = [("index.html", "Home"), ("products.html", "Products"),
              ("lures.html", "Ready-Ship Lures")]
    page("lures.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "lures.html"), breadcrumb_ld(crumbs)])


def build_products():
    title = "Rod Models & Components | OEM Spec Library | Entrol Fishing"
    desc = ("Rod and component reference library: 22 carbon rod specifications, braid, leader, "
            "lures, reels and terminal tackle. Start an OEM brief from an existing model.")
    assert len(title) <= 65 and len(desc) <= 160
    kw = ("fishing rod model list, OEM fishing rod specifications, carbon rod models, fishing rod "
          "components wholesale, braid and leader OEM, fishing reel sourcing")
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
    tables = "".join("""
    <h3 class="lib-head">%(label)s <span>&middot; %(n)d models</span></h3>
    %(table)s""" % {"label": label, "n": len(rows),
                    "table": spec_table(LIB_COLS, rows,
                                        "Current Weihai tooling. Every model can be re-specced — "
                                        "length, power, guides, seat, handle, cosmetics, packaging.")}
        for label, rows in [
            ("Spinning &amp; casting rods", library_rows("spinning")),
            ("Carp rods", library_rows("carp")),
            ("Boat &amp; bottom rods", library_rows("boat")),
            ("Slow-pitch jigging rods", library_rows("jig")),
            ("Rock &amp; surf rods", library_rows("surf")),
        ])

    comp_html = "".join("""
    <details class="lib-details"%s>
      <summary>%s <span>&middot; %d SKUs</span></summary>
      %s
    </details>""" % (" open" if i == 0 else "", label, len(rows),
                     spec_table(COMP_COLS, rows, note))
        for i, (label, rows, note) in enumerate([
            ("Braid, leader &amp; mono", comp_rows(cat.LINES),
             "Neutral-specification lines — we do not print a third-party brand on a spool we have "
             "not been asked to. Branded spools from 1,000 pcs."),
            ("Lures &amp; metal jigs", comp_rows(cat.LURES),
             "Soft plastics, hard lures and metal jigs sourced to your species, method and price "
             "point. Mixed selections in one carton are normal."),
            ("Reels", comp_rows(cat.REELS),
             "Reel sizes we can source alongside a rod program. Gear ratio, drag and weight are "
             "specified per brief — tell us the target and we come back with options."),
            ("Hooks &amp; terminal tackle", comp_rows(cat.TERMINAL),
             "Reference combinations for a complete set-up. Availability, pack quantity and OEM "
             "minimum are confirmed with the selected supplying line before quotation."),
        ]))

    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Product Library</span>
    <h1>Start From a Verified Rod Specification</h1>
    <p class="lead">%(nrods)d rod specifications give you a practical starting point, alongside
    line, lure, reel and terminal-tackle references for a complete set. Pick one and the OEM
    builder opens with its measurements already filled in; supplier availability is confirmed
    before quotation.</p>
    <div class="grid grid-2" style="margin-top:38px">%(items)s</div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">Rod Models</span>
    <h2>The Full Specification Library</h2>
    <p class="lead">Lengths, powers, line ratings and weights as they come off the line. Treat them
    as a starting point: almost every OEM program changes something.</p>
    %(tables)s
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Components</span>
    <h2>What Goes in the Box With the Rod</h2>
    <p class="lead">We are a rod builder, not a reel factory — so the components below are sourced
    to your brief rather than made by us, and we say so. How they are labelled is your call.</p>
    %(comp)s
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Start From a Model, or Start From Scratch</h2>
      <p>Found a model close to what you want? Open the builder with it preselected and change only
      what needs changing. Nothing fits? Describe the rod and we will spec it from zero.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="oem-builder.html">Open the OEM Builder &rarr;</a>
        <a class="btn btn-outline" href="custom-rod.html">Build one rod for yourself</a>
      </div>
    </div>
  </div>
</section>""" % {"items": items, "tables": tables, "comp": comp_html, "nrods": len(cat.RODS)}
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
     "For rods, 300 pieces per model. Mixed-model containers are welcome for first orders, and "
     "charter or fleet programs can be quoted at different volumes. The minimum rises when you ask "
     "us to put other components in the carton: a rod plus reel, line or a lure set starts at 500 "
     "pieces, and a full retail kit — or reels, spools and lure cards printed with your own brand "
     "— starts at 1,000. Each part carries its own minimum because each part is made by a "
     "different supplier, and we quote them on separate lines so you can see exactly what you are "
     "paying for."),
    ("Can you supply a matched kit — rod, reel, line and lures in one carton?",
     "Yes, and we assemble it to the specification you build in the configurator. Be clear about "
     "one thing though: the rod is built on our own production lines and always carries your brand, "
     "while the reel, line and lures are sourced from component makers to your brief. We do not "
     "manufacture those and we will not put our own badge on them. You choose how they are "
     "labelled: your brand from 1,000 pieces, the component maker's own brand, an unbranded neutral "
     "pack, or a house brand we propose to your target price point."),
    ("How long does a sample take?",
     "Pre-production samples take 20 days from specification confirmation, depending on blank "
     "tooling and component availability. Bulk production takes 45 days after sample approval."),
    ("Can I buy just one rod for myself?",
     "You can commission one, but you cannot buy one off a shelf — there is no stock, no cart and "
     "no online checkout. Every rod is built to order, so a single rod is quoted the same way a "
     "container is: you tell us the water, the fish, the length and feel you want, plus any reels, "
     "line and lures you want sent with it, and we come back with a price and a build time. A "
     "single build runs 20 days before it ships, and freight is quoted to your country "
     "separately. It costs more per rod than a production order because there is no run to spread "
     "the set-up across — and because it is built to your measurements, it cannot be returned or "
     "exchanged unless it arrives damaged."),
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
    desc = ("Answers on fishing rod OEM: MOQ 300 pcs/model, 20-day samples, 45-day production, "
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


def build_oem_builder():
    import configurator as C
    crumbs = [("index.html", "Home"), ("oem-builder.html", "OEM Rod Builder")]
    body = C.render_body(wa_link(), FORM_ENDPOINT, path="oem")
    page("oem-builder.html", C.TITLE_OEM, C.DESC_OEM, C.KEYWORDS_OEM, body,
         [ORG_LD, webpage_ld(C.TITLE_OEM, C.DESC_OEM, "oem-builder.html"),
          breadcrumb_ld(crumbs)])


def build_custom_rod():
    import configurator as C
    crumbs = [("index.html", "Home"), ("custom-rod.html", "Custom Fishing Rod")]
    body = C.render_body(wa_link(), FORM_ENDPOINT, path="custom")
    page("custom-rod.html", C.TITLE_CUSTOM, C.DESC_CUSTOM, C.KEYWORDS_CUSTOM, body,
         [ORG_LD, webpage_ld(C.TITLE_CUSTOM, C.DESC_CUSTOM, "custom-rod.html"),
          breadcrumb_ld(crumbs)])


def build_capabilities():
    title = "Manufacturing Capability | Carbon Rod OEM | Entrol Fishing"
    desc = ("What our Weihai partner lines build: 24T-46T carbon blanks, guide trains, reel "
            "seats, handles, cosmetics, packaging and in-line QC for OEM rod programs.")
    assert len(title) <= 65 and len(desc) <= 160
    kw = ("fishing rod manufacturing capability, carbon blank OEM, rod building process, Fuji "
          "guides OEM, custom rod packaging, fishing rod QC")
    crumbs = [("index.html", "Home"), ("capabilities.html", "Manufacturing Capability")]
    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">Manufacturing Capability</span>
    <h1>What the Lines in Weihai Can Actually Build</h1>
    <p class="lead">Capability claims are easy to write and hard to verify, so this page sticks to
    what our partner lines do every week. Each heading below is a decision you make on a rod
    program — and each one has a cost, a lead time and a minimum attached to it. If you need
    something that is not on this page, ask; the answer is often yes, just not on this line.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">The Blank</span>
    <h2>Carbon Grade, Taper and How They Are Chosen</h2>
    <p class="lead">The blank is the rod. Everything else is fitted to it, and everything else can
    be changed later — the taper cannot.</p>
    <div class="grid grid-3" style="margin-top:30px">
      <div class="card"><h3>24T–30T</h3><p>Tougher, more forgiving, cheaper. The right answer for
      entry and mid-tier programs, heavy boat rods, and anywhere a rod is likely to be knocked
      about. Slightly heavier for a given power.</p></div>
      <div class="card"><h3>30T–40T</h3><p>The volume sweet spot: noticeably lighter and more
      sensitive without becoming brittle. Most branded spinning and carp programs sit here.</p></div>
      <div class="card"><h3>40T–46T</h3><p>Maximum sensitivity and the lowest weight, at the cost
      of impact resistance and price. Used where feel sells the rod — finesse spinning, specimen
      carp — and usually with a scrim or mixed layup for safety.</p></div>
    </div>
    <div class="card" style="margin-top:26px">
      <h3 style="margin-top:0">Taper, not just tonnage</h3>
      <p>Two rods built from identical cloth fish completely differently. Fast, moderate-fast and
      parabolic tapers are produced by changing the mandrel and the ply schedule, which is why we
      ask for a target species and a target retail price before we recommend a blank — the grade
      follows the price, not the other way round.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Components</span>
    <h2>Guide Train, Reel Seat and Handle</h2>
    <div class="cfg-why" style="margin-top:26px">
      <div class="card"><h4>Guide train</h4><p>Single-foot, double-foot, KW anti-tangle and micro
      guide layouts. Rings in Alconite, SiC or Torzite on stainless or titanium frames. Guide count
      and spacing are set from your length and line rating, not copied from a catalogue — a badly
      spaced train is the most common cause of a rod that casts worse than its price suggests.</p></div>
      <div class="card"><h4>Reel seat</h4><p>Screw-down seats in the patterns buyers already know
      (VSS, ECS, ACS, TCS and their equivalents), plus custom collars and carbon inserts. Trigger
      seats for baitcasting, slim profiles for carp, exposed-blank designs for finesse spinning.</p></div>
      <div class="card"><h4>Handle</h4><p>Full grip, split grip or custom length. Cork (including
      graded and composite cork), EVA in any density and colour, or shrink tube over carbon. Shaped
      foregrips and butt caps made to your drawing.</p></div>
      <div class="card"><h4>Wrapping &amp; cosmetics</h4><p>Thread colour, metallic trims, decals,
      hydro-dip patterns, matte or gloss clear coat. Cosmetics are the cheapest way to make a rod
      look like your brand and the easiest thing to get wrong — we send a photo of the first
      wrapped blank before the run starts.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">Your Brand</span>
    <h2>Logo Methods and Packaging</h2>
    <div class="grid grid-2" style="margin-top:28px">
      <div class="card">
        <h3>Getting your name on the rod</h3>
        <ul class="feature-list">
          <li><strong>Silk-screen</strong> — the default. Any colour, low tooling cost, durable
          under a clear coat.</li>
          <li><strong>Laser engraving</strong> — permanent, no ink, works on reel seats and metal
          parts. Also how single custom rods are personalised.</li>
          <li><strong>Hydro-dip / water transfer</strong> — full patterns and camo across the
          blank; higher set-up cost, better suited to longer runs.</li>
          <li><strong>Decals &amp; badges</strong> — for complex artwork and multi-colour logos
          that screen printing cannot hold.</li>
        </ul>
      </div>
      <div class="card">
        <h3>How it leaves the factory</h3>
        <ul class="feature-list">
          <li><strong>Rod bag</strong> — cloth or non-woven, printed with your logo.</li>
          <li><strong>Tube or triangular carton</strong> — sized to the closed length, printed
          retail artwork or plain.</li>
          <li><strong>Retail box</strong> — full-colour print, barcode, hang tab, warning text in
          your market's language.</li>
          <li><strong>Master carton</strong> — specced for container efficiency, not just to
          survive the trip.</li>
        </ul>
        <p class="form-hint" style="margin-top:10px">Printed packaging carries its own minimum
        because the printer does — usually 500–1,000 units for a custom printed box.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Quality</span>
    <h2>What We Check, and When You Hear About It</h2>
    <p class="lead">Nobody can promise zero defects on a hand-finished product. What we can promise
    is that you see the rod being built, and that a problem is our phone call to make, not yours to
    discover on the shelf.</p>
    <div class="grid grid-4" style="margin-top:30px">
      <div class="card"><h3>Incoming</h3><p>Blanks checked for straightness, weight and finish;
      components counted and inspected before they reach the line.</p></div>
      <div class="card"><h3>In-line</h3><p>Guide alignment, wrapping tension and epoxy checked
      during assembly, not only at the end of it.</p></div>
      <div class="card"><h3>Pre-shipment</h3><p>Photo report plus a defect-rate summary against an
      AQL you set. Third-party inspection welcomed and coordinated by us.</p></div>
      <div class="card"><h3>Documents</h3><p>Packing list, commercial invoice, certificate of
      origin and any market-specific paperwork agreed up front.</p></div>
    </div>
    <div class="cta-band" style="margin-top:36px">
      <h2>Want the Capability List as a Document?</h2>
      <p>We keep a one-page capability sheet with the ranges, minimums and lead times for each
      process above. It is easier to forward to a colleague than a web page.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Request the Capability Sheet</a>
        <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Or ask on WhatsApp</a>
      </div>
    </div>
  </div>
</section>""" % {"wa": wa_link()}
    page("capabilities.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "capabilities.html"), breadcrumb_ld(crumbs)])


def build_process():
    title = "How We Work | OEM Rod Process & Lead Times | Entrol Fishing"
    desc = ("From first inquiry to landed goods: RFQ, quotation, sampling, production, inspection "
            "and shipment for OEM fishing rod programs built in Weihai, China.")
    assert len(title) <= 65 and len(desc) <= 160
    kw = ("fishing rod OEM process, rod sampling lead time, FOB Qingdao fishing rods, rod "
          "production lead time, OEM rod shipping, How to import fishing rods")
    crumbs = [("index.html", "Home"), ("process.html", "How We Work")]
    body = """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">How We Work</span>
    <h1>From First Message to Landed Goods</h1>
    <p class="lead">Six stages, and you know where the order is in all six. The numbers below are
    the ones we actually work to — a sample in 20 days, production 45 days after you approve
    it — but they move with the season, so treat them as planning figures and confirm on the quote.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-3" style="margin-top:0">
      <div class="card"><h3>1 · Enquiry</h3><p>Send a spec, a reference rod, or just the species
      and the price point. The configurator on the OEM page produces the most useful first
      message, but an email or a photo works too.</p>
      <p class="form-hint">You hear back within one business day (GMT+8).</p></div>
      <div class="card"><h3>2 · Quotation</h3><p>A costed build sheet: blank, components,
      cosmetics, packaging, labour, MOQ, sample cost and an estimated freight figure. Each part on
      its own line so you can see what the reel costs against the rod.</p></div>
      <div class="card"><h3>3 · Sample</h3><p>One pre-production sample built to the agreed spec,
      ready in 20 days. Sample cost is normally credited against the production order.</p></div>
      <div class="card"><h3>4 · Approval</h3><p>You test it. Changes at this stage are normal and
      cheap — changing a guide layout after 3,000 rods are wrapped is neither.</p></div>
      <div class="card"><h3>5 · Production</h3><p>45 days after sample approval. Photo reports
      at blank, wrapping and finishing milestones; pre-shipment inspection against an agreed
      AQL.</p></div>
      <div class="card"><h3>6 · Shipment</h3><p>Consolidated sea or air from Qingdao with full
      export documentation. We track until it is on the water and confirm the arrival estimate.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">Lead Times</span>
    <h2>Where the Weeks Actually Go</h2>
    <div class="table-wrap">
      <table class="spec">
        <thead><tr><th>Stage</th><th>Typical duration</th><th>What can delay it</th></tr></thead>
        <tbody>
          <tr><td>Quotation</td><td>1 business day</td><td>A spec that needs component makers to price — reels and line add two to three days.</td></tr>
          <tr><td>Sample build</td><td>20 days</td><td>Custom blanks, hydro-dip patterns and printed packaging each add time.</td></tr>
          <tr><td>Sample shipping</td><td>3–7 days by air</td><td>Customs clearance at your end, which we cannot control.</td></tr>
          <tr><td>Production</td><td>45 days</td><td>Peak season (roughly September to February for the following spring), or a change of spec mid-run.</td></tr>
          <tr><td>Sea freight</td><td>15–20 days to Australia, 30–40 days to Northern Europe</td><td>Port congestion and transhipment.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="table-note">Plan backwards from the date the rods need to be on the shelf. For a
    European spring season, the conversation starts in the autumn.</p>
  </div>
</section>

<section class="section">
  <div class="container grid grid-2">
    <div class="card">
      <h3 style="margin-top:0">Trade terms &amp; payment</h3>
      <ul class="feature-list">
        <li><strong>EXW / FOB Qingdao</strong> — the default for volume orders. You control the
        freight forwarder, or we quote one.</li>
        <li><strong>CIF / DDP</strong> — available to major ports and, for DDP, selected markets.
        Slower to quote and worth it mainly for first-time importers.</li>
        <li><strong>Payment</strong> — 30%% deposit with the order, balance against bill of lading.
        Other structures are negotiable on repeat programs.</li>
        <li><strong>Samples</strong> — paid up front, credited back when a production order is
        placed.</li>
      </ul>
    </div>
    <div class="card">
      <h3 style="margin-top:0">What slows a program down</h3>
      <ul class="feature-list">
        <li>A target retail price that is not shared — every component decision then has to be
        re-quoted twice.</li>
        <li>Choosing a carbon grade before choosing the species and method.</li>
        <li>Printed packaging approved late; the printer is usually the longest lead item.</li>
        <li>Compliance questions raised after tooling, especially REACH for the EU and UKCA for
        Great Britain.</li>
      </ul>
      <p class="form-hint" style="margin-top:10px">Tell us these four things in the first email and
      the quote will be right the first time.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="cta-band">
      <h2>Start With a Specification, Not a Price List</h2>
      <p>The OEM builder takes about two minutes and gives us everything we need for an accurate
      first quote — including the two answers that matter most: how many, and what it sells for.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="oem-builder.html">Open the OEM Builder &rarr;</a>
        <a class="btn btn-outline" href="contact.html">Or just send us a message</a>
      </div>
    </div>
  </div>
</section>""" % {}
    page("process.html", title, desc, kw, body,
         [ORG_LD, webpage_ld(title, desc, "process.html"), breadcrumb_ld(crumbs)])


def build_contact():
    title = "Request a Quote | Fishing Rod OEM Inquiry | Entrol Fishing"
    desc = ("Request a fishing rod OEM quotation from Weihai, China. MOQ 300 pcs/model, samples in "
            "20 days. Reply within one business day, or WhatsApp +86 152 6313 0999.")
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
        <input type="hidden" name="_subject" value="New fishing rod OEM inquiry — fishing.entrol.com">
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

    urls = "".join("""
  <url>
    <loc>%s/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>monthly</changefreq>
    <priority>%s</priority>
  </url>""" % (DOMAIN, u, TODAY, pri) for u, pri in ALL_PAGES)
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
    build_ready_ship_rods()
    build_ready_ship_reels()
    build_ready_ship_lures()
    build_products()
    build_capabilities()
    build_process()
    build_oem_builder()
    build_custom_rod()
    build_about()
    build_faq()
    build_contact()
    import blog_pages
    blog_pages.build_all(sys.modules[__name__])
    print("\nAll pages generated.")
