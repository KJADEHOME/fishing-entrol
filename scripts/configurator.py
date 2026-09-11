#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rod configurator page content — two paths, one catalogue.

Two different buyers land on this page:

  * an OEM buyer specifying a production run (300 pcs and up), and
  * an angler who wants one rod built around their own water, body and taste.

They need different questions, so every field carries a `path`: "oem",
"custom", or None for both. The switch at the top shows one set and disables
the other — a disabled field is skipped by FormData, so the hidden half never
reaches the enquiry.

Every option list is generated from scripts/catalog_data.py wherever a real
product exists, so the picker, the spec tables and the compatibility engine
can never drift apart. Change the catalogue, rebuild, and both follow.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog_data as cat  # noqa: E402


def _num(v):
    """Leading number of a spec value so 1, 2 and '1.5 (jointed)' can be sorted together."""
    try:
        return float(str(v).replace(",", ".").split()[0])
    except (ValueError, IndexError, AttributeError):
        return 9999.0


def _rod_opts(key, fmt=None, numeric=False, extra=()):
    """Unique rod values for `key` — catalogue first, then generic extras."""
    rods = sorted(cat.RODS, key=lambda r: _num(r["specs"].get(key))) if numeric else cat.RODS
    out = []
    for p in rods:
        v = p["specs"].get(key)
        if v in (None, "", "—"):
            continue
        s = fmt(v, p) if fmt else str(v)
        if s and s not in out:
            out.append(s)
    for e in extra:
        if e not in out:
            out.append(e)
    return out


def _metres(v, _p):
    return "%.2f m (%s)" % (v, _p["specs"]["length_ft"])


def _sections(v, _p):
    if isinstance(v, int):
        return "%d piece" % v if v == 1 else "%d pieces" % v
    return str(v)


# option lists straight out of the catalogue -------------------------------
LENGTH_OPTS = _rod_opts("length_m", fmt=_metres, numeric=True,
                        extra=("1.68 m (5'6\")", "1.80 m (5'11\")", "2.10 m (6'11\")",
                               "2.40 m (7'10\")", "3.30 m (10'10\")", "3.90 m (12'9\")",
                               "Custom length"))
POWER_OPTS = _rod_opts("power", extra=("Ultra-Light", "Advise me"))
ACTION_OPTS = _rod_opts("action", extra=("Slow", "Moderate", "Extra-Fast", "Advise me"))
LINE_OPTS = _rod_opts("line_rating", extra=("PE 0.6–1.2", "PE 1.5–3.0", "PE 3.0–5.0",
                                            "4–12 lb", "20–40 lb", "Advise me"))
CAST_OPTS = _rod_opts("cast_weight_g", extra=("under 5 g", "5–21 g", "10–30 g", "20–50 g",
                                              "30–80 g", "50–120 g", "100–200 g",
                                              "over 200 g", "Advise me"))
REEL_OPTS = _rod_opts("reel_type", extra=("Both in one program", "Advise me"))
HANDLE_OPTS = _rod_opts("handle", extra=("Portuguese cork", "EVA foam", "Cork + EVA mix",
                                         "Carbon tube", "Hypersensitive (exposed blank)",
                                         "Advise me"))
SECTION_OPTS = _rod_opts("sections", fmt=_sections, numeric=True,
                         extra=("4 pieces", "5 pieces or more", "Telescopic", "Advise me"))

MODEL_GROUPS = [
    ("spinning", "Spinning"),
    ("casting", "Baitcasting"),
    ("carp", "Carp"),
    ("boat", "Boat &amp; bottom"),
    ("jigging", "Slow-pitch jigging"),
    ("surf", "Rock &amp; surf"),
]

