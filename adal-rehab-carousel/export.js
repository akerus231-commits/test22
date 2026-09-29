// Экспорт слайдов карусели в PNG: slide-01.png … slide-07.png (2160×2700).
//
//   npm install
//   npm run export            # или: node export.js [папка-вывода]
//
// Шрифты грузятся с Google Fonts, поэтому нужен интернет.

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const SRC = path.join(__dirname, 'carousel.html');
const OUT = path.resolve(process.argv[2] || path.join(__dirname, 'png'));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1160, height: 1430 },
    deviceScaleFactor: 2,
  });

  await page.goto('file://' + SRC, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  // document.fonts.check() возвращает true и при системном фолбэке,
  // поэтому проверяем, что веб-шрифты реально загружены.
  const missing = await page.evaluate(() => {
    const loaded = [...document.fonts]
      .filter((f) => f.status === 'loaded')
      .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`);
    return [
      'IBM Plex Sans 400',
      'IBM Plex Sans 500',
      'Source Serif 4 600',
    ].filter((f) => !loaded.includes(f));
  });
  if (missing.length) {
    console.error('Шрифты не загрузились:', missing.join(', '));
    await browser.close();
    process.exit(1);
  }

  const slides = await page.$$('section.slide');
  for (let i = 0; i < slides.length; i++) {
    const file = path.join(OUT, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await slides[i].screenshot({ path: file });
    console.log('→', path.relative(process.cwd(), file));
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
