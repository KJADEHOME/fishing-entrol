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

  function setVals(obj) {
    Object.keys(obj).forEach(k => {
      const s = form.querySelector('select[name="' + k + '"]');
      if (!s) { fail('missing select: ' + k); return; }
      s.value = obj[k];
      if (s.value !== obj[k]) fail('could not set ' + k + ' = ' + obj[k]);
    });
    form.dispatchEvent(new window.Event('change', { bubbles: true }));
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
    rod_type: 'Spinning rod', length: "2.13 m (7'0\")", sections: '2 pieces',
    power: 'Medium-Light', action: 'Fast', lure_weight: '5–21 g', line_rating: 'PE 0.8–2.0',
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
