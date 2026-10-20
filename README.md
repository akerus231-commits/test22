# revanite.kz — персональный сайт Руслана Хасанова

Статический сайт (RU + EN), рассчитанный на индексацию поисковиками и ИИ-системами.

## Структура

- `build.py` — генератор. Весь текст сайта находится в нём (словари `T`, `FAQ`, `EXPERIENCE`, `SERVICES`, `CASES`, `TEACH`, `CLIENTS`).
- `site/` — готовый сайт, который заливается на хостинг.
- `site_src/` — исходники. Сюда кладётся фото `ruslan-khasanov.jpg`.

## Как обновить

1. Поправь текст в `build.py` или положи фото в `site_src/ruslan-khasanov.jpg`.
2. Запусти `python3 build.py`. Папка `site/` пересоберётся целиком.
3. Закоммить изменения и залей `site/` на хостинг.

## Что внутри для SEO и GEO

- Чистый HTML без JavaScript: ИИ-краулеры видят весь текст.
- JSON-LD schema.org: Person, ProfessionalService (Revanite), FAQPage, Service, BreadcrumbList.
- `llms.txt` с ключевыми фактами на двух языках.
- `sitemap.xml` с hreflang (ru / en / x-default).
- `robots.txt` с разрешением для GPTBot, ClaudeBot, PerplexityBot, Google-Extended, YandexBot, Bingbot и других.

## Открытые вопросы

- Должность в BI GROUP (сейчас: «Опыт работы в компании, затем — клиент Revanite»).
- Подтвердить публикацию цифр кейса бизнес-форума.
- Фото.
