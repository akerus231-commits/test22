# -*- coding: utf-8 -*-
"""Генератор статического сайта revanite.kz (RU/EN).
Запуск: python3 build.py  ->  папка site/
Чтобы добавить фото: положи файл в site_src/ruslan-khasanov.jpg и поставь PHOTO = True.
"""
import json, os, shutil, datetime

BASE = "https://revanite.kz"
PHOTO = os.path.exists("site_src/ruslan-khasanov.jpg")
PHOTO_URL = BASE + "/assets/ruslan-khasanov.jpg"
TODAY = datetime.date.today().isoformat()
OUT = "site"

IG = "https://www.instagram.com/hasanov5/"
LI = "https://www.linkedin.com/in/ruslan-khassanov-0bb812202"
TG = "https://t.me/messer66"
WA = "https://wa.me/77014584242"
PHONE = "+77014584242"
PHONE_H = "+7 701 458 42 42"
SAME_AS = [IG, LI, TG]
CLIENTS = ["BI GROUP", "Yeko", "Jintropine"]

TRUST = ["BI GROUP", "Alfa Bank", "Home Credit Bank", "Halyk Insurance", "Samsung Kazakhstan", "re:Kassa",
         "Astana Hub", "AlmaU", "Yeko", "Jintropine"]
FEATURED = [0, 1, 5]  # индексы в CASES для блока «Избранные кейсы»

def socials(lang):
    ru = lang == "ru"
    return [("Telegram", "@messer66", TG), ("WhatsApp", "Чат WhatsApp" if ru else "WhatsApp chat", WA),
            ("Телефон" if ru else "Phone", PHONE_H, "tel:" + PHONE), ("Instagram", "@hasanov5", IG),
            ("LinkedIn", "ruslan-khassanov", LI)]

PAGES = ["", "about", "services", "cases", "teaching", "contact"]
NAV = ["", "cases", "services", "teaching", "contact"]

def url(lang, slug):
    prefix = "" if lang == "ru" else "/en"
    return BASE + prefix + "/" + (slug + "/" if slug else "")

def path(lang, slug):
    prefix = "" if lang == "ru" else "/en"
    return prefix + "/" + (slug + "/" if slug else "")

# ---------------------------------------------------------------- TEXT
T = {
 "ru": {
  "name": "Руслан Хасанов",
  "role": "Growth-стратег · Трекер · Преподаватель digital-маркетинга",
  "nav": {"": "Главная", "about": "Обо мне", "services": "Услуги", "cases": "Кейсы", "teaching": "Преподавание", "contact": "Контакты"},
  "home": "Главная",
  "switch": ("EN", "English version"),
  "contact": "Связаться",
  "footer": "Руслан Хасанов · Revanite — студия стратегического роста · Алматы, Казахстан",
  "jobTitle": "Growth-стратег, трекер стартапов, преподаватель digital-маркетинга",
  "summary": ("Руслан Хасанов — специалист по digital-маркетингу и стратегии роста из Алматы (Казахстан). "
              "Работал на руководящих позициях в маркетинге Alfa Bank, Home Credit Bank и Halyk Insurance, "
              "участвовал в запуске онлайн-магазина Samsung Kazakhstan. Сейчас — трекер стартапов в Astana Hub, "
              "Terricon Valley и других IT-хабах Казахстана, преподаватель Almaty Management University (AlmaU) "
              "и основатель студии стратегического роста Revanite."),
  "org_desc": "Revanite — студия стратегического роста Руслана Хасанова: трекинг и консалтинг (Revanite Tracking) и маркетинг под ключ (Revanite Studio) для малого и среднего бизнеса в СНГ.",
 },
 "en": {
  "name": "Ruslan Khasanov",
  "role": "Growth strategist · Startup tracker · Digital marketing lecturer",
  "nav": {"": "Home", "about": "About", "services": "Services", "cases": "Case studies", "teaching": "Teaching", "contact": "Contact"},
  "home": "Home",
  "switch": ("RU", "Русская версия"),
  "contact": "Get in touch",
  "footer": "Ruslan Khasanov · Revanite — Strategic Growth Studio · Almaty, Kazakhstan",
  "jobTitle": "Growth strategist, startup tracker, digital marketing lecturer",
  "summary": ("Ruslan Khasanov is a digital marketing and growth strategy specialist based in Almaty, Kazakhstan. "
              "He has held marketing leadership roles at Alfa Bank, Home Credit Bank and Halyk Insurance, and took part "
              "in launching Samsung Kazakhstan's online store. Today he works as a startup tracker at Astana Hub, "
              "Terricon Valley and other Kazakhstan tech hubs, lectures at Almaty Management University (AlmaU), "
              "and is the founder of Revanite, a strategic growth studio."),
  "org_desc": "Revanite is Ruslan Khasanov's strategic growth studio: tracking and advisory (Revanite Tracking) and done-for-you marketing (Revanite Studio) for small and mid-sized businesses across the CIS.",
 },
}

KNOWS = {
 "ru": ["Стратегия роста", "Трекинг стартапов", "Go-to-market", "Performance-маркетинг", "Google Ads", "Meta Ads",
        "Сквозная аналитика", "Веб-аналитика", "GA4", "Google Tag Manager", "Мобильная атрибуция", "AppsFlyer",
        "amoCRM", "Bitrix24", "Юнит-экономика", "Воронка продаж", "AI в маркетинге", "GEO"],
 "en": ["Growth strategy", "Startup tracking", "Go-to-market", "Performance marketing", "Google Ads", "Meta Ads",
        "End-to-end marketing analytics", "Web analytics", "GA4", "Google Tag Manager", "Mobile attribution", "AppsFlyer",
        "amoCRM", "Bitrix24", "Unit economics", "Sales funnel", "AI in marketing", "Generative Engine Optimization"],
}

