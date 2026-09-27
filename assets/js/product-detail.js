/* product-detail.js — progressive enhancement for the Entrol product detail template.
   All key content is hardcoded in HTML for SEO; this script only adds interactivity.
   - gallery: click thumbnail to switch main image
   - model chips: click to highlight the matching spec row (and switch main image if a per-model image exists)
   - spec row: click to activate the matching chip
   - FAQ: accordion toggle
*/
(function () {
  'use strict';
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    /* ---- gallery: thumbnail -> main image ---- */
    var main = document.getElementById('pdMain');
    var thumbs = document.querySelectorAll('.pd-thumb');
    if (main && thumbs.length) {
      thumbs.forEach(function (t) {
        t.addEventListener('click', function () {
          var src = t.getAttribute('data-src') || t.getAttribute('src');
          if (src) {
            main.src = src;
            main.alt = t.getAttribute('alt') || main.alt;
          }
          thumbs.forEach(function (x) { x.classList.remove('active'); });
          t.classList.add('active');
        });
      });
    }

    /* ---- model chips <-> spec rows ---- */
    var chips = Array.prototype.slice.call(document.querySelectorAll('.pd-chip'));
    var rows = Array.prototype.slice.call(document.querySelectorAll('.pd-spec tbody tr'));
    function activate(rowId) {
      chips.forEach(function (c) {
        c.classList.toggle('active', c.getAttribute('data-row') === rowId);
      });
      rows.forEach(function (r) {
        var on = r.id === rowId;
        r.classList.toggle('active', on);
        if (on && r.scrollIntoView) r.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    }
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var id = c.getAttribute('data-row');
        activate(id);
        var img = c.getAttribute('data-img');
        if (main && img) { main.src = img; main.alt = c.textContent.trim() + ' — main view'; }
      });
    });
    rows.forEach(function (r) {
      r.addEventListener('click', function () {
        if (r.id) activate(r.id);
      });
    });

    /* ---- FAQ accordion ---- */
    var qs = document.querySelectorAll('.pd-faq-q');
    qs.forEach(function (q) {
      q.addEventListener('click', function () {
        var item = q.closest('.pd-faq-item');
        if (item) item.classList.toggle('open');
      });
    });
  });
})();
