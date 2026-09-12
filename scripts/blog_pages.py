#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Original, buyer-focused SEO guides for Entrol Fishing."""
import json


POSTS = [
    {
        "file": "australia-fishing-rod-oem-guide.html",
        "title": "Fishing Rod OEM for Australia | Buyer’s Sourcing Guide",
        "h1": "Fishing Rod OEM for Australia: A Practical Buyer’s Guide",
        "desc": "A practical guide for Australian tackle retailers and brands sourcing OEM fishing rods: range planning, specifications, samples, MOQ, packaging and freight.",
        "keywords": "fishing rod OEM Australia, wholesale fishing rods Australia, private label fishing rods, fishing tackle supplier Australia",
        "intro": "For an Australian tackle retailer or emerging brand, the hard part is rarely finding a factory. The hard part is translating a market idea into a range that can be sampled, compared, priced and reordered without losing control of the specification.",
        "sections": [
            ("Start with the customer and fishing method", "Define where the rod will be used, the target species, lure or sinker range, reel type and intended retail position before choosing carbon grade or decoration. A compact range normally works better than many overlapping models. For example, a retailer may begin with one general-purpose estuary spin rod, one heavier inshore model and one surf option, then expand after sell-through data is available."),
            ("Turn the range plan into measurable specifications", "Each model should have a controlled specification covering length, sections, power, action, line rating, lure or cast weight, guide train, reel seat, handle, finish and packaging. Reference samples are useful, but the approved specification and signed sample should become the production standard. This avoids relying on subjective descriptions such as ‘medium’ or ‘fast’, which can differ between suppliers."),
            ("Plan samples before committing to volume", "A useful sample review checks balance with the intended reel, guide alignment, ferrule fit, handle finish, cosmetic consistency and packaging protection. Field testing should match the intended fishing method. Record requested changes in one revision list, then approve a final sample or clearly documented golden sample before production."),
            ("Build a commercially realistic first order", "MOQ is affected by blank construction, component colour, printed packaging and the number of models. Concentrating volume into fewer models usually creates a cleaner first order. Ask for a quotation that separates product, packaging, tooling if any, inspection and freight assumptions. Confirm the Incoterm and destination before comparing suppliers."),
            ("Prepare for Australian delivery", "Confirm carton dimensions, gross weight, port or delivery point, labelling and any material or packaging requirements with your customs broker before shipment. Requirements vary by product and shipment, so obtain product-specific advice rather than treating a general guide as a compliance decision. Keep the approved specification, inspection record and packing list under the same project reference."),
        ],
        "related": [("spinning-rods.html", "Review spinning and casting rod specifications"), ("rock-surf-rods.html", "Review surf rod specifications"), ("oem-builder.html", "Create an OEM brief")],
    },
    {
        "file": "australian-surf-rod-specification-guide.html",
        "title": "Australian Surf Rod Specifications | OEM Buyer Guide",
        "h1": "How to Specify a Surf Rod Range for Australian Buyers",
        "desc": "Compare length, sections, cast weight, guides, handles and corrosion resistance when developing private-label surf rods for the Australian market.",
        "keywords": "Australian surf rod supplier, surf fishing rod OEM, long cast rod manufacturer, private label surf rods Australia",
        "intro": "A surf rod should be specified around the beach, casting load and buyer—not simply copied from a catalogue. The same nominal length can feel very different when blank recovery, guide layout, handle geometry and reel choice change.",
        "sections": [
            ("Choose length around the fishing environment", "Longer rods can support line control and casting clearance, while shorter designs can be easier to manage around rocks, vehicles and repeated lure casting. Define whether the range is intended for bait fishing, metal lures, general beach use or heavier rock work. A range can share visual branding while using different blank actions for each job."),
            ("State a realistic cast-weight window", "Avoid selecting a rod only from its maximum printed cast weight. Give the supplier the most common sinker or lure weight and the total rig weight. The sample should be evaluated near the everyday working load, not only at the extremes. If several sinker sizes are common, identify the primary load and acceptable range."),
            ("Match guides, reel seat and handle", "Guide material and frame finish should suit salt exposure and the intended line. Guide size and spacing must match the blank and reel type. Handle length affects leverage and comfort, while reel-seat position affects balance. Ask for a dimensioned handle drawing and guide layout in the controlled specification."),
            ("Design for transport and retail", "Two- and three-piece formats change packed length, freight efficiency and the customer experience. Check ferrule engagement, alignment marks, bag construction and carton protection. Retail packaging should communicate length, cast range, sections, line recommendation and intended use without forcing store staff to interpret factory codes."),
            ("Use field testing to close the loop", "Test casting, recovery, joint stability, grip comfort and line flow with the intended reel and rig. Photograph the test set-up and record the reel size, line, leader and casting load. Feed one consolidated change list back to the supplier, then lock the approved version before bulk production."),
        ],
        "related": [("rock-surf-rods.html", "Compare current surf rod models"), ("custom-rod.html", "Configure a complete personal set-up"), ("oem-builder.html", "Brief an OEM surf rod")],
    },
    {
        "file": "fishing-rod-oem-moq-sampling-guide.html",
        "title": "Fishing Rod OEM MOQ & Samples | Private Label Guide",
        "h1": "Fishing Rod OEM: MOQ, Samples and the Path to Production",
        "desc": "Understand how model count, components, packaging and branding affect fishing rod OEM MOQ, sample development and production planning.",
        "keywords": "fishing rod OEM MOQ, private label fishing rod samples, custom fishing rod production, fishing rod manufacturer China",
        "intro": "MOQ is not just a factory rule. It reflects how many blanks, components, decals, packages and production changes a project creates. A clear range plan can reduce complexity even when the total order remains modest.",
        "sections": [
            ("What usually drives MOQ", "Blank construction, custom colours, exclusive components and printed packaging each have their own production economics. Splitting one order across many lengths or actions can create a separate minimum for each model. Before requesting the lowest possible MOQ, decide which differences customers can actually recognise and pay for."),
            ("Separate base models from cosmetic variants", "A practical first range may use a small number of proven base blanks, then vary decoration or packaging only where the commercial reason is clear. Confirm whether a colour change counts as another model, whether components can be shared, and whether packaging quantities exceed the rod quantity."),
            ("Use the sample as a controlled decision point", "The sample stage should answer fit, function, finish and packaging questions before volume production. Review the specification alongside the physical rod and record every approved change. If a component is substituted, the replacement should be documented rather than accepted through an informal message."),
            ("Compare quotations on the same basis", "Check the Incoterm, currency, model quantity, packaging, sample credit, tooling, inspection and freight assumptions. A lower unit price can conceal different components or excluded work. Ask suppliers to quote against the same revision of the specification and keep the quotation attached to that revision."),
            ("Create a repeatable reorder file", "A useful production file contains the approved specification, artwork, packaging files, sample approval, change log, inspection criteria and shipping marks. Reorders become faster when each item has a stable model code and the buyer can state exactly which approved version should be repeated."),
        ],
        "related": [("process.html", "See the quote-to-shipment process"), ("capabilities.html", "Review manufacturing capabilities"), ("oem-builder.html", "Build a quotation-ready specification")],
    },
    {
        "file": "carbon-fishing-rod-blank-guide.html",
        "title": "Carbon Fishing Rod Blanks | OEM Material Selection Guide",
        "h1": "Choosing a Carbon Fishing Rod Blank for an OEM Program",
        "desc": "A buyer-focused guide to carbon rod blank selection: action, power, wall design, reinforcement, durability, weight and sample validation.",
        "keywords": "carbon fishing rod blank OEM, 24T 30T 40T carbon rod, fishing rod blank manufacturer, custom carbon fishing rods",
        "intro": "Carbon grade is useful information, but it does not describe the whole rod. Resin system, fibre orientation, wall profile, reinforcement, mandrel design and cure control all influence weight, recovery and durability.",
        "sections": [
            ("Specify performance before material labels", "Start with target species, fishing method, lure or cast range, line class, length and sections. Then define the required power, action, balance and durability. A supplier can propose a construction that meets those targets; selecting a high modulus label first can push cost into a feature the end customer may not value."),
            ("Understand what tonnage labels can and cannot tell you", "Terms such as 24T, 30T or 40T are commonly used to describe carbon fibre modulus categories, but they do not by themselves prove finished-rod performance. Two blanks carrying the same headline label may use different fibre mixes, tapers, resin content and reinforcement. Treat the label as one input, not the acceptance test."),
            ("Balance sensitivity, weight and robustness", "Reducing weight can improve handling, but the correct construction depends on impact exposure, transport, casting load and customer expectations. Reinforcement can be placed where the design needs it rather than applied as a marketing layer. Ask the supplier to explain which construction decisions support the intended use."),
            ("Test the complete rod, not only the blank", "Guides, wraps, finish, ferrules, reel seat and handle change the behaviour of the finished rod. Compare samples with the intended reel and line. Inspect straightness, recovery, joint fit, guide alignment and cosmetic consistency, then conduct controlled field tests at the normal working load."),
            ("Write acceptance criteria that can be repeated", "Record dimensions, component models, guide layout, finished weight tolerance, cosmetic references and functional checks. Where laboratory data or material certificates matter to the buyer, request the specific document and confirm that it applies to the supplied material and production lot. Do not substitute a general marketing claim for product-specific evidence."),
        ],
        "related": [("capabilities.html", "See blank and component capabilities"), ("spinning-rods.html", "Compare carbon spinning rod specifications"), ("oem-builder.html", "Define your blank requirements")],
    },
]


