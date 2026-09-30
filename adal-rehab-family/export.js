// Экспорт креативов в PNG (1080×1350, deviceScaleFactor 2 → файлы 2160×2700):
//   png/statics/a-01.png …       — одиночные макеты из statics.html
//   png/carousels/c1-01.png …    — слайды каруселей из carousels.html
//
//   npm install
//   npm run export            # или: node export.js [папка-вывода]
//
// Шрифты грузятся с Google Fonts, поэтому нужен интернет.

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const OUT = path.resolve(process.argv[2] || path.join(__dirname, 'png'));
const SOURCES = [
  { file: 'statics.html', selector: 'section.ad', dir: 'statics' },
  { file: 'carousels.html', selector: 'section.slide', dir: 'carousels' },
];

async function checkFonts(page) {
  // document.fonts.check() возвращает true и при системном фолбэке,
  // поэтому проверяем, что веб-шрифты реально загружены.
  return page.evaluate(() => {
    const loaded = [...document.fonts]
      .filter((f) => f.status === 'loaded')
      .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`);
    return ['IBM Plex Sans 400', 'IBM Plex Sans 500', 'Source Serif 4 400']
      .filter((f) => !loaded.includes(f));
  });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1160, height: 1430 },
    deviceScaleFactor: 2,
  });

  for (const src of SOURCES) {
    await page.goto('file://' + path.join(__dirname, src.file), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => window.fixWraps && window.fixWraps());
    const missing = await checkFonts(page);
    if (missing.length) {
      console.error(`${src.file}: шрифты не загрузились:`, missing.join(', '));
      await browser.close();
      process.exit(1);
    }

    const outDir = path.join(OUT, src.dir);
    fs.mkdirSync(outDir, { recursive: true });
    for (const el of await page.$$(src.selector)) {
      const name = await el.getAttribute('data-name');
      const file = path.join(outDir, `${name}.png`);
      await el.screenshot({ path: file });
      console.log('→', path.relative(process.cwd(), file));
    }
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