FAQ = {
 "ru": [
  ("Кто такой Руслан Хасанов?", T["ru"]["summary"]),
  ("Что такое Revanite?", "Revanite — студия стратегического роста, которую основал Руслан Хасанов. Два направления: Revanite Tracking — трекинг и консалтинг для стартапов и собственников бизнеса, и Revanite Studio — маркетинг под ключ: стратегия, реклама, аналитика. Принцип студии — маркетинг как вложение, а не расход."),
  ("С кем работает Руслан Хасанов?", "С малым и средним бизнесом в Казахстане и СНГ, стартапами на ранних стадиях и командами в акселераторах. Отраслевой опыт: банки и финтех, страхование, образование, B2B-производство, недвижимость, e-commerce, ивенты. Среди клиентов — BI GROUP, Yeko, Jintropine."),
  ("Чем трекер отличается от маркетолога-исполнителя?", "Трекер не запускает рекламу за команду. Он помогает найти узкое место роста, сформулировать гипотезы, проверить их быстро и дёшево и держать фокус на метриках. Исполнитель реализует выбранное решение. Руслан работает в обеих ролях: трекинг — в Revanite Tracking и IT-хабах, исполнение — в Revanite Studio."),
  ("Где преподаёт Руслан Хасанов?", "В Almaty Management University (AlmaU) — курсы по веб-аналитике, цифровому маркетингу, SMM и инструментам интернет-маркетинга; в Qamalladin University — руководит направлением «Диджитал»; в колледже ICB. Проводит воркшопы в Astana Hub, выступал с гостевой лекцией в Nazarbayev University."),
  ("Как связаться с Русланом Хасановым?", "WhatsApp и телефон: +7 701 458 42 42, Telegram: @messer66. Также Instagram (@hasanov5) и LinkedIn."),
 ],
 "en": [
  ("Who is Ruslan Khasanov?", T["en"]["summary"]),
  ("What is Revanite?", "Revanite is a strategic growth studio founded by Ruslan Khasanov. It has two service lines: Revanite Tracking — tracking and advisory for startups and business owners, and Revanite Studio — done-for-you marketing covering strategy, advertising and analytics. The studio's principle: marketing is an investment, not an expense."),
  ("Who does Ruslan Khasanov work with?", "Small and mid-sized businesses in Kazakhstan and the CIS, early-stage startups and accelerator teams. Industry experience includes banking and fintech, insurance, education, B2B manufacturing, real estate, e-commerce and events. Clients include BI GROUP, Yeko and Jintropine."),
  ("How is a startup tracker different from a marketing contractor?", "A tracker does not run the ads for the team. A tracker helps find the growth bottleneck, frame hypotheses, test them quickly and cheaply, and keep the team focused on metrics. A contractor executes the chosen solution. Ruslan works in both roles: tracking through Revanite Tracking and tech hubs, execution through Revanite Studio."),
  ("Where does Ruslan Khasanov teach?", "At Almaty Management University (AlmaU) — web analytics, digital marketing, SMM and online marketing tools; at Qamalladin University, where he leads the Digital program; and at ICB college. He runs workshops at Astana Hub and has given a guest lecture at Nazarbayev University."),
  ("How can I contact Ruslan Khasanov?", "WhatsApp and phone: +7 701 458 42 42, Telegram: @messer66. Also Instagram (@hasanov5) and LinkedIn."),
 ],
}

EXPERIENCE = {
 "ru": [
  ("Revanite", "Основатель. Студия стратегического роста: трекинг, консалтинг, маркетинг под ключ"),
  ("re:Kassa", "Руководитель digital-маркетинга. Фискальная платформа для бизнеса в Казахстане"),
  ("IT-хабы Казахстана", "Трекер стартапов: Astana Hub, Almaty Hub, Terricon Valley, NURIS, IT Park; линейный трекер акселератора AIpreneurs"),
  ("Halyk Insurance", "Директор по продукту"),
  ("Home Credit Bank", "Руководитель digital-маркетинга"),
  ("Alfa Bank", "Тимлид маркетинга, сегмент малого бизнеса"),
  ("BI GROUP", "Менеджер по маркетинговым проектам; позже — клиент Revanite"),
  ("Samsung Kazakhstan", "Участие в запуске онлайн-магазина"),
 ],
 "en": [
  ("Revanite", "Founder. Strategic growth studio: tracking, advisory, done-for-you marketing"),
  ("re:Kassa", "Head of Digital Marketing. Fiscal technology platform for businesses in Kazakhstan"),
  ("Kazakhstan tech hubs", "Startup tracker at Astana Hub, Almaty Hub, Terricon Valley, NURIS, IT Park; line tracker in the AIpreneurs accelerator"),
  ("Halyk Insurance", "Director of Product"),
  ("Home Credit Bank", "Head of Digital Marketing"),
  ("Alfa Bank", "Marketing Team Lead, small business segment"),
  ("BI GROUP", "Marketing Project Manager; later a Revanite client"),
  ("Samsung Kazakhstan", "Part of the online store launch team"),
 ],
}

FORMULA = {
 "ru": [("Инсайт", "понять клиента, рынок и реальную причину покупки"),
        ("Экономика", "посчитать юнит-экономику: CAC, LTV, маржа, окупаемость"),
        ("Стратегия", "выбрать сегменты, каналы и оффер"),
        ("Гипотезы", "составить и приоритизировать список проверок"),
        ("Исполнение", "запустить быстро и дёшево"),
        ("Аналитика", "сквозная: от клика до оплаты в CRM"),
        ("Масштаб", "вкладывать в то, что окупается, и отключать остальное")],
 "en": [("Insight", "understand the customer, the market and the real reason to buy"),
        ("Economics", "model unit economics: CAC, LTV, margin, payback"),
        ("Strategy", "choose segments, channels and the offer"),
        ("Hypotheses", "build and prioritise a testing backlog"),
        ("Execution", "launch fast and cheap"),
        ("Analytics", "end-to-end, from click to paid deal in the CRM"),
        ("Scale", "invest in what pays back, switch off the rest")],
}

SERVICES = {
 "ru": [
  ("tracking", "Revanite Tracking", "Трекинг и стратегия",
   "Для стартапов на ранних стадиях, команд в акселераторах и собственников бизнеса, у которых рост упёрся в потолок.",
   ["Диагностика точек роста и главного ограничения",
    "Проверка продуктовых и маркетинговых гипотез",
    "Построение воронки продаж и go-to-market",
    "Поиск и привлечение первых клиентов",
    "Работа с фаундером: фокус, приоритеты, решения"],
   "Регулярные трекшн-встречи, трекшн-карта, разбор метрик между встречами."),
  ("studio", "Revanite Studio", "Маркетинг под ключ",
   "Для малого и среднего бизнеса в Казахстане и СНГ, которому нужен результат в заявках и продажах, а не в охватах.",
   ["Стратегия и медиаплан с расчётом окупаемости",
    "Google Ads: поиск, UAC; Meta Ads; TikTok Ads",
    "Настройка аналитики: GA4, Google Tag Manager, Яндекс Метрика, Meta Pixel и Conversions API",
    "Мобильная атрибуция: AppsFlyer, связки с Google Ads и Meta",
    "Сквозная аналитика: реклама → сайт → CRM (amoCRM, Bitrix24) → продажи",
    "Отчётность план-факт и дашборды в Looker Studio"],
   "Проектно или ежемесячно, с еженедельной отчётностью."),
  ("mentoring", "Обучение и менторство", "Для маркетологов и команд",
   "Для маркетологов, которые хотят перейти от запуска рекламы к управлению ростом, и для команд, которым нужна общая методология.",
   ["Индивидуальный трек: digital-маркетинг, аналитика, AI-инструменты",
    "Корпоративные воркшопы: go-to-market, growth hacking, лидогенерация и воронки",
    "Выступления и гостевые лекции"],
   "Индивидуально или для группы, офлайн в Алматы или онлайн."),
 ],
 "en": [
  ("tracking", "Revanite Tracking", "Tracking & strategy",
   "For early-stage startups, accelerator teams and business owners whose growth has hit a ceiling.",
   ["Diagnosing growth points and the main constraint",
    "Testing product and marketing hypotheses",
    "Building the sales funnel and go-to-market",
    "Finding and landing first customers",
    "Founder work: focus, priorities, decisions"],
   "Regular traction meetings, a traction map, metric reviews between sessions."),
  ("studio", "Revanite Studio", "Done-for-you marketing",
   "For small and mid-sized businesses in Kazakhstan and the CIS that need leads and sales, not just reach.",
   ["Strategy and media plan with payback modelling",
    "Google Ads (Search, App campaigns), Meta Ads, TikTok Ads",
    "Analytics setup: GA4, Google Tag Manager, Yandex Metrica, Meta Pixel and Conversions API",
    "Mobile attribution: AppsFlyer integrations with Google Ads and Meta",
    "End-to-end analytics: ads → website → CRM (amoCRM, Bitrix24) → sales",
    "Plan-vs-actual reporting and Looker Studio dashboards"],
   "Project-based or monthly retainer, with weekly reporting."),
  ("mentoring", "Teaching & mentoring", "For marketers and teams",
   "For marketers who want to move from running ads to managing growth, and for teams that need a shared method.",
   ["One-to-one track: digital marketing, analytics, AI tools",
    "Corporate workshops: go-to-market, growth hacking, lead generation and funnels",
    "Talks and guest lectures"],
   "One-to-one or group, in person in Almaty or online."),
 ],
}