# field = dict(name, label, opts|None, hint=None, full=False, required=False,
#              kind=select|text|email|textarea|model|path, path="oem"|"custom"|None)
GROUPS = [
    {
        "step": 0,
        "title": "Which Kind of Build Is This?",
        "note": "Both paths build the same rods on the same lines — they differ in how many, "
                "how they are labelled, and how long they take.",
        "fields": [
            dict(name="build_path", label="I am ordering as", kind="path", required=True),
        ],
    },
    {
        "step": 1,
        "title": "Start From a Model, or Start From Scratch",
        "note": "Picking an existing model fills in its real measurements — length, power, line "
                "rating and recommended reel — and everything after that becomes a change you are "
                "making to a rod that already exists. Leave it blank to specify from nothing.",
        "fields": [
            dict(name="base_model", label="Start from an existing model", kind="model",
                 hint="Optional. Choose a model to prefill, then change anything you like below."),
            dict(name="rod_type", label="Rod type", opts=[
                "Spinning rod", "Casting / baitcasting rod", "Carp rod", "Surf / rock rod",
                "Boat &amp; jigging rod", "Telescopic travel rod", "Fly rod", "Ice rod",
                "Not sure — advise me"]),
            dict(name="length", label="Length", opts=LENGTH_OPTS),
            dict(name="sections", label="Sections", opts=SECTION_OPTS),
            dict(name="power", label="Power", opts=POWER_OPTS),
            dict(name="action", label="Action / taper", opts=ACTION_OPTS),
            dict(name="lure_weight", label="Lure / cast weight", opts=CAST_OPTS),
            dict(name="line_rating", label="Line rating", opts=LINE_OPTS),
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
                     "fish size allow, paired with a fluorocarbon leader. Everything listed here "
                     "is in stock as a neutral-specification spool."),
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
            dict(name="reel_type", label="Reel type", opts=REEL_OPTS,
                 hint="Drives guide size, spacing and handle shape."),
            dict(name="reel_size", label="Reel size", opts=[
                "1000", "2000", "2500", "3000", "4000", "5000", "6000",
                "Baitcaster 100", "Baitcaster 200", "Overhead / conventional", "Advise me"],
                hint="Sizes in stock. Reel-to-rod mismatches are flagged in the summary panel."),
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
            dict(name="handle_material", label="Handle material", opts=HANDLE_OPTS),
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
        "path": "oem",
        "note": "Your name goes on the rod, the sock and the box. Retail-ready packaging is quoted "
                "separately from the rod because carton tooling is a one-off cost. Reels, line and "
                "lures are labelled separately too — see the last question in this group.",
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
                hint="Kits ship in one carton on one purchase order. Note the MOQ rises when reels, "
                     "line or lures are included — see the minimum-order table before you choose."),
            dict(name="kit_brand", label="Brand on the reel / line / lures", opts=[
                "Our brand on everything (1,000 pcs min)",
                "Component maker's own brand",
                "Unbranded / neutral bulk pack",
                "Recommend a house brand that fits my price point",
                "Not ordering a kit — rod only",
                "Advise me"],
                hint="The rod always carries your brand. Reels, line and lures are bought in from "
                     "component makers — we do not manufacture them and we do not put our own name "
                     "on them. They can be printed with your brand from 1,000 pcs, or shipped under "
                     "the maker's own brand, an unbranded neutral pack, or a house brand we propose "
                     "to your target price."),
        ],
    },
    {
        "step": 6,
        "title": "Finish &amp; Personal Details",
        "path": "custom",
        "note": "One rod, built for one angler. There is no stock to pull from and no bulk print "
                "run to spread tooling across, so a single build costs more per rod than a "
                "production order — and because it is made to your measurements it cannot be "
                "resold to anyone else if you change your mind.",
        "fields": [
            dict(name="engraving", label="Engraving on the butt cap", kind="text",
                 placeholder="Up to 24 characters — a name, a date, a boat name",
                 hint="Laser engraved. Personalised rods cannot be returned or exchanged unless "
                      "they arrive damaged."),
            dict(name="thread_colour", label="Guide wrap &amp; trim colour", opts=[
                "Match the blank (subtle)", "Black", "Deep blue", "Burgundy", "Olive",
                "Metallic silver", "Metallic gold", "Two-tone — tell us in the notes",
                "Advise me"]),
            dict(name="custom_pack", label="How it ships to you", opts=[
                "Cloth rod sock", "Hard PVC tube", "Sock + hard tube", "No case — rod only",
                "Advise me"],
                hint="A hard tube is worth it for anything travelling by air freight."),
    dict(name="kit_option_custom", label="Do you want it rigged and ready?", opts=[
                "Rod only", "Rod + reel", "Rod + reel + line spooled",
                "Rod + reel + line + starter lures", "Advise me"],
                hint="Components are sourced to your budget and shipped under a neutral or "
                     "component-maker label — we do not put our own badge on them."),
            dict(name="spool_service", label="Spool the line onto the reel?", opts=[
                "Yes — spool it and tie the leader", "Yes — line only, I will rig it",
                "No — send the spool separately", "Not ordering line", "Advise me"],
                hint="A reel spooled by hand with the right backing and the right amount of line "
                     "behaves differently from one filled at random — worth doing properly."),
            dict(name="ship_to", label="Shipping country", kind="text",
                 placeholder="e.g. Australia, Germany, Japan",
                 hint="Freight on a single rod is quoted per destination before we start."),
        ],
    },
    {
        "step": 7,
        "title": "What Else Goes in the Box",
        "path": "custom",
        "note": "Pick the reels, line and lures you want with the rod and say how many of each. "
                "Add a second row when you want two different models — a 2500 for the estuary and "
                "a 4000 for the rocks, or two line strengths for two different waters.",
        "extra": ('<input type="hidden" name="kit_lines" id="kit-lines-input" value="">'
                  '<div class="kit-lines" id="kit-lines"></div>'
                  '<p class="form-hint">Leave a row on "none" if you do not want that item. '
                  'Everything here is a neutral-specification component bought in from component '
                  'makers, so it ships under a neutral label — not ours, and not a brand we '
                  'invented.</p>'),
        "fields": [
            dict(name="budget", label="Budget for the whole order", opts=[
                "Under $150", "$150–300", "$300–500", "$500–800", "$800 or more",
                "Not sure — quote me and I will decide"],
                hint="This is what decides whether a 40T blank with titanium guides makes sense or "
                     "whether a 30T build puts the money where you will actually feel it."),
            dict(name="urgency", label="When do you want it in your hands?", opts=[
                "As soon as possible", "Within a month", "2–3 months is fine",
                "No rush — I am planning ahead", "It is a gift — I have a date"],
                hint="A single build runs 20–25 days before it ships. If you have a date, say so "
                     "and we will tell you honestly whether we can hit it."),
        ],
    },
    {
        "step": 8,
        "title": "Quantity, Timing &amp; Contact",
        "note": '<span id="cfg-qty-note">Two different minimums apply, and it is worth knowing which '
                'one you are buying before we quote: rod-only programs run from 300 pieces per model, '
                'while anything that puts a reel, line or lures in the carton starts at 500 — and '
                '1,000 if those components also carry your brand. Mixed rod models in one container '
                'are always fine.</span>',
        "extra": '<div class="cfg-moq" id="cfg-moq"></div>',
        "fields": [
            dict(name="quantity", label="Quantity per model", path="oem", opts=[
                "300 pcs", "500 pcs", "1,000 pcs", "3,000 pcs", "5,000 pcs or more",
                "Sample order first", "Not decided yet"]),
            dict(name="model_count", label="How many models in this order", path="oem", opts=[
                "1 model", "2–3 models", "4–6 models", "7 or more", "Not decided yet"],
                hint="Each model is its own mandrel and its own print run, which is why the "
                     "minimum is quoted per model rather than per order."),
            dict(name="target_price", label="Target retail price per rod", path="oem", opts=[
                "Under $30", "$30–60", "$60–100", "$100–200", "$200 and up",
                "Tell me what my spec costs first"],
                hint="The single most useful number you can give us. It decides the blank, the "
                     "guide train and the packaging before we quote anything."),
            dict(name="annual_volume", label="Expected volume over 12 months", path="oem", opts=[
                "This is a first trial", "1,000–5,000 pcs", "5,000–20,000 pcs",
                "20,000 pcs or more", "Not decided yet"],
                hint="Tells us whether to quote a one-off or a program price, and whether "
                     "dedicated tooling pays for itself."),
            dict(name="ship_window", label="When do you need it on the water", path="oem", opts=[
                "As soon as possible", "Within 3 months", "Within 6 months",
                "Next season", "No fixed date yet"],
                hint="Rod programs run 35–45 days after sample approval, plus freight. Season "
                     "deadlines are the usual reason a program slips, so tell us early."),
            dict(name="compliance", label="Certification you need", path="oem", opts=[
                "REACH (EU)", "UKCA (UK)", "CPSIA / CA Prop 65 (US)", "EN71 (if sold as toy)",
                "None specified yet", "Not sure — advise me"],
                hint="Compliance testing is booked against your market, not ours — telling us now "
                     "avoids a shipment held at the border."),
            dict(name="trade_terms", label="Preferred terms", path="oem", opts=[
                "FOB Qingdao", "EXW", "CIF", "DDP to my warehouse", "Not sure — advise me"]),
            dict(name="sample_plan", label="How do you want to start?", path="oem", opts=[
                "Send a pre-production sample first", "Quote only for now",
                "I will send you a reference rod", "Ready to order", "Not decided yet"]),
            dict(name="quantity_custom", label="How many rods", path="custom", opts=[
                "1 rod", "2 rods", "3 rods", "4 rods", "5 rods", "6–10 rods",
                "More than 10", "Not decided yet"]),
            dict(name="target_market", label="Target market", opts=[
                "Australia", "United Kingdom", "Europe (EU)", "Japan", "South Korea",
                "North America", "Other"]),
            dict(name="name", label="Full name *", kind="text", required=True,
                 placeholder="Jane Smith"),
            dict(name="email", label="Email *", kind="email", required=True,
                 placeholder="jane@company.com"),
            dict(name="company", label="Company / brand", path="oem", kind="text",
                 placeholder="Company name"),
            dict(name="notes", label="Anything else we should know", kind="textarea", full=True,
                 placeholder="A reference product or link, a spec sheet you want matched, a rod "
                             "you already fish and want changed, or anything the questions above "
                             "did not cover."),
        ],
    },
]