def article_ld(site, post):
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": post["h1"], "description": post["desc"],
        "datePublished": "2026-09-12", "dateModified": "2026-09-12",
        "mainEntityOfPage": site.DOMAIN + "/" + post["file"],
        "author": {"@type": "Organization", "name": site.BRAND},
        "publisher": {"@type": "Organization", "name": site.BRAND,
                      "logo": {"@type": "ImageObject", "url": site.DOMAIN + "/assets/logo.svg"}},
        "image": site.OG_IMAGE,
    }


def post_body(post):
    sections = "".join('<section class="guide-section"><h2>%s</h2><p>%s</p></section>' % x for x in post["sections"])
    related = "".join('<li><a href="%s">%s &rarr;</a></li>' % x for x in post["related"])
    return """
<article class="guide-wrap">
  <header class="guide-hero"><div class="container guide-narrow">
    <span class="eyebrow">OEM Buyer Guide &middot; Australia</span>
    <h1>%(h1)s</h1><p class="lead">%(intro)s</p>
    <div class="guide-meta">Updated 12 September 2026 &middot; 6 minute read &middot; Entrol Fishing</div>
  </div></header>
  <div class="container guide-layout">
    <div class="guide-article">
      <div class="guide-takeaway"><strong>Buyer takeaway</strong><p>Use this guide to prepare a clearer sourcing brief. Final specifications, costs, compliance and freight must be confirmed for the actual product and shipment.</p></div>
      %(sections)s
      <section class="guide-next"><h2>Turn the research into a quotation-ready brief</h2>
        <p>Select a starting model or describe the target market, price position and quantity. We will return the missing technical questions before quoting.</p>
        <div class="btn-row"><a class="btn btn-accent" href="oem-builder.html">Open OEM Builder</a><a class="btn btn-outline" href="contact.html">Ask a sourcing question</a></div>
      </section>
    </div>
    <aside class="guide-aside"><h2>Related resources</h2><ul>%(related)s</ul><p>Planning a private-label range for Australia?</p><a class="btn btn-primary" href="oem-builder.html">Start your brief</a></aside>
  </div>
</article>""" % {"h1": post["h1"], "intro": post["intro"], "sections": sections, "related": related}


