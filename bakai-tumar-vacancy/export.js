// Экспорт баннера вакансии в PNG:
//   png/vacancy[-b|-c]-1080x1350.png — лента Instagram (4:5)
//   png/vacancy[-b|-c]-1080x1920.png — Stories / Reels
//
// Варианты дизайна: banner.html (A), banner-b.html (B), banner-c.html (C).
//
//   npm install
//   npm run export            # или: node export.js [папка-вывода] [--scale=2]
//
// Шрифты Montserrat и Noto Sans Old Turkic (руны) грузятся с Google Fonts — нужен интернет.

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const SOURCES = ['banner.html', 'banner-b.html', 'banner-c.html'];
const args = process.argv.slice(2);
const scaleArg = args.find((a) => a.startsWith('--scale='));
const SCALE = scaleArg ? Number(scaleArg.split('=')[1]) : 1;
const OUT = path.resolve(args.find((a) => !a.startsWith('--')) || path.join(__dirname, 'png'));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 2400, height: 2000 },
    deviceScaleFactor: SCALE,
  });

  for (const src of SOURCES) {
    await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    // document.fonts.check() возвращает true и при системном фолбэке,
    // поэтому проверяем, что веб-шрифт реально загружен.
    const missing = await page.evaluate(() => {
      const loaded = [...document.fonts]
        .filter((f) => f.status === 'loaded')
        .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`);
      return ['Montserrat 500', 'Montserrat 600', 'Montserrat 700', 'Noto Sans Old Turkic 400']
        .filter((f) => !loaded.includes(f));
    });
    if (missing.length) {
      console.error(`${src}: шрифты не загрузились:`, missing.join(', '));
      await browser.close();
      process.exit(1);
    }

    const overflow = await page.evaluate(() => window.checkFit());
    if (overflow.length) {
      console.error(`${src}: текст не помещается:`, overflow.join(', '));
      await browser.close();
      process.exit(1);
    }

    fs.mkdirSync(OUT, { recursive: true });
    for (const ad of await page.$$('section.ad')) {
      const name = await ad.getAttribute('data-name');
      const file = path.join(OUT, `${name}.png`);
      await ad.screenshot({ path: file });
      console.log('→', path.relative(process.cwd(), file));
    }
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