def _attr(s):
    """Escape for use inside a double-quoted HTML attribute.

    Only the quote character is touched: option text deliberately carries
    pre-escaped entities such as &amp; (e.g. "Boat &amp; jigging rod"), so a
    full html.escape() would double-escape them.
    """
    return str(s).replace('"', "&quot;")


def _model_select(name, label):
    """Start-from-a-model picker, grouped by rod family, built from the catalogue."""
    groups = []
    for sub, title in MODEL_GROUPS:
        opts = []
        for p in cat.rods_by_sub(sub):
            s = p["specs"]
            desc = "%s · %s · %s" % (s["length_ft"], s["power"], s.get("line_rating", "—"))
            opts.append('<option value="%s">%s — %s</option>'
                        % (_attr(p["sku"]), _attr(p["sku"]), _attr(desc)))
        if opts:
            groups.append('<optgroup label="%s">%s</optgroup>' % (title, "".join(opts)))
    ctl = ('<select id="cfg-%s" name="%s"><option value="">— build from scratch —</option>%s'
           '</select>' % (name, name, "".join(groups)))
    return ('<div class="form-field"><label for="cfg-%s">%s</label>%s</div>'
            % (name, label, ctl))


def _path_switch(name, label):
    """Two-card radio: OEM program vs a single custom build."""
    cards = [
        ("oem", "OEM / private-label program",
         "300 pcs and up · your brand on the rod · full spec, packaging and kit options"),
        ("custom", "One rod, built for me",
         "A single custom rod, or a handful · your measurements and finish · 1 rod minimum"),
    ]
    html_cards = []
    for val, title, sub in cards:
        html_cards.append(
            '<label class="cfg-path" for="cfg-path-%s">'
            '<input type="radio" id="cfg-path-%s" name="%s" value="%s"%s>'
            '<span class="cfg-path-t">%s</span><span class="cfg-path-s">%s</span></label>'
            % (val, val, name, val, " checked" if val == "oem" else "", title, sub))
    return ('<div class="form-field full"><span class="cfg-path-lab">%s</span>'
            '<div class="cfg-path-row">%s</div></div>' % (label, "".join(html_cards)))


