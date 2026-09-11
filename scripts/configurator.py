#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OEM rod configurator page content.

Every field below maps to something a Weihai rod line actually needs in order
to quote: blank layup, guide train, reel seat, handle, cosmetics and packing.
The buyer picks what they know and skips the rest — a partially filled spec is
still far more useful than "please send catalogue".
"""
import html

# field = dict(name, label, opts|None, hint=None, full=False, required=False, kind=select|text|email|textarea)
GROUPS = [
    {
        "step": 1,
        "title": "Blank &amp; Action",
        "note": "The base of the rod. If you are matching an existing model, pick the closest "
                "length and power — we will fine-tune the mandrel later.",
        "fields": [
            dict(name="rod_type", label="Rod type", opts=[
                "Spinning rod", "Casting / baitcasting rod", "Carp rod", "Surf / rock rod",
                "Boat &amp; jigging rod", "Telescopic travel rod", "Fly rod", "Ice rod",
                "Not sure — advise me"]),
            dict(name="length", label="Length", opts=[
                "1.68 m (5'6\")", "1.80 m (5'11\")", "1.98 m (6'6\")", "2.10 m (6'11\")",
                "2.13 m (7'0\")", "2.29 m (7'6\")", "2.40 m (7'10\")", "2.70 m (8'10\")",
                "3.00 m (9'10\")", "3.30 m (10'10\")", "3.60 m (11'10\")", "3.90 m (12'9\")",
                "4.20 m (13'9\")", "4.50 m (14'9\")", "Custom length"]),
            dict(name="sections", label="Sections", opts=[
                "1 piece", "2 pieces", "3 pieces", "4 pieces", "5 pieces or more",
                "Telescopic", "Advise me"]),
            dict(name="power", label="Power", opts=[
                "Ultra-Light", "Light", "Medium-Light", "Medium", "Medium-Heavy", "Heavy",
                "Extra-Heavy", "Advise me"]),
            dict(name="action", label="Action / taper", opts=[
                "Slow", "Moderate", "Moderate-Fast", "Fast", "Extra-Fast", "Advise me"]),
            dict(name="lure_weight", label="Lure / cast weight", opts=[
                "under 5 g", "5–21 g", "10–30 g", "20–50 g", "30–80 g", "50–120 g",
                "100–200 g", "over 200 g", "Advise me"]),
            dict(name="line_rating", label="Line rating", opts=[
                "PE 0.6–1.2", "PE 0.8–2.0", "PE 1.5–3.0", "PE 3.0–5.0",
                "4–12 lb", "6–14 lb", "10–20 lb", "20–40 lb", "Advise me"]),
        ],
    },
    {
        "step": 2,
        "title": "Carbon &amp; Blank Construction",
        "note": "T-value is the tensile modulus of the carbon cloth in tons. Higher T is lighter "
                "and more sensitive, but more brittle and more expensive — most volume programs "
                "sit at 24T–30T with a 40T reinforcement layer only where it pays off.",
        "fields": [
            dict(name="carbon_grade", label="Carbon grade (T value)", opts=[
                "24T", "30T", "36T", "40T", "46T", "24T + 30T mix", "30T + 40T mix",
                "E-glass (fibreglass)", "Carbon + glass composite", "Advise me"],
                hint="Higher T = lighter, stiffer, more brittle, higher cost."),
            dict(name="carbon_cloth", label="Cloth / reinforcement", opts=[
                "Unidirectional carbon", "Cross-weave carbon", "X-wrap reinforced",
                "Carbon tape reinforced", "Standard layup", "Advise me"]),
            dict(name="blank_finish", label="Blank finish", opts=[
                "Unpainted matte carbon", "Gloss paint", "Matte paint",
                "Hydro-dip camo", "Fade / gradient", "Custom finish"],
                hint="Unpainted carbon is the lightest and shows the cloth."),
            dict(name="blank_color", label="Blank colour", opts=[
                "Natural carbon black", "Matte black paint", "Dark blue", "Red", "Green",
                "Camo", "Custom Pantone"]),
        ],
    },
    {
        "step": 3,
        "title": "Target Fish, Bait &amp; Line",
        "note": "Lure type and line decide the taper more than anything else: soft plastics and "
                "jig heads need a sensitive tip and no stretch, crankbaits need a softer blank that "
                "gives, and metal lures need a fast backbone to drive the hook home.",
        "fields": [
            dict(name="target_species", label="Target species", opts=[
                "Bass", "Trout / perch", "Bream / flathead", "Snapper / grouper",
                "Kingfish / tuna", "Mackerel / bonito", "Carp", "Catfish", "Cod / ling",
                "Squid (egi)", "Pike / zander", "Mixed / general", "Advise me"]),
            dict(name="fishing_method", label="Fishing method", opts=[
                "Shore casting", "Boat / offshore", "Kayak", "Rock &amp; surf",
                "Estuary / river", "Lake / reservoir", "Ice fishing", "Advise me"]),
            dict(name="lure_type", label="Lure / bait type", opts=[
                "Soft plastic — curly tail grub", "Soft plastic — paddle tail shad",
                "Soft plastic — worm / stick bait", "Soft plastic — creature / craw",
                "Hard lure — minnow", "Hard lure — crankbait",
                "Hard lure — vibration / lipless", "Hard lure — pencil / stickbait",
                "Hard lure — popper (topwater)", "Metal jig (slow pitch)",
                "Metal jig (shore jig / casting)", "Spoon / spinner",
                "Glow or UV lure (night fishing)", "Jig head rig",
                "Texas / Carolina rig", "Live or cut bait",
                "Boilie / pellet (carp)", "Fly", "Mixed range", "Advise me"],
                hint="Curly tail and paddle tail are soft plastics; metal jigs and spoons are the "
                     "'iron' lures; glow and UV patterns are for night and deep water."),
            dict(name="main_line", label="Main line", opts=[
                "PE 0.4", "PE 0.6", "PE 0.8", "PE 1.0", "PE 1.2", "PE 1.5", "PE 2.0",
                "PE 3.0", "PE 4.0", "PE 5.0 or heavier",
                "Nylon 4–8 lb", "Nylon 10–14 lb", "Nylon 17–25 lb",
                "Fluorocarbon main line", "Advise me"],
                hint="Thinner line casts further and spooks fewer fish, but it is weaker and "
                     "abrades fast on rock. Best practice: the thinnest braid your structure and "
                     "fish size allow, paired with a fluorocarbon leader."),
            dict(name="leader", label="Leader / shock leader", opts=[
                "None", "Fluorocarbon 6 lb", "Fluorocarbon 10 lb", "Fluorocarbon 16 lb",
                "Fluorocarbon 20 lb", "Fluorocarbon 30 lb", "Fluorocarbon 40 lb",
                "Nylon shock leader", "Wire / tooth-proof leader", "Advise me"],
                hint="Braid has almost no abrasion resistance — a fluorocarbon leader is what "
                     "actually survives contact with rock, teeth and structure."),
            dict(name="lure_colour", label="Lure colour preference", opts=[
                "Natural / clear", "Glow in the dark", "UV reactive", "Chartreuse / high-vis",
                "Dark silhouette", "Mixed selection", "Advise me"]),
        ],
    },
    {
        "step": 4,
        "title": "Guide Train",
        "note": "The reel type decides the whole guide layout: spinning rods need a large first "
                "guide to control line flow, casting rods run a trigger handle with smaller, "
                "lower-profile guides.",
        "fields": [
            dict(name="reel_type", label="Reel type", opts=[
                "Spinning reel", "Baitcasting reel", "Both in one program",
                "Conventional / overhead", "Advise me"],
                hint="Drives guide size, spacing and handle shape."),
            dict(name="guide_type", label="Guide type", opts=[
                "Single-foot guides", "Double-foot guides", "KW anti-tangle",
                "KT micro guides", "Lowrider (long cast)", "MN style", "Advise me"],
                hint="Double-foot guides are stiffer and standard on carp, surf and boat rods."),
            dict(name="guide_ring", label="Guide ring material", opts=[
                "Fuji Alconite", "Fuji SiC", "Fuji Torzite", "Domestic SiC equivalent",
                "Ceramic", "Stainless steel", "Advise me"]),
            dict(name="guide_frame", label="Guide frame", opts=[
                "Stainless steel", "Titanium", "Advise me"]),
            dict(name="guide_count", label="Guide count", opts=[
                "5 + tip", "6 + tip", "7 + tip", "8 + tip", "9 + tip", "10 + tip",
                "Advise me"]),
        ],
    },
    {
        "step": 5,
        "title": "Reel Seat &amp; Handle",
        "note": "This is where a rod is recognised as yours. Seat model, grip material and grip "
                "shape are all tooled to your drawing.",
        "fields": [
            dict(name="reel_seat", label="Reel seat", opts=[
                "Fuji VSS", "Fuji ECS", "Fuji ACS", "Fuji TCS", "Fuji SK2",
                "Aluminium screw seat", "Graphite seat", "Plate / clip seat", "Advise me"]),
            dict(name="handle_material", label="Handle material", opts=[
                "Portuguese cork", "EVA foam", "Cork + EVA mix", "Carbon tube",
                "Hypersensitive (exposed blank)", "Advise me"]),
            dict(name="handle_style", label="Handle shape", opts=[
                "Split grip", "Full grip", "Pistol / trigger (casting)",
                "Straight (spinning)", "Extended fighting butt", "Advise me"]),
            dict(name="butt_cap", label="Butt cap", opts=[
                "Rubber", "Metal", "Carbon", "Weighted / balanced", "Advise me"]),
        ],
    },
    {
        "step": 6,
        "title": "Branding &amp; Packaging",
        "note": "Your name goes on the rod, the sock and the box. Retail-ready packaging is quoted "
                "separately from the rod because carton tooling is a one-off cost.",
        "fields": [
            dict(name="logo_method", label="Logo method", opts=[
                "Silk-screen print", "Laser engraving", "Hydro-dip transfer",
                "Woven / embroidered label", "No logo", "Advise me"]),
            dict(name="packaging", label="Packaging", opts=[
                "Cloth rod bag", "Paper tube", "PVC hard tube", "Printed colour box",
                "Bulk / no retail pack", "Custom retail packaging", "Advise me"]),
            dict(name="hook_keeper", label="Hook keeper", opts=[
                "Yes", "No", "Advise me"]),
            dict(name="kit_option", label="Supply as", opts=[
                "Rod only", "Rod + reel combo", "Rod + reel + line spooled",
                "Rod + starter lure set", "Full retail kit (rod, reel, line, lures, packaging)",
                "Advise me"],
                hint="Reels, line and lures come from audited partner factories and ship in the "
                     "same carton as the rod — one purchase order instead of four."),
        ],
    },
    {
        "step": 7,
        "title": "Quantity &amp; Contact",
        "note": "MOQ is 300 pieces per model. Mixed models in one container are welcome, and "
                "first programs often start with one model before expanding.",
        "fields": [
            dict(name="quantity", label="Quantity per model", opts=[
                "300 pcs", "500 pcs", "1,000 pcs", "3,000 pcs", "5,000 pcs or more",
                "Sample order first", "Not decided yet"]),
            dict(name="target_market", label="Target market", opts=[
                "Australia", "United Kingdom", "Europe (EU)", "Japan", "South Korea",
                "North America", "Other"]),
            dict(name="name", label="Full name *", kind="text", required=True,
                 placeholder="Jane Smith"),
            dict(name="email", label="Work email *", kind="email", required=True,
                 placeholder="jane@company.com"),
            dict(name="company", label="Company / brand", kind="text", placeholder="Company name"),
            dict(name="notes", label="Anything else we should know", kind="textarea", full=True,
                 placeholder="Reference product or link, target retail price, timeline, "
                             "certifications you need (REACH, UKCA), or a spec sheet you want matched."),
        ],
    },
]


def _field_html(f):
    name = f["name"]
    label = f["label"]
    kind = f.get("kind", "select")
    hint = ('<p class="form-hint">%s</p>' % f["hint"]) if f.get("hint") else ""
    req = " required" if f.get("required") else ""
    cls = "form-field full" if f.get("full") else "form-field"
    if kind == "select":
        opts = ['<option value="">— select —</option>']
        opts += ['<option value="%s">%s</option>' % (o, o) for o in f["opts"]]
        ctl = '<select id="cfg-%s" name="%s"%s>%s</select>' % (name, name, req, "".join(opts))
    elif kind == "textarea":
        ctl = ('<textarea id="cfg-%s" name="%s" rows="4"%s placeholder="%s"></textarea>'
               % (name, name, req, f.get("placeholder", "")))
    else:
        ctl = ('<input id="cfg-%s" name="%s" type="%s"%s placeholder="%s">'
               % (name, name, kind, req, f.get("placeholder", "")))
    return ('<div class="%s"><label for="cfg-%s">%s</label>%s%s</div>'
            % (cls, name, label, ctl, hint))


def render_body(wa_url, form_endpoint):
    groups = []
    for g in GROUPS:
        fields = "".join(_field_html(f) for f in g["fields"])
        groups.append("""
      <fieldset class="cfg-group">
        <h3><span class="cfg-step">%d</span>%s</h3>
        <p class="cfg-note">%s</p>
        <div class="cfg-fields">%s</div>
      </fieldset>""" % (g["step"], g["title"], g["note"], fields))

    return """