CASES = {
 "ru": [
  ("Бизнес-форум, Астана: таргетированная реклама и аналитика воронки",
   "Ивенты · Meta Ads · amoCRM",
   "Продать билеты на бизнес-форум через Meta Ads и видеть, что происходит с заявками после клика.",
   ["Еженедельный разбор воронки amoCRM: статусы, каналы, эффективность менеджеров, доля квалифицированных заявок",
    "Аудит переписки менеджеров в WhatsApp: выявлены 4 повторяющихся типа ошибок, по итогам внедрён чат-бот",
    "Сведение данных Meta Ads и CRM в единую отчётность"],
   "Итоги запуска: 1 089 заявок с форм и сайта плюс 544 обращения в WhatsApp, ROAS 234%. Формат масштабирован на запуски в Шымкенте и Алматы."),
  ("Инвестиционное мобильное приложение, Казахстан: ноль установок в Meta",
   "Финтех · Мобильная атрибуция · AppsFlyer",
   "Кабинет Meta показывал 0 установок при расходе около $200, а AppsFlyer приписывал Facebook 34 установки на Android. Алгоритм оптимизировался вслепую.",
   ["Проверил цепочку от SDK до Events Manager: какие события доходят, какие пропали и когда",
    "Нашёл причину: постбэки AppsFlyer уходили на несуществующий Meta App ID",
    "Исправил связку, переподключил интеграцию расходов, зафиксировал правило: установки считаем по AppsFlyer, а не по данным кабинетов"],
   "Причина расхождения устранена, отчётность по нескольким продуктовым линиям приложения сведена в план-факт против медиаплана."),
  ("Производитель огнезащитных покрытий: B2B-стратегия",
   "B2B · Производство · Стратегия",
   "Вывести казахстанского производителя на рынок, где основной конкурент — импортный бренд.",
   ["Позиционирование: локальный производитель полного цикла — материал, нанесение, экспертное сопровождение, без задержек импорта",
    "География: промышленные и нефтегазовые регионы плюс поиск в Алматы и Астане",
    "5 портретов клиента; каналы: поиск Google и Яндекс, 2GIS, Instagram, ABM и тендеры",
    "Сознательное ограничение: продукт сертифицирован под стандартный пожарный режим, поэтому технологические объекты нефтегаза исключены из таргетинга, чтобы не покупать нецелевые заявки"],
   "Стратегия, медиаплан и контент-план переданы в работу."),
  ("Карта рассрочки, банк в Кыргызстане",
   "Финтех · Google Ads · Meta Ads",
   "Запуск и ведение платного трафика на BNPL-продукт банка.",
   ["Структура кампаний Google Ads, сборка через Google Ads Editor",
    "Лид-кампании Meta Ads и ежемесячная отчётность по стоимости результата",
    "Интеграция Facebook SDK в приложение и связка AppsFlyer с Google Ads"],
   "Рекламная инфраструктура и отчётность работают на постоянной основе."),
  ("Магистратура по психологии: сквозная атрибуция",
   "Образование · CRM · Автоматизация",
   "Понять, какая реклама приводит студентов, когда заявки приходят в WhatsApp и теряют источник.",
   ["Атрибуция заявок к рекламе через сопоставление первого сообщения в WhatsApp",
    "Автоматизация выгрузок amoCRM и Bitrix24 через API и Google Apps Script",
    "Сценарии видеорекламы под разные мотивы поступающих"],
   "Источник заявки виден в CRM, отчётность по Meta Ads связана с продажами."),
  ("Трекинг онлайн-образовательного проекта",
   "Трекинг · Стратегия рынков",
   "Команда планировала выход на рынок США.",
   ["Анализ продаж показал: международная выручка идёт от русскоязычной диаспоры, а не от иноязычных рынков",
    "Приоритет сменён с США на Узбекистан и Турцию",
    "Найден недоиспользованный канал: партнёрская программа уже давала около 30% выручки"],
   "Команда перераспределила ресурсы на рынки и каналы с подтверждённым спросом."),
 ],
 "en": [
  ("Business forum, Astana: paid social and funnel analytics",
   "Events · Meta Ads · amoCRM",
   "Sell tickets to a business forum via Meta Ads and see what happens to leads after the click.",
   ["Weekly amoCRM funnel review: stages, channels, sales rep performance, qualified-lead share",
    "Audit of sales reps' WhatsApp conversations: 4 recurring failure types found, leading to a chatbot rollout",
    "Meta Ads and CRM data merged into one reporting view"],
   "Launch results: 1,089 form and website leads plus 544 WhatsApp conversations, 234% ROAS. The format was scaled to launches in Shymkent and Almaty."),
  ("Investment mobile app, Kazakhstan: zero installs in Meta",
   "Fintech · Mobile attribution · AppsFlyer",
   "Meta Ads Manager reported 0 installs on roughly $200 spend, while AppsFlyer attributed 34 Android installs to Facebook. The algorithm was optimising blind.",
   ["Traced the chain from SDK to Events Manager: which events arrived, which stopped and when",
    "Found the root cause: AppsFlyer postbacks were going to a non-existent Meta App ID",
    "Fixed the integration, reconnected cost sync, set the rule: installs are counted in AppsFlyer, not in ad dashboards"],
   "Discrepancy resolved; reporting for several product lines consolidated into plan-vs-actual against the media plan."),
  ("Fire-retardant coatings manufacturer: B2B strategy",
   "B2B · Manufacturing · Strategy",
   "Position a Kazakhstan manufacturer in a market led by an imported brand.",
   ["Positioning: local full-cycle producer — material, application and expert support, no import delays",
    "Geography: industrial and oil & gas regions plus search in Almaty and Astana",
    "5 buyer personas; channels: Google and Yandex search, 2GIS, Instagram, ABM and tenders",
    "Deliberate constraint: the product is certified for the standard fire curve, so oil & gas process facilities were excluded from targeting to avoid paying for unqualified leads"],
   "Strategy, media plan and content plan handed over for execution."),
  ("Instalment card, bank in Kyrgyzstan",
   "Fintech · Google Ads · Meta Ads",
   "Launch and run paid traffic for a bank's BNPL product.",
   ["Google Ads account structure built via Google Ads Editor",
    "Meta lead campaigns with monthly cost-per-result reporting",
    "Facebook SDK integration in the app and AppsFlyer–Google Ads linking"],
   "Ad infrastructure and reporting run on an ongoing basis."),
  ("Psychology master's programme: end-to-end attribution",
   "Education · CRM · Automation",
   "Identify which ads bring students when leads arrive via WhatsApp and lose their source.",
   ["Lead-to-ad attribution by matching the first WhatsApp message",
    "amoCRM and Bitrix24 exports automated via API and Google Apps Script",
    "Video ad scripts for different applicant motivations"],
   "Lead source is visible in the CRM; Meta Ads reporting is tied to enrolments."),
  ("Tracking an online education project",
   "Tracking · Market strategy",
   "The team planned to expand into the US.",
   ["Sales analysis showed international revenue came from the Russian-speaking diaspora, not foreign-language markets",
    "Priority shifted from the US to Uzbekistan and Turkey",
    "Under-used channel found: the affiliate programme already drove about 30% of revenue"],
   "The team reallocated resources to markets and channels with proven demand."),
 ],
}

