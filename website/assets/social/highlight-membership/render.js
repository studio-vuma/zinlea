// Zinlea Night membership story series (1080x1920) for an Instagram highlight, plus highlight covers.
// Text stays inside Instagram's safe zone (roughly y 260-1640) so the profile bar and reply box never cover it.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const D = __dirname;
const W = 1080, H = 1920, PAD = 96;
const MOON = '#CCD9EF', INK = '#EEF1F7', MUTED = 'rgba(238,241,247,.74)', LINE = 'rgba(238,241,247,.14)';
const FONT = `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;500;600&family=DM+Mono&display=block">`;

function word(size) {
  const d = Math.round(size * 0.21), h = Math.round(size * 0.08), top = Math.round(size * 0.1);
  return `<span style="font:600 ${size}px/1 'Albert Sans';letter-spacing:-.045em;color:${INK}">z<span style="position:relative;display:inline-block">&#305;<span style="position:absolute;left:50%;top:${top}px;width:${d}px;height:${d}px;border-radius:50%;transform:translateX(-50%);background:${MOON};box-shadow:0 0 0 ${h}px rgba(204,217,239,.22)"></span></span>nlea</span>`;
}
const brand = `<div style="display:flex;align-items:baseline;gap:10px">${word(38)}<span style="font:300 28px 'Albert Sans';color:${MUTED}">night</span></div>`;
const arrow = `<svg width="120" height="20" viewBox="0 0 120 20"><path d="M0 10h116M108 2l8 8-8 8" fill="none" stroke="${INK}" stroke-width="2"/></svg>`;

// Background: midnight with a soft moonlight glow and the night-dial arcs as a quiet motif (like Prenuvo's graph lines).
function bg(variant = 0) {
  const glows = ['80% 12%', '15% 30%', '70% 70%', '20% 85%'];
  const g = glows[variant % glows.length];
  const arcs = [0, 1, 2, 3].map(i => `<circle cx="${variant % 2 ? 1080 : 0}" cy="${variant % 2 ? 1700 : 1650}" r="${260 + i * 90}" fill="none" stroke="${MOON}" stroke-opacity="${0.16 - i * 0.03}" stroke-width="${i === 0 ? 10 : 3}" stroke-dasharray="${i === 1 ? '2 16' : 'none'}" stroke-linecap="round"/>`).join('');
  return `<div style="position:absolute;inset:0;background:radial-gradient(60% 40% at ${g},rgba(60,86,150,.45),transparent 70%),radial-gradient(120% 60% at 50% 110%,#16213C 0%,#070B17 60%)"></div>
  <svg style="position:absolute;inset:0" width="${W}" height="${H}">${arcs}</svg>`;
}
const frame = (inner, v) => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:#070B17;color:${INK};font-family:'Albert Sans'">${bg(v)}
  <div style="position:absolute;left:${PAD}px;right:${PAD}px;top:270px;display:flex;justify-content:space-between;align-items:center">${brand}<span style="font:400 24px 'DM Mono';color:${MUTED}">20:00 &mdash; 08:00</span></div>
  ${inner}</div></body>`;
const block = (inner, top = 620) => `<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:${top}px">${inner}</div>`;
const h = (t, size = 76) => `<h1 style="margin:0;font:400 ${size}px/1.06 'Albert Sans';letter-spacing:-.035em">${t}</h1>`;
const p = (t, m = 34) => `<p style="margin:${m}px 0 0;font:300 38px/1.45 'Albert Sans';color:${MUTED}">${t}</p>`;

