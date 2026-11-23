// Mock-up of the overall Zinlea Instagram profile: bio, highlights in brand colours and a sample grid.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const S = path.join(__dirname, '..');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(S, f)).toString('base64');

const BIO = [
  'Expert medical advice, when you need it',
  'Night · senior nurses overnight, London 20:00–08:00',
  'Global · healthcare partnerships, Africa',
  'Membership ↓',
];
const HL = [
  ['About', 'stories2/out/highlight-cover-about-health.png'],
  ['Membership', 'stories/out/highlight-cover-membership.png'],
  ['How it works', 'stories2/out/highlight-cover-how-it-works-night.png'],
  ['Private Client', 'stories/out/highlight-cover-private-client.png'],
  ['FAQ', 'stories2/out/highlight-cover-faq-health.png'],
  ['Global', 'stories2/out/highlight-cover-global-dawn.png'],
];
const GRID = [
  'carousel/zinlea-night-carousel-1.png', 'stories2/out/about-1.png', 'post/zinlea-night-post-4x5.png',
  'stories2/out/global-1.png', 'carousel/zinlea-night-carousel-4.png', 'stories2/out/how-it-works-2.png',
  'stories2/out/faq-2.png', 'carousel/zinlea-night-carousel-6.png', 'stories/out/membership-story-4.png',
];

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2 });
  await pg.setContent(`<body style="margin:0;background:#E9EBEF;padding:24px;font-family:-apple-system,'Helvetica Neue',Arial,sans-serif">
  <div id="c" style="width:390px;background:#fff;border-radius:34px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.4)">
    <div style="padding:16px 16px 8px;font-weight:700;font-size:20px;display:flex;justify-content:space-between"><span>zinleanight</span><span style="letter-spacing:3px">&middot;&middot;&middot;</span></div>
    <div style="display:flex;align-items:center;gap:22px;padding:4px 16px 0">
      <img src="${img('wordmarks/profile-dawn-zinlea.png')}" style="width:86px;height:86px;border-radius:50%">
      <div style="display:flex;gap:20px;text-align:center;font-size:13px;color:#737373">
        <div><b style="display:block;color:#0A0A0A;font-size:16px">18</b>posts</div><div><b style="display:block;color:#0A0A0A;font-size:16px">1,204</b>followers</div><div><b style="display:block;color:#0A0A0A;font-size:16px">310</b>following</div></div>
    </div>
    <div style="padding:12px 16px 0;font-size:13.5px;line-height:1.42;color:#0A0A0A">
      <b>Zinlea Health · Overnight Care London</b><br><span style="color:#737373">Medical &amp; health</span><br>${BIO.join('<br>')}<br>
      <span style="color:#00376B;font-weight:600">zinlea.com</span></div>
    <div style="display:flex;gap:6px;padding:14px 16px"><span style="flex:1;text-align:center;padding:8px;border-radius:8px;background:#EFEFEF;font-weight:600;font-size:13.5px">Follow</span><span style="flex:1;text-align:center;padding:8px;border-radius:8px;background:#EFEFEF;font-weight:600;font-size:13.5px">Message</span></div>
    <div style="display:flex;gap:14px;padding:2px 16px 16px;overflow:hidden">
      ${HL.map(([n, f]) => `<div style="flex-shrink:0;width:62px;display:flex;flex-direction:column;align-items:center;gap:6px"><div style="width:62px;height:62px;border-radius:50%;border:1px solid #DBDBDB;display:flex;align-items:center;justify-content:center"><div style="width:56px;height:56px;border-radius:50%;background:url(${img(f)}) center/cover"></div></div><span style="font-size:11px;white-space:nowrap">${n}</span></div>`).join('')}
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;border-top:1px solid #DBDBDB">
      ${GRID.map(f => `<div style="aspect-ratio:3/4;background:url(${img(f)}) center/cover"></div>`).join('')}
    </div>
  </div></body>`);
  await pg.waitForTimeout(500);
  await (await pg.$('#c')).screenshot({ path: path.join(__dirname, '_profile-mockup.png') });
  await b.close();
  console.log(BIO.join('\n').length, 'characters in bio');
})();
