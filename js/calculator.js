/**
 * Логика расчёта себестоимости медицинской услуги.
 * Повторяет формулы из таблицы «Себестоимость медицинской услуги — сводная форма»:
 *
 *   Итого прямые расходы        = SUM(C10:C17)
 *   Итого накладные расходы     = SUM(C21:C29)
 *   Накладные расходы на 1 врача = IFERROR(C30 / C31, 0)
 *   Итого себестоимость услуги  = C18 + C32
 *   Маржа                       = IFERROR((C7 - C34) / C7, 0)
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.DentalCalc = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Структура таблицы: ключ поля, подпись, значение по умолчанию (как в исходном файле).
  var DIRECT_COSTS = [
    { key: 'doctorPay', label: 'ФОТ (оплата врачу)', value: 7500 },
    { key: 'nursePay', label: 'ФОТ м/сестра', value: 0 },
    { key: 'payrollTaxes', label: 'Налоги по ФОТ', value: 0 },
    { key: 'instruments', label: 'Мед. инструменты', value: 0 },
    { key: 'medicines', label: 'Лекарственные средства', value: 0 },
    { key: 'softInventory', label: 'Мягкий инвентарь', value: 0 },
    { key: 'consumables', label: 'Расходные материалы', value: 5000 },
    { key: 'depreciation', label: 'Амортизация оборудования', value: 0 }
  ];

  var OVERHEAD_COSTS = [
    { key: 'rent', label: 'Аренда', value: 0 },
    { key: 'utilities', label: 'Коммунальные', value: 0 },
    { key: 'adminPay', label: 'ФОТ адм. персонала', value: 20000 },
    { key: 'taxes', label: 'Налоги', value: 0 },
    { key: 'banking', label: 'Банковские услуги', value: 0 },
    { key: 'advertising', label: 'Реклама', value: 10000 },
    { key: 'crm', label: 'CRM', value: 5000 },
    { key: 'loanInterest', label: '% по кредиту', value: 0 },
    { key: 'other', label: 'Прочие расходы', value: 0 }
  ];

  var DEFAULTS = {
    serviceName: 'услуга',
    price: 25000,
    doctors: 3,
    direct: toMap(DIRECT_COSTS),
    overhead: toMap(OVERHEAD_COSTS)
  };

  function toMap(items) {
    var map = {};
    items.forEach(function (item) {
      map[item.key] = item.value;
    });
    return map;
  }

  function num(value) {
    var n = Number(value);
    return isFinite(n) ? n : 0;
  }

  function sum(map) {
    return Object.keys(map || {}).reduce(function (acc, key) {
      return acc + num(map[key]);
    }, 0);
  }

  // Аналог IFERROR(a / b, 0) из Excel.
  function safeDivide(a, b) {
    var result = num(a) / num(b);
    return isFinite(result) ? result : 0;
  }

  function calculate(input) {
    var price = num(input.price);
    var doctors = num(input.doctors);
    var directTotal = sum(input.direct);
    var overheadTotal = sum(input.overhead);
    var overheadPerDoctor = safeDivide(overheadTotal, doctors);
    var costPrice = directTotal + overheadPerDoctor;
    var margin = safeDivide(price - costPrice, price);

    return {
      price: price,
      directTotal: directTotal,
      overheadTotal: overheadTotal,
      overheadPerDoctor: overheadPerDoctor,
      costPrice: costPrice,
      profit: price - costPrice,
      margin: margin
    };
  }

  return {
    DIRECT_COSTS: DIRECT_COSTS,
    OVERHEAD_COSTS: OVERHEAD_COSTS,
    DEFAULTS: DEFAULTS,
    calculate: calculate
  };
});