def _field_html(f):
    name = f["name"]
    label = f["label"]
    kind = f.get("kind", "select")
    hint = ('<p class="form-hint">%s</p>' % f["hint"]) if f.get("hint") else ""
    req = " required" if f.get("required") else ""
    cls = "form-field full" if f.get("full") else "form-field"
    if f.get("path"):
        cls += " cfg-only-%s" % f["path"]
    if kind == "select":
        opts = ['<option value="">— select —</option>']
        opts += ['<option value="%s">%s</option>' % (_attr(o), o) for o in f["opts"]]
        ctl = '<select id="cfg-%s" name="%s"%s>%s</select>' % (name, name, req, "".join(opts))
    elif kind == "textarea":
        ctl = ('<textarea id="cfg-%s" name="%s" rows="4"%s placeholder="%s"></textarea>'
               % (name, name, req, _attr(f.get("placeholder", ""))))
    elif kind == "text" or kind == "email":
        ctl = ('<input id="cfg-%s" name="%s" type="%s"%s placeholder="%s"%s>'
               % (name, name, kind, req, _attr(f.get("placeholder", "")),
                  "" if kind == "text" else ' autocomplete="email"'))
    elif kind == "model":
        return '<div class="%s">%s%s</div>' % (cls, _model_select(name, label), hint)
    elif kind == "path":
        return '<div class="%s">%s</div>' % (cls, _path_switch(name, label))
    else:
        ctl = ('<input id="cfg-%s" name="%s" type="text"%s placeholder="%s">'
               % (name, name, req, _attr(f.get("placeholder", ""))))
    return ('<div class="%s"><label for="cfg-%s">%s</label>%s%s</div>'
            % (cls, name, label, ctl, hint))


