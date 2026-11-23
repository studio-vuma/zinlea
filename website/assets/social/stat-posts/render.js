// Zinlea statistic posts on deep purple (1080x1350 @2x).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = __dirname, W = 1080, H = 1350, PAD = 90;
const INK = '#F3EEFB', MUTED = 'rgba(243,238,251,.72)', LAV = '#C9B8F0';
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600&family=DM+Mono&display=block">`;
const word = `<span style="display:inline-flex;align-items:baseline;gap:9px"><span style="font:600 34px/1 'Albert Sans';letter-spacing:-.045em;color:${INK}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:3px;width:7px;height:7px;border-radius:50%;transform:translateX(-50%);background:${LAV};box-shadow:0 0 0 3px rgba(201,184,240,.25)"></span></span>nlea</span><span style="font:300 25px 'Albert Sans';color:${MUTED}">night</span></span>`;
const BG = 'radial-gradient(80% 55% at 85% 0%,rgba(140,100,210,.45),transparent 65%),radial-gradient(100% 60% at 10% 110%,#3A2463 0%,#170F2B 62%)';
const arcs = [0,1,2,3].map(i=>`<circle cx="${W}" cy="${H}" r="${260+i*95}" fill="none" stroke="${LAV}" stroke-opacity="${.18-i*.04}" stroke-width="${i===0?10:3}" ${i===1?'stroke-dasharray="2 16"':''} stroke-linecap="round"/>`).join('');
const post = (big, unit, line, sub, src) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:${BG};color:${INK};font-family:'Albert Sans'">
  <svg style="position:absolute;inset:0" width="${W}" height="${H}">${arcs}</svg>
  <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:90px;display:flex;justify-content:space-between;align-items:center">${word}<span style="font:400 22px 'DM Mono';color:${MUTED}">By the numbers</span></div>
  <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:180px;bottom:220px;display:flex;flex-direction:column;justify-content:center">
    <div style="font:300 ${big.length>6?200:250}px/1 'Albert Sans';letter-spacing:-.055em;color:${LAV}">${big}</div>
    <div style="margin-top:20px;font:400 30px 'DM Mono';color:${LAV}">${unit}</div>
    <div style="margin-top:56px;padding-top:44px;border-top:1px solid rgba(243,238,251,.16);font:300 66px/1.1 'Albert Sans';letter-spacing:-.035em">${line}</div>
    <div style="margin-top:28px;font:300 32px/1.45 'Albert Sans';color:${MUTED}">${sub}</div></div>
  <div style="position:absolute;left:${PAD}px;right:${PAD}px;bottom:80px;font:400 20px/1.5 'DM Mono';color:rgba(243,238,251,.5)">${src}</div>
</div></body>`;
const POSTS = [
  post('354,125', 'people living in care homes in England', 'Behind every one is a family <span style="color:'+LAV+'">wondering how the night went.</span>',
       'Zinlea Night gives care teams and families access to senior nurses, 8pm to 8am.', 'Source: DHSC, Adult social care in England, monthly statistics (week ending 14 October 2025).'),
  post('1 in 3', 'people with a parent over 75', 'say they live too far away <span style="color:'+LAV+'">to help with daily care.</span>',
       'Distance shouldn&rsquo;t mean lying awake wondering. Senior nurses, 8pm to 8am.', 'Source: Royal Voluntary Service survey of 1,000 people with parents over 75 (2015).'),
];
(async () => { fs.mkdirSync(path.join(D,'out'),{recursive:true});
  const b = await chromium.launch(); const pg = await b.newPage({ viewport:{width:W,height:H}, deviceScaleFactor:2 });
  for (let i=0;i<POSTS.length;i++){ await pg.setContent(POSTS[i]); await pg.evaluate(()=>document.fonts.ready); await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D,'out',`zinlea-stat-${i+1}.png`) }); }
  await b.close(); })();
