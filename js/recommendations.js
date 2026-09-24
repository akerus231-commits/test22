/**
 * Рекомендации по услуге на основе данных калькулятора.
 *
 *   analyze(input)      — быстрый анализ по правилам, работает без сети;
 *   buildPrompt(input)  — запрос для ИИ с данными расчёта;
 *   parseLine(line)     — разбор одной рекомендации из ответа ИИ.
 *
 * Рекомендация: { level: 'high' | 'medium' | 'low' | 'good', title, text }.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('./calculator.js'));
  } else {
    root.DentalRecs = factory(root.DentalCalc);
  }
})(typeof self !== 'undefined' ? self : this, function (Calc) {
  'use strict';

  var TARGET_MARGIN = 0.3;
  var LEVEL_ORDER = { high: 0, medium: 1, low: 2, good: 3 };

  function money(n) {
    var rounded = Math.round(n);
    var sign = rounded < 0 ? '−' : '';
    return sign + String(Math.abs(rounded)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' тг';
  }

  function pct(n) {
    return (Math.round(n * 1000) / 10).toString().replace('.', ',') + '%';
  }

  function num(v) {
    var n = Number(v);
    return isFinite(n) ? n : 0;
  }

  function largest(items, values) {
    var best = null;
    items.forEach(function (item) {
      var v = num(values && values[item.key]);
      if (v > 0 && (!best || v > best.value)) best = { label: item.label, value: v };
    });
    return best;
  }

  // Цена, при которой маржа равна целевой: цена = себестоимость / (1 − маржа).
  function priceForMargin(costPrice, margin) {
    return costPrice / (1 - margin);
  }

  function analyze(input) {
    var r = Calc.calculate(input);
    var direct = input.direct || {};
    var overhead = input.overhead || {};
    var recs = [];

    if (!r.price) {
      return [{
        level: 'medium',
        title: 'Укажите цену по прайсу',
        text: 'Без цены нельзя посчитать маржу. Себестоимость услуги сейчас ' + money(r.costPrice) + '.'
      }];
    }

    var targetPrice = priceForMargin(r.costPrice, TARGET_MARGIN);

    if (r.margin < 0) {
      recs.push({
        level: 'high',
        title: 'Услуга убыточна',
        text: 'С каждой услуги клиника теряет ' + money(-r.profit) + '. Цена безубыточности — ' +
          money(r.costPrice) + ', для маржи 30% нужна цена ' + money(targetPrice) + '.'
      });
    } else if (r.margin < 0.2) {
      recs.push({
        level: 'medium',
        title: 'Низкая маржа: ' + pct(r.margin),
        text: 'Прибыль с услуги — всего ' + money(r.profit) + '. Для маржи 30% цена должна быть ' +
          money(targetPrice) + ' (+' + pct(targetPrice / r.price - 1) + ' к текущей) или себестоимость ниже на ' +
          money(r.costPrice - r.price * (1 - TARGET_MARGIN)) + '.'
      });
    } else {
      recs.push({
        level: 'good',
        title: 'Маржа в норме: ' + pct(r.margin),
        text: 'Услуга приносит ' + money(r.profit) + ' прибыли. Скидка до ' + pct(r.margin) +
          ' ещё не уводит её в убыток.'
      });
    }

    var doctors = num(input.doctors);
    if (r.overheadTotal > 0 && doctors > 0 && r.costPrice > 0) {
      var share = r.overheadPerDoctor / r.costPrice;
      if (share > 0.3) {
        var withOneMore = Calc.calculate(Object.assign({}, input, { doctors: doctors + 1 }));
        var top = largest(Calc.OVERHEAD_COSTS, overhead);
        recs.push({
          level: share > 0.45 ? 'medium' : 'low',
          title: 'Накладные — ' + pct(share) + ' себестоимости',
          text: 'На одного врача приходится ' + money(r.overheadPerDoctor) + ' накладных' +
            (top ? ', больше всего — «' + top.label + '» (' + money(top.value) + ')' : '') +
            '. С ещё одним врачом накладные на врача снизятся до ' + money(withOneMore.overheadPerDoctor) +
            ', а маржа вырастет до ' + pct(withOneMore.margin) + '.'
        });
      }
    }

    var doctorPay = num(direct.doctorPay);
    if (doctorPay / r.price > 0.35) {
      recs.push({
        level: 'medium',
        title: 'Высокая доля оплаты врача',
        text: 'ФОТ врача — ' + pct(doctorPay / r.price) + ' от цены услуги. Обычно ориентируются на 25–35%.'
      });
    }

    var consumables = num(direct.consumables);
    if (consumables / r.price > 0.25) {
      recs.push({
        level: 'low',
        title: 'Дорогие расходные материалы',
        text: 'Материалы занимают ' + pct(consumables / r.price) + ' цены (' + money(consumables) +
          '). Сравните поставщиков или закупайте объёмом.'
      });
    }

    var missing = [];
    if (doctorPay > 0 && !num(direct.payrollTaxes)) missing.push('налоги по ФОТ');
    if (!num(direct.depreciation)) missing.push('амортизация оборудования');
    if (!num(overhead.rent)) missing.push('аренда');
    if (!num(overhead.utilities)) missing.push('коммунальные');
    if (missing.length) {
      recs.push({
        level: 'low',
        title: 'Проверьте незаполненные статьи',
        text: 'Не указаны: ' + missing.join(', ') + '. Если эти расходы есть, реальная себестоимость выше расчётной.'
      });
    }

    return recs.sort(function (a, b) { return LEVEL_ORDER[a.level] - LEVEL_ORDER[b.level]; });
  }

  function listLines(items, values) {
    return items.map(function (item) {
      return '- ' + item.label + ': ' + money(num(values && values[item.key]));
    }).join('\n');
  }

  function buildPrompt(input) {
    var r = Calc.calculate(input);
    return [
      'Ты финансовый консультант стоматологических клиник в Казахстане. Проанализируй себестоимость услуги и дай рекомендации владельцу клиники.',
      '',
      'Как считается: себестоимость = прямые расходы + (накладные расходы ÷ количество врачей); маржа = (цена − себестоимость) ÷ цена. Суммы в тенге.',
      '',
      'Услуга: ' + (input.serviceName || 'без названия'),
      'Цена по прайсу: ' + money(r.price),
      '',
      'Прямые расходы:',
      listLines(Calc.DIRECT_COSTS, input.direct),
      'Итого прямые: ' + money(r.directTotal),
      '',
      'Накладные расходы:',
      listLines(Calc.OVERHEAD_COSTS, input.overhead),
      'Итого накладные: ' + money(r.overheadTotal),
      'Количество врачей: ' + num(input.doctors),
      'Накладные на 1 врача: ' + money(r.overheadPerDoctor),
      '',
      'Себестоимость: ' + money(r.costPrice),
      'Прибыль с услуги: ' + money(r.profit),
      'Маржа: ' + pct(r.margin),
      '',
      'Дай 4–6 конкретных рекомендаций: что изменить в цене, расходах или загрузке врачей, с расчётами в тенге и процентах по этим данным. Отметь статьи, которые, похоже, не заполнены. Не выдумывай данных, которых нет.',
      '',
      'Формат ответа: каждая рекомендация — отдельная строка с JSON-объектом, без другого текста и без Markdown:',
      '{"level": "high" | "medium" | "low" | "good", "title": "короткий заголовок до 60 символов", "text": "1–3 предложения на русском"}',
      'level: high — срочно исправить, medium — важно, low — можно улучшить, good — всё хорошо.'
    ].join('\n');
  }

  function parseLine(line) {
    var s = String(line).trim().replace(/,$/, '');
    if (!s || s[0] !== '{') return null;
    try {
      var obj = JSON.parse(s);
      if (!obj || typeof obj.title !== 'string' || typeof obj.text !== 'string') return null;
      return {
        level: LEVEL_ORDER.hasOwnProperty(obj.level) ? obj.level : 'low',
        title: obj.title,
        text: obj.text
      };
    } catch (e) {
      return null;
    }
  }

  return {
    TARGET_MARGIN: TARGET_MARGIN,
    analyze: analyze,
    buildPrompt: buildPrompt,
    parseLine: parseLine
  };
});