PAGE_META = {
    None: {
        "eyebrow": "Rod Configurator",
        "h1": "Build Your Rod — We Quote What You Choose",
        "lead": "Pick what matters to you and skip the rest. Every option below is something our "
                "Weihai lines actually build, so the specification you create here goes straight "
                "into a quotation — no generic catalogue, no waiting for someone to guess your "
                "market. You will get pricing, MOQ, sample cost and a freight estimate within one "
                "business day.",
        "second": "<p><strong>If two of your choices will not work together, the site tells you "
                  "here and now.</strong> A spinning blank with a baitcasting reel, a 2-metre rod "
                  "asked to throw 100 g, PE 0.6 behind a heavy shore jig — each of those is a rod "
                  "that breaks, casts badly or injures someone, and each one is caught before it "
                  "reaches a production order. Watch the summary panel as you go.</p>",
    },
    "oem": {
        "eyebrow": "OEM Program",
        "h1": "Define the Rod Your Brand Sells",
        "lead": "This is the form for a production program: you are deciding what goes on your "
                "shelves, in your carton and under your logo. Work through the groups below and we "
                "come back with a costed build sheet — blank, components, cosmetics, packaging, "
                "MOQ, sample cost and freight — within one business day.",
        "second": "<p><strong>Two answers shape everything else: how many, and what it has to sell "
                  "for.</strong> Give us the quantity per model and the retail price you are aiming "
                  "at, and we engineer towards that number instead of quoting a rod you then have "
                  "to talk down. If two of your choices will not work together — a baitcasting reel "
                  "on a spinning blank, PE 0.6 behind a heavy shore jig — the page flags it here, "
                  "before it reaches a production order.</p>",
    },
    "custom": {
        "eyebrow": "One Custom Rod",
        "h1": "One Rod, Built Around How You Fish",
        "lead": "This is the form for a single rod, or two — yours, not a shelf full of them. "
                "Choose the blank and the components, add the reel, line and lures you want "
                "alongside it, tell us what to engrave, and we quote the whole thing before "
                "anything is built.",
        "second": "<p><strong>There is no minimum, and there is no stock to pick from.</strong> "
                  "Your rod is made after you order it — which is also why a rod carrying your own "
                  "engraving cannot be returned. We send photos before it ships, but the rod is "
                  "yours the moment it is built. If two of your choices will not work together, "
                  "the page flags it here and now.</p>",
    },
}