def build_blog(site):
    cards = "".join("""<article class="card guide-card"><span class="cat-tag">Buyer guide</span><h2><a href="%(file)s">%(h1)s</a></h2><p>%(desc)s</p><a class="card-link" href="%(file)s">Read the guide &rarr;</a></article>""" % p for p in POSTS)
    title = "Fishing Rod OEM Guides | Australia & Private Label"
    desc = "Practical fishing rod OEM guides for Australian tackle retailers, importers and brands: specifications, MOQ, samples, surf rods and carbon blanks."
    body = """<section class="guide-hero"><div class="container"><span class="eyebrow">Sourcing Knowledge</span><h1>Fishing Rod OEM Buyer Guides</h1><p class="lead">Practical guidance for tackle retailers, importers and emerging brands. Build a clearer range, compare like-for-like quotations and move from idea to controlled sample.</p></div></section><section class="section"><div class="container"><div class="grid grid-2">%s</div></div></section><section class="section section-alt"><div class="container"><div class="cta-band"><h2>Already know what you need?</h2><p>Turn your market, target price and quantity into a structured OEM brief.</p><div class="btn-row"><a class="btn btn-accent" href="oem-builder.html">Build an OEM brief</a><a class="btn btn-outline" href="products.html">Browse product specifications</a></div></div></div></section>""" % cards
    crumbs = [("index.html", "Home"), ("blog.html", "Guides")]
    site.page("blog.html", title, desc,
              "fishing rod OEM guide, private label fishing rods, fishing tackle sourcing, Australia fishing rod wholesale",
              body, [site.ORG_LD, site.webpage_ld(title, desc, "blog.html"), site.breadcrumb_ld(crumbs)])
    for post in POSTS:
        crumbs = [("index.html", "Home"), ("blog.html", "Guides"), (post["file"], post["h1"])]
        site.page(post["file"], post["title"], post["desc"], post["keywords"], post_body(post),
                  [site.ORG_LD, article_ld(site, post), site.breadcrumb_ld(crumbs)])


def build_all(site):
    build_blog(site)