TEACH = {
 "ru": [
  ("Almaty Management University (AlmaU)", "Преподаватель с 2022 года",
   ["Веб-аналитика", "Цифровой маркетинг", "SMM и социальные сети", "Инструменты интернет-маркетинга",
    "Автор программ курсов «AI в маркетинге» и «SEO-оптимизация и веб-аналитика»"]),
  ("Qamalladin University", "Руководитель направления «Диджитал»",
   ["Управление маркетинговыми проектами", "Лидогенерация и оптимизация воронки продаж"]),
  ("Колледж ICB", "Преподаватель", []),
  ("Astana Hub", "Воркшопы",
   ["Go-to-market и первые шаги привлечения клиентов в AI, цифровых и традиционных продуктах",
    "Growth hacking", "Лидогенерация и воронки продаж"]),
  ("Nazarbayev University", "Гостевая лекция", ["Основы маркетинга и его роль в современном мире"]),
  ("Акселераторы и IT-хабы", "Трекер стартапов",
   ["Astana Hub, Almaty Hub, Terricon Valley, NURIS, IT Park", "AIpreneurs — линейный трекер"]),
 ],
 "en": [
  ("Almaty Management University (AlmaU)", "Lecturer since 2022",
   ["Web analytics", "Digital marketing", "SMM and social media", "Online marketing tools",
    "Author of the course programmes “AI in Marketing” and “SEO and Web Analytics”"]),
  ("Qamalladin University", "Head of the Digital programme",
   ["Marketing project management", "Lead generation and sales funnel optimisation"]),
  ("ICB college", "Instructor", []),
  ("Astana Hub", "Workshops",
   ["Go-to-market and first customer acquisition for AI, digital and traditional products",
    "Growth hacking", "Lead generation and sales funnels"]),
  ("Nazarbayev University", "Guest lecture", ["Fundamentals of marketing and its role in the modern world"]),
  ("Accelerators and tech hubs", "Startup tracker",
   ["Astana Hub, Almaty Hub, Terricon Valley, NURIS, IT Park", "AIpreneurs — line tracker"]),
 ],
}

AI_COURSE = {
 "ru": ("Курс «AI в маркетинге»", ["AI в маркетинге без мифов: типы моделей, LLM, промптинг, инструменты",
        "AI, SEO и GEO: оптимизация под поисковики и генеративные ответы",
        "AI в маркетинговой аналитике и прогнозировании",
        "Сквозная аналитика: реклама → сайт → CRM → продажи, расчёт ROAS и CAC",
        "Vibe coding: от исследования конкурентов до живого сайта",
        "Маркетинговая воронка: построение и стресс-тест с помощью AI"]),
 "en": ("“AI in Marketing” course", ["AI in marketing demystified: model types, LLMs, prompting, tools",
        "AI, SEO and GEO: optimising for search engines and generative answers",
        "AI in marketing analytics and forecasting",
        "End-to-end analytics: ads → website → CRM → sales, ROAS and CAC",
        "Vibe coding: from competitor research to a live website",
        "Marketing funnel: building and stress-testing it with AI"]),
}

META = {
 "ru": {
  "": ("Руслан Хасанов — growth-стратег, трекер стартапов, digital-маркетинг | Алматы",
       "Руслан Хасанов — маркетолог из Алматы: трекер стартапов в IT-хабах Казахстана, преподаватель AlmaU, основатель студии Revanite. Стратегия роста, performance-маркетинг и сквозная аналитика."),
  "about": ("Обо мне — Руслан Хасанов",
            "Биография Руслана Хасанова: опыт в Alfa Bank, Home Credit Bank, Halyk Insurance, Samsung Kazakhstan, re:Kassa; трекинг стартапов, преподавание в AlmaU, студия Revanite."),
  "services": ("Услуги: трекинг, маркетинг под ключ, менторство — Руслан Хасанов",
               "Revanite Tracking, Revanite Studio и менторство: стратегия роста, Google Ads и Meta Ads, сквозная аналитика, атрибуция и обучение маркетологов."),
  "cases": ("Кейсы — Руслан Хасанов, Revanite",
            "Кейсы Руслана Хасанова: аналитика воронки бизнес-форума с ROAS 234%, мобильная атрибуция финтех-приложения, B2B-стратегия производителя, трекинг стартапов."),
  "teaching": ("Преподавание и выступления — Руслан Хасанов",
               "Руслан Хасанов преподаёт digital-маркетинг в AlmaU, руководит направлением «Диджитал» в Qamalladin University, проводит воркшопы в Astana Hub."),
  "contact": ("Контакты — Руслан Хасанов, Revanite",
              "Как связаться с Русланом Хасановым: Telegram @messer66, WhatsApp и телефон +7 701 458 42 42, Instagram, LinkedIn. Алматы, Казахстан."),
 },
 "en": {
  "": ("Ruslan Khasanov — growth strategist, startup tracker, digital marketing | Almaty",
       "Ruslan Khasanov is a marketing specialist in Almaty: startup tracker at Kazakhstan tech hubs, AlmaU lecturer and founder of Revanite. Growth strategy, performance marketing and end-to-end analytics."),
  "about": ("About — Ruslan Khasanov",
            "Biography of Ruslan Khasanov: Alfa Bank, Home Credit Bank, Halyk Insurance, Samsung Kazakhstan, re:Kassa; startup tracking, lecturing at AlmaU, Revanite studio."),
  "services": ("Services: tracking, done-for-you marketing, mentoring — Ruslan Khasanov",
               "Revanite Tracking, Revanite Studio and mentoring: growth strategy, Google Ads and Meta Ads, end-to-end analytics, attribution and training for marketers."),
  "cases": ("Case studies — Ruslan Khasanov, Revanite",
            "Ruslan Khasanov's case studies: business forum funnel analytics with 234% ROAS, fintech app attribution, B2B manufacturer strategy, startup tracking."),
  "teaching": ("Teaching and talks — Ruslan Khasanov",
               "Ruslan Khasanov lectures in digital marketing at AlmaU, leads the Digital programme at Qamalladin University and runs workshops at Astana Hub."),
  "contact": ("Contact — Ruslan Khasanov, Revanite",
              "How to reach Ruslan Khasanov: Telegram @messer66, WhatsApp and phone +7 701 458 42 42, Instagram, LinkedIn. Almaty, Kazakhstan."),
 },
}

H1 = {
 "ru": {"about": "Руслан Хасанов: биография", "services": "Услуги", "cases": "Кейсы", "teaching": "Преподавание и выступления", "contact": "Контакты"},
 "en": {"about": "Ruslan Khasanov: biography", "services": "Services", "cases": "Case studies", "teaching": "Teaching and talks", "contact": "Contact"},
}

