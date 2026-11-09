const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 } });
  const errs=[]; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(__dirname, '../kepchik-story.html') + ''); await p.click('#playBtn');
  const tl = await p.evaluate(() => window.__timeline);
  require('fs').writeFileSync('timeline.json', JSON.stringify(tl)); console.log('total', tl.total, 'events', tl.events.length, 'errors', errs);
  await b.close();
})();
