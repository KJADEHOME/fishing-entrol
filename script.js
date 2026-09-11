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
      return items;
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
