const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../mifutka-story.html') + ''); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: 's0.png' });
  await p.click('#playBtn'); const t0 = Date.now();
  const ts=[25000,30000,34500,48000,51000,57500,66000,77000,87500,93500];
  for (const t of ts) { await p.waitForTimeout(t-(Date.now()-t0)); await p.screenshot({ path: `s${t}.png` }); }
  console.log('errors', errs); await b.close();
})();
