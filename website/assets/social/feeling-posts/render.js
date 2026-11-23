// "The morning after" feeling posts: white editorial frame, photo above, time + one line below.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = __dirname, W = 1080, H = 1350;
const img = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(D, f)).toString('base64');
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600&family=DM+Mono&display=block">`;
const word = sub => `<span style="display:inline-flex;align-items:baseline;gap:8px"><span style="font:600 32px/1 'Albert Sans';letter-spacing:-.045em;color:#0E1116">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:3px;width:7px;height:7px;border-radius:50%;transform:translateX(-50%);background:#2D4A8A;box-shadow:0 0 0 3px rgba(45,74,138,.16)"></span></span>nlea</span><span style="font:300 24px 'Albert Sans';color:#5A606B">${sub}</span></span>`;
const POSTS = [
  ['p1.jpg', '50% 40%', '07:30', 'The morning after a worried night.', 'Everyone&rsquo;s okay.', 'night'],
  ['p2.jpg', '50% 45%', '08:00', 'Peace of mind for the people', 'who look after the people they love.', 'health'],
  ['p3.jpg', '45% 40%', '16:00', 'Less lying awake.', 'More of this.', 'health'],
  ['p4.jpg', '50% 55%', '08:15', 'A quiet night.', 'A normal morning.', 'night'],
];
const page = ([f, pos, t, a, b, sub]) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;background:#fff;font-family:'Albert Sans';color:#0E1116">
  <div style="position:absolute;left:50px;right:50px;top:50px;height:880px;border-radius:36px;overflow:hidden"><img src="${img(f)}" style="width:100%;height:100%;object-fit:cover;object-position:${pos}"></div>
  <div style="position:absolute;left:84px;right:84px;top:990px">
    <div style="display:flex;align-items:center;gap:14px;font:400 26px 'DM Mono';color:#2D4A8A"><span style="width:10px;height:10px;border-radius:50%;background:#2D4A8A;box-shadow:0 0 0 6px rgba(45,74,138,.14)"></span>${t}</div>
    <div style="margin-top:22px;font:300 58px/1.1 'Albert Sans';letter-spacing:-.035em">${a} <span style="color:#9AA0AA">${b}</span></div></div>
  <div style="position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;align-items:center">${word(sub)}<span style="font:400 22px 'DM Mono';color:#5A606B">zinlea.com</span></div>
</div></body>`;
(async () => { fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  for (let i = 0; i < POSTS.length; i++) { await pg.setContent(page(POSTS[i])); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `zinlea-feeling-${i + 1}.png`) }); }
  await b.close(); })();
