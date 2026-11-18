const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../chats.html') + ''); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: 's0.png' });
  await p.click('#playBtn'); const t0 = Date.now();
  const ts=[2500,9000,24000,31000,40000,52000,62000,72000,90000,100000,110000,118000];
  for (const t of ts) { await p.waitForTimeout(t-(Date.now()-t0)); await p.screenshot({ path: `s${t}.png` }); }
  console.log('errors', errs); await b.close();
})();
