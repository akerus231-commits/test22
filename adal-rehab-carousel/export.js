// Экспорт карусели в PNG, два формата по 7 слайдов, ровно в размер площадки:
//   png/1080x1080/slide-01.png … slide-07.png  — лента
//   png/1080x1920/slide-01.png … slide-07.png  — Stories / Reels
//
//   npm install
//   npm run export            # или: node export.js [папка-вывода] [--scale=2]
//
// --scale=2 даёт удвоенные файлы (2160×2160, 2160×3840) для печати/архива.
//
// Шрифты грузятся с Google Fonts, поэтому нужен интернет.
// Фото обложки и финала берутся из bg/cover.jpg и bg/final.jpg.

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const SRC = path.join(__dirname, 'carousel.html');
const args = process.argv.slice(2);
const scaleArg = args.find((a) => a.startsWith('--scale='));
const SCALE = scaleArg ? Number(scaleArg.split('=')[1]) : 1;
const OUT = path.resolve(args.find((a) => !a.startsWith('--')) || path.join(__dirname, 'png'));
const FORMATS = { square: '1080x1080', story: '1080x1920' };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 2400, height: 2000 },
    deviceScaleFactor: SCALE,
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

  const noPhoto = await page.evaluate(() =>
    [...document.querySelectorAll('.deck[data-format="square"] .scene')]
      .filter((s) => !s.querySelector('img'))
      .map((s) => s.closest('.slide').id)
  );
  if (noPhoto.length) console.warn('Нет фото (bg/*.jpg) на слайдах:', noPhoto.join(', '));

  for (const [format, dir] of Object.entries(FORMATS)) {
    const outDir = path.join(OUT, dir);
    fs.mkdirSync(outDir, { recursive: true });
    const slides = await page.$$(`.deck[data-format="${format}"] section.slide`);
    for (let i = 0; i < slides.length; i++) {
      const file = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
      await slides[i].screenshot({ path: file });
      console.log('→', path.relative(process.cwd(), file));
    }
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
