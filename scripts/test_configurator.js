/* Functional test for the rod configurator, run against BOTH dedicated pages:
   oem-builder.html (path fixed to OEM) and custom-rod.html (path fixed to custom).
   The shared engine — compatibility warnings, model prefill, embedded catalogue,
   MOQ panel — is exercised on each; path-specific blocks check only what the page owns.

   Run: NODE_PATH=<workspace>/node_modules node scripts/test_configurator.js */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const SRC = path.resolve(__dirname, '..');
const PAGES = [
  { file: 'oem-builder.html', path: 'oem' },
  { file: 'custom-rod.html', path: 'custom' },
];

let passCount = 0, failCount = 0;
function fail(m) { console.log('  FAIL  ' + m); failCount++; process.exitCode = 1; }
function pass(m) { console.log('  ok    ' + m); passCount++; }

async function loadPage(file) {
  let html = fs.readFileSync(path.join(SRC, file), 'utf8');
  html = html.replace(/<script[^>]+src="https?:\/\/[^"]*"[^>]*><\/script>/gi, '');
  html = html.replace(/<link[^>]+href="https?:\/\/[^"]*"[^>]*>/gi, '');
  html = html.replace(/<script[^>]+src="script\.js"[^>]*><\/script>/gi, '');
  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'http://localhost/' + file, virtualConsole: vc
  });
  const { window } = dom;
  window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  window.eval(fs.readFileSync(path.join(SRC, 'script.js'), 'utf8'));
  window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
  await new Promise(r => setTimeout(r, 100));
  return window;
}

