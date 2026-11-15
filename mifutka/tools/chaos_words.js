// Renders big rotated words as transparent PNGs for the chaos montage.
const { chromium } = require('playwright');
const words = { w1: ['ЛЮТО', '#ffd84d'], w2: ['ФЛЕКС', '#ff3bd4'], w3: ['МИФУТКА', '#7ff3ff'], w4: ['ВАКХАНАЛИЯ', '#ff3b6b'], w5: ['ПОДЪЕЗД В ШОКЕ', '#ffffff'] };
(async () => {
  const b = await chromium.launch();
  for (const [k, [txt, col]] of Object.entries(words)) {
    const p = await b.newPage({ viewport: { width: 1000, height: 300 } });
    await p.setContent(`<style>@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@900&display=swap');
      html,body{margin:0;background:transparent;width:1000px;height:300px;display:grid;place-items:center}
      b{font:900 ${txt.length > 9 ? 84 : 140}px Unbounded;color:${col};-webkit-text-stroke:8px #111;paint-order:stroke fill;text-shadow:0 0 30px ${col}}</style><b>${txt}</b>`);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    await p.screenshot({ path: `ov/${k}.png`, omitBackground: true }); await p.close();
  }
  await b.close(); console.log('words done');
})();
