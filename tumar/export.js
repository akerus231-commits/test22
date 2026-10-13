// Экспорт каруселей Тумар в PNG 1080×1080:
//   png/1-zh-22-35/01-cover.png …
//
//   npm install
//   npm run export            # чистовик: падает, если нет фото, шрифтов или текст не помещается
//   npm run draft             # черновик: вместо недостающих фото — заглушки, в png-draft/
//   node export.js [папка] [--scale=2] [--draft]
//
// Фото категорий лежат в photos/<имя>.jpg (имена — PHOTOS в carousels.html).
// Шрифт Manrope грузится с Google Fonts — нужен интернет.

const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const SRC = path.join(__dirname, 'carousels.html');
const args = process.argv.slice(2);
const DRAFT = args.includes('--draft');
const scaleArg = args.find((a) => a.startsWith('--scale='));
const SCALE = scaleArg ? Number(scaleArg.split('=')[1]) : 1;
const OUT = path.resolve(args.find((a) => !a.startsWith('--'))
  || path.join(__dirname, DRAFT ? 'png-draft' : 'png'));

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2300, height: 1200 }, deviceScaleFactor: SCALE });
  await page.goto('file://' + SRC, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  const missingFonts = await page.evaluate(() => {
    const loaded = [...document.fonts].filter((f) => f.status === 'loaded')
      .map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`);
    return ['Manrope 300', 'Manrope 500', 'Manrope 600', 'Manrope 700', 'Manrope 800']
      .filter((f) => !loaded.includes(f));
  });
  if (missingFonts.length) { await browser.close(); fail('Шрифты не загрузились: ' + missingFonts.join(', ')); }

  const missingPhotos = await page.evaluate(() =>
    [...new Set([...document.querySelectorAll('.cat')]
      .filter((ad) => ad.querySelector('.ph'))
      .map((ad) => `photos/${ad.dataset.photo}.jpg`))]);
  if (missingPhotos.length) {
    const msg = 'Нет фото: ' + missingPhotos.join(', ');
    if (!DRAFT) { await browser.close(); fail(msg); }
    console.warn(msg + ' — в черновике стоят заглушки');
  }

  const problems = await page.evaluate(() => {
    window.fitAds();
    return [...document.querySelectorAll('.ad')]
      .filter((a) => a.dataset.fitResult !== 'ok')
      .map((a) => `${a.dataset.name}: ${a.dataset.fitResult}`);
  });
  if (problems.length) {
    const msg = 'Вёрстка не прошла проверку:\n  ' + problems.join('\n  ');
    if (!DRAFT) { await browser.close(); fail(msg); }
    console.warn(msg);
  }

  fs.rmSync(OUT, { recursive: true, force: true });
  let n = 0;
  for (const ad of await page.$$('section.ad')) {
    const file = path.join(OUT, (await ad.getAttribute('data-name')) + '.png');
    fs.mkdirSync(path.dirname(file), { recursive: true });
    await ad.screenshot({ path: file });
    n++;
  }
  console.log(`${n} карточек → ${path.relative(process.cwd(), OUT) || '.'}`);
  await browser.close();
})().catch((err) => fail(err.stack || String(err)));