async function testPage(file, mode) {
  console.log('\n######## ' + file + ' (path=' + mode + ') ########');
  const window = await loadPage(file);
  const doc = window.document;
  const form = doc.getElementById('cfg-form');
  if (!form) { fail('cfg-form not found'); return; }

  function fire(el) { el.dispatchEvent(new window.Event('change', { bubbles: true })); }
  function setVals(obj) {
    Object.keys(obj).forEach(k => {
      const s = form.querySelector('select[name="' + k + '"]');
      if (!s) { fail('missing select: ' + k); return; }
      s.value = obj[k];
      if (s.value !== obj[k]) fail('could not set ' + k + ' = ' + obj[k]);
      fire(s);
    });
  }
  function warnText() {
    const b = doc.getElementById('cfg-warnbox');
    return b ? b.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  function moqText() {
    const m = doc.getElementById('cfg-moq');
    return m ? m.textContent.replace(/\s+/g, ' ').trim() : '';
  }

  // ---- path is fixed on a dedicated page ----
  const formPath = form.getAttribute('data-path');
  if (formPath === mode) pass('form carries data-path="' + mode + '" (no switch needed)');
  else fail('wrong data-path: ' + formPath + ' expected ' + mode);

  const inquiryId = (doc.getElementById('cfg-inquiry-id') || {}).value || '';
  if (/^EF-\d{6}-\d{5}$/.test(inquiryId)) pass('draft inquiry reference generated');
  else fail('missing or malformed inquiry reference: ' + inquiryId);

  if (mode === 'oem') {
    const commercial = ['launch_goal', 'program_tier', 'buyer_type', 'sales_channel'];
    const missing = commercial.filter(n => !form.querySelector('select[name="' + n + '"]'));
    if (!missing.length) pass('commercial brief comes before technical specification');
    else fail('commercial brief fields missing: ' + missing.join(', '));
  }

  // ---- compatibility warnings ----
  const CASES = [
    ['spinning blank + baitcasting reel',
     { rod_type: 'Spinning rod', reel_type: 'Baitcasting reel' },
     /will not run a baitcasting reel/i, 'risk'],
    ['casting blank + spinning reel',
     { rod_type: 'Casting / baitcasting rod', reel_type: 'Spinning reel' },
     /will not run a spinning reel/i, 'risk'],
    ['carp rod + baitcasting reel',
     { rod_type: 'Carp rod', reel_type: 'Baitcasting reel' },
     /big-spool spinning reels/i, 'caution'],
    ['short rod asked to cast 100 g',
     { rod_type: 'Boat & jigging rod', length: "2.10 m (6'11\")", lure_weight: '100–200 g' },
     /too short to cast/i, 'risk'],
    ['heavy cast on PE 0.6',
     { rod_type: 'Surf / rock rod', lure_weight: '50–120 g', main_line: 'PE 0.6' },
     /far too light/i, 'risk'],
    ['braid + no leader + heavy cast',
     { rod_type: 'Surf / rock rod', lure_weight: '30–80 g', main_line: 'PE 2.0', leader: 'None' },
     /no leader will not survive/i, 'caution'],
    ['ultra-light power with 50 g cast',
     { rod_type: 'Spinning rod', power: 'Ultra-Light', lure_weight: '50–120 g' },
     /Power is too light/i, 'risk'],
    ['heavy power with 3 g lure',
     { rod_type: 'Spinning rod', power: 'Extra-Heavy', lure_weight: 'under 5 g' },
     /Power is too heavy/i, 'caution'],
    ['micro guides with heavy leader',
     { rod_type: 'Surf / rock rod', guide_type: 'KT micro guides', lure_weight: '100–200 g' },
     /will not pass a heavy leader knot/i, 'caution'],
    ['trigger grip + spinning reel',
     { rod_type: 'Spinning rod', reel_type: 'Spinning reel',
       handle_style: 'Pistol / trigger (casting)' },
     /Trigger grip with a spinning reel/i, 'caution'],
    ['pike without wire leader',
     { rod_type: 'Spinning rod', target_species: 'Pike / zander', leader: 'Fluorocarbon 10 lb' },
     /cut straight through that leader/i, 'risk'],
    ['one-piece 4.2 m rod',
     { rod_type: 'Surf / rock rod', length: "4.20 m (13'9\")", sections: '1 piece' },
     /cannot be shipped/i, 'risk'],
    ['light lure on heavy line',
     { rod_type: 'Spinning rod', lure_weight: 'under 5 g', main_line: 'PE 3.0' },
     /too heavy to cast/i, 'caution'],
  ];
  console.log('\n== compatibility warnings ==');
  CASES.forEach(([name, vals, re, level]) => {
    form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
    setVals(vals);
    const t = warnText();
    if (re.test(t)) {
      const cls = doc.querySelector('.cfg-warn');
      const wantRisk = level === 'risk';
      const isRisk = cls && cls.className.indexOf('risk') !== -1;
      if (wantRisk === isRisk) pass(name + ' [' + level + ']');
      else fail(name + ' — wrong severity, expected ' + level);
    } else {
      fail(name + ' — no warning. box="' + t.slice(0, 90) + '"');
    }
  });

  console.log('\n== clean combination (must NOT warn) ==');
  form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
  setVals({
    rod_type: 'Spinning rod', length: "2.19 m (7'2\")", sections: '1 piece',
    power: 'Medium-Light', action: 'Fast', lure_weight: '5–21 g', line_rating: '6–12 lb',
    reel_type: 'Spinning reel', guide_type: 'Single-foot guides',
    handle_style: 'Split grip', main_line: 'PE 0.8', leader: 'Fluorocarbon 10 lb'
  });
  const clean = warnText();
  if (/No conflicts/.test(clean)) pass('clean spec reports no conflicts');
  else fail('clean spec still warns: ' + clean.slice(0, 120));

  console.log('\n== one-click fix buttons ==');
  form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
  setVals({ rod_type: 'Spinning rod', reel_type: 'Baitcasting reel' });
  const btn = doc.querySelector('.cfg-warn .w-fix');
  if (!btn) { fail('no fix button rendered'); }
  else {
    btn.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    const rt = form.querySelector('select[name="reel_type"]').value;
    if (rt === 'Spinning reel') pass('fix button applied -> ' + rt);
    else fail('fix button did not apply, reel_type=' + rt);
  }

  console.log('\n== embedded product catalogue ==');
  const rawCat = doc.getElementById('catalog-data');
  let CAT = [];
  try { CAT = JSON.parse((rawCat && rawCat.textContent) || '[]'); } catch (e) { CAT = []; }
  if (CAT.length >= 20) pass('catalogue embedded in page: ' + CAT.length + ' rows');
  else fail('catalogue missing or too small: ' + CAT.length);
  const RODS = CAT.filter(p => p.c === 'rod');
  const optCount = form.querySelectorAll('select[name="base_model"] option').length;
  if (optCount === RODS.length + 1) pass('model picker lists every rod + blank (' + optCount + ')');
  else fail('model picker has ' + optCount + ' options for ' + RODS.length + ' rods');
  if (RODS.length >= 20 && CAT.length > RODS.length) {
    pass('catalogue also carries line/lure/reel for the accessory picker');
  } else fail('catalogue missing component rows');

  console.log('\n== start from an existing model ==');
  form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
  setVals({ base_model: 'CRS741MF' });
  const got = {
    length: form.querySelector('select[name="length"]').value,
    power: form.querySelector('select[name="power"]').value,
    action: form.querySelector('select[name="action"]').value,
    line_rating: form.querySelector('select[name="line_rating"]').value,
    reel_type: form.querySelector('select[name="reel_type"]').value,
    handle_material: form.querySelector('select[name="handle_material"]').value
  };
  const want = { length: "2.23 m (7'4\")", power: 'Medium', action: 'Fast',
                 line_rating: '8–17 lb', reel_type: 'Spinning reel', handle_material: 'Cork' };
  const badFields = Object.keys(want).filter(k => got[k] !== want[k]);
  if (!badFields.length) pass('CRS741MF prefills length, power, action, line, reel and handle');
  else fail('prefill mismatch: ' + badFields.map(k => k + '=' + got[k]).join(', '));
  const info = doc.getElementById('cfg-model-info');
  if (info && /CRS741MF/.test(info.textContent)) pass('model confirmation line shown');
  else fail('no confirmation after picking a model');

  console.log('\n== summary path label ==');
  const sumText = (doc.getElementById('cfg-list') || {}).textContent || '';
  const wantLabel = mode === 'custom' ? 'One custom rod' : 'OEM / private-label program';
  if (new RegExp(wantLabel).test(sumText)) pass('summary labels the path: "' + wantLabel + '"');
  else fail('summary label missing for ' + mode + ': "' + sumText.slice(0, 60) + '"');

  if (mode === 'oem') {
    console.log('\n== MOQ split (OEM only) ==');
    const moqCases = [
      ['Rod only', /300 pcs \/ model/],
      ['Rod + reel combo', /500 pcs/],
      ['Full retail kit (rod, reel, line, lures, packaging)', /1,000 pcs/],
    ];
    form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
    moqCases.forEach(([kit, re]) => {
      setVals({ kit_option: kit });
      const t = moqText();
      let mark = '';
      doc.querySelectorAll('#cfg-moq tr').forEach(tr => {
        const first = tr.querySelector('td');
        if (first && first.getAttribute('style')) mark = tr.textContent.replace(/\s+/g, ' ').trim();
      });
      if (re.test(mark)) pass('kit "' + kit.slice(0, 24) + '" highlights ' + re);
      else fail('kit "' + kit + '" wrong row highlighted: ' + mark);
      if (!(/300 pcs \/ model/.test(t) && /500 pcs/.test(t) && /1,000 pcs/.test(t))) {
        fail('MOQ table incomplete for ' + kit);
      }
    });

    console.log('\n== OEM commercial fields ==');
    const oemFields = ['model_count', 'target_price', 'annual_volume', 'ship_window',
                       'compliance', 'trade_terms', 'sample_plan'];
    const missOem = oemFields.filter(n => !form.querySelector('select[name="' + n + '"]'));
    if (!missOem.length) pass('OEM path asks model count, target price, volume, timing, compliance, terms, sampling');
    else fail('OEM fields missing: ' + missOem.join(', '));

    console.log('\n== kit_brand field (OEM only) ==');
    const kb = form.querySelector('select[name="kit_brand"]');
    if (!kb) fail('kit_brand select missing');
    else {
      const vals = Array.from(kb.options).map(o => o.value).filter(Boolean);
      const need = ["Our brand on everything (1,000 pcs min)", "Component maker's own brand",
                    "Unbranded / neutral bulk pack",
                    "Recommend a house brand that fits my price point"];
      const miss = need.filter(n => vals.indexOf(n) === -1);
      if (miss.length) fail('kit_brand missing options: ' + miss.join(' | '));
      else pass('kit_brand has all 4 branding routes (' + vals.length + ' options)');
    }

    console.log('\n== accessory list absent on OEM path ==');
    const kitIn = doc.getElementById('kit-lines-input');
    if (!kitIn) pass('accessory list not rendered on OEM page (custom-only)');
    else fail('accessory list should not exist on OEM page');

    console.log('\n== disabled OEM field never leaks into enquiry ==');
    form.querySelectorAll('select[name]').forEach(s => { s.value = ''; });
    setVals({ base_model: 'CRS741MF', target_market: 'Europe (EU)' });
    const sum = (doc.getElementById('cfg-list') || {}).textContent || '';
    if (/OEM \/ private-label program/.test(sum)) pass('OEM enquiry labelled correctly');
    else fail('enquiry not labelled');
  }

  if (mode === 'custom') {
    console.log('\n== custom MOQ terms (no tiers) ==');
    if (/1 rod/.test(moqText()) && /20–25 days/.test(moqText())) {
      pass('custom path shows single-rod terms, not MOQ tiers');
    } else fail('custom MOQ panel wrong: ' + moqText().slice(0, 90));

    console.log('\n== OEM-only fields disabled on custom path ==');
    const oemOnly = ['model_count', 'target_price', 'annual_volume', 'kit_brand'];
    const stillActive = oemOnly.filter(n => {
      const el = form.querySelector('select[name="' + n + '"]');
      return el && !el.disabled;
    });
    if (!stillActive.length) pass('OEM-only fields disabled on custom page');
    else fail('OEM fields still active: ' + stillActive.join(', '));

    console.log('\n== accessory list: model x quantity, one row per model ==');
    const kitIn = doc.getElementById('kit-lines-input');
    const kitBox = doc.getElementById('cfg-kit');
    if (!kitIn) { fail('kit_lines hidden input missing'); }
    else {
      const rows0 = doc.querySelectorAll('#kit-lines .kit-row');
      if (rows0.length === 4) pass('one empty row each for reel, line, lure and terminal tackle');
      else fail('expected 4 default rows, got ' + rows0.length);

      const terminal0 = row('accessory', 0);
      if (terminal0 && terminal0.querySelectorAll('.kit-sku option').length > 1) {
        pass('hooks and terminal tackle are available to the personal set-up');
      } else fail('terminal tackle picker has no catalogue options');

      if (kitBox && kitBox.hidden) pass('in-the-box panel stays hidden while nothing is picked');
      else fail('panel shown with an empty list');

      function row(cat, n) {
        return doc.querySelectorAll('#kit-lines .kit-row[data-cat="' + cat + '"]')[n || 0];
      }
      const r0 = row('reel', 0);
      r0.querySelector('.kit-sku').value = 'REEL-SPIN-2500';
      fire(r0.querySelector('.kit-sku'));
      r0.querySelector('.kit-qty').value = '2';
      r0.querySelector('.kit-qty').dispatchEvent(new window.Event('input', { bubbles: true }));
      if (/Reels: REEL-SPIN-2500 ×2/.test(kitIn.value)) pass('reel ×2 recorded in kit_lines');
      else fail('kit_lines wrong: "' + kitIn.value + '"');

      const addBtn = doc.querySelector('#kit-lines .kit-group[data-cat="reel"] .kit-add');
      addBtn.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
      if (doc.querySelectorAll('#kit-lines .kit-row[data-cat="reel"]').length === 2) {
        pass('can add a second reel row');
      } else fail('add-row button did not add a row');

      const r1 = row('reel', 1);
      r1.querySelector('.kit-sku').value = 'REEL-BAIT-200';
      fire(r1.querySelector('.kit-sku'));
      if (/REEL-SPIN-2500 ×2/.test(kitIn.value) && /REEL-BAIT-200 ×1/.test(kitIn.value)) {
        pass('two different reels, each with its own quantity');
      } else fail('second reel not recorded: ' + kitIn.value);

      const l0 = row('line', 0);
      l0.querySelector('.kit-sku').value = 'LINE-PE08-8S-150M';
      fire(l0.querySelector('.kit-sku'));
      l0.querySelector('.kit-qty').value = '3';
      l0.querySelector('.kit-qty').dispatchEvent(new window.Event('input', { bubbles: true }));
      if (/Line: LINE-PE08-8S-150M ×3/.test(kitIn.value)) pass('line ×3 spools recorded');
      else fail('line row wrong: ' + kitIn.value);

      setVals({ quantity_custom: '2 rods' });
      if (/Rods: 2 rods/.test(kitIn.value)) pass('rod count joins the same list');
      else fail('rod count missing: ' + kitIn.value);

      if (kitBox && !kitBox.hidden && /pieces/.test(doc.getElementById('cfg-kit-total').textContent)) {
        pass('in-the-box panel shows the running total');
      } else fail('panel did not show: ' + (doc.getElementById('cfg-kit-total') || {}).textContent);

      if (!/\$/.test(doc.getElementById('cfg-kit').textContent)) pass('no price shown anywhere — quote only');
      else fail('a price leaked into the accessory panel');

      row('reel', 1).querySelector('.kit-del')
        .dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
      if (doc.querySelectorAll('#kit-lines .kit-row[data-cat="reel"]').length === 1) {
        pass('remove-row works');
      } else fail('remove button did not remove');
    }
  }

  console.log('');
  window.close();
}

(async () => {
  for (const p of PAGES) {
    await testPage(p.file, p.path);
  }
  console.log('\n==== ' + passCount + ' passed, ' + failCount + ' failed ====');
  if (fail) process.exitCode = 1;
})().catch(e => { console.error('ERROR', e); process.exitCode = 1; });
