const test = require('node:test');
const assert = require('node:assert/strict');
const { calculate, DEFAULTS } = require('../js/calculator.js');

test('значения по умолчанию совпадают с исходной таблицей', () => {
  const r = calculate(DEFAULTS);
  assert.equal(r.directTotal, 12500); // C18 = 7500 + 5000
  assert.equal(r.overheadTotal, 35000); // C30 = 20000 + 10000 + 5000
  assert.ok(Math.abs(r.overheadPerDoctor - 35000 / 3) < 1e-9); // C32
  assert.ok(Math.abs(r.costPrice - (12500 + 35000 / 3)) < 1e-9); // C34
  assert.ok(Math.abs(r.margin - (25000 - r.costPrice) / 25000) < 1e-12); // C36
  assert.equal(r.margin.toFixed(4), '0.0333');
});

test('0 врачей — накладные на врача 0 (IFERROR)', () => {
  const r = calculate({ ...DEFAULTS, doctors: 0 });
  assert.equal(r.overheadPerDoctor, 0);
  assert.equal(r.costPrice, 12500);
});

test('цена 0 — маржа 0 (IFERROR)', () => {
  const r = calculate({ ...DEFAULTS, price: 0 });
  assert.equal(r.margin, 0);
});

test('отрицательная маржа при себестоимости выше цены', () => {
  const r = calculate({ ...DEFAULTS, price: 20000 });
  assert.ok(r.margin < 0);
  assert.ok(r.profit < 0);
});

test('пустые и некорректные значения считаются нулём', () => {
  const r = calculate({ price: '', doctors: 'abc', direct: { a: null }, overhead: {} });
  assert.deepEqual(
    [r.directTotal, r.overheadTotal, r.overheadPerDoctor, r.costPrice, r.margin],
    [0, 0, 0, 0, 0]
  );
});
