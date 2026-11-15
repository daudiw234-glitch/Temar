// Subtitle PNG for the narrator's line over the chaos montage.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 400 } });
  await p.setContent(`<style>@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');
    html,body{margin:0;background:transparent;width:1080px;height:400px;display:grid;place-items:center}
    div{font:800 64px/1.25 Montserrat;color:#fff;text-align:center;padding:0 80px;text-shadow:0 4px 0 rgba(0,0,0,.7),0 0 26px rgba(0,0,0,.9)} b{color:#ffd84d}</style>
    <div>Короче, подъезд такого <b>ещё не видел!</b></div>`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
  await p.screenshot({ path: 'ov/sub_chaos.png', omitBackground: true }); await b.close(); console.log('sub done');
})();