// Simple line icons (stroke only) drawn to match the site.
const IC = {
  moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/>',
  phone: '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
  pill: '<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="m9.2 8.1 5.6 7.8"/>',
  path: '<path d="M4 19c4 0 4-6 8-6s4-6 8-6"/><circle cx="4" cy="19" r="1.6"/><circle cx="20" cy="7" r="1.6"/>',
  loop: '<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>',
  card: '<rect x="2.5" y="5.5" width="19" height="13" rx="2.5"/><path d="M2.5 10h19M6 15h4"/>',
  q: '<circle cx="12" cy="12" r="9.5"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 1c0 1.8-2.5 2.2-2.5 4M12 17.5v.01"/>',
  mail: '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
  key: '<circle cx="8" cy="15" r="4"/><path d="m11 12 8.5-8.5M16.5 6.5l2.5 2.5"/>',
  steps: '<path d="M4 18h5v-5h5V8h5V4"/>',
};
const icon = (k, s = 54, c = MOON, sw = 1.5) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${IC[k]}</svg>`;
const item = (k, title, sub) => `<div style="display:flex;gap:30px;align-items:flex-start;padding:30px 0;border-top:1px solid ${LINE}">
  <div style="flex-shrink:0;margin-top:4px">${icon(k)}</div>
  <div><div style="font:400 38px/1.2 'Albert Sans';letter-spacing:-.015em">${title}</div><div style="margin-top:8px;font:300 31px/1.4 'Albert Sans';color:${MUTED}">${sub}</div></div></div>`;

function mcard(kind, tier, w = 360) {
  const bgs = {
    silver: 'linear-gradient(140deg,#E9EDF4 0%,#C3CAD6 55%,#E2E6EE 100%)',
    midnight: 'radial-gradient(120% 120% at 0% 0%,#2A3B68 0%,#0B1124 60%)',
    obsidian: 'radial-gradient(130% 120% at 100% 0%,#2A2F3D 0%,#0A0B0F 55%)',
  };
  const ink = kind === 'silver' ? '#0E1116' : '#EEF1F7';
  return `<div style="width:${w}px;aspect-ratio:1.586;border-radius:20px;padding:20px 22px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;background:${bgs[kind]};color:${ink};box-shadow:0 24px 50px -22px rgba(0,0,0,.8),inset 0 0 0 1px rgba(255,255,255,.14)">
    <div style="display:flex;justify-content:space-between"><span style="font:600 21px 'Albert Sans';letter-spacing:-.045em">zinlea night</span><span style="font:400 15px 'Albert Sans';opacity:.8">${tier}</span></div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end"><span style="font:400 15px 'DM Mono';opacity:.75">20:00 &mdash; 08:00</span><span style="width:40px;height:28px;border-radius:7px;background:linear-gradient(135deg,rgba(255,255,255,.6),rgba(255,255,255,.15))"></span></div></div>`;
}
const tier = (kind, name, price, sub) => `<div style="display:flex;gap:36px;align-items:center;padding:28px 0;border-top:1px solid ${LINE}">
  ${mcard(kind, name, 300)}
  <div><div style="font:400 40px/1.1 'Albert Sans';letter-spacing:-.02em">${name}</div><div style="margin-top:10px;font:400 34px 'Albert Sans';color:${MOON}">${price}</div><div style="margin-top:8px;font:300 28px/1.35 'Albert Sans';color:${MUTED}">${sub}</div></div></div>`;
const step = (when, title, sub) => `<div style="display:grid;grid-template-columns:250px 1fr;gap:20px;padding:30px 0;border-top:1px solid ${LINE}">
  <div style="font:400 26px 'DM Mono';color:${MOON};padding-top:8px">${when}</div>
  <div><div style="font:400 40px/1.15 'Albert Sans';letter-spacing:-.02em">${title}</div><div style="margin-top:8px;font:300 30px/1.4 'Albert Sans';color:${MUTED}">${sub}</div></div></div>`;