CUSTOM_KIT_BLOCK = """
<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">What Comes With It</span>
      <h2>Rod, Reel, Line and Lures — You Decide How Much</h2>
      <p class="lead">A custom rod does not have to arrive alone. Add a reel, line or a starter set
      of lures and we source them to the same brief, then ship the lot in one package. We do not
      put our own badge on someone else's reel: the rod is ours to build, the components are
      sourced to what you asked for.</p>
    </div>
    <div class="cfg-why" style="margin-top:30px">
      <div class="card"><h4>Rod (built for you)</h4><p>Your blank, guides, seat, handle, wrapping
      colours and engraving. One is enough — there is no minimum on this page.</p></div>
      <div class="card"><h4>Reel (sourced to your brief)</h4><p>Size, gear ratio, drag and budget.
      We come back with two or three options and you pick; add more than one if you fish two
      methods.</p></div>
      <div class="card"><h4>Line &amp; leader</h4><p>Braid and fluorocarbon at the rating the page
      recommends for your rod, in as many spools as you want. We can spool it on the reel before
      shipping.</p></div>
      <div class="card"><h4>Lures &amp; terminal tackle</h4><p>Soft plastics, metal jigs or hard
      lures chosen for your species and method. Tell us how many of each — mixed selections are
      normal.</p></div>
    </div>

    <div class="card" style="margin-top:30px">
      <h3 style="margin-top:0">Three things to know before you send this</h3>
      <ul class="feature-list">
        <li><strong>Lead time.</strong> A single custom rod takes about 20–25 days to build, plus
        shipping to your country. We confirm the date before you pay anything.</li>
        <li><strong>Deposit.</strong> Custom builds start on a 50% deposit, with the balance due
        before shipment. Photos of the finished rod go out first.</li>
        <li><strong>No returns on engraved rods.</strong> Once your name or text is on the blank it
        cannot be sold to anyone else, so custom rods are not returnable. Damage in transit is of
        course a different matter — we sort that out with the carrier.</li>
      </ul>
      <p class="form-hint" style="margin-top:12px">Freight for a single rod is quoted to your door
      before the build starts. On a long, one-piece blank it can be a real share of the total, so
      it is worth seeing that number first.</p>
    </div>

    <div class="center" style="margin-top:28px">
      <a class="btn btn-accent" href="contact.html">Ask a Question First</a>
    </div>
  </div>
</section>
"""