# ---------------------------------------------------------------- SCHEMA
def person(lang):
    t = T[lang]
    p = {
        "@type": "Person", "@id": BASE + "/#person",
        "name": t["name"],
        "alternateName": ["Руслан Хасанов", "Ruslan Khasanov", "Ruslan Khassanov", "Хасанов Руслан Фархадович", "Ruslan Farkhadovich Khasanov"],
        "givenName": "Руслан" if lang == "ru" else "Ruslan",
        "familyName": "Хасанов" if lang == "ru" else "Khasanov",
        "jobTitle": t["jobTitle"],
        "description": t["summary"],
        "url": url(lang, ""),
        "address": {"@type": "PostalAddress", "addressLocality": "Almaty", "addressCountry": "KZ"},
        "worksFor": [{"@id": BASE + "/#org"}],
        "affiliation": [
            {"@type": "CollegeOrUniversity", "name": "Almaty Management University (AlmaU)", "url": "https://almau.edu.kz"},
            {"@type": "CollegeOrUniversity", "name": "Qamalladin University"},
        ],
        "knowsAbout": KNOWS[lang],
        "knowsLanguage": ["ru", "en"],
        "sameAs": SAME_AS,
        "telephone": PHONE,
    }
    if PHOTO:
        p["image"] = PHOTO_URL
    return p

def org(lang):
    return {
        "@type": "ProfessionalService", "@id": BASE + "/#org",
        "name": "Revanite",
        "alternateName": ["Revanite Strategic Growth Studio", "Revanite Studio", "Revanite Tracking"],
        "slogan": "Маркетинг как вложение, а не расход." if lang == "ru" else "Marketing as an investment, not an expense.",
        "description": T[lang]["org_desc"],
        "url": BASE + "/",
        "logo": BASE + "/assets/logo.svg",
        "founder": {"@id": BASE + "/#person"},
        "address": {"@type": "PostalAddress", "addressLocality": "Almaty", "addressCountry": "KZ"},
        "areaServed": ["KZ", "KG", "UZ", "CIS"],
        "telephone": PHONE,
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "contactType": "sales",
                         "availableLanguage": ["ru", "en"], "url": WA},
    }

def website(lang):
    return {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
            "name": T[lang]["name"], "inLanguage": ["ru", "en"], "publisher": {"@id": BASE + "/#person"}}

def breadcrumbs(lang, slug, title):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": T[lang]["home"], "item": url(lang, "")},
        {"@type": "ListItem", "position": 2, "name": title, "item": url(lang, slug)}]}

