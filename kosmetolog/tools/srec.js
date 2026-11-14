const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, recordVideo: { dir: 'vid4', size: { width: 1080, height: 1920 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + require('path').resolve(__dirname, '../kosmetolog-story.html') + '');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1500);
  await p.click('#playBtn');
  await p.waitForTimeout(JSON.parse(require('fs').readFileSync('timeline.json','utf8')).total + 1500);
  await ctx.close(); await b.close();
})();