const STORIES = [
  // 1 Cover
  frame(block(`${h('Introducing Zinlea Night membership', 104)}
    <p style="margin:44px 0 0;font:300 42px/1.4 'Albert Sans';color:${MUTED}">Everything you need to know to get started.</p>
    <div style="margin-top:40px">${arrow}</div>`, 820), 0),

  // 2 What is it
  frame(block(`${h('What is Zinlea Night?', 84)}
    ${p('A private membership that gives you direct access to an experienced Advanced Nurse Practitioner through the night, by phone or video.')}
    ${p('If something worries you between 8pm and 8am, you speak to a senior clinician who listens, assesses and tells you clearly what to do next.', 28)}`, 640), 1),

  // 3 What's included
  frame(block(`${h('What does membership include?', 80)}
    <div style="margin-top:44px">
      ${item('moon', 'Overnight access', '8pm to 8am, whenever you need us')}
      ${item('phone', 'Phone or video consultations', 'with an experienced Advanced Nurse Practitioner')}
      ${item('pill', 'Medication guidance', 'and remote prescribing where clinically appropriate')}
      ${item('path', 'Reassurance and escalation', 'clear next steps if you need in-person care')}
      ${item('loop', 'Continuity', 'support that knows you, night after night')}
    </div>`, 520), 2),

  // 4 Which membership
  frame(block(`${h('Which membership is right for me?', 80)}
    <div style="margin-top:44px">
      ${tier('silver', 'Individual', 'From &pound;85 a month', 'Personal overnight support')}
      ${tier('midnight', 'Family', 'From &pound;225 a month', 'Support for your household')}
      ${tier('obsidian', 'Private Client', 'By consultation', 'A named lead clinician and specialist coordination')}
    </div>`, 520), 3),

  // 5 How to join
  frame(block(`${h('How do I join?', 84)}
    <div style="margin-top:44px">
      ${step('Today', 'Request membership', 'A short enquiry through our website.')}
      ${step('Within 24 hours', 'We reply', 'A member of our team responds personally.')}
      ${step('Onboarding', 'A brief call', 'To understand your needs and confirm your membership.')}
      ${step('From 20:00', 'Call when you need us', 'Overnight advice until 08:00.')}
    </div>`, 560), 0),

  // 6 For organisations
  frame(block(`${h('Do you work with care homes and organisations?', 80)}
    ${p('Yes. We partner with a small number of care homes, residences and family offices, providing overnight clinical support, triage and escalation from 8pm to 8am.')}
    ${p('Partnerships are tailored after an introductory conversation.', 28)}`, 640), 1),

  // 7 Emergencies
  frame(block(`<div style="font:400 150px/1 'DM Mono';color:#F08A72;letter-spacing:-.04em">999</div>
    <div style="margin-top:40px">${h('Is Zinlea Night an emergency service?', 76)}</div>
    ${p('No. For chest pain, difficulty breathing, signs of stroke, severe bleeding or any life-threatening symptoms, call 999 or go to A&amp;E straight away.')}`, 600), 2),

  // 8 Book (space left for Instagram's link sticker)
  frame(`<div style="position:absolute;left:${PAD}px;right:${PAD}px;top:700px;text-align:center">
      ${h('How do I become a member?', 84)}
      <p style="margin:40px 0 0;font:300 40px 'Albert Sans';color:${MUTED}">Request membership here</p>
      <svg style="margin:40px auto 0;display:block" width="40" height="90" viewBox="0 0 40 90"><path d="M20 0v84M6 70l14 14 14-14" fill="none" stroke="${MOON}" stroke-width="2.5"/></svg>
      <div style="margin:40px auto 0;width:640px;height:150px;border-radius:28px;border:2px dashed rgba(204,217,239,.35);display:flex;align-items:center;justify-content:center;font:400 24px 'DM Mono';color:rgba(204,217,239,.5)">place link sticker here</div>
      <p style="margin:56px 0 0;font:400 30px 'DM Mono';color:${MUTED}">zinlea.com/night/membership</p>
    </div>`, 3),
];

// Highlight covers: one line icon in the middle of the frame (Instagram crops covers to a circle).
const COVERS = { membership: 'card', 'zinlea-night': 'moon', 'private-client': 'key', 'how-it-works': 'steps', faq: 'q', contact: 'mail' };
const cover = k => `${FONT}<body style="margin:0"><div id="c" style="position:relative;width:${W}px;height:${H}px;overflow:hidden;background:radial-gradient(70% 40% at 50% 50%,#1B2747 0%,#070B17 70%)">
  <div style="position:absolute;left:50%;top:50%;width:820px;height:820px;transform:translate(-50%,-50%);border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 3px rgba(204,217,239,.2)">${icon(COVERS[k], 440, MOON, 1.1)}</div></div></body>`;

(async () => {
  fs.mkdirSync(path.join(D, 'out'), { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (let i = 0; i < STORIES.length; i++) {
    await pg.setContent(STORIES[i]);
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(300);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `membership-story-${i + 1}.png`) });
  }
  for (const k of Object.keys(COVERS)) {
    await pg.setContent(cover(k));
    await pg.waitForTimeout(150);
    await (await pg.$('#c')).screenshot({ path: path.join(D, 'out', `highlight-cover-${k}.png`) });
  }
  await b.close();
})();
