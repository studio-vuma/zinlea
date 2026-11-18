// Render a LinkedIn carousel: one high-resolution PNG per slide and a PDF document.
// Usage: node src/render_linkedin.js src/linkedin_case01.html linkedin/case-01 case-01
const { chromium } = require('playwright');
const path = require('path');

const [srcFile, outDir, prefix] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(srcFile), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);

  const slides = await page.$$('section.s');
  for (let i = 0; i < slides.length; i++) {
    const name = `${prefix}-slide-${String(i + 1).padStart(2, '0')}.png`;
    await slides[i].screenshot({ path: path.join(outDir, name) });
  }

  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: path.join(outDir, `${prefix}-linkedin-carousel.pdf`),
    width: '1080px', height: '1350px', printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  console.log(`${slides.length} slides rendered to ${outDir}`);
  await browser.close();
})();
