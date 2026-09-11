/* Functional test for the OEM configurator: compatibility warnings + MOQ split.
   Run: NODE_PATH=<workspace>/node_modules node scripts/test_configurator.js */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const SRC = path.resolve(__dirname, '..');
const PAGE = path.join(SRC, 'configure.html');

function fail(m) { console.log('  FAIL  ' + m); process.exitCode = 1; }
function pass(m) { console.log('  ok    ' + m); }

(async () => {
  // strip external resources (GTM, fonts) so jsdom never touches the network
  let html = fs.readFileSync(PAGE, 'utf8');
  html = html.replace(/<script[^>]+src="https?:\/\/[^"]*"[^>]*><\/script>/gi, '');
  html = html.replace(/<link[^>]+href="https?:\/\/[^"]*"[^>]*>/gi, '');
  html = html.replace(/<script[^>]+src="script\.js"[^>]*><\/script>/gi, '');

  const vc = new VirtualConsole();
  vc.on('jsdomError', () => {});
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'http://localhost/configure.html', virtualConsole: vc
  });
  const { window } = dom;
  window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  window.eval(fs.readFileSync(path.join(SRC, 'script.js'), 'utf8'));
  window.document.dispatchEvent(new window.Event('DOMContentLoaded'));
  await new Promise(r => setTimeout(r, 100));

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
    // reset every select first so cases stay independent
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
    if (!/No conflicts|will not run/i.test(warnText()) === false) { /* noop */ }
  }

  console.log('\n== MOQ split ==');
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
    if (/300 pcs \/ model/.test(t) && /500 pcs/.test(t) && /1,000 pcs/.test(t)) {
      /* all three rows always listed */
    } else fail('MOQ table incomplete for ' + kit);
  });

  console.log('\n== embedded product catalogue ==');
  const rawCat = doc.getElementById('catalog-data');
  let CAT = [];
  try { CAT = JSON.parse((rawCat && rawCat.textContent) || '[]'); } catch (e) { CAT = []; }
  if (CAT.length >= 20) pass('catalogue embedded in page: ' + CAT.length + ' rods');
  else fail('catalogue missing or too small: ' + CAT.length);
  const optCount = form.querySelectorAll('select[name="base_model"] option').length;
  if (optCount === CAT.length + 1) pass('model picker lists every rod + blank (' + optCount + ')');
  else fail('model picker has ' + optCount + ' options for ' + CAT.length + ' rods');

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

  console.log('\n== two commercial paths ==');
  function pathRadio(v) { return form.querySelector('input[name="build_path"][value="' + v + '"]'); }
  if (!pathRadio('oem') || !pathRadio('custom')) { fail('path radios missing'); }
  else {
    const brandFs = Array.from(form.querySelectorAll('fieldset[data-path]'))
      .find(fs => fs.getAttribute('data-path') === 'oem');
    const persFs = Array.from(form.querySelectorAll('fieldset[data-path]'))
      .find(fs => fs.getAttribute('data-path') === 'custom');
    if (!brandFs || !persFs) fail('path fieldsets missing');
    else {
      if (!brandFs.hidden && persFs.hidden) pass('default path is OEM (branding shown, personal hidden)');
      else fail('default path wrong: branding.hidden=' + brandFs.hidden +
                ' personal.hidden=' + persFs.hidden);

      pathRadio('custom').checked = true;
      fire(pathRadio('custom'));
      if (persFs.hidden === false && brandFs.hidden === true) pass('switching to custom swaps the groups');
      else fail('path switch did not swap groups');

      const qOem = form.querySelector('select[name="quantity"]');
      const qCustom = form.querySelector('select[name="quantity_custom"]');
      if (qOem && qOem.disabled && qCustom && !qCustom.disabled) pass('hidden-path fields are disabled');
      else fail('disabled state wrong: quantity.disabled=' + (qOem && qOem.disabled) +
                ' quantity_custom.disabled=' + (qCustom && qCustom.disabled));

      if (/1 rod/.test(moqText()) && /20–25 days/.test(moqText())) {
        pass('custom path shows single-rod terms, not MOQ tiers');
      } else fail('custom MOQ panel wrong: ' + moqText().slice(0, 90));

      if (/One custom rod/.test(doc.getElementById('cfg-list').textContent)) {
        pass('summary labels the path for the sales team');
      } else fail('summary missing path label');

      setVals({ quantity: '300 pcs' });
      if (!/One custom rod[\s\S]*300 pcs/.test(doc.getElementById('cfg-list').textContent)) {
        pass('a disabled OEM field does not leak into the enquiry');
      } else fail('disabled field leaked into the summary');

      pathRadio('oem').checked = true;
      fire(pathRadio('oem'));
      if (/300 pcs \/ model/.test(moqText())) pass('switching back restores the MOQ table');
      else fail('MOQ table did not come back');
    }
  }

  console.log('\n== kit_brand field ==');
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

  console.log('\ndone.');
  window.close();
})().catch(e => { console.error('ERROR', e); process.exitCode = 1; });
