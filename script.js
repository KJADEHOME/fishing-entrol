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
      fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(Object.fromEntries(fd))
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
})();