def schema(lang, slug):
    title, desc = META[lang][slug]
    page_type = {"": "WebPage", "about": "ProfilePage", "services": "WebPage", "cases": "CollectionPage", "teaching": "WebPage", "contact": "ContactPage"}[slug]
    page = {"@type": page_type, "@id": url(lang, slug) + "#webpage", "url": url(lang, slug), "name": title,
            "description": desc, "inLanguage": lang, "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@id": BASE + "/#person"}, "dateModified": TODAY}
    if slug == "about":
        page["mainEntity"] = {"@id": BASE + "/#person"}
    graph = [person(lang), org(lang), website(lang), page]
    if slug:
        graph.append(breadcrumbs(lang, slug, H1[lang][slug]))
    if slug == "":
        graph.append({"@type": "FAQPage", "@id": url(lang, "") + "#faq", "inLanguage": lang,
                      "mainEntity": [{"@type": "Question", "name": q,
                                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]})
    if slug == "services":
        for key, name, sub, who, items, fmt in SERVICES[lang]:
            graph.append({"@type": "Service", "@id": url(lang, "services") + "#" + key, "name": f"{name} — {sub}",
                          "description": who + " " + "; ".join(items) + ".", "provider": {"@id": BASE + "/#org"},
                          "areaServed": ["KZ", "CIS"]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- HTML
LOGO = ('<svg class="logo" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M10 26V6h7.5a5 5 0 0 1 0 10H10"/><path d="M15.5 16 22 26"/>'
        '<path d="M4 29 28 3" stroke="#5B82C9" stroke-width="1.2"/></svg>')

CSS = """
:root{--bg:#0E1014;--surface:#151920;--line:#252B34;--text:#ECEEF1;--muted:#9BA3AF;--accent:#5B82C9;--max:1040px}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--text);font:400 17px/1.65 Manrope,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:inherit}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(14,16,20,.92);backdrop-filter:blur(8px);z-index:5}
.bar{display:flex;align-items:center;gap:20px;height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:600;white-space:nowrap}
.logo{width:28px;height:28px}
nav{display:flex;gap:18px;margin-left:auto;min-width:0;align-items:center;overflow-x:auto;scrollbar-width:none}
nav::-webkit-scrollbar{display:none}
nav a{text-decoration:none;color:var(--muted);font-size:15px;white-space:nowrap}
nav a:hover,nav a[aria-current]{color:var(--text)}
.lang{flex:none;text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:2px 8px;font-size:13px;color:var(--text)}
main section{padding:64px 0;border-bottom:1px solid var(--line)}
main section:last-child{border-bottom:0}
.eyebrow{color:var(--accent);font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px}
h1{font-size:clamp(40px,7vw,72px);line-height:1.05;font-weight:600;letter-spacing:-.02em}
.page h1{font-size:clamp(32px,5vw,48px)}
h2{font-size:clamp(24px,3.5vw,32px);font-weight:600;letter-spacing:-.01em;margin-bottom:24px}
h3{font-size:19px;font-weight:600;margin-bottom:8px}
p+p{margin-top:14px}
.lead{font-size:clamp(19px,2.4vw,23px);color:var(--muted);max-width:720px;margin-top:22px}
.hero{padding:88px 0 72px}
.hero-grid{display:grid;grid-template-columns:1fr auto;gap:40px;align-items:center}
.portrait{width:220px;height:260px;border-radius:14px;border:1px solid var(--line);background:var(--surface);object-fit:cover;display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:56px;font-weight:600;letter-spacing:.04em}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.btn{display:inline-block;padding:12px 22px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:15px}
.btn.ghost{background:transparent;border:1px solid var(--line);color:var(--text)}
.answer{font-size:19px;max-width:820px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:24px}
.card .tag{color:var(--accent);font-size:13px;margin-bottom:10px;display:block}
.card p{color:var(--muted);font-size:15px}
.card ul{margin-top:14px;padding-left:18px;color:var(--muted);font-size:15px}
.card li+li{margin-top:6px}
.exp{list-style:none}
.exp li{display:grid;grid-template-columns:220px 1fr;gap:20px;padding:16px 0;border-top:1px solid var(--line)}
.exp li:first-child{border-top:0}
.exp b{font-weight:600}
.exp span{color:var(--muted)}
.case{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:28px;margin-bottom:16px}
.case h2{font-size:22px;margin-bottom:6px}
.case .tag{color:var(--accent);font-size:13px;display:block;margin-bottom:16px}
.case h3{font-size:14px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin:18px 0 6px}
.case ul{padding-left:18px}
.case li+li{margin-top:6px}
.result{border-left:2px solid var(--accent);padding-left:14px}
.note{color:var(--muted);font-size:15px;margin-top:18px}
footer{border-top:1px solid var(--line);padding:64px 0 32px;background:var(--surface)}
.footer-title{font-size:clamp(26px,4vw,40px);margin-bottom:10px}
.footer-sub{color:var(--muted);margin-bottom:28px}
.copy{color:var(--muted);font-size:14px;margin-top:32px}
.socials{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}
.socials a{display:block;text-decoration:none;border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:var(--bg)}
.socials a:hover{border-color:var(--accent)}
.socials b{display:block;font-weight:600}
.socials span{color:var(--muted);font-size:14px;overflow-wrap:anywhere}
.role{color:var(--accent);font-size:clamp(16px,2vw,19px);margin-top:14px}
.section-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.section-head h2{margin-bottom:0}
.more{color:var(--accent);text-decoration:none;font-size:15px;white-space:nowrap}
.projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.project{border:1px solid var(--line);border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:10px}
.project .tag{color:var(--accent);font-size:13px}
.project h3{margin:0}
.project p{color:var(--muted);font-size:15px;flex:1}
.project a{color:var(--accent);text-decoration:none;font-size:15px}
.trust h2{font-size:15px;color:var(--muted);font-weight:400;letter-spacing:.08em;text-transform:uppercase}
.trust ul{list-style:none;display:flex;flex-wrap:wrap;gap:10px 28px}
.trust li{font-size:clamp(17px,2.2vw,21px);font-weight:600;letter-spacing:.01em}
.card-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:16px;font-size:15px}
.card-links a{color:var(--accent);text-decoration:none}
.knowledge{display:grid;grid-template-columns:1fr 1fr;gap:48px}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:8px}
.chips li{border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:14px}
.steps{padding-left:22px;color:var(--muted);font-size:15px}
.steps li+li{margin-top:8px}.steps b{color:var(--text);font-weight:600}
.rows{list-style:none}
.rows li{display:grid;grid-template-columns:220px 1fr;gap:20px;padding:18px 0;border-top:1px solid var(--line)}
.rows li:first-child{border-top:0}
.rows .when{color:var(--accent);font-size:14px;padding-top:3px}
.rows h3{margin-bottom:4px}.rows p{color:var(--muted);font-size:15px}
details summary{cursor:pointer;list-style:none}
details summary::-webkit-details-marker{display:none}
.more-box summary{color:var(--accent);font-size:15px;margin-top:12px}
.more-box[open] summary{margin-bottom:4px}
.qa{border-top:1px solid var(--line);padding:18px 0}
.qa summary{font-weight:600;font-size:18px;display:flex;justify-content:space-between;gap:16px}
.qa summary::after{content:"+";color:var(--accent)}
.qa[open] summary::after{content:"−"}
.qa p{color:var(--muted);margin-top:10px;max-width:820px}
.crumbs{font-size:14px;color:var(--muted);margin-bottom:18px}
.crumbs a{text-decoration:none}
@media (max-width:760px){
 body{font-size:16px}
 .bar{gap:8px}.brand span{display:none}
 nav{gap:10px}nav a{font-size:13px}nav .nav-home{display:none}
 .hero{padding:56px 0 48px}
 .hero-grid{grid-template-columns:1fr}
 .portrait{width:120px;height:140px;font-size:32px;order:-1}
 main section{padding:48px 0}
 .exp li,.rows li{grid-template-columns:1fr;gap:2px}
 .knowledge{grid-template-columns:1fr;gap:40px}
}
"""

def portrait(lang):
    alt = T[lang]["name"]
    if PHOTO:
        return f'<img class="portrait" src="/assets/ruslan-khasanov.jpg" alt="{alt}" width="220" height="260">'
    return f'<div class="portrait" role="img" aria-label="{alt}">{"РХ" if lang=="ru" else "RK"}</div>'

def head(title, link=None, label=None):
    more = f'<a class="more" href="{link}">{label} →</a>' if link else ""
    return f'<div class="section-head"><h2>{title}</h2>{more}</div>'

def social_list(lang):
    out = []
    for name, handle, href in socials(lang):
        ext = "" if href.startswith("tel:") else ' rel="me noopener" target="_blank"'
        out.append(f'<li><a href="{href}"{ext}><b>{name}</b><span>{handle}</span></a></li>')
    return '<ul class="socials">' + "".join(out) + "</ul>"

def body_home(lang):
    t = T[lang]
    ru = lang == "ru"
    lead = ("Нахожу точки роста в бизнесе. Дальше — делаю сам, учу команду или помогаю принять решение."
            if ru else "I find where a business can grow. Then I either do the work, teach the team, or help make the call.")
    cta = "Обсудить задачу" if ru else "Discuss your project"
    projects = "".join(
        f'<article class="project"><span class="tag">{CASES[lang][i][1]}</span><h3>{CASES[lang][i][0]}</h3>'
        f'<p>{CASES[lang][i][4]}</p><a href="{path(lang,"cases")}#case-{i+1}">{"Открыть кейс" if ru else "Open case"} →</a></article>'
        for i in FEATURED)
    trust = "".join(f"<li>{c}</li>" for c in TRUST)
    services = "".join(
        f'<article class="card"><span class="tag">{name}</span><h3>{sub}</h3><p>{who}</p>'
        f'<p class="card-links"><a href="{WA}" rel="noopener" target="_blank">{cta}</a>'
        f'<a href="{path(lang,"services")}#{key}">{"Подробнее" if ru else "Details"} →</a></p></article>'
        for key, name, sub, who, items, fmt in SERVICES[lang])
    chips = "".join(f"<li>{k}</li>" for k in KNOWS[lang])
    formula = "".join(f"<li><b>{a}</b> — {b}</li>" for a, b in FORMULA[lang])
    teach = "".join(
        f'<li><span class="when">{role}</span><div><h3>{place}</h3>'
        + (f'<p>{"; ".join(items)}.</p>' if items else "") + "</div></li>"
        for place, role, items in TEACH[lang])
    rows = [f"<li><b>{a}</b><span>{b}</span></li>" for a, b in EXPERIENCE[lang]]
    exp = ('<ul class="exp">' + "".join(rows[:4]) + "</ul>"
           f'<details class="more-box"><summary>{"Показать ещё опыт" if ru else "Show more experience"}</summary>'
           '<ul class="exp">' + "".join(rows[4:]) + "</ul></details>")
    faq = "".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ[lang])
    return f"""
<section class="hero"><div class="hero-grid"><div>
<h1>{t["name"]}</h1>
<p class="role">{t["role"]}</p>
<p class="lead">{lead}</p>
<div class="cta"><a class="btn" href="{WA}" rel="noopener" target="_blank">{cta}</a><a class="btn ghost" href="{TG}" rel="me noopener" target="_blank">Telegram</a></div>
</div>{portrait(lang)}</div></section>
<section>{head("Избранные кейсы" if ru else "Selected case studies", path(lang,"cases"), "Все кейсы" if ru else "All case studies")}<div class="projects">{projects}</div></section>
<section class="trust"><h2>{"Мне доверяют" if ru else "Trusted by"}</h2><ul>{trust}</ul></section>
<section>{head("Чем могу помочь" if ru else "How I can help")}<div class="cards">{services}</div></section>
<section><h2>{"Обо мне" if ru else "About me"}</h2><p class="answer">{t["summary"]}</p>
<p class="card-links"><a href="{path(lang,"about")}">{"Подробная биография" if ru else "Full biography"} →</a><a href="{IG}" rel="me noopener" target="_blank">Instagram</a><a href="{LI}" rel="me noopener" target="_blank">LinkedIn</a></p></section>
<section><div class="knowledge">
<div><h2>{"Навыки" if ru else "Skills"}</h2><ul class="chips">{chips}</ul></div>
<div><h2>{"Метод: Revanite Growth Formula" if ru else "Method: Revanite Growth Formula"}</h2><ol class="steps">{formula}</ol></div>
</div></section>
<section>{head("Преподавание и выступления" if ru else "Teaching and talks", path(lang,"teaching"), "Подробнее" if ru else "Details")}<ul class="rows">{teach}</ul></section>
<section>{head("Опыт работы" if ru else "Work experience", path(lang,"about"), "Биография" if ru else "Biography")}{exp}</section>
<section id="faq">{head("Частые вопросы" if ru else "FAQ")}{faq}</section>"""

def body_contact(lang):
    ru = lang == "ru"
    lead = ("Напишите в Telegram или WhatsApp: коротко о бизнесе и задаче. Отвечу и предложу формат работы."
            if ru else "Message me on Telegram or WhatsApp with a short note about your business and the challenge. I will reply with a suggested format.")
    note = ("Алматы, Казахстан. Работаю с клиентами в Казахстане, СНГ и онлайн."
            if ru else "Almaty, Kazakhstan. Working with clients across Kazakhstan, the CIS and online.")
    return f"""
<section class="page">{crumbs(lang,"contact")}<h1>{H1[lang]["contact"]}</h1><p class="lead">{lead}</p></section>
<section>{social_list(lang)}<p class="note">{note}</p></section>"""

def crumbs(lang, slug):
    return f'<p class="crumbs"><a href="{path(lang,"")}">{T[lang]["home"]}</a> / {H1[lang][slug]}</p>'

def body_about(lang):
    ru = lang == "ru"
    t = T[lang]
    exp = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in EXPERIENCE[lang])
    if ru:
        bio = """<p>Руслан Хасанов — маркетолог и growth-стратег из Алматы. Вырос из корпоративного маркетинга в финансовом секторе: руководил маркетингом сегмента малого бизнеса в Alfa Bank, digital-маркетингом в Home Credit Bank, отвечал за продукт в Halyk Insurance. Участвовал в запуске онлайн-магазина Samsung Kazakhstan.</p>
<p>Сейчас работает по четырём связанным направлениям. Трекинг: помогает стартапам в Astana Hub, Almaty Hub, Terricon Valley, NURIS и IT Park найти точки роста, проверить гипотезы и получить первых клиентов. Исполнение: через студию Revanite ведёт рекламу, аналитику и стратегию для малого и среднего бизнеса в Казахстане и СНГ. Преподавание: учит digital-маркетингу в AlmaU, Qamalladin University и колледже ICB. Работа в продукте: руководит digital-маркетингом фискальной платформы re:Kassa.</p>
<p>Общее у всех направлений — подход трекера: сначала найти, где на самом деле теряется рост, и только потом решать, что делать. Отсюда принцип Revanite: маркетинг как вложение, а не расход. Каждый канал должен окупаться и быть измеримым — от клика до оплаты в CRM.</p>"""
        names = "Как пишется имя"
        names_p = "Руслан Хасанов (полное имя — Хасанов Руслан Фархадович). Латиницей — Ruslan Khasanov; в LinkedIn используется написание Ruslan Khassanov."
    else:
        bio = """<p>Ruslan Khasanov is a marketing specialist and growth strategist based in Almaty, Kazakhstan. He came up through corporate marketing in financial services: he led small business marketing at Alfa Bank, digital marketing at Home Credit Bank and product at Halyk Insurance, and was part of the team that launched Samsung Kazakhstan's online store.</p>
<p>Today his work spans four connected lines. Tracking: he helps startups at Astana Hub, Almaty Hub, Terricon Valley, NURIS and IT Park find growth points, test hypotheses and land first customers. Execution: through his studio Revanite he runs advertising, analytics and strategy for small and mid-sized businesses across Kazakhstan and the CIS. Teaching: he lectures in digital marketing at AlmaU, Qamalladin University and ICB college. In-house: he heads digital marketing at the fiscal technology platform re:Kassa.</p>
<p>What ties it together is a tracker's approach: first find where growth is actually being lost, then decide what to do. Hence Revanite's principle — marketing as an investment, not an expense. Every channel has to pay back and be measurable, from click to paid deal in the CRM.</p>"""
        names = "Name spelling"
        names_p = "Ruslan Khasanov (Russian: Руслан Хасанов; full name Хасанов Руслан Фархадович). LinkedIn uses the spelling Ruslan Khassanov."
    kn = ", ".join(KNOWS[lang])
    return f"""
<section class="page">{crumbs(lang,"about")}<h1>{H1[lang]["about"]}</h1><p class="lead">{t["role"]}</p></section>
<section>{bio}</section>
<section><h2>{"Опыт" if ru else "Experience"}</h2><ul class="exp">{exp}</ul></section>
<section><h2>{"Компетенции" if ru else "Expertise"}</h2><p>{kn}</p></section>
<section><h2>{names}</h2><p>{names_p}</p></section>"""

def body_services(lang):
    ru = lang == "ru"
    out = [f'<section class="page">{crumbs(lang,"services")}<h1>{H1[lang]["services"]}</h1>'
           f'<p class="lead">{"Три формата работы — от диагностики до исполнения и обучения." if ru else "Three formats — from diagnosis to execution and training."}</p></section>']
    for key, name, sub, who, items, fmt in SERVICES[lang]:
        li = "".join(f"<li>{i}</li>" for i in items)
        out.append(f'<section id="{key}"><p class="eyebrow">{name}</p><h2>{sub}</h2><p>{who}</p>'
                   f'<div class="card" style="margin-top:20px"><h3>{"Что входит" if ru else "What is included"}</h3><ul>{li}</ul>'
                   f'<p style="margin-top:14px"><b>{"Формат" if ru else "Format"}:</b> {fmt}</p></div></section>')
    return "".join(out)

def body_cases(lang):
    ru = lang == "ru"
    intro = ("Среди клиентов — BI GROUP, Yeko, Jintropine. В кейсах ниже названия не раскрываются без согласия клиента: описаны задача, решение и результат."
             if ru else "Clients include BI GROUP, Yeko and Jintropine. The cases below do not name clients without consent; each covers the task, the solution and the outcome.")
    out = [f'<section class="page">{crumbs(lang,"cases")}<h1>{H1[lang]["cases"]}</h1><p class="lead">{intro}</p></section><section>']
    for n, (title, tag, task, done, result) in enumerate(CASES[lang], 1):
        li = "".join(f"<li>{d}</li>" for d in done)
        out.append(f'<article class="case" id="case-{n}"><h2>{title}</h2><span class="tag">{tag}</span>'
                   f'<h3>{"Задача" if ru else "Task"}</h3><p>{task}</p>'
                   f'<h3>{"Что сделано" if ru else "What was done"}</h3><ul>{li}</ul>'
                   f'<h3>{"Результат" if ru else "Outcome"}</h3><p class="result">{result}</p></article>')
    out.append("</section>")
    return "".join(out)

def body_teaching(lang):
    ru = lang == "ru"
    cards = ""
    for place, role, items in TEACH[lang]:
        li = "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>" if items else ""
        cards += f'<article class="card"><span class="tag">{role}</span><h3>{place}</h3>{li}</article>'
    ctitle, citems = AI_COURSE[lang]
    cli = "".join(f"<li>{i}</li>" for i in citems)
    lead = ("Преподаёт digital-маркетинг в университетах Алматы и проводит воркшопы для стартапов."
            if ru else "Teaches digital marketing at Almaty universities and runs workshops for startups.")
    return f"""
<section class="page">{crumbs(lang,"teaching")}<h1>{H1[lang]["teaching"]}</h1><p class="lead">{lead}</p></section>
<section><div class="cards">{cards}</div></section>
<section><h2>{ctitle}</h2><p>{"Авторская программа для AlmaU: от основ LLM до сквозной аналитики и создания сайта с AI. Практические задания построены так, чтобы студент сначала делал работу руками, а потом проверял её с помощью AI." if ru else "An original programme for AlmaU, from LLM basics to end-to-end analytics and building a website with AI. Assignments require students to do the work by hand first and then check it with AI."}</p>
<div class="card" style="margin-top:20px"><ol style="padding-left:20px">{cli}</ol></div></section>"""

BODIES = {"": body_home, "about": body_about, "services": body_services, "cases": body_cases, "teaching": body_teaching, "contact": body_contact}

def render(lang, slug):
    t = T[lang]
    title, desc = META[lang][slug]
    other = "en" if lang == "ru" else "ru"
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{path(lang,s)}"{cur if s == slug else ""}{"" if s else ' class="nav-home"'}>{t["nav"][s]}</a>'
        for s in NAV)
    og_img = f'<meta property="og:image" content="{PHOTO_URL}">' if PHOTO else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{t["name"]}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url(lang,slug)}">
