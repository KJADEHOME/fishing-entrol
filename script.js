/*!
 * Entrol Fishing — site behaviour
 * - mobile nav
 * - WeChat popup (WeChat button never deep-links)
 * - dataLayer events: whatsapp_click / wechat_click / rfq_submit (GTM)
 * - RFQ form client-side spam screen (mirrors supabase/functions/fishing-submit-lead)
 */
(function () {
  'use strict';

  // Same durable first-party inquiry pipeline used by Entrol Pet and Entrol Socks.
  // A success message is shown only when Supabase confirms that the lead was stored.
  var ENTROL_LEAD_API_URL = 'https://jipgzavuxvnaisgxcvts.supabase.co/functions/v1/entrol-submit-lead';

  function requestId() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') return window.crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 3 | 8)).toString(16);
    });
  }

  function leadPayload(formData, overrides) {
    var payload = {};
    formData.forEach(function (value, key) {
      if (typeof value === 'string' && key.charAt(0) !== '_' && value.trim() !== '') payload[key] = value;
    });
    payload.request_id = requestId();
    payload.submission_type = 'inquiry';
    payload.source_page = window.location.href;
    payload.landing_page = sessionStorage.getItem('entrol_fishing_landing_page') || window.location.href;
    payload.referrer = document.referrer || 'direct';
    var params = new URLSearchParams(window.location.search);
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (name) {
      payload[name] = params.get(name) || sessionStorage.getItem('entrol_fishing_' + name) || '';
    });
    Object.keys(overrides || {}).forEach(function (key) {
      if (overrides[key] !== undefined && overrides[key] !== null && String(overrides[key]).trim() !== '') payload[key] = overrides[key];
    });
    return payload;
  }

  function submitLead(payload) {
    return fetch(ENTROL_LEAD_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Request-Id': payload.request_id },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (result) {
        if (!res.ok || !result.ok || !result.lead_id) throw new Error(result.error || 'submission_failed');
        return result;
      });
    });
  }

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  /* ---------- dataLayer helper ---------- */
  function track(event, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: event }, params || {}));
  }

  /* ---------- WhatsApp float ---------- */
  document.querySelectorAll('a[data-track="whatsapp"]').forEach(function (a) {
    a.addEventListener('click', function () {
      track('whatsapp_click', { page: location.pathname });
    });
  });

  /* ---------- WeChat popup ---------- */
  var wcBtn = document.querySelector('.wc-float');
  var wcModal = document.querySelector('.wc-modal');
  if (wcBtn && wcModal) {
    wcBtn.addEventListener('click', function () {
      wcModal.classList.add('open');
      track('wechat_click', { page: location.pathname });
    });
    var close = wcModal.querySelector('.wc-close');
    if (close) close.addEventListener('click', function () { wcModal.classList.remove('open'); });
    wcModal.addEventListener('click', function (e) {
      if (e.target === wcModal) wcModal.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') wcModal.classList.remove('open');
    });
  }

  /* ---------- RFQ form: client-side spam screen ---------- */
  var DISPOSABLE = ['mailinator.com', 'guerrillamail.com', '10minutemail.com', 'tempmail.com',
    'temp-mail.org', 'yopmail.com', 'trashmail.com', 'sharklasers.com', 'getnada.com',
    'dispostable.com', 'maildrop.cc', 'fakeinbox.com'];

  function isCompactGibberish(v) {
    if (!v || /\s/.test(v) || v.length < 14) return false;
    return /^[A-Za-z]+$/.test(v) && /[a-z]/.test(v) && /[A-Z]/.test(v);
  }

  var risks = [];
  function flag(pts, reason) { risks.push({ pts: pts, reason: reason }); }

  var form = document.getElementById('rfq-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      risks = [];
      var fd = new FormData(form);
      var email = (fd.get('email') || '').trim().toLowerCase();
      var name = (fd.get('name') || '').trim();
      var msg = (fd.get('message') || '').trim();
      var qty = (fd.get('quantity') || '').trim();

      if (fd.get('_honey')) {           // honeypot filled -> bot
        e.preventDefault();
        return;
      }
      var domain = email.split('@')[1] || '';
      if (DISPOSABLE.indexOf(domain) !== -1) flag(3, 'disposable email domain');
      if (msg && /^\d{7,15}$/.test(msg)) flag(2, 'message is only a phone-like number');
      if (isCompactGibberish(name)) flag(2, 'name is compact gibberish');
      if (isCompactGibberish(qty)) flag(2, 'quantity is compact gibberish');

      track('rfq_submit', {
        page: location.pathname,
        risk_score: risks.reduce(function (s, r) { return s + r.pts; }, 0)
      });

      // risk >= 4: block locally (server-side mirror quarantines as well)
      if (risks.reduce(function (s, r) { return s + r.pts; }, 0) >= 4) {
        e.preventDefault();
        var st = document.querySelector('.form-status');
        if (st) {
          st.textContent = 'Your submission could not be processed. Please reach us directly at wangyan@entrol.com or WhatsApp +86 152 6313 0999.';
          st.style.background = '#FDECEA';
          st.style.color = '#B03A2E';
          st.classList.add('show');
        }
        return;
      }

      // Durable first-party capture: database storage must succeed before success is shown.
      e.preventDefault();
      var status = document.querySelector('.form-status');
      var button = form.querySelector('button[type="submit"]');
      var originalText = button ? button.textContent : '';
      if (button) { button.disabled = true; button.textContent = 'Sending...'; }
      var payload = leadPayload(fd, {
        product_interest: fd.get('rod_category') || '',
        target_market: fd.get('target_market') || ''
      });
      submitLead(payload).then(function () {
        if (status) {
          status.textContent = 'Thank you — your inquiry has been received. We reply within one business day (GMT+8).';
          status.classList.add('show');
        }
        track('inquiry_success', { form_path: 'contact', page: location.pathname });
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { form_path: 'contact' });
        form.reset();
      }).catch(function () {
        if (status) {
          status.textContent = 'We could not save your inquiry. Please retry, email wangyan@entrol.com, or contact us on WhatsApp.';
          status.style.background = '#FDECEA';
          status.style.color = '#B03A2E';
          status.classList.add('show');
        }
      }).then(function () {
        if (button) { button.disabled = false; button.textContent = originalText; }
      });
    });
  }

  /* ---------- OEM rod configurator ---------- */
  var cfgForm = document.getElementById('cfg-form');
  if (cfgForm) {
    var ROD_PRESET = {
      spinning: 'Spinning rod',
      casting: 'Casting / baitcasting rod',
      carp: 'Carp rod',
      boat: 'Boat & jigging rod',
      surf: 'Surf / rock rod'
    };

    // preselect rod type when arriving from a category page (?rod=carp)
    var preset = /[?&]rod=([a-z]+)/.exec(location.search);
    var rodSel = cfgForm.querySelector('select[name="rod_type"]');
    if (preset && ROD_PRESET[preset[1]] && rodSel) rodSel.value = ROD_PRESET[preset[1]];

    // ?model=CRS741MF — arriving from a model card, so start from that rod
    var modelParam = /[?&]model=([A-Za-z0-9\-]+)/.exec(location.search);
    var modelSel = cfgForm.querySelector('select[name="base_model"]');
    if (modelParam && modelSel) {
      var wanted = modelParam[1].toUpperCase();
      for (var mi = 0; mi < modelSel.options.length; mi++) {
        if (modelSel.options[mi].value.toUpperCase() === wanted) {
          modelSel.value = modelSel.options[mi].value;
          break;
        }
      }
    }

    /* ---------- two paths: OEM program vs a single custom rod ---------- */
    var CATALOG = [];
    try {
      var rawCat = document.getElementById('catalog-data');
      if (rawCat) CATALOG = JSON.parse(rawCat.textContent || '[]');
    } catch (e) { CATALOG = []; }

    function currentPath() {
      var r = cfgForm.querySelector('input[name="build_path"]:checked');
      if (r) return r.value;
      // Dedicated pages (oem-builder / custom-rod) have no switch — the path
      // arrives in a hidden field instead.
      var fx = cfgForm.getAttribute('data-path');
      if (fx) return fx;
      var h = cfgForm.querySelector('input[name="build_path"][type="hidden"]');
      return h ? h.value : 'oem';
    }

    function applyPath() {
      var p = currentPath();
      cfgForm.querySelectorAll('fieldset[data-path]').forEach(function (fs) {
        var on = fs.getAttribute('data-path') === p;
        fs.hidden = !on;
        fs.querySelectorAll('select, input, textarea').forEach(function (c) { c.disabled = !on; });
      });
      cfgForm.querySelectorAll('.cfg-only-oem, .cfg-only-custom').forEach(function (d) {
        var on = d.classList.contains('cfg-only-' + p);
        d.hidden = !on;
        var c = d.querySelector('select, input, textarea');
        if (c) c.disabled = !on;
      });
      var note = document.getElementById('cfg-qty-note');
      if (note) {
        note.textContent = p === 'custom'
          ? 'One rod is one rod — tell us how many you want and where they are going. There is no '
            + 'minimum, and freight is quoted to your door before anything is built.'
          : 'Two different minimums apply, and it is worth knowing which one you are buying before '
            + 'we quote: rod-only programs run from 300 pieces per model, while anything that puts '
            + 'a reel, line or lures in the carton starts at 500 — and 1,000 if those components '
            + 'also carry your brand. Mixed rod models in one container are always fine.';
      }
    }

    function setSel(name, value) {
      var s = cfgForm.querySelector('select[name="' + name + '"]');
      if (!s || s.disabled || !value || value === '—') return;
      for (var i = 0; i < s.options.length; i++) {
        if (s.options[i].value === value) { s.value = value; return; }
      }
    }

    var MODEL_TYPE = {
      spinning: 'Spinning rod',
      casting: 'Casting / baitcasting rod',
      carp: 'Carp rod',
      boat: 'Boat & jigging rod',
      jigging: 'Boat & jigging rod',
      surf: 'Surf / rock rod'
    };

    function applyModel() {
      var sel = cfgForm.querySelector('select[name="base_model"]');
      if (!sel) return;
      var info = document.getElementById('cfg-model-info');
      if (!info) {
        info = document.createElement('p');
        info.className = 'form-hint';
        info.id = 'cfg-model-info';
        if (sel.parentNode) sel.parentNode.appendChild(info);
      }
      if (!sel.value) { info.textContent = ''; return; }
      // CATALOG is the slim form: {s:sku, c:category, b:subcategory, n:name, p:specs}
      var rod = null;
      for (var i = 0; i < CATALOG.length; i++) {
        if (CATALOG[i].s === sel.value) { rod = CATALOG[i]; break; }
      }
      if (!rod) { info.textContent = ''; return; }
      var s = rod.p || {};
      setSel('rod_type', MODEL_TYPE[rod.b]);
      if (typeof s.length_m === 'number') {
        setSel('length', s.length_m.toFixed(2) + ' m (' + s.length_ft + ')');
      }
      setSel('sections', typeof s.sections === 'number'
        ? s.sections + (s.sections === 1 ? ' piece' : ' pieces') : s.sections);
      setSel('power', s.power);
      setSel('action', s.action);
      setSel('lure_weight', s.cast_weight_g);
      setSel('line_rating', s.line_rating);
      setSel('reel_type', s.reel_type);
      setSel('handle_material', s.handle);
      info.textContent = 'Loaded ' + rod.s + ' — ' + rod.n
        + '. Everything below is now editable.';
    }

    /* ---------- accessory list: model x quantity, one row per model ---------- */
    // A personal build is not a shop — nothing here shows a price. It exists so
    // an angler can say "that reel, and one more of the other one, three spools
    // of that line" without writing an email about it.
    var KIT_CATS = [
      { c: 'reel', label: 'Reels', unit: 'sets', add: 'Add another reel' },
      { c: 'line', label: 'Line', unit: 'spools', add: 'Add another spool' },
      { c: 'lure', label: 'Lures', unit: 'packs', add: 'Add another lure' },
      { c: 'accessory', label: 'Hooks & terminal tackle', unit: 'packs',
        add: 'Add another hook or terminal item' }
    ];

    function kitOptions(cat) {
      return CATALOG.filter(function (p) { return p.c === cat; });
    }

    function kitRow(cat, unit) {
      var row = document.createElement('div');
      row.className = 'kit-row';
      row.setAttribute('data-cat', cat);

      var sel = document.createElement('select');
      sel.className = 'kit-sku';
      sel.setAttribute('aria-label', 'Model');
      var none = document.createElement('option');
      none.value = '';
      none.textContent = '— none —';
      sel.appendChild(none);
      kitOptions(cat).forEach(function (p) {
        var o = document.createElement('option');
        o.value = p.s;
        o.textContent = p.n;
        sel.appendChild(o);
      });

      var qty = document.createElement('input');
      qty.type = 'number';
      qty.className = 'kit-qty';
      qty.min = '1';
      qty.max = '99';
      qty.step = '1';
      qty.value = '1';
      qty.setAttribute('aria-label', 'Quantity');

      var u = document.createElement('span');
      u.className = 'kit-unit';
      u.textContent = unit;

      var del = document.createElement('button');
      del.type = 'button';
      del.className = 'kit-del';
      del.textContent = '×';
      del.title = 'Remove this row';
      del.addEventListener('click', function () {
        if (row.parentNode) row.parentNode.removeChild(row);
        syncKit();
      });

      sel.addEventListener('change', syncKit);
      qty.addEventListener('input', syncKit);

      row.appendChild(sel);
      row.appendChild(qty);
      row.appendChild(u);
      row.appendChild(del);
      return row;
    }

    function buildKit() {
      var host = document.getElementById('kit-lines');
      if (!host || host.childNodes.length) return;
      KIT_CATS.forEach(function (k) {
        var grp = document.createElement('div');
        grp.className = 'kit-group';
        grp.setAttribute('data-cat', k.c);
        var lab = document.createElement('span');
        lab.className = 'kit-lab';
        lab.textContent = k.label;
        var rows = document.createElement('div');
        rows.className = 'kit-rows';
        rows.appendChild(kitRow(k.c, k.unit));
        var add = document.createElement('button');
        add.type = 'button';
        add.className = 'kit-add';
        add.textContent = '+ ' + k.add;
        add.addEventListener('click', function () {
          rows.appendChild(kitRow(k.c, k.unit));
          syncKit();
        });
        grp.appendChild(lab);
        grp.appendChild(rows);
        grp.appendChild(add);
        host.appendChild(grp);
      });
    }

    function syncKit() {
      var input = document.getElementById('kit-lines-input');
      var box = document.getElementById('cfg-kit');
      var list = document.getElementById('cfg-kit-list');
      var total = document.getElementById('cfg-kit-total');
      if (!input) return;

      var parts = [];
      var items = [];
      var pieces = 0;

      // the rod itself is specified above, its count lives in quantity_custom
      var rods = cfgForm.querySelector('select[name="quantity_custom"]');
      if (rods && rods.value && !rods.disabled) {
        var n = parseInt(String(rods.value).replace(/[^\d]/g, ''), 10);
        if (n > 0) {
          items.push(['Rods', rods.value]);
          parts.push('Rods: ' + rods.value);
          pieces += n;
        }
      }

      KIT_CATS.forEach(function (k) {
        var picked = [];
        cfgForm.querySelectorAll('.kit-row[data-cat="' + k.c + '"]').forEach(function (row) {
          var sel = row.querySelector('.kit-sku');
          var q = row.querySelector('.kit-qty');
          if (!sel || sel.disabled || !sel.value) return;
          var n = parseInt(q.value, 10);
          if (!n || n < 1) n = 1;
          picked.push(sel.value + ' ×' + n);
          parts.push(k.label + ': ' + sel.value + ' ×' + n);
          pieces += n;
        });
        if (picked.length) items.push([k.label, picked.join(', ')]);
      });

      input.value = parts.join(' | ');

      if (list) {
        list.innerHTML = items.map(function (it) {
          return '<li><span class="k">' + esc(it[0]) + '</span><span class="v">'
            + esc(it[1]) + '</span></li>';
        }).join('');
      }
      if (total) {
        total.textContent = parts.length
          ? pieces + ' piece' + (pieces === 1 ? '' : 's') + ' — priced on request, '
            + 'quoted with the rod before anything is built.'
          : '';
      }
      if (box) box.hidden = !parts.length;
    }

    cfgForm.addEventListener('change', function (e) {
      if (!e.target) return;
      if (e.target.name === 'build_path') { applyPath(); renderSummary(); syncKit(); }
      if (e.target.name === 'base_model') { applyModel(); renderSummary(); }
      if (e.target.name === 'quantity_custom') { syncKit(); }
    });

    var listEl = document.getElementById('cfg-list');
    var countEl = document.getElementById('cfg-count');
    var sumInput = document.getElementById('cfg-summary-input');
    var subjInput = document.getElementById('cfg-subject');
    var inquiryInput = document.getElementById('cfg-inquiry-id');
    var pagePathInput = document.getElementById('cfg-page-path');
    var refEl = document.getElementById('cfg-ref');

    function makeInquiryId() {
      var d = new Date();
      var y = String(d.getFullYear()).slice(-2);
      var m = String(d.getMonth() + 1).padStart(2, '0');
      var day = String(d.getDate()).padStart(2, '0');
      var rnd = Math.floor(Math.random() * 100000).toString().padStart(5, '0');
      return 'EF-' + y + m + day + '-' + rnd;
    }

    if (inquiryInput && !inquiryInput.value) inquiryInput.value = makeInquiryId();
    if (pagePathInput) pagePathInput.value = location.pathname || '';
    if (refEl && inquiryInput) refEl.textContent = 'Draft reference ' + inquiryInput.value;

    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // Text inputs worth echoing in the summary panel. Name, email and the free
    // text box are submitted but not repeated back to the buyer.
    var TEXT_FIELDS = ['engraving', 'ship_to', 'company'];

    function cfgItems() {
      var out = [];
      cfgForm.querySelectorAll('select[name]').forEach(function (s) {
        if (!s.value || s.disabled) return;
        var lab = cfgForm.querySelector('label[for="' + s.id + '"]');
        var k = lab ? lab.textContent.replace(/\s*\*$/, '').trim() : s.name;
        out.push([k, s.value]);
      });
      TEXT_FIELDS.forEach(function (n) {
        var i = cfgForm.querySelector('input[name="' + n + '"]');
        if (!i || !i.value || i.disabled) return;
        var lab = cfgForm.querySelector('label[for="' + i.id + '"]');
        out.push([lab ? lab.textContent.replace(/\s*\*$/, '').trim() : n, i.value]);
      });
      return out;
    }

    function renderSummary() {
      var items = cfgItems();
      var isCustom = currentPath() === 'custom';
      items.unshift(['Ordering as', isCustom ? 'One custom rod' : 'OEM / private-label program']);
      if (countEl) {
        countEl.textContent = items.length + ' option' + (items.length === 1 ? '' : 's') + ' selected';
      }
      if (listEl) {
        listEl.innerHTML = items.map(function (p) {
          return '<li><span class="k">' + esc(p[0]) + '</span><span class="v">' + esc(p[1]) + '</span></li>';
        }).join('');
      }
      var text = items.map(function (p) { return p[0] + ': ' + p[1]; }).join(' | ');
      if (sumInput) sumInput.value = (inquiryInput ? 'Inquiry: ' + inquiryInput.value + ' | ' : '') + text;
      if (subjInput) {
        var mkt = cfgForm.querySelector('select[name="target_market"]');
        subjInput.value = (inquiryInput ? inquiryInput.value + ' — ' : '')
          + (isCustom ? 'Custom rod build' : 'OEM configurator') + ' — '
          + (rodSel && rodSel.value ? rodSel.value : 'rod')
          + (mkt && mkt.value ? ' — ' + mkt.value : '');
      }
      renderWarnings();
      renderCombo();
      renderMoq();
      return items;
    }

    /* ---------- set-up advisor ---------- */
    var LINE_BY_WEIGHT = [
      { up: 5, pe: 'PE 0.4', ld: 'Fluorocarbon 6 lb', reel: '1000–2000',
        why: 'Finesse class — thin braid lets small lures swim naturally and casts further.' },
      { up: 21, pe: 'PE 0.8', ld: 'Fluorocarbon 10 lb', reel: '2500',
        why: 'The all-round freshwater and estuary class.' },
      { up: 30, pe: 'PE 1.2', ld: 'Fluorocarbon 16 lb', reel: '3000',
        why: 'Enough backbone for snapper, cod and bigger estuary fish.' },
      { up: 50, pe: 'PE 2.0', ld: 'Fluorocarbon 20 lb', reel: '4000',
        why: 'Shore jigging and light offshore casting.' },
      { up: 120, pe: 'PE 3.0', ld: 'Fluorocarbon 30 lb', reel: '5000',
        why: 'Heavy shore casting and inshore species.' },
      { up: 99999, pe: 'PE 4.0', ld: 'Fluorocarbon 40 lb', reel: '6000+',
        why: 'Big metal lures and offshore fish.' }
    ];

    var TAPER_BY_LURE = [
      { key: 'curly tail', taper: 'Fast', guide: 'Single-foot guides',
        why: 'A sensitive tip reads the bite; single-foot guides keep the blank light and responsive.' },
      { key: 'paddle tail', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Needs a responsive tip to keep the tail kicking at slow retrieve speeds.' },
      { key: 'worm', taper: 'Extra-Fast', guide: 'Single-foot guides',
        why: 'Worms and stick baits are fished on slack line — maximum sensitivity wins.' },
      { key: 'creature', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Punching and flipping need tip sensitivity plus a strong butt section.' },
      { key: 'minnow', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Twitching a minnow needs a tip that recovers quickly between jerks.' },
      { key: 'crankbait', taper: 'Moderate', guide: 'Single-foot guides',
        why: 'A softer parabolic blank keeps treble hooks pinned when a fish lunges.' },
      { key: 'vibration', taper: 'Moderate-Fast', guide: 'Single-foot guides',
        why: 'Lipless lures pull hard all day — a slightly softer tip absorbs the vibration.' },
      { key: 'pencil', taper: 'Moderate-Fast', guide: 'Single-foot guides',
        why: 'Topwater walking needs a tip soft enough to throw slack line.' },
      { key: 'popper', taper: 'Moderate-Fast', guide: 'Single-foot guides',
        why: 'Soft tip to work the pop, strong butt to drive the hooks home.' },
      { key: 'slow pitch', taper: 'Moderate', guide: 'Double-foot guides',
        why: 'Slow-pitch jigging loads the whole blank — a parabolic taper does the work.' },
      { key: 'shore jig', taper: 'Fast', guide: 'Double-foot guides',
        why: 'Long casts with heavy metal need a fast, powerful blank and rigid guides.' },
      { key: 'spoon', taper: 'Moderate', guide: 'Single-foot guides',
        why: 'Spoons and spinners are constant-retrieve lures — a through-action blank is kinder.' },
      { key: 'glow', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Night fishing with glow lures: sensitivity matters more than distance.' },
      { key: 'jig head', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Bottom contact is the bite — you need to feel gravel from sand.' },
      { key: 'texas', taper: 'Fast', guide: 'Single-foot guides',
        why: 'Weedless rigs need a strong butt to drive the hook through cover.' },
      { key: 'cut bait', taper: 'Moderate', guide: 'Double-foot guides',
        why: 'Bait fishing needs a forgiving tip so fish are not spooked off the hook.' },
      { key: 'boilie', taper: 'Moderate', guide: 'Double-foot guides',
        why: 'Carp rods are progressive: soft tip for casting, deep power for playing.' },
      { key: 'fly', taper: 'Moderate', guide: 'Single-foot guides',
        why: 'Fly blanks load on the cast — the taper carries the line.' }
    ];

    var SPECIES_ALERT = {
      'Pike': 'Pike and zander cut braid instantly — specify a wire or tooth-proof leader.',
      'Kingfish': 'Kingfish and tuna run hard with sharp gill plates — go one leader class heavier than the rod suggests.',
      'Carp': 'Carp fight deep and steadily; most European buyers prefer a nylon main line because its stretch protects the blank.',
      'Catfish': 'Catfish need strength over finesse — do not go below PE 3.0 with a 40 lb leader.',
      'Squid': 'Egi rods are short, ultra-sensitive and very soft-tipped — a standard fast taper feels dead.',
      'Cod': 'Cod and ling live on rough ground — abrasion resistance beats thin diameter.',
      'Snapper': 'Snapper head straight for structure the moment they are hooked — the leader takes the abuse, not the braid.'
    };

    function pick(selName, wanted) {
      var sel = cfgForm.querySelector('select[name="' + selName + '"]');
      if (!sel || !wanted) return null;
      var opts = Array.prototype.slice.call(sel.options), i;
      for (i = 0; i < opts.length; i++) if (opts[i].value === wanted) return { sel: sel, value: wanted };
      for (i = 0; i < opts.length; i++) if (opts[i].value.indexOf(wanted) === 0) return { sel: sel, value: opts[i].value };
      return null;
    }

    function val(name) {
      var s = cfgForm.querySelector('select[name="' + name + '"]');
      return s && s.value ? s.value : '';
    }

    function renderCombo() {
      var box = document.getElementById('cfg-combo-list');
      var lead = document.getElementById('cfg-combo-lead');
      if (!box) return;
      var lure = val('lure_type'), sp = val('target_species'), lw = val('lure_weight');
      var rows = [], i;

      if (lw) {
        var w = Math.max.apply(null, (lw.match(/\d+/g) || ['0']).map(Number));
        var rule = LINE_BY_WEIGHT[LINE_BY_WEIGHT.length - 1];
        for (i = 0; i < LINE_BY_WEIGHT.length; i++) if (w <= LINE_BY_WEIGHT[i].up) { rule = LINE_BY_WEIGHT[i]; break; }
        rows.push({ part: 'Main line', value: rule.pe, why: rule.why, apply: pick('main_line', rule.pe) });
        rows.push({ part: 'Leader', value: rule.ld,
          why: 'Braid alone will not survive rock or teeth — the leader does that job.',
          apply: pick('leader', rule.ld) });
        rows.push({ part: 'Reel size', value: rule.reel,
          why: 'Balances the rod and holds enough line for the cast weights you chose.', apply: null });
      }

      if (lure) {
        var low = lure.toLowerCase(), t = null;
        for (i = 0; i < TAPER_BY_LURE.length; i++) if (low.indexOf(TAPER_BY_LURE[i].key) !== -1) { t = TAPER_BY_LURE[i]; break; }
        if (t) {
          rows.push({ part: 'Taper', value: t.taper, why: t.why, apply: pick('action', t.taper) });
          rows.push({ part: 'Guides', value: t.guide,
            why: t.guide.indexOf('Double') === 0
              ? 'Double-foot guides are stiffer and handle heavy loads and big fish.'
              : 'Single-foot guides keep the tip light and sensitive.',
            apply: pick('guide_type', t.guide) });
        }
      }

      if (sp) {
        for (var key in SPECIES_ALERT) {
          if (sp.indexOf(key) !== -1) {
            rows.push({ part: 'Watch out', value: key, why: SPECIES_ALERT[key], apply: null });
            break;
          }
        }
      }

      if (!val('kit_option') && (lure || sp)) {
        rows.push({ part: 'Worth adding', value: 'Rod + starter lure set',
          why: 'Ships the rod with lures matched to your target species — one carton, one purchase order.',
          apply: pick('kit_option', 'Rod + starter lure set') });
      }

      if (lead) {
        lead.textContent = rows.length
          ? 'Based on what you have chosen so far — tap Apply to accept any suggestion:'
          : 'Pick a target species or lure type and we will suggest the matching taper, line and reel size here.';
      }

      box.innerHTML = rows.map(function (r, idx) {
        return '<li class="cfg-advice"><span class="part">' + esc(r.part) + '</span>'
          + '<span class="val">' + esc(r.value) + '</span>'
          + '<span class="why">' + esc(r.why) + '</span>'
          + (r.apply ? '<button type="button" class="cfg-apply" data-i="' + idx + '">Apply</button>' : '')
          + '</li>';
      }).join('');

      box.querySelectorAll('.cfg-apply').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var r = rows[parseInt(btn.getAttribute('data-i'), 10)];
          if (r && r.apply) { r.apply.sel.value = r.apply.value; renderSummary(); }
        });
      });
    }

    /* ---------- compatibility warnings ---------- */
    var POWER_IX = { 'Ultra-Light': 1, 'Light': 2, 'Medium-Light': 3, 'Medium': 4,
                     'Medium-Heavy': 5, 'Heavy': 6, 'Extra-Heavy': 7 };

    function allNum(s) { return (String(s).match(/[\d.]+/g) || []).map(Number); }
    function maxNum(s) { var a = allNum(s); return a.length ? Math.max.apply(null, a) : 0; }
    function firstNum(s) { var a = allNum(s); return a.length ? a[0] : 0; }

    function renderWarnings() {
      var box = document.getElementById('cfg-warnbox');
      if (!box) return;

      var rod = val('rod_type'), len = val('length'), pw = val('power'), lw = val('lure_weight');
      var line = val('main_line'), ld = val('leader'), reel = val('reel_type');
      var guide = val('guide_type'), handle = val('handle_style'), sec = val('sections');
      var sp = val('target_species'), hook = val('hook_keeper');

      var lenM = firstNum(len);
      var wMax = maxNum(lw);
      var pe = /PE/i.test(line) ? firstNum(line) : 0;
      var nylonLb = /nylon/i.test(line) ? maxNum(line) : 0;
      var pIx = POWER_IX[pw] || 0;
      var w = [];
      var picks = 0;

      cfgForm.querySelectorAll('select[name]').forEach(function (s) { if (s.value) picks++; });

      function add(level, title, body, fixSel, fixVal) {
        w.push({ level: level, title: title, body: body,
                 fix: (fixSel && fixVal) ? pick(fixSel, fixVal) : null });
      }

      /* --- reel vs rod --- */
      if (/Spinning/.test(rod) && /Baitcasting/.test(reel)) {
        add('risk', 'A spinning blank will not run a baitcasting reel',
          'Spinning rods use large, high-standing guides so line can peel off a fixed spool in coils. ' +
          'A baitcaster feeds line in a straight, fast stream through guides that are too small and sit ' +
          'too low — expect wind knots, casts that die halfway, and the rod loading in the wrong place.',
          'reel_type', 'Spinning reel');
      }
      if (/Casting/.test(rod) && /Spinning/.test(reel)) {
        add('risk', 'A casting blank will not run a spinning reel',
          'Casting rods are built with small, low-profile guides because the line leaves a revolving ' +
          'spool under control. Fit a spinning reel and the coils slap against every ring — line ' +
          'twists, distance collapses and the tip rings wear grooves.',
          'reel_type', 'Baitcasting reel');
      }
      if (/Carp/.test(rod) && /Baitcasting|Conventional/.test(reel)) {
        add('caution', 'Carp rods are built around big-spool spinning reels',
          'European carp anglers use baitrunner-style spinning reels with a free-spool clutch; the butt ' +
          'ring and guide spacing are set for that. A baitcaster leaves no room for the clutch and the ' +
          'rod will not be accepted in that market.',
          'reel_type', 'Spinning reel');
      }
      if (/Surf/.test(rod) && /Baitcasting/.test(reel)) {
        add('caution', 'Surf rods are spinning-reel rods in practice',
          'Long surf blanks need a large stripper guide to gather line coming off a fixed spool at speed. ' +
          'A baitcaster cannot deliver that and will backlash into the wind.',
          'reel_type', 'Spinning reel');
      }

      /* --- reel vs handle --- */
      if (/Pistol/.test(handle) && /Spinning/.test(reel)) {
        add('caution', 'Trigger grip with a spinning reel fights your hand',
          'The trigger exists so your finger has something to brace against while palming a baitcaster. ' +
          'With a spinning reel it digs into the palm on long retrieves — buyers notice it immediately.',
          'handle_style', 'Split grip');
      }
      if (/Straight/.test(handle) && /Baitcasting/.test(reel)) {
        add('caution', 'A straight spinning grip gives a baitcaster no control',
          'Without a trigger you cannot palm the reel, so you cannot thumb the spool on the cast. ' +
          'Backlash on every cast is the result.',
          'handle_style', 'Pistol / trigger (casting)');
      }

      /* --- length vs cast weight --- */
      if (lenM && lenM <= 2.10 && wMax >= 50) {
        add('risk', 'This blank is too short to cast ' + lw,
          'Under about 2.1 m there is not enough lever length to load ' + lw + ' safely. The rod ' +
          'overloads the tip section and breaks — and it breaks on the forward cast, not on a fish.',
          'lure_weight', '20–50 g');
      }
      if (lenM && lenM >= 3.30 && wMax && wMax <= 5) {
        add('caution', 'A rod this long will not load a ' + lw + ' lure',
          'Below roughly 5 g the blank never bends far enough to store energy. The lure travels a few ' +
          'metres and all that extra length kills any feel of the bite.',
          'lure_weight', '10–30 g');
      }
      if (lenM && lenM >= 3.90 && /1 piece/.test(sec)) {
        add('risk', 'A one-piece rod this long cannot be shipped economically',
          'At ' + lenM + ' m the parcel is over every courier length limit and will not fit a standard ' +
          'export carton — air freight refuses it and sea freight needs an oversized crate. Split it into ' +
          'sections or the freight number will be the biggest surprise in the quote.',
          'sections', '3 pieces');
      }

      /* --- line vs cast weight --- */
      if (wMax >= 50 && ((pe && pe <= 1.0) || (nylonLb && nylonLb <= 14))) {
        add('risk', 'Line far too light for a ' + lw + ' cast',
          'On the cast the lure accelerates hard and the shock load lands on a few centimetres of line ' +
          'at the tip. At this rating it parts and throws ' + Math.round(wMax / 28.35) + ' oz of metal ' +
          'back past the angler — this is the classic crack-off, and it is how people get hurt.',
          'main_line', wMax >= 100 ? 'PE 3.0' : 'PE 2.0');
      }
      if (wMax && wMax <= 5 && (pe >= 3 || nylonLb >= 17)) {
        add('caution', 'Line too heavy to cast a ' + lw + ' lure',
          'Thick line has too much drag and memory for a light lure — casts collapse short, and the wind ' +
          'bowls the line into a belly you cannot feel a bite through.',
          'main_line', 'PE 0.6');
      }
      if (pe && wMax >= 30 && /^None$/.test(ld)) {
        add('caution', 'Braid with no leader will not survive contact',
          'Braid has almost no abrasion resistance. One touch of rock, shell or a toothy fish and the ' +
          'whole rig is gone. Heavy casting needs a shock leader as well.',
          'leader', wMax >= 100 ? 'Fluorocarbon 40 lb' : 'Fluorocarbon 30 lb');
      }

      /* --- power vs cast weight --- */
      if (wMax >= 50 && pIx && pIx <= 3) {
        add('risk', 'Power is too light for the cast weight',
          'A ' + pw + ' blank is rated for small lures. Casting ' + lw + ' overloads it — the rod snaps ' +
          'on the cast, not on the fish, and that reads as a quality defect to your customer.',
          'power', 'Heavy');
      }
      if (wMax && wMax <= 5 && pIx >= 6) {
        add('caution', 'Power is too heavy for the cast weight',
          'A ' + pw + ' blank will not bend under a ' + lw + ' lure, so it stores no energy. The cast dies ' +
          'and the tip is too stiff to register a bite at all.',
          'power', 'Light');
      }

      /* --- guides vs line/reel --- */
      if (/KT micro/.test(guide) && wMax >= 50) {
        add('caution', 'Micro guides will not pass a heavy leader knot',
          'KT rings are built for thin braid and finesse work. A 30–40 lb shock-leader knot hangs up in ' +
          'the ring on the cast — and on a heavy cast that is precisely when a crack-off happens.',
          'guide_type', 'Double-foot guides');
      }
      if (/Single-foot/.test(guide) && /Surf|Boat/.test(rod) && wMax >= 50) {
        add('caution', 'Single-foot guides are under-built for this load',
          'Heavy surf and boat work puts a bending load on every guide foot. Double-foot guides spread it; ' +
          'single-foot ones eventually crack at the wrap.',
          'guide_type', 'Double-foot guides');
      }
      if (/Lowrider/.test(guide) && /Baitcasting/.test(reel)) {
        add('caution', 'Lowrider trains are a spinning-reel design',
          'The Lowrider concept controls the coils coming off a fixed spool. On a baitcaster it adds ' +
          'friction and noise without any benefit.',
          'guide_type', 'KT micro guides');
      }

      /* --- species vs terminal tackle --- */
      if (/Pike/.test(sp) && !/Wire|tooth-proof/.test(ld)) {
        add('risk', 'Pike will cut straight through that leader',
          'Pike and zander teeth part fluorocarbon on the strike. Without a wire or tooth-proof leader ' +
          'your customer loses every fish — and blames the rod, not the leader.',
          'leader', 'Wire / tooth-proof leader');
      }
      if (/Kingfish/.test(sp) && pe && pe < 2) {
        add('caution', 'Kingfish will find the weak point in a light line',
          'Kingfish and tuna run hard with sharp gill plates. Step the main line and leader up one class ' +
          'over what the cast weight alone suggests.',
          'main_line', 'PE 3.0');
      }

      if (!w.length) {
        box.innerHTML = picks >= 4
          ? '<div class="cfg-warn-none">No conflicts in what you have picked so far — this combination can be built as specified.</div>'
          : '';
        return;
      }

      box.innerHTML = w.map(function (r, i) {
        return '<div class="cfg-warn ' + r.level + '">'
          + '<span class="w-title">' + (r.level === 'risk' ? 'Will not work — ' : 'Worth reconsidering — ')
          + esc(r.title) + '</span>'
          + '<span class="w-body">' + esc(r.body) + '</span>'
          + (r.fix ? '<button type="button" class="w-fix" data-w="' + i + '">Change to: ' + esc(r.fix.value) + '</button>' : '')
          + '</div>';
      }).join('');

      box.querySelectorAll('.w-fix').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var r = w[parseInt(btn.getAttribute('data-w'), 10)];
          if (r && r.fix) { r.fix.sel.value = r.fix.value; renderSummary(); }
        });
      });
    }

    /* ---------- MOQ notice (rod vs kit vs branded kit) ---------- */
    function renderMoq() {
      var el = document.getElementById('cfg-moq');
      if (!el) return;
      if (currentPath() === 'custom') {
        el.innerHTML = '<strong>One rod, priced before we start</strong>'
          + '<table class="inline">'
          + '<tr><td>Minimum</td><td>1 rod</td></tr>'
          + '<tr><td>Build time</td><td>20–25 days, then shipping</td></tr>'
          + '<tr><td>Freight</td><td>Quoted to your country before we start</td></tr>'
          + '<tr><td>Payment</td><td>50% to book the build, balance before shipping</td></tr>'
          + '</table>'
          + '<p style="margin:8px 0 0">A single rod costs more per piece than a production order '
          + 'because there is no run to spread the set-up across, and the blank, guides and trim '
          + 'are chosen for you alone. Because it is built to your measurements and engraving, '
          + '<strong>it cannot be returned or exchanged</strong> unless it arrives damaged — we '
          + 'photograph every build before it is packed.</p>';
        return;
      }
      var kit = val('kit_option'), kb = val('kit_brand');
      var isKit = kit && !/Rod only/.test(kit);
      var isFull = /Full retail kit/.test(kit);
      var ownBrand = /Our brand on everything/.test(kb);
      var rows = [
        ['Rod only — your spec, your brand, our line', '300 pcs / model', !isKit],
        ['Rod + reel, + line or + lure set', '500 pcs', isKit && !isFull],
        ['Full kit, or components also printed with your brand', '1,000 pcs', isFull || ownBrand]
      ];
      var html = '<strong>Minimum order depends on what goes in the carton</strong>'
        + '<table class="inline">'
        + rows.map(function (r) {
            return '<tr><td' + (r[2] ? ' style="font-weight:800"' : '') + '>' + esc(r[0])
              + (r[2] ? ' &larr; your selection' : '') + '</td><td>' + esc(r[1]) + '</td></tr>';
          }).join('')
        + '</table>'
        + '<p style="margin:8px 0 0">Why they differ: the rod is built on our own line, so 300 pieces '
        + 'covers one mandrel set-up and one print run. Reels, line and lures come from separate '
        + 'component makers — each has its own minimum, and 500 is where they will open a slot. '
        + 'Putting your brand on those components means their own tooling and print run, which starts '
        + 'at 1,000. We quote each part separately so you can see exactly where the money goes.</p>';
      el.innerHTML = html;
    }

    buildKit();
    applyPath();
    if (modelSel && modelSel.value) applyModel();
    cfgForm.addEventListener('change', renderSummary);
    renderSummary();
    syncKit();

    cfgForm.addEventListener('submit', function (e) {
      risks = [];
      var fd = new FormData(cfgForm);
      var email = (fd.get('email') || '').trim().toLowerCase();
      var name = (fd.get('name') || '').trim();

      if (fd.get('_honey')) { e.preventDefault(); return; }
      var domain = email.split('@')[1] || '';
      if (DISPOSABLE.indexOf(domain) !== -1) flag(3, 'disposable email domain');
      if (isCompactGibberish(name)) flag(2, 'name is compact gibberish');

      var items = renderSummary();
      var score = risks.reduce(function (s, r) { return s + r.pts; }, 0);
      track('configurator_submit', {
        options_selected: items.length,
        spec_summary: items.map(function (p) { return p[0] + ': ' + p[1]; }).join(' | '),
        risk_score: score
      });

      var st = cfgForm.querySelector('.form-status');
      if (score >= 4) {
        e.preventDefault();
        if (st) {
          st.textContent = 'Your submission could not be processed. Please reach us directly at wangyan@entrol.com or WhatsApp +86 152 6313 0999.';
          st.style.background = '#FDECEA';
          st.style.color = '#B03A2E';
          st.classList.add('show');
        }
        return;
      }

      e.preventDefault();
      var button = cfgForm.querySelector('button[type="submit"]');
      var originalText = button ? button.textContent : '';
      if (button) { button.disabled = true; button.textContent = 'Sending...'; }
      var path = currentPath();
      var specSummary = String(fd.get('spec_summary') || '');
      var notes = String(fd.get('notes') || '');
      var payload = leadPayload(fd, {
        product_interest: fd.get('base_model') || fd.get('rod_type') || (path === 'custom' ? 'One custom rod' : 'OEM fishing rod program'),
        quantity: path === 'custom' ? fd.get('quantity_custom') : fd.get('quantity'),
        target_market: fd.get('target_market') || fd.get('ship_to') || '',
        message: [notes, specSummary].filter(Boolean).join('\n\n')
      });
      submitLead(payload).then(function () {
        if (st) {
          st.textContent = path === 'custom'
            ? 'Build request received — ' + items.length + ' options logged. We reply with a build sheet, a price and a freight quote within one business day (GMT+8).'
            : 'Specification received — ' + items.length + ' options logged. We reply with pricing, MOQ and sample cost within one business day (GMT+8).';
          st.classList.add('show');
        }
        track('inquiry_success', { form_path: path, page: location.pathname, options_selected: items.length });
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { form_path: path });
      }).catch(function () {
        if (st) {
          st.textContent = 'We could not save your inquiry. Please retry, email wangyan@entrol.com, or contact us on WhatsApp.';
          st.style.background = '#FDECEA';
          st.style.color = '#B03A2E';
          st.classList.add('show');
        }
      }).then(function () {
        if (button) { button.disabled = false; button.textContent = originalText; }
      });
    });
  }
})();
