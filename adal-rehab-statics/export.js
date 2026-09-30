// Экспорт статичных макетов в PNG по имени макета, два формата:
//   png/1080x1080/a-01.png …  — лента
//   png/1080x1920/a-01.png …  — Stories / Reels
//
//   npm install
//   npm run export            # или: node export.js [папка-вывода] [--scale=2]
//
// По умолчанию файлы ровно в размер площадки; --scale=2 даёт удвоенные
// (2160×2160, 2160×3840). Шрифты грузятся с Google Fonts — нужен интернет.
// Фото фонов лежат в bg/ (имя задаётся полем photo в statics.html).

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const SRC = path.join(__dirname, 'statics.html');
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
  const brokenPhotos = await page.evaluate(() =>
    [...document.querySelectorAll('img.ad__photo')]
      .filter((img) => !img.complete || img.naturalWidth === 0)
      .map((img) => img.getAttribute('src')));
  if (brokenPhotos.length) {
    console.error('Не загрузились фото:', [...new Set(brokenPhotos)].join(', '));
    await browser.close();
    process.exit(1);
  }

  // document.fonts.check() возвращает true и при системном фолбэке,
  // поэтому проверяем, что веб-шрифты реально загружены.
  const missing = await page.evaluate(() => {
    const loaded = [...document.fonts]
      .filter((f) => f.status === 'loaded')
      .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`);
    return ['IBM Plex Sans 400', 'IBM Plex Sans 500', 'Source Serif 4 400']
      .filter((f) => !loaded.includes(f));
  });
  if (missing.length) {
    console.error('Шрифты не загрузились:', missing.join(', '));
    await browser.close();
    process.exit(1);
  }

  // Подгонка размеров под шрифты — после их загрузки.
  const overflow = await page.evaluate(() => {
    window.fitAds();
    return [...document.querySelectorAll('.ad')]
      .filter((a) => a.dataset.fit.includes('OVERFLOW'))
      .map((a) => `${a.closest('.deck').dataset.format}/${a.dataset.name}`);
  });
  if (overflow.length) {
    console.error('Текст не помещается:', overflow.join(', '));
    await browser.close();
    process.exit(1);
  }

  for (const [format, dir] of Object.entries(FORMATS)) {
    const outDir = path.join(OUT, dir);
    fs.mkdirSync(outDir, { recursive: true });
    for (const ad of await page.$$(`.deck[data-format="${format}"] section.ad`)) {
      const name = await ad.getAttribute('data-name');
      const file = path.join(outDir, `${name}.png`);
      await ad.screenshot({ path: file });
      console.log('→', path.relative(process.cwd(), file));
    }
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
