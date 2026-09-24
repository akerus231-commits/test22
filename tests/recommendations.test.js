const test = require('node:test');
const assert = require('node:assert/strict');
const { DEFAULTS } = require('../js/calculator.js');
const { analyze, buildPrompt, parseLine } = require('../js/recommendations.js');

test('пример из таблицы: низкая маржа и цена для 30%', () => {
  const recs = analyze(DEFAULTS);
  assert.equal(recs[0].level, 'medium');
  assert.match(recs[0].title, /Низкая маржа: 3,3%/);
  // 24 166,67 / 0,7 = 34 523,81
  assert.match(recs[0].text, /34 524 тг/);
});

test('убыточная услуга идёт первой с уровнем high', () => {
  const recs = analyze({ ...DEFAULTS, price: 20000 });
  assert.equal(recs[0].level, 'high');
  assert.match(recs[0].text, /4 167 тг/);
});

test('нет цены — одна подсказка указать цену', () => {
  const recs = analyze({ ...DEFAULTS, price: 0 });
  assert.equal(recs.length, 1);
  assert.match(recs[0].title, /цену/);
});

test('подсказывает незаполненные статьи', () => {
  const recs = analyze(DEFAULTS);
  const missing = recs.find((r) => r.title.includes('незаполненные'));
  assert.ok(missing);
  assert.match(missing.text, /налоги по ФОТ/);
});

test('запрос к ИИ содержит данные расчёта', () => {
  const prompt = buildPrompt(DEFAULTS);
  assert.match(prompt, /Цена по прайсу: 25 000 тг/);
  assert.match(prompt, /Себестоимость: 24 167 тг/);
  assert.match(prompt, /Маржа: 3,3%/);
});

test('разбор строки ответа ИИ', () => {
  assert.deepEqual(parseLine('{"level":"high","title":"A","text":"B"}'), { level: 'high', title: 'A', text: 'B' });
  assert.equal(parseLine('{"level":"x","title":"A","text":"B"},').level, 'low');
  assert.equal(parseLine('просто текст'), null);
  assert.equal(parseLine('{"title": 1}'), null);
});