def render_body(wa_url, form_endpoint, path=None):
    """Render the configurator form.

    path=None  -> combined page with the OEM / personal switch at the top
    path=oem   -> OEM program page only (switch replaced by a hidden field)
    path=custom-> personal rod page only
    """
    fixed = path in ("oem", "custom")
    groups = []
    for g in GROUPS:
        if fixed and g.get("step") == 0:
            continue
        if fixed and g.get("path") and g["path"] != path:
            continue
        fl = g["fields"]
        if fixed:
            fl = [f for f in fl if not f.get("path") or f["path"] == path]
        if not fl:
            continue
        fields = "".join(_field_html(f) for f in fl)
        groups.append("""
      <fieldset class="cfg-group">
        <h3><span class="cfg-step">%d</span>%s</h3>
        <p class="cfg-note">%s</p>
        <div class="cfg-fields">%s</div>
        %s
      </fieldset>""" % (g["step"], g["title"], g["note"], fields, g.get("extra", "")))

    # The page needs rods (for the "start from a model" prefill) and the line,
    # lure and reel rows (for the accessory picker), so ship a slimmed full
    # catalogue: short keys, no fields the browser never reads.
    slim = [dict(s=p["sku"], c=p["category"], b=p["subcategory"], n=p["name"], p=p["specs"])
            for p in cat.PRODUCTS]
    # </ inside a <script> block would end the element early; \/ is valid JSON.
    catalog_payload = json.dumps(slim, ensure_ascii=False,
                                 separators=(",", ":")).replace("</", "<\\/")

    meta = PAGE_META.get(path, PAGE_META[None])
    path_field = ('<input type="hidden" name="build_path" value="%s">' % path) if fixed else ""
    body = """
<script type="application/json" id="catalog-data">%(catalog)s</script>

<section class="section" style="padding-top:34px">
  <div class="container">
    <span class="eyebrow">%(eyebrow)s</span>
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    %(second)s
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container cfg-layout">
    <form id="cfg-form" class="cfg-form" action="%(form)s" method="POST" data-path="%(pathattr)s">
      %(pathfield)s
      <div class="hp-field" aria-hidden="true">
        <label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>
      </div>
      <input type="hidden" name="_subject" id="cfg-subject" value="Rod configurator inquiry — entrol-fishing.com">
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
      <div class="cfg-warnbox" id="cfg-warnbox"></div>
      <h3>Your Specification</h3>
      <p class="cfg-count" id="cfg-count">0 options selected</p>
      <ul class="cfg-list" id="cfg-list"></ul>

      <div class="cfg-combo" id="cfg-combo">
        <h4>Suggested set-up</h4>
        <p class="cfg-combo-lead" id="cfg-combo-lead">Pick a target species or lure type and we
        will suggest the matching taper, line and reel size here.</p>
        <ul id="cfg-combo-list"></ul>
      </div>

      <div class="cfg-kit" id="cfg-kit" hidden>
        <h4>In the box</h4>
        <ul id="cfg-kit-list"></ul>
        <p class="cfg-kit-total" id="cfg-kit-total"></p>
      </div>

      <a class="btn btn-outline" href="%(wa)s" target="_blank" rel="noopener" data-track="whatsapp">Or chat on WhatsApp</a>
    </aside>
  </div>
</section>

<!-- kits:start -->
<section class="section">
  <div class="container">
    <div class="center">
      <span class="eyebrow">Matched Kits</span>
      <h2>One Carton, One Order — and Honest Labels</h2>
      <p class="lead">Most importers buy the rod from one factory, the reel from a second and the
      terminal tackle from a third, then pay three times to consolidate. We can assemble the whole
      set to the specification above and ship it together. One thing we will not do is put our own
      badge on someone else's reel: <strong>the rod is ours to build, the components are sourced to
      your brief</strong>, and how they are labelled is your call.</p>
    </div>
    <div class="cfg-why" style="margin-top:30px">
      <div class="card"><h4>Rod (built by us)</h4><p>Your blank, guides, seat, handle, cosmetics and
      packaging. Always carries your brand — 300 pcs per model, any spec you configure above.</p></div>
      <div class="card"><h4>Reel (sourced to your brief)</h4><p>Tell us the size, gear ratio, drag
      and price point and we come back with two or three options from component makers — your brand
      from 1,000 pcs, or theirs below that.</p></div>
      <div class="card"><h4>Line &amp; leader pack</h4><p>Braid and fluorocarbon at the rating we
      recommend above, spooled on the reel or boxed as its own retail SKU. Branded spools from
      1,000 pcs; unbranded bulk below that.</p></div>
      <div class="card"><h4>Lures &amp; terminal tackle</h4><p>Soft plastics, metal jigs or hard
      lures chosen for your species and method, bagged and header-carded. Mixed selections are
      normal — a starter set usually runs five to ten pieces.</p></div>
    </div>

    <div class="card" style="margin-top:30px">
      <h3 style="margin-top:0">How the minimum order splits</h3>
      <p>A rod program and a kit program are not the same purchase, and quoting them as if they were
      is how container deals fall apart at the last minute. Each part carries its own minimum because
      each part is made by someone else.</p>
      <table class="spec-table">
        <thead><tr><th>What you order</th><th>Minimum</th><th>What it covers</th></tr></thead>
        <tbody>
          <tr><td>Rod only — your spec, your brand</td><td><strong>300 pcs / model</strong></td>
              <td>Blank, guide train, reel seat, handle, cosmetics and packaging, all to your
              specification. Mixed models in one container are welcome.</td></tr>
          <tr><td>Rod + reel, + line or + lure set</td><td><strong>500 pcs</strong></td>
              <td>The rod plus matched components in one carton. Below 500 the component makers will
              not open a production slot for a custom specification.</td></tr>
          <tr><td>Full kit, or components printed with your brand</td>
              <td><strong>1,000 pcs</strong></td>
              <td>Your logo on the reel body, line spool or lure cards means their own tooling and
              print run — that is where the 1,000 starts.</td></tr>
        </tbody>
      </table>
      <p class="form-hint" style="margin-top:12px">We quote each part on its own line so you can see
      exactly what the reel costs versus the rod — and drop a component if it does not work for your
      market. Nothing is bundled into a single number you cannot check.</p>
    </div>

    <div class="center" style="margin-top:28px">
      <a class="btn btn-primary" href="contact.html">Ask About a Complete Kit</a>
    </div>
  </div>
</section>

<!-- kits:end -->
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
</section>""" % {"form": form_endpoint, "groups": "".join(groups), "wa": wa_url,
                 "catalog": catalog_payload,
                 "eyebrow": meta["eyebrow"], "h1": meta["h1"], "lead": meta["lead"],
                 "second": meta["second"], "pathattr": path or "", "pathfield": path_field}

    if path == "custom":
        start = body.index("<!-- kits:start -->")
        end = body.index("<!-- kits:end -->") + len("<!-- kits:end -->")
        body = body[:start] + CUSTOM_KIT_BLOCK + body[end:]
    return body


