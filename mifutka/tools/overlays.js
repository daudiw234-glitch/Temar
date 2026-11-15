// Renders transparent 1080x1920 PNG overlays for the real-footage part.
const { chromium } = require('playwright');
const fs = require('fs');
const css = `
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800;900&family=Unbounded:wght@900&display=swap');
  html,body{margin:0;width:1080px;height:1920px;background:transparent;font-family:Montserrat,sans-serif;color:#fff}
  .player{position:absolute;left:70px;right:70px;top:150px;background:rgba(14,10,24,.82);border:3px solid rgba(255,255,255,.18);border-radius:44px;padding:30px 36px;display:flex;align-items:center;gap:28px}
  .cover{width:110px;height:110px;border-radius:24px;background:linear-gradient(135deg,#ff3bd4,#6a4bb0);display:grid;place-items:center;font:900 54px Unbounded}
  .meta{flex:1;min-width:0} .k{font:600 26px Montserrat;color:#c8bfe6;letter-spacing:2px} .t{font:900 44px Montserrat;margin-top:6px}
  .bar{position:absolute;left:206px;right:110px;bottom:34px;height:8px;border-radius:4px;background:rgba(255,255,255,.18)}
  .eq{display:flex;gap:8px;align-items:flex-end;height:60px}.eq i{width:12px;background:#ff3b6b;border-radius:6px}
  .ring{position:absolute;left:70px;top:430px;width:940px;height:940px;border-radius:50%;box-shadow:0 0 0 14px #fff, 0 0 60px 20px rgba(255,59,212,.55)}
  .cap{position:absolute;left:60px;right:60px;top:1450px;text-align:center}
  .tag{display:inline-block;font:900 50px Unbounded;background:#ff3b6b;padding:18px 36px;border-radius:26px;box-shadow:0 10px 0 #8f1239;transform:rotate(-2deg)}
  .sub{font:800 52px Montserrat;margin-top:40px;text-shadow:0 4px 0 rgba(0,0,0,.6),0 0 24px rgba(0,0,0,.7)}
  .end{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px;text-align:center;padding:0 80px}
  .end .h{font:900 108px/1.05 Unbounded;text-shadow:0 0 30px #ff3bd4,0 0 60px #ff3bd4,8px 8px 0 #3a0b4a}
  .end .s{font:800 56px Montserrat} .end .c{font:800 40px Montserrat;background:rgba(255,255,255,.15);border:3px solid rgba(255,255,255,.4);padding:24px 40px;border-radius:999px}
  .dot{width:26px;height:26px;border-radius:50%;background:#ff3b6b;box-shadow:0 0 16px #ff3b6b}
`;
const player = `<div class="player"><div class="cover">M</div><div class="meta"><div class="k">СЕЙЧАС ИГРАЕТ · ПОДЪЕЗД</div><div class="t">Мифутка — трек</div></div>
  <div class="eq"><i style="height:30px"></i><i style="height:55px"></i><i style="height:40px"></i><i style="height:60px"></i></div><div class="bar"></div></div><div class="ring"></div>`;
const pages = {
  c1: player + `<div class="cap"><div class="tag">ФЛЕКС №1</div><div class="sub">разминка. соседи ещё спят</div></div>`,
  c2: player + `<div class="cap"><div class="tag">ФЛЕКС №2</div><div class="sub">вторая волна пошла</div></div>`,
  c3: player + `<div class="cap"><div class="tag">ФЛЕКС №3</div><div class="sub">трек Мифутки на репите</div></div>`,
  c4: player + `<div class="cap"><div class="tag">ФЛЕКС №4</div><div class="sub">финал. подъезд в шоке</div></div>`,
  end: `<div class="end"><div class="h">МИФУТКА,<br>ТЫ ЛЕГЕНДА</div><div class="s">ждём новый трек</div><div class="c">пиши в комменты, кто флексит лучше ↓</div></div>`,
  dot: `<div class="dot"></div>`,
};
(async () => {
  const b = await chromium.launch();
  for (const [k, html] of Object.entries(pages)) {
    const small = k === 'dot';
    const p = await b.newPage({ viewport: small ? { width: 26, height: 26 } : { width: 1080, height: 1920 } });
    await p.setContent(`<style>${css}${small ? 'html,body{width:26px;height:26px}' : ''}</style>${html}`);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: `ov/${k}.png`, omitBackground: true });
    await p.close();
  }
  await b.close(); console.log('overlays done');
})();
