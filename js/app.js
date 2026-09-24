(function () {
  'use strict';

  var Calc = window.DentalCalc;
  var Recs = window.DentalRecs;
  var STORAGE_KEY = 'dental-calc:v1';

  var fmtMoney = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 });
  var fmtInput = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 });
  var fmtPct = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 });

  var $ = function (id) { return document.getElementById(id); };
  var form = $('calc-form');

  // ---------- Построение полей ----------

  function buildFields(containerId, items, group) {
    var container = $(containerId);
    items.forEach(function (item) {
      var id = group + '-' + item.key;
      var field = document.createElement('div');
      field.className = 'field';
      field.innerHTML =
        '<label for="' + id + '">' + item.label + '</label>' +
        '<div class="input-wrap">' +
        '<input type="text" inputmode="decimal" class="input input-num" id="' + id + '"' +
        ' data-group="' + group + '" data-key="' + item.key + '" placeholder="0">' +
        '<span class="unit">тг</span>' +
        '</div>';
      container.appendChild(field);
    });
  }

  buildFields('direct-fields', Calc.DIRECT_COSTS, 'direct');
  buildFields('overhead-fields', Calc.OVERHEAD_COSTS, 'overhead');

  // ---------- Чтение / запись значений ----------

  function parseNumber(str) {
    if (str == null) return 0;
    var clean = String(str).replace(/[\s  ]/g, '').replace(',', '.').replace(/[^\d.-]/g, '');
    var n = parseFloat(clean);
    return isFinite(n) ? n : 0;
  }

  function formatInput(n) {
    return n ? fmtInput.format(n) : '';
  }

  function money(n) {
    return fmtMoney.format(Math.round(n)) + ' тг';
  }

  function readState() {
    var state = {
      serviceName: $('serviceName').value.trim(),
      price: parseNumber($('price').value),
      doctors: parseNumber($('doctors').value),
      direct: {},
      overhead: {}
    };
    form.querySelectorAll('[data-group]').forEach(function (input) {
      state[input.dataset.group][input.dataset.key] = parseNumber(input.value);
    });
    return state;
  }

  function writeState(state) {
    $('serviceName').value = state.serviceName || '';
    $('price').value = formatInput(state.price);
    $('doctors').value = formatInput(state.doctors);
    form.querySelectorAll('[data-group]').forEach(function (input) {
      var group = state[input.dataset.group] || {};
      input.value = formatInput(group[input.dataset.key]);
    });
  }

  function emptyState() {
    var state = { serviceName: '', price: 0, doctors: 0, direct: {}, overhead: {} };
    Calc.DIRECT_COSTS.forEach(function (i) { state.direct[i.key] = 0; });
    Calc.OVERHEAD_COSTS.forEach(function (i) { state.overhead[i.key] = 0; });
    return state;
  }

  function save(state) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) { /* хранилище недоступно */ }
  }

  function load() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  // ---------- Отрисовка результата ----------

  function render() {
    var state = readState();
    var r = Calc.calculate(state);

    $('out-direct').textContent = money(r.directTotal);
    $('out-overhead').textContent = money(r.overheadTotal);
    $('out-per-doctor').textContent = money(r.overheadPerDoctor);
    $('out-cost').textContent = money(r.costPrice);
    $('out-price').textContent = money(r.price);
    $('out-profit').textContent = money(r.profit);
    $('out-margin').textContent = fmtPct.format(r.margin * 100) + '%';
    $('out-service').textContent = state.serviceName || 'Услуга без названия';

    $('lg-direct').textContent = money(r.directTotal);
    $('lg-overhead').textContent = money(r.overheadPerDoctor);
    $('lg-profit').textContent = money(Math.max(r.profit, 0));

    // Структура цены: доли от большего из (цена, себестоимость).
    var base = Math.max(r.price, r.costPrice) || 1;
    $('bar-direct').style.width = (r.directTotal / base) * 100 + '%';
    $('bar-overhead').style.width = (r.overheadPerDoctor / base) * 100 + '%';
    $('bar-profit').style.width = (Math.max(r.profit, 0) / base) * 100 + '%';

    var box = $('margin-box');
    var hint = $('margin-hint');
    box.classList.remove('is-bad', 'is-warn', 'is-good');
    if (!r.price) {
      hint.textContent = 'Укажите цену по прайсу, чтобы рассчитать маржу.';
    } else if (r.margin < 0) {
      box.classList.add('is-bad');
      hint.textContent = 'Услуга убыточна: себестоимость выше цены.';
    } else if (r.margin < 0.2) {
      box.classList.add('is-warn');
      hint.textContent = 'Низкая маржа — стоит пересмотреть цену или расходы.';
    } else {
      box.classList.add('is-good');
      hint.textContent = 'Хорошая маржа.';
    }

    save(state);
    if (!aiActive) renderRecs(Recs.analyze(state));
  }

  // ---------- Рекомендации ----------

  var LEVEL_LABELS = { high: 'Срочно', medium: 'Важно', low: 'Совет', good: 'Хорошо' };
  var recsList = $('recs-list');
  var recsStatus = $('recs-status');
  var aiBtn = $('btn-ai');
  var aiStopBtn = $('btn-ai-stop');
  var sample = null;
  var aiActive = false;   // на экране ответ ИИ, а не быстрый анализ
  var aiCtl = null;

  function recItem(rec) {
    var li = document.createElement('li');
    li.className = 'rec';
    var chip = document.createElement('span');
    chip.className = 'chip chip-' + rec.level;
    chip.textContent = LEVEL_LABELS[rec.level];
    var h = document.createElement('h4');
    h.textContent = rec.title;
    var p = document.createElement('p');
    p.textContent = rec.text;
    li.append(chip, h, p);
    return li;
  }

  function renderRecs(recs) {
    recsList.replaceChildren.apply(recsList, recs.map(recItem));
  }

  function setStatus(text, busy) {
    recsStatus.hidden = !text;
    recsStatus.textContent = text || '';
    recsStatus.classList.toggle('is-busy', !!busy);
  }

  function setMode(ai) {
    aiActive = ai;
    $('recs-badge').textContent = ai ? 'ИИ · Claude' : 'Быстрый анализ';
    $('recs-badge').classList.toggle('is-ai', ai);
    $('recs-sub').textContent = ai
      ? 'Персональные рекомендации по текущему расчёту.'
      : 'Подсказки по вашим цифрам обновляются вместе с расчётом.';
    $('recs-note').hidden = !ai;
  }

  function backToQuick(message) {
    setMode(false);
    setStatus(message || '');
    renderRecs(Recs.analyze(readState()));
  }

  var AI_ERRORS = {
    rate_limited: 'Слишком много запросов. Попробуйте чуть позже.',
    session_expired: 'Войдите в Claude заново и повторите запрос.',
    refused: 'ИИ не смог ответить на этот запрос. Проверьте введённые данные.',
    empty_completion: 'ИИ вернул пустой ответ. Попробуйте ещё раз.',
    prompt_too_large: 'Слишком много данных для запроса.'
  };
  var AI_UNAVAILABLE = ['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'];

  function askAI() {
    if (!sample) return;
    var ctl = new AbortController();
    aiCtl = ctl;
    var items = [];
    var pending = '';

    function take(line) {
      var rec = Recs.parseLine(line);
      if (rec) {
        items.push(rec);
        recsList.appendChild(recItem(rec));
        setStatus('Claude пишет рекомендации…', true);
      }
    }

    setMode(true);
    recsList.replaceChildren();
    setStatus('Claude анализирует расчёт. Обычно это занимает до минуты…', true);
    aiBtn.disabled = true;
    aiStopBtn.hidden = false;

    sample(Recs.buildPrompt(readState()), {
      signal: ctl.signal,
      onText: function (update) {
        var lines = (pending + update.delta).split('\n');
        pending = lines.pop();
        lines.forEach(take);
      }
    }).then(function (res) {
      if (aiCtl !== ctl) return;
      take(pending);
      if (!items.length) {
        renderRecs([{ level: 'low', title: 'Ответ ИИ', text: res.text }]);
      }
      setStatus(res.truncated ? 'Ответ получился слишком длинным и обрезан.' : '');
    }).catch(function (e) {
      if (aiCtl !== ctl) return; // запрос отменён вводом новых данных
      var code = e && e.code;
      if (AI_UNAVAILABLE.indexOf(code) !== -1) {
        aiBtn.hidden = true;
        backToQuick('ИИ-рекомендации недоступны. Показан быстрый анализ.');
      } else if (code === 'cancelled') {
        if (items.length) setStatus('Остановлено.'); else backToQuick();
      } else if (items.length) {
        setStatus(AI_ERRORS[code] || 'Ответ прервался. Нажмите кнопку, чтобы попробовать ещё раз.');
      } else {
        backToQuick(AI_ERRORS[code] || 'Не удалось получить ответ. Попробуйте ещё раз.');
      }
    }).then(function () {
      if (aiCtl === ctl) finishAI();
    });
  }

  function finishAI() {
    aiCtl = null;
    aiBtn.disabled = false;
    aiStopBtn.hidden = true;
  }

  aiBtn.addEventListener('click', askAI);
  aiStopBtn.addEventListener('click', function () { if (aiCtl) aiCtl.abort(); });

  // ИИ доступен, когда страница открыта в Claude; иначе остаётся быстрый анализ.
  if (window.claude && typeof window.claude.use === 'function') {
    window.claude.use('sample').then(function (fn) {
      sample = fn;
      aiBtn.hidden = !fn;
    }, function () {});
  }

  // ---------- События ----------

  // Новые данные — ответ ИИ устарел, возвращаемся к быстрому анализу.
  form.addEventListener('input', function () {
    if (aiCtl) {
      var ctl = aiCtl;
      finishAI();
      ctl.abort();
    }
    if (aiActive) setMode(false);
    setStatus('');
    render();
  });

  // Форматирование числа при выходе из поля: 25000 → 25 000
  form.addEventListener('focusout', function (e) {
    var input = e.target;
    if (input.classList && input.classList.contains('input-num')) {
      input.value = formatInput(parseNumber(input.value));
    }
  });

  form.addEventListener('submit', function (e) { e.preventDefault(); });

  $('btn-reset').addEventListener('click', function () {
    writeState(Calc.DEFAULTS);
    form.dispatchEvent(new Event('input'));
  });

  $('btn-clear').addEventListener('click', function () {
    writeState(emptyState());
    form.dispatchEvent(new Event('input'));
    $('price').focus();
  });

  var printBtn = $('btn-print');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });

  $('year').textContent = new Date().getFullYear();

  writeState(load() || Calc.DEFAULTS);
  render();
})();