<link rel="alternate" hreflang="ru" href="{url("ru",slug)}">
<link rel="alternate" hreflang="en" href="{url("en",slug)}">
<link rel="alternate" hreflang="x-default" href="{url("ru",slug)}">
<link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt">
<meta property="og:type" content="{"profile" if slug in ("", "about") else "website"}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url(lang,slug)}">
<meta property="og:locale" content="{"ru_RU" if lang=="ru" else "en_US"}">
<meta property="og:site_name" content="{t["name"]}">
{og_img}
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0E1014">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap&subset=cyrillic" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">
{schema(lang,slug)}
</script>
</head>
<body>
<header><div class="wrap bar">
<a class="brand" href="{path(lang,"")}">{LOGO}<span>Revanite</span></a>
<nav aria-label="{"Основное меню" if lang=="ru" else "Main menu"}">{nav}</nav><a class="lang" href="{path(other,slug)}" hreflang="{other}" lang="{other}" title="{t["switch"][1]}">{t["switch"][0]}</a>
</div></header>
<main class="wrap">{BODIES[slug](lang)}</main>
<footer id="contact"><div class="wrap">
<h2 class="footer-title">{"Маркетинг как вложение, а не расход." if lang=="ru" else "Marketing as an investment, not an expense."}</h2>
<p class="footer-sub">{"Живу в Алматы, работаю с клиентами в Казахстане и СНГ." if lang=="ru" else "Based in Almaty, working with clients across Kazakhstan and the CIS."}</p>
{social_list(lang)}
<p class="copy">© {datetime.date.today().year} {t["footer"]}</p>
</div></footer>
</body>
</html>
"""

# ---------------------------------------------------------------- EXTRA FILES
def llms_txt():
    ru, en = T["ru"], T["en"]
    lines = [
        "# Руслан Хасанов (Ruslan Khasanov)",
        "",
        f"> {ru['summary']}",
        "",
        f"> {en['summary']}",
        "",
        "## Ключевые факты / Key facts",
        "- Имя: Руслан Хасанов (Хасанов Руслан Фархадович); латиницей Ruslan Khasanov, в LinkedIn — Ruslan Khassanov",
        "- Город: Алматы, Казахстан / Almaty, Kazakhstan",
        "- Роль: growth-стратег, трекер стартапов, преподаватель digital-маркетинга, основатель Revanite",
        "- Revanite — студия стратегического роста: Revanite Tracking (трекинг и консалтинг), Revanite Studio (маркетинг под ключ). Принцип: маркетинг как вложение, а не расход",
        "- Метод: Revanite Growth Formula — Инсайт → Экономика → Стратегия → Гипотезы → Исполнение → Аналитика → Масштаб",
        "- Трекер стартапов: Astana Hub, Almaty Hub, Terricon Valley, NURIS, IT Park; акселератор AIpreneurs",
        "- Преподавание: Almaty Management University (AlmaU), Qamalladin University (руководитель направления «Диджитал»), колледж ICB; воркшопы Astana Hub; гостевая лекция Nazarbayev University",
        "- Опыт: Alfa Bank (тимлид маркетинга, малый бизнес), Home Credit Bank (руководитель digital-маркетинга), Halyk Insurance (директор по продукту), Samsung Kazakhstan (запуск онлайн-магазина), BI GROUP (менеджер по маркетинговым проектам), re:Kassa (руководитель digital-маркетинга)",
        "- Клиенты: " + ", ".join(CLIENTS),
        "- Компетенции: " + ", ".join(KNOWS["ru"]),
        "",
        "## Страницы / Pages",
    ]
    for s in PAGES:
        lines.append(f"- [{META['ru'][s][0]}]({url('ru', s)}): {META['ru'][s][1]}")
    for s in PAGES:
        lines.append(f"- [{META['en'][s][0]}]({url('en', s)}): {META['en'][s][1]}")
    lines += ["", "## Профили / Profiles", f"- Instagram: {IG}", f"- LinkedIn: {LI}", f"- Telegram: {TG}", "", "## Контакты / Contact", f"- WhatsApp / телефон: {PHONE_H} ({WA})", "- Telegram: @messer66", ""]
    return "\n".join(lines)

def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot",
            "Perplexity-User", "Google-Extended", "Applebot-Extended", "YandexBot", "Bingbot", "CCBot"]
    out = ["User-agent: *", "Allow: /", ""]
    for b in bots:
        out += [f"User-agent: {b}", "Allow: /", ""]
    out.append(f"Sitemap: {BASE}/sitemap.xml")
    return "\n".join(out) + "\n"

def sitemap():
    items = []
    for lang in ("ru", "en"):
        for s in PAGES:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l,s)}"/>' for l in ("ru", "en"))
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("ru",s)}"/>'
            items.append(f"<url><loc>{url(lang,s)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(items) + "\n</urlset>\n")

def page404():
    return render("ru", "").replace("<title>", "<title>404 · ", 1).replace(
        '<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex">')

LOGO_FILE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0E1014"/>'
             '<g fill="none" stroke="#ECEEF1" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M10 26V6h7.5a5 5 0 0 1 0 10H10"/><path d="M15.5 16 22 26"/></g>'
             '<path d="M4 29 28 3" stroke="#5B82C9" stroke-width="1.2" stroke-linecap="round"/></svg>')

def write(p, content):
    full = os.path.join(OUT, p.lstrip("/"))
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    for lang in ("ru", "en"):
        for s in PAGES:
            write(path(lang, s) + "index.html", render(lang, s))
    write("/llms.txt", llms_txt())
    write("/robots.txt", robots())
    write("/sitemap.xml", sitemap())
    write("/404.html", page404())
    write("/assets/logo.svg", LOGO_FILE)
    if PHOTO:
        shutil.copy("site_src/ruslan-khasanov.jpg", os.path.join(OUT, "assets/ruslan-khasanov.jpg"))
    print("built", OUT, "photo:", PHOTO)
