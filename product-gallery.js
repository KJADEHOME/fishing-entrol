/*!
 * Product Gallery lightbox — Entrol
 * Attaches to any [data-pg-gallery] container holding .pg-item > img
 * Keyboard: Esc close, ArrowLeft / ArrowRight navigate.
 */
(function () {
  'use strict';

  var lb = null;
  var img = null;
  var cap = null;
  var counter = null;
  var items = [];
  var index = 0;

  function build() {
    if (lb) return lb;
    lb = document.createElement('div');
    lb.className = 'pg-lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Product image viewer');

    img = document.createElement('img');
    img.alt = '';

    var close = document.createElement('button');
    close.className = 'pg-lb-close';
    close.setAttribute('aria-label', 'Close');
    close.innerHTML = '&times;';
    close.addEventListener('click', hide);

    var prev = document.createElement('button');
    prev.className = 'pg-lb-nav pg-lb-prev';
    prev.setAttribute('aria-label', 'Previous image');
    prev.innerHTML = '&#8249;';
    prev.addEventListener('click', function (e) { e.stopPropagation(); step(-1); });

    var next = document.createElement('button');
    next.className = 'pg-lb-nav pg-lb-next';
    next.setAttribute('aria-label', 'Next image');
    next.innerHTML = '&#8250;';
    next.addEventListener('click', function (e) { e.stopPropagation(); step(1); });

    cap = document.createElement('div');
    cap.className = 'pg-lb-caption';

    counter = document.createElement('div');
    counter.className = 'pg-lb-counter';

    lb.appendChild(img);
    lb.appendChild(close);
    lb.appendChild(prev);
    lb.appendChild(next);
    lb.appendChild(cap);
    lb.appendChild(counter);

    lb.addEventListener('click', function (e) {
      if (e.target === lb) hide();
    });

    document.body.appendChild(lb);
    return lb;
  }

  function show(i) {
    if (!items.length) return;
    index = (i + items.length) % items.length;
    var it = items[index];
    build();
    img.src = it.src;
    img.alt = it.alt || '';
    cap.textContent = it.caption || '';
    counter.textContent = (index + 1) + ' / ' + items.length;
    lb.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function hide() {
    if (!lb) return;
    lb.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  function step(d) { show(index + d); }

  function collect() {
    items = [];
    var groups = document.querySelectorAll('[data-pg-gallery]');
    groups.forEach(function (g) {
      var caption = g.getAttribute('data-pg-caption') || '';
      g.querySelectorAll('.pg-item img').forEach(function (im) {
        im.dataset.pgIndex = items.length;
        items.push({ src: im.getAttribute('src'), alt: im.getAttribute('alt') || '', caption: caption });
        im.style.cursor = 'zoom-in';
        im.parentElement.addEventListener('click', function () {
          show(parseInt(im.dataset.pgIndex, 10));
        });
      });
    });
  }

  document.addEventListener('keydown', function (e) {
    if (!lb || !lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') hide();
    else if (e.key === 'ArrowLeft') step(-1);
    else if (e.key === 'ArrowRight') step(1);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', collect);
  } else {
    collect();
  }
})();
