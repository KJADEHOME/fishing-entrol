/*!
 * Entrol Fishing — site behaviour
 * - mobile nav
 * - WeChat popup (WeChat button never deep-links)
 * - dataLayer events: whatsapp_click / wechat_click / rfq_submit (GTM)
 * - RFQ form client-side spam screen (mirrors supabase/functions/fishing-submit-lead)
 */
(function () {
  'use strict';

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
          st.textContent = 'Your submission could not be processed. Please reach us directly at sales@entrol-fishing.com or WhatsApp +86 152 6313 0999.';
          st.style.background = '#FDECEA';
          st.style.color = '#B03A2E';
          st.classList.add('show');
        }
        return;
      }

      // FormSubmit AJAX mode keeps the visitor on-page and shows a status line
      e.preventDefault();
      var status = document.querySelector('.form-status');
      // drop empty fields so the emailed enquiry stays readable
      var payload = {};
      fd.forEach(function (v, k) { if (String(v).trim() !== '') payload[k] = v; });
      fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (status) {
          status.textContent = 'Thank you — your inquiry has been received. We reply within one business day (GMT+8).';
          status.classList.add('show');
        }
        form.reset();
      }).catch(function () {
        // fall back to normal POST if fetch fails
        form.removeEventListener('submit', arguments.callee);
        form.submit();
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

    var listEl = document.getElementById('cfg-list');
    var countEl = document.getElementById('cfg-count');
    var sumInput = document.getElementById('cfg-summary-input');
    var subjInput = document.getElementById('cfg-subject');

    function esc(s) {
      return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function cfgItems() {
      var out = [];
      cfgForm.querySelectorAll('select[name]').forEach(function (s) {
        if (!s.value) return;
        var lab = cfgForm.querySelector('label[for="' + s.id + '"]');
        var k = lab ? lab.textContent.replace(/\s*\*$/, '').trim() : s.name;
        out.push([k, s.value]);
      });
      return out;
    }

    function renderSummary() {
      var items = cfgItems();
      if (countEl) {
        countEl.textContent = items.length + ' option' + (items.length === 1 ? '' : 's') + ' selected';
      }
      if (listEl) {
        listEl.innerHTML = items.map(function (p) {
          return '<li><span class="k">' + esc(p[0]) + '</span><span class="v">' + esc(p[1]) + '</span></li>';
        }).join('');
      }
      var text = items.map(function (p) { return p[0] + ': ' + p[1]; }).join(' | ');
      if (sumInput) sumInput.value = text;
      if (subjInput) {
        var mkt = cfgForm.querySelector('select[name="target_market"]');
        subjInput.value = 'OEM configurator — ' + (rodSel && rodSel.value ? rodSel.value : 'rod')
          + (mkt && mkt.value ? ' — ' + mkt.value : '');
      }
      renderCombo();
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

    cfgForm.addEventListener('change', renderSummary);
    renderSummary();

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
          st.textContent = 'Your submission could not be processed. Please reach us directly at sales@entrol-fishing.com or WhatsApp +86 152 6313 0999.';
          st.style.background = '#FDECEA';
          st.style.color = '#B03A2E';
          st.classList.add('show');
        }
        return;
      }

      e.preventDefault();
      var payload = {};
      fd.forEach(function (v, k) { if (String(v).trim() !== '') payload[k] = v; });
      fetch(cfgForm.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (st) {
          st.textContent = 'Specification received — ' + items.length + ' options logged. We reply with pricing, MOQ and sample cost within one business day (GMT+8).';
          st.classList.add('show');
        }
      }).catch(function () {
        cfgForm.submit();
      });
    });
  }
})();
