// Zinlea Night "02:14" Reels: 1080x1920, 15s, 30fps. Frames are rendered deterministically
// (render(t) sets every style from the time t), then encoded to MP4 with ffmpeg.
// Text stays inside the Reels safe zone (top ~14%, bottom ~35% left clear for Instagram's UI).
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'); const path = require('path');
const D = __dirname, W = 1080, H = 1920, FPS = 30, DUR = 15;

const REELS = {
  temperature: { time: '02:14', pos: 6.23, lines: ['Your daughter has a temperature.', 'The GP surgery is closed.', 'And you&rsquo;re not sure it can wait until morning.'] },
  parent:      { time: '03:40', pos: 7.67, lines: ['Your mum sounds confused on the phone.', 'She was fine at dinner.', 'Is this something, or nothing?'] },
  medication:  { time: '23:52', pos: 3.87, lines: ['You&rsquo;ve taken the wrong dose.', 'The pharmacy closed hours ago.', 'Who do you ask?'] },
};

const page = r => `<!doctype html><html><head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400;600&family=DM+Mono&display=block">
<style>
  html,body{margin:0;background:#070B17}
  #c{position:relative;width:${W}px;height:${H}px;overflow:hidden;font-family:'Albert Sans';color:#EEF1F7;
     background:radial-gradient(90% 55% at 50% 112%,#1F2D52 0%,#070B17 62%)}
  .glow{position:absolute;left:50%;top:560px;width:900px;height:900px;margin-left:-450px;border-radius:50%;
     background:radial-gradient(circle,rgba(204,217,239,.16),transparent 62%)}
  .top{position:absolute;left:72px;right:72px;top:290px;display:flex;justify-content:space-between;align-items:center}
  .wm{font:600 40px/1 'Albert Sans';letter-spacing:-.045em}
  .wm i{position:relative;display:inline-block;font-style:normal}
  .wm i b{position:absolute;left:50%;top:4px;width:8px;height:8px;border-radius:50%;transform:translateX(-50%);background:#CCD9EF;box-shadow:0 0 0 3px rgba(204,217,239,.22)}
  .sub{font:300 30px 'Albert Sans';color:rgba(238,241,247,.7);margin-left:10px}
  .clock{position:absolute;left:0;right:0;top:420px;text-align:center;font:400 168px/1 'DM Mono';letter-spacing:-.03em}
  .dial{position:absolute;left:50%;top:640px;margin-left:-330px}
  .line{position:absolute;left:84px;right:84px;top:1010px;text-align:center;font:400 64px/1.15 'Albert Sans';letter-spacing:-.03em}
  .end{position:absolute;left:84px;right:84px;top:960px;text-align:center}
  .end h1{margin:0;font:400 76px/1.06 'Albert Sans';letter-spacing:-.04em}
  .end h1 span{color:#CCD9EF}
  .end p{margin:30px 0 0;font:300 34px/1.4 'Albert Sans';color:rgba(238,241,247,.8)}
  .pill{display:inline-block;margin-top:40px;padding:18px 34px;border-radius:999px;background:#CCD9EF;color:#070B17;font:500 32px 'Albert Sans'}
  .note{position:absolute;left:0;right:0;top:1500px;text-align:center;font:400 24px 'DM Mono';color:rgba(238,241,247,.55)}
</style></head><body><div id="c">
  <div class="glow" id="glow"></div>
  <div class="top" id="top"><span><span class="wm">z<i>&#305;<b></b></i>nlea</span><span class="sub">night</span></span>
    <span style="font:400 24px 'DM Mono';color:rgba(238,241,247,.6)">London</span></div>
  <div class="clock" id="clock">${r.time}</div>
  <svg class="dial" id="dial" width="660" height="350" viewBox="-24 0 568 300"></svg>
  ${r.lines.map((l, i) => `<div class="line" id="l${i}">${l}</div>`).join('')}
  <div class="end" id="end"><h1>Speak to a senior nurse, <span>8pm to 8am.</span></h1>
    <p>Private overnight medical advice for London families, by phone or video.</p><div class="pill">zinlea.com</div></div>
  <div class="note" id="note">In an emergency, always call 999.</div>
</div>
<script>
const R = ${JSON.stringify({ pos: r.pos })};
const cx = 260, cy = 270, rad = 220;
function ticks(){let t='';for(let h=0;h<=12;h++){const a=Math.PI-(h/12)*Math.PI,m=h%2===0,r1=rad+8,r2=rad+(m?20:14);
  t+='<line x1="'+(cx+r1*Math.cos(a))+'" y1="'+(cy-r1*Math.sin(a))+'" x2="'+(cx+r2*Math.cos(a))+'" y2="'+(cy-r2*Math.sin(a))+'" stroke="#EEF1F7" stroke-opacity="'+(m?.55:.28)+'" stroke-width="2"/>';
  if(m)t+='<text x="'+(cx+(rad+46)*Math.cos(a))+'" y="'+(cy-(rad+46)*Math.sin(a)+7)+'" text-anchor="middle" font-family="DM Mono" font-size="21" fill="#EEF1F7" fill-opacity=".6">'+String((20+h)%24).padStart(2,'0')+'</text>';}return t;}
const TICKS = ticks();
const ease = x => x<0?0:x>1?1:1-Math.pow(1-x,3);
const win = (t,a,b,fi=.6,fo=.6) => Math.min(ease((t-a)/fi), 1-ease((t-(b-fo))/fo));
function render(t){
  const s=(id,o,y=0)=>{const e=document.getElementById(id);e.style.opacity=o;e.style.transform='translateY('+y+'px)';};
  // intro
  s('top', ease(t/0.8)); s('glow', ease(t/1.5)*.9);
  const clockO = Math.min(ease((t-.3)/.8), 1-ease((t-10.4)/.6));
  s('clock', clockO, (1-ease((t-.3)/.8))*20);
  const p = R.pos * ease((t-.5)/2.2);  // marker sweeps from 20:00 to the scene time
  const a=Math.PI-(p/12)*Math.PI, mx=cx+rad*Math.cos(a), my=cy-rad*Math.sin(a);
  const pulse = 1 + .25*Math.sin(t*3);
  document.getElementById('dial').innerHTML='<path d="M 40 270 A 220 220 0 0 1 480 270" fill="none" stroke="#EEF1F7" stroke-opacity=".16" stroke-width="2"/>'+
    (p>0.01?'<path d="M 40 270 A 220 220 0 0 1 '+mx+' '+my+'" fill="none" stroke="#CCD9EF" stroke-width="3" stroke-linecap="round"/>':'')+TICKS+
    '<circle cx="'+mx+'" cy="'+my+'" r="'+(24*pulse)+'" fill="#CCD9EF" opacity=".18"/><circle cx="'+mx+'" cy="'+my+'" r="10" fill="#CCD9EF"/>';
  s('dial', Math.min(ease((t-.2)/1), 1-ease((t-10.4)/.6)));
  // three lines, one after another
  s('l0', win(t,2.8,5.4), (1-ease((t-2.8)/.6))*24);
  s('l1', win(t,5.4,8.0), (1-ease((t-5.4)/.6))*24);
  s('l2', win(t,8.0,10.8), (1-ease((t-8.0)/.6))*24);
  // end card
  s('end', ease((t-11)/.8), (1-ease((t-11)/.8))*30);
  s('note', ease((t-11.8)/.8));
}
render(0);
</script></body></html>`;

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const [name, r] of Object.entries(REELS)) {
    const dir = path.join(D, 'frames', name); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    await pg.setContent(page(r)); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(400);
    const el = await pg.$('#c');
    for (let f = 0; f < FPS * DUR; f++) {
      await pg.evaluate(t => render(t), f / FPS);
      await el.screenshot({ path: path.join(dir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
    const out = path.join(D, `zinlea-reel-${name}.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.jpg'),
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out]);
    console.log('wrote', out);
  }
  await b.close();
})();