<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">OEM Configurator</span>
    <h1>Build Your Rod — We Quote What You Choose</h1>
    <p class="lead">Pick what matters to you and skip the rest. Every option below is something our
    Weihai lines actually build, so the specification you create here goes straight into a quotation
    — no generic catalogue, no waiting for someone to guess your market. You will get pricing,
    MOQ, sample cost and a freight estimate within one business day.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container cfg-layout">
    <form id="cfg-form" class="cfg-form" action="%(form)s" method="POST">
      <div class="hp-field" aria-hidden="true">
        <label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>
      </div>
      <input type="hidden" name="_subject" id="cfg-subject" value="OEM rod configurator inquiry — entrol-fishing.com">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="spec_summary" id="cfg-summary-input" value="">
      %(groups)s
      <div class="cfg-group">
        <p class="form-hint">Fields marked * are required. Everything else is optional — the more
        you select, the more accurate the first quotation. Nothing here is shared outside this
        inquiry.</p>
        <button class="btn btn-primary" type="submit" style="width:100%%;margin-top:14px">Send My Specification</button>
        <div class="form-status" role="status" style="margin-top:12px"></div>
      </div>
    </form>

    <aside class="cfg-summary" aria-live="polite">
      <h3>Your Specification</h3>
      <p class="cfg-count" id="cfg-count">0 options selected</p>
      <ul class="cfg-list" id="cfg-list"></ul>

      <div class="cfg-combo" id="cfg-combo">
        <h4>Suggested set-up</h4>
        <p class="cfg-combo-lead" id="cfg-combo-lead">Pick a target species or lure type and we
        will suggest the matching taper, line and reel size here.</p>
        <ul id="cfg-combo-list"></ul>
      </div>

      <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Or chat on WhatsApp</a>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">Matched Kits</span>
      <h2>Take the Whole Set — Rod, Reel, Line and Lures in One Carton</h2>
      <p class="lead">Most importers buy the rod from one factory, the reel from a second and the
      terminal tackle from a third, then pay three times to consolidate. We can ship the complete
      set, matched to the specification above and packed together under your brand.</p>
    </div>
    <div class="cfg-why" style="margin-top:30px">
      <div class="card"><h4>Rod + reel combo</h4><p>A size-matched reel mounted on the rod you
      specified, balanced and spooled. One carton, one barcode, retail-ready.</p></div>
      <div class="card"><h4>Starter lure set</h4><p>Five to ten lures chosen for the species and
      method you selected — soft plastics, metal jigs or hard lures, bagged and header-carded.</p></div>
      <div class="card"><h4>Line &amp; leader pack</h4><p>Braid and fluorocarbon leader at the rating
      we recommend above, spooled on the reel or boxed as its own retail SKU.</p></div>
      <div class="card"><h4>Private-label accessories</h4><p>Hooks, jig heads, swivels and tools from
      audited partner factories, packed under your brand alongside the rod.</p></div>
    </div>
    <div class="center" style="margin-top:28px">
      <a class="btn btn-primary" href="contact.html">Ask About a Complete Kit</a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <span class="eyebrow">Why Bother Specifying</span>
    <h2>Four Things a Configured Enquiry Gets You That an Email Doesn't</h2>
    <div class="cfg-why" style="margin-top:26px">
      <div class="card"><h4>A real number, not a range</h4><p>Guide material and carbon grade are
      the two largest cost drivers in a blank. Tell us which you want and we price the actual rod,
      not a "from $X" placeholder.</p></div>
      <div class="card"><h4>No sample roulette</h4><p>A configured spec means the first sample
      arrives close to what you sell. Most programs are approved within two sample rounds.</p></div>
      <div class="card"><h4>Your brand on the rod</h4><p>Logo method, colour and packaging are part
      of the build, not an afterthought you negotiate later at extra cost.</p></div>
      <div class="card"><h4>Locked for reorders</h4><p>We keep your specification on file, so a
      repeat order twelve months later matches the first one exactly.</p></div>
    </div>
    <div class="cta-band" style="margin-top:36px">
      <h2>Not Sure Which Options to Pick?</h2>
      <p>Send us a photo or a link to a rod you like and we will reverse-engineer the specification
      for you — then you can approve the build sheet before any tooling starts.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="contact.html">Send a Reference Rod</a>
        <a class="btn btn-outline" href="products.html">Browse Rod Categories</a>
      </div>
    </div>
  </div>
</section>""" % {"form": form_endpoint, "groups": "".join(groups), "wa": wa_url}


TITLE = "Build Your Rod | OEM Fishing Rod Configurator | Entrol Fishing"
DESC = ("Configure a custom fishing rod: carbon grade, guide type, reel seat, handle and packaging. "
        "Get an OEM quotation from Weihai, China within one business day. MOQ 300 pcs/model.")
KEYWORDS = ("custom fishing rod configurator, OEM rod builder, carbon rod specification, "
            "Fuji guide rod OEM, carp rod specification, build your own fishing rod wholesale")