TITLE_OEM = "OEM Rod Builder | Define a Production Rod | Entrol Fishing"
DESC_OEM = ("Define a production fishing rod for your brand: blank, guide train, reel seat, handle, "
            "cosmetics and packaging. MOQ 300 pcs per model, samples in 15-20 days. Quoted within "
            "one business day.")
KEYWORDS_OEM = ("fishing rod OEM program, private label fishing rods, custom rod specification, "
                "rod manufacturer MOQ, bulk fishing rods wholesale, OEM carbon rod builder")

TITLE_CUSTOM = "Custom Fishing Rod | Built to Your Measurements | Entrol Fishing"
DESC_CUSTOM = ("Order a single custom fishing rod built to your measurements — blank, guides, "
               "handle, wrapping colours and engraving. Add a reel, line and lures. No minimum "
               "order, quoted before anything is built.")
KEYWORDS_CUSTOM = ("custom fishing rod, bespoke fishing rod, custom built carp rod, one off fishing "
                   "rod, personalised fishing rod, custom rod builder")


TITLE = "Build Your Rod | OEM & Custom Rod Configurator | Entrol Fishing"
DESC = ("Configure a custom fishing rod — OEM programs from 300 pcs, or a single rod built to "
        "your own measurements. Start from an existing model or specify carbon grade, guide "
        "train, reel seat, handle, line and lures. Incompatible choices are flagged before "
        "you order.")
KEYWORDS = ("custom fishing rod configurator, OEM rod builder, bespoke fishing rod, carbon rod "
            "specification, Fuji guide rod OEM, carp rod specification, build your own fishing "
            "rod wholesale, custom built carp rod")
