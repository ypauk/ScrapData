# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `app/scraper.py`.

Не меняй другие файлы. Не создавай новые папки.

---

# ПРАВИЛА

ПРАВИЛА РАЗРАБОТКИ

1. Всегда использовать starter-project.

2. Не менять структуру каталогов.

3. Не создавать новые папки без необходимости.

4. Не писать код, который не требуется клиентом.

5. Предпочитать простое решение сложному.

6. Сначала искать API.

7. Если API нет — рассматривать requests + BeautifulSoup.

8. Playwright использовать только при необходимости.

9. Код должен быть модульным.

10. Docker создавать только после успешного локального запуска.

---

# КОНТЕКСТ ПРОЕКТА

## Анализ (этап 1)

1. Краткое описание задачи

Клиент хочет однократно собрать данные только со страницы №2 результатов поиска AUTO.RIA:

https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page=2

Необходимо получить список автомобилей и сохранить его в CSV.

Для каждого объявления нужно собрать:

URL изображения;
название автомобиля;
цену;
тип топлива;
город.

Уровень уверенности: высокий (≈99%).

2. Какой конечный результат нужен

Формат результата:

CSV.

Поля:

Image URL;
Car Name;
Price;
Fuel Type;
City.

Это одноразовая задача, без необходимости периодического парсинга.

Уровень уверенности: высокий.

3. Как лучше решить задачу
Рекомендуемый вариант

Python + requests + BeautifulSoup

Почему

Из предоставленного HTML видно, что все необходимые данные уже присутствуют в разметке страницы:

название автомобиля;
цена;
изображение;
тип топлива;
город.

Следовательно, нет признаков того, что для получения этих данных требуется выполнение JavaScript.

Для одноразового сбора одной страницы полноценный браузер является избыточным.

Уровень уверенности: высокий (≈95%).

4. Почему остальные варианты хуже
Playwright

Не рекомендуется.

Причина:

значительно медленнее;
сложнее;
не дает преимуществ, если HTML уже содержит нужные данные.
Selenium

Не рекомендуется.

Причины:

тяжелее;
менее стабилен;
не нужен для данной задачи.
Scrapy

Не рекомендуется.

Причина:

проект слишком маленький;
настройка Scrapy не оправдана ради одной страницы.
API

Пока рекомендовать нельзя.

Причина:

network.har пустой;
наличие внутреннего API не подтверждено.
5. Анализ сайта

На основании предоставленных материалов.

Возможность	Статус
JavaScript Rendering	Частично используется, но необходимые данные уже есть в HTML
React	Определить невозможно
Vue	Определить невозможно
Angular	Определить невозможно
API	Не подтверждено
GraphQL	Не подтверждено
Infinite Scroll	Нет
Pagination	Да
Login	Нет
Cookies	Не требуются (cookies.json пустой)
JWT	Не обнаружен
Bearer Token	Не обнаружен
CAPTCHA	Не обнаружена
Cloudflare	Не подтвержден
Rate Limits	Неизвестно
Download Files	Нет
Upload Files	Нет
Lazy Loading	Частично (изображения через <picture>)
WebSocket	Не обнаружен
XHR / Fetch	Не удалось определить
Sitemap	Не проверялся
robots.txt	Не проверялся

Уровень уверенности: средний (≈75%), поскольку отсутствует HAR.

6. Что необходимо собрать до начала разработки

Для данной задачи дополнительная информация практически не требуется.

Полезно иметь:

пример ожидаемого CSV (не обязательно);
network.har (если HTML внезапно окажется неполным).

На текущий момент имеющегося HTML достаточно для выбора стратегии.

7. Возможные сложности

Возможные риски:

изменение HTML-разметки;
изменение CSS-классов;
временные ограничения сайта по частоте запросов;
возможное появление антибот-защиты в будущем.

Для одной страницы вероятность возникновения проблем невысока.

8. Что нужно уточнить у клиента

Информации в целом достаточно.

При желании можно уточнить:

Нужно ли сохранять цену только в долларах или вместе с гривной?
Нужно ли сохранять абсолютный URL изображения (как в HTML)?
Нужно ли включать заголовок (header) в CSV?
Какая кодировка CSV предпочтительна (UTF-8 обычно подходит)?

Без ответов на эти вопросы разработку также можно выполнить.

9. Рекомендуемый стек технологий
Python
requests
BeautifulSoup
10. План разработки
Этап 1. Получение страницы

Цель

Получить HTML страницы №2.

Результат

Исходный HTML страницы.

Зависимости

Нет.

Этап 2. Извлечение данных

Цель

Получить:

URL изображения;
название;
цену;
тип топлива;
город.

Результат

Структурированный список автомобилей.

Зависимости

HTML страницы.

Этап 3. Экспорт

Цель

Сохранить данные.

Результат

CSV-файл.

Зависимости

Успешный парсинг данных.

11. Оценка сложности
Параметр	Оценка
Сложность	2/10
Estimation	0.5–1.5 часа
Вероятность блокировок	Низкая
Вероятность необходимости браузера	Низкая (~10%)
Вероятность изменения сайта	Средняя
Общий риск	Низкий
12. Можно ли решить проще

Да.

Самое простое решение:

requests → BeautifulSoup → CSV

Использование браузера (Playwright/Selenium) не выглядит оправданным для данной задачи.

Если бы в network.har обнаружился внутренний API, его стоило бы предпочесть HTML-парсингу. Однако предоставленный network.har пуст, поэтому оснований рекомендовать API нет.

13. Итоговая рекомендация

Рекомендуемое решение:

Python;
requests;
BeautifulSoup;
экспорт в CSV.

Почему это оптимально:

задача одноразовая;
требуется обработать только одну страницу;
необходимые данные уже присутствуют в HTML;
решение будет самым простым, быстрым и надежным без использования браузера.

Что желательно получить перед началом разработки:

Дополнительные материалы не обязательны. При необходимости можно уточнить формат CSV (например, кодировку или точный формат цены), но это не препятствует началу работы.

Можно ли переходить к написанию кода?

Да. На основании предоставленного описания и HTML информации достаточно для реализации. Единственное ограничение — внутренний API нельзя оценить, так как network.har пуст, но для данной задачи это не является критичным.

---

## План проекта (этап 2)

1. Полный поток данныхURL (заданная страница 2)↓[Технология: requests]↓[Сырые данные: HTML]↓[Парсер: BeautifulSoup]↓[Структура: dict]↓[Список: list[dict]]↓[Экспортер: exporter.py → CSV]2. Проектирование app/scraper.py2.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеfetch_page(url)Выполняет GET-запрос к заданной странице.url: strstr (HTML)2.2 АлгоритмПагинация: В данной задаче пагинация не требуется, так как клиент запрашивает конкретную страницу (№2). Скрапер просто забирает контент по переданному URL.Поведение: Поскольку данные уже присутствуют в статическом HTML (согласно анализу), браузер не нужен.Утилиты: Вызвать random_delay() из app.utils перед выполнением сетевого запроса для имитации поведения человека.3. Проектирование app/parser.py3.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеparse_listing(html)Ищет все карточки товаров в HTML-коде.html: strList[dict]parse_single_item(card)Извлекает данные из конкретной карточки.card: bs4.element.Tagdict3.2. Спецификация полейImage URL: img (атрибут src внутри тега <picture>).Car Name: Текст из блока class="common-text size-16-20 titleS fw-bold mb-4".Price: Текст из блока class="common-text titleM c-green". Используем clean_price() из utils.py.Fuel Type: Текст из 3-го блока structure-row внутри grid-wrapper.City: Текст из 4-го блока structure-row внутри grid-wrapper.3.3. Финальная структура результатаJSON{
    "Image URL": "https://cdn3.riastatic.com/photosnew/auto/photo/...",
    "Car Name": "BMW 3 Series 2017",
    "Price": "16 500 $",
    "Fuel Type": "Бензин, 2 л",
    "City": "Львів (Львівська)"
}
4. Обработка ошибокСценарийДействиеTimeoutПовторить запрос 3 раза с паузой. Если не помогло — логировать и завершить.HTTP 403/404Логировать ошибку и прервать выполнение (одноразовая задача).Элемент не найденВернуть None для конкретного поля, чтобы не ломать структуру CSV.5. Оценка рисковCloudflare (защита): Низкий риск (для одной страницы).Rate Limiting: Низкий риск.Сложная структура DOM: Средний риск (возможны изменения имен классов).6. Порядок реализацииparser.py: Создать на базе page.html. Протестировать извлечение всех полей.scraper.py: Реализовать запрос requests и передачу ответа в парсер.Интеграция: Вызвать связку в main.py и передать результат в exporter.save_to_csv().7. Краткое резюмеВыбранная технология: requests + BeautifulSoup (стандартный HTTP-запрос).Основные функции scraper.py: fetch_page.Основные функции parser.py: parse_listing, parse_single_item.Итоговая структура данных: Словарь с полями: Image URL, Car Name, Price, Fuel Type, City.Главные риски: Изменение верстки сайта (классов CSS).Что останется неизвестнымТочное соответствие CSS-селекторов: ПРЕДПОЛОЖЕНИЕ: Использование представленных в HTML классов будет стабильным для текущей версии страницы.Наличие защиты: ПРЕДПОЛОЖЕНИЕ: Сайт не выдаст 403 ошибку при стандартном User-Agent.Почему выбран именно этот способ:Выбран HTML-парсинг, так как сайт отдает полный HTML с данными в первом же ответе. Playwright избыточен, медленнее и потребляет больше ресурсов. Метод requests + BS4 является самым быстрым и надежным для одноразовой операции.Могу ли я приступать к написанию логики (псевдокода) или реализации?Да, проект спроектирован полностью в рамках требований.

---

## Данные клиента



--- ФАЙЛ: description.txt ---
# Описание задачи клиента

URL:https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1

нужно собрать товары только со страницы 2.
https://auto.ria.com/uk/search/?search_type=2&category=1&abroad=0&customs_cleared=1&page=2


собери мне в любом формате csv инфу только первую страницу (однопазовая задача)
урл картинки
название авто
цену
тип топливо
город





--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---


--- ФАЙЛ: page.html ---
<a class="link product-card horizontal" data-width-type="content" href="/uk/auto_bmw_3-series_38561317.html" target="_self" style="" id="38561317" data-car-id="38561317" data-v-52606b65=""><!--[--><div class="product-card-template" data-v-52606b65=""><div class="product-card-gallery" data-v-52606b65=""><!--[--><span class="picture" style="--aspectRatio:4/3;" data-v-5d3d3206=""><!----><picture data-v-5d3d3206=""><source data-src="https://cdn3.riastatic.com/photosnew/auto/photo/bmw_3-series__611464884fx.webp" type="image/webp" data-v-5d3d3206="" srcset="https://cdn3.riastatic.com/photosnew/auto/photo/bmw_3-series__611464884fx.webp"><img data-src="https://cdn3.riastatic.com/photosnew/auto/photo/bmw_3-series__611464884fx.jpg" title="Седан BMW 3 Series 2017 в Львові" alt="Седан BMW 3 Series 2017 в Львові" data-v-5d3d3206="" src="https://cdn3.riastatic.com/photosnew/auto/photo/bmw_3-series__611464884fx.jpg"></picture></span><!----><!----><!--]--><div class="product-card-actions" data-v-52606b65=""><div class="inside product-card-badges events-none"><!--[--><!--[--><div class="badge-template" style=""><span class="common-badge contrast medium" style="" id="Auto38561317BotBadge0"><!--[--><!--[--><!--[--><!--[--><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="common-icon"><path d="M0.5 5H2L5 2H11L11.75 2.75L8 6.5L6 4.5L4.5 6L8 9.5L13.25 4.25L14 5H15.5C15.7761 5 16 5.22386 16 5.5C16 5.77614 15.7761 6 15.5 6H15V12C15 12.5523 14.5523 13 14 13H13C12.4477 13 12 12.5523 12 12V11H4V12C4 12.5523 3.55228 13 3 13H2C1.44772 13 1 12.5523 1 12V6H0.5C0.223858 6 0 5.77614 0 5.5C0 5.22386 0.223858 5 0.5 5Z" fill="var(--inverse)"></path></svg><!--]--><!--[--><span class="common-text ws-pre-wrap badge" style="color:var(--inverse);"><!--[-->Перевірений VIN<!--]--></span><!--]--><!--]--><!--]--><!--]--></span></div><!--]--><!--[--><div class="car-number ua" style="" data-v-068172c4=""><!--[--><!--[--><span class="common-text ws-pre-wrap badge" style="color:var(--staticBlack);"><!--[-->BC 9696 IM<!--]--></span><!--]--><!--]--></div><!--]--><!--]--></div><div class="product-card-action left top structure-row gap-8 ai-center events-none"><!--[--><span class="common-badge strokeLight medium" style=""><!--[--><span class="common-text badge">ТОП 102</span><!--]--></span><span class="common-badge brand medium" style=""><!--[--><span class="common-text badge">Тільки на AUTO.RIA</span><!--]--></span><!--]--></div><!----><!----><!----><!----><!----><!----></div></div></div><div class="product-card-content" data-v-52606b65=""><div class="structure-row mb-8"><div class="grow-1 basis-0"><div class="common-text size-16-20 titleS fw-bold mb-4"><!--[--><!----> BMW 3 Series 2017<!--]--></div><div class="common-text size-14-16 ellipsis-1 mb-8"><!--[-->F30 (FL)  •  330i MT (252 к.с.)  •  Base<!--]--></div><!----><div><span class="common-text titleM c-green"><!--[-->16&nbsp;500 $ <!--]--></span><span class="common-text body"><!--[--> · 737&nbsp;385 грн <!--]--></span></div></div><div class="button-icon absolute favorite"><button class="size-large ghost" type="button" aria-label="Поділитися" data-type="common-button" data-width-type="custom" data-action=""><!--[--><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" class="common-icon"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.0001 3.87654C9.48365 1.37442 5.40384 1.37449 2.88747 3.87675C0.371098 6.379 0.370749 10.4362 2.88699 12.9385L11.295 21.2989C11.6851 21.6867 12.3151 21.6867 12.7052 21.2989L21.1129 12.9383C23.6291 10.4359 23.629 6.37905 21.1127 3.87682C18.5963 1.37458 14.5166 1.37449 12.0001 3.87654ZM19.7026 11.5202C19.7027 11.5201 19.7027 11.5201 19.7027 11.5201C21.4325 9.79968 21.4324 7.01529 19.7024 5.295C17.9662 3.56849 15.1466 3.56843 13.4103 5.29481L12.0001 6.6969L10.5899 5.29479C8.85362 3.56836 6.03397 3.5684 4.2977 5.29493C2.56759 7.01534 2.56745 9.80004 4.29717 11.5203C4.29721 11.5204 4.29724 11.5204 4.29728 11.5204L12.0001 19.1795L19.7026 11.5202Z" fill="var(--contrastPrimary)"></path></svg><!--]--></button></div></div><div class="grid-wrapper"><!--[--><div class="structure-row ai-center gap-8 flex-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="common-icon"><path d="M11 3.80385C10.0879 3.27724 9.05322 3 8 3C6.94678 3 5.91212 3.27724 5 3.80385C4.08788 4.33046 3.33046 5.08789 2.80385 6C2.27724 6.91212 2 7.94678 2 9C2 10.0532 2.27724 11.0879 2.80385 12C3.07999 12.4783 2.91612 13.0899 2.43782 13.366C1.95953 13.6422 1.34794 13.4783 1.0718 13C0.369651 11.7838 0 10.4043 0 9C0 7.59571 0.36965 6.21615 1.0718 5C1.77394 3.78385 2.78385 2.77394 4 2.0718C5.21615 1.36965 6.59571 1 8 1C9.40429 1 10.7838 1.36965 12 2.0718C13.2162 2.77394 14.2261 3.78385 14.9282 5C15.6303 6.21615 16 7.59571 16 9C16 10.4043 15.6304 11.7838 14.9282 13C14.6521 13.4783 14.0405 13.6422 13.5622 13.366C13.0839 13.0899 12.92 12.4783 13.1962 12C13.7228 11.0879 14 10.0532 14 9C14 7.94678 13.7228 6.91212 13.1962 6C12.6695 5.08788 11.9121 4.33046 11 3.80385Z" fill="var(--contrastPrimary)"></path><path d="M8.00002 11C9.10459 11 10 10.1046 10 9.00002C10 7.89545 9.10459 7.00002 8.00002 7.00002C7.7952 7.00002 7.59756 7.03081 7.4115 7.08801C7.36317 6.98104 7.29504 6.88083 7.20713 6.79291L6.20713 5.79291C5.8166 5.40239 5.18344 5.40239 4.79291 5.79291C4.40239 6.18344 4.40239 6.8166 4.79291 7.20713L5.79291 8.20713C5.88083 8.29504 5.98104 8.36317 6.08801 8.4115C6.03081 8.59756 6.00002 8.7952 6.00002 9.00002C6.00002 10.1046 6.89545 11 8.00002 11Z" fill="var(--contrastPrimary)"></path></svg><span class="common-text ellipsis-1 body"><!--[-->127 тис. км<!--]--></span></div><div class="structure-row ai-center gap-8 flex-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="common-icon"><path d="M4 5C4 4.44772 4.44772 4 5 4C5.55228 4 6 4.44772 6 5V7H7V5C7 4.44772 7.44772 4 8 4C8.55229 4 9 4.44772 9 5V7H10V5C10 4.44772 10.4477 4 11 4C11.5523 4 12 4.44772 12 5V8C12 8.55229 11.5523 9 11 9H9V11C9 11.5523 8.55229 12 8 12C7.44772 12 7 11.5523 7 11V9H6V11C6 11.5523 5.55228 12 5 12C4.44772 12 4 11.5523 4 11V5Z" fill="var(--contrastPrimary)"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M0 4C0 1.79086 1.79086 0 4 0H12C14.2091 0 16 1.79086 16 4V12C16 14.2091 14.2091 16 12 16H4C1.79086 16 0 14.2091 0 12V4ZM4 2H12C13.1046 2 14 2.89543 14 4V12C14 13.1046 13.1046 14 12 14H4C2.89543 14 2 13.1046 2 12V4C2 2.89543 2.89543 2 4 2Z" fill="var(--contrastPrimary)"></path></svg><span class="common-text ellipsis-1 body"><!--[-->Ручна / Механіка<!--]--></span></div><div class="structure-row ai-center gap-8 flex-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="common-icon"><path fill-rule="evenodd" clip-rule="evenodd" d="M2 14V3C2 1.34315 3.34315 0 5 0H9C10.6569 0 12 1.34315 12 3V11L14 11V6.4142L13.2929 5.70709C12.9024 5.31656 12.9024 4.6834 13.2929 4.29288C13.6834 3.90236 14.3166 3.90237 14.7071 4.29291L15.5606 5.14646C15.8419 5.42776 16 5.80929 16 6.2071V11.5C16 12.3284 15.3284 13 14.5 13L12 13V14C12.5523 14 13 14.4477 13 15C13 15.5523 12.5523 16 12 16H2C1.44772 16 1 15.5523 1 15C1 14.4477 1.44772 14 2 14ZM5 2H9C9.55228 2 10 2.44772 10 3V5H4V3C4 2.44772 4.44772 2 5 2ZM4 7H10V14H4V7Z" fill="var(--contrastPrimary)"></path></svg><span class="common-text ellipsis-1 body"><!--[-->Бензин, 2 л<!--]--></span></div><div class="structure-row ai-center gap-8 flex-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="common-icon"><path d="M7.61732 6.07612C7.73864 6.02587 7.86868 6 8 6C8.13132 6 8.26136 6.02587 8.38268 6.07612C8.50401 6.12638 8.61425 6.20003 8.70711 6.29289C9.09763 6.68342 9.7308 6.68342 10.1213 6.29289C10.5118 5.90237 10.5118 5.2692 10.1213 4.87868C9.84274 4.6001 9.51203 4.37913 9.14805 4.22836C8.78407 4.0776 8.39396 4 8 4C7.60603 4 7.21593 4.0776 6.85195 4.22836C6.48797 4.37913 6.15726 4.6001 5.87868 4.87868C5.6001 5.15726 5.37913 5.48797 5.22836 5.85195C5.0776 6.21593 5 6.60604 5 7C5 7.39397 5.0776 7.78407 5.22836 8.14805C5.37913 8.51203 5.6001 8.84274 5.87868 9.12132C6.2692 9.51184 6.90237 9.51184 7.29289 9.12132C7.68342 8.7308 7.68342 8.09763 7.29289 7.70711C7.20004 7.61425 7.12638 7.50401 7.07612 7.38268C7.02587 7.26136 7 7.13132 7 7C7 6.86868 7.02587 6.73864 7.07612 6.61732C7.12638 6.49599 7.20003 6.38575 7.29289 6.29289C7.38575 6.20004 7.49599 6.12638 7.61732 6.07612Z" fill="var(--contrastPrimary)"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M15 7C15 10.866 10 16 8 16C6 16 1 10.866 1 7C1 3.13401 4.13401 0 8 0C11.866 0 15 3.13401 15 7ZM13 7C13 8.20997 12.1315 9.99918 10.7254 11.6553C10.0607 12.4382 9.36411 13.0844 8.76644 13.5161C8.46742 13.7321 8.22577 13.8707 8.05299 13.9486C8.0334 13.9574 8.01575 13.965 8 13.9715C7.98425 13.965 7.9666 13.9574 7.94701 13.9486C7.77423 13.8707 7.53258 13.7321 7.23356 13.5161C6.63589 13.0844 5.93928 12.4382 5.27462 11.6553C3.86853 9.99918 3 8.20997 3 7C3 4.23858 5.23858 2 8 2C10.7614 2 13 4.23858 13 7Z" fill="var(--contrastPrimary)"></path></svg><span class="common-text ellipsis-1 body"><!--[-->Львів (Львівська)<!--]--></span></div><!--]--></div><div class="structure-row gap-8 mt-12 labels-wrapper"><!--[--><!--[--><div class="badge-template" style=""><span class="common-badge accent medium" style="" id="Auto38561317BotBadge0"><!--[--><!--[--><!--[--><!--[--><span class="common-text ws-pre-wrap badge" style="color:var(--contrastPrimary);"><!--[-->Є звіт по VIN<!--]--></span><!--]--><!--]--><!--]--><!--]--></span></div><!--]--><!--[--><div class="badge-template" style=""><span class="common-badge accent medium" style="" id="Auto38561317BotBadge1"><!--[--><!--[--><!--[--><!--[--><span class="common-text ws-pre-wrap badge" style="color:var(--contrastPrimary);"><!--[-->Доступний кредит<!--]--></span><!--]--><!--]--><!--]--><!--]--></span></div><!--]--><!--[--><div class="badge-template" style=""><span class="common-badge strokeLight medium" style="" id="Auto38561317BotBadge2"><!--[--><!--[--><!--[--><!--[--><span class="common-text ws-pre-wrap badge" style="color:var(--contrastPrimary);"><!--[-->Був в ДТП<!--]--></span><!--]--><!--]--><!--]--><!--]--></span></div><!--]--><!--]--></div><!----><p class="common-text footnote mt-12 ellipsis-1"><!--[-->Авто в чудовому стані, заводський М-пакет. 
Були мінімальні пошкодження бокових дверей, замінили в колір. 
Повний рестайлінг, двигун B48. 
На 100 тис/км  замінено комплект щеплення, нові форсунки, нові свічки, масло в коробці, масло в редукторі, проведено огляд циліндрів ендоскопом на наявність задирів. 
Машина обслуговувалась виключно оригінальними запчастинами та розхідниками. Заміна масла кожні 5-6 тисяч км. Зроблено лайтовий Stage 1 на DTS Dyno Tuning Lviv (зашита під 95 бензин, їздила на 100), зроблено роздвоєний вихлоп із заслонкою для регулювання гучності (Вся екологія на місці, працювали лише із задньою частиною). 
19 колеса Japan Racing на Мішелінах
Авто робилось з 0 повністю під себе.<!--]--></p><!----><div class="structure-row jc-between wrap ai-center gap-12 mt-8"><span class="common-text footnote c-contrastSecondary"><!--[-->11 днів тому<!--]--></span><!----></div></div><!--]--></a>

--- ФАЙЛ: traceback.txt ---


---

# ЯДРО ПРОЕКТА (НЕ МЕНЯТЬ)

Следующие файлы уже написаны и протестированы. Используй их интерфейсы, не дублируй логику:



--- app/main.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))  # Добавляет starter-project в пути Python
from playwright.sync_api import sync_playwright

from app.config import COOKIES_FILE
from app.browser import get_browser_context
from app.scraper import fetch_page_data
from app.parser import parse_html_data
from app.exporter import save_to_csv, save_to_json

def main() -> None:
    """
    Главная точка входа. Управляет жизненным циклом парсера.
    """
    print("=" * 70)
    print(f"[{__file__}] ЗАПУСК ПАРСЕРА")
    print("=" * 70)

    # Инициализируем хранилище для собранных данных
    scraped_results = []

    try:
        # 1. Запуск контекста автоматизации (Playwright)
        with sync_playwright() as playwright:
            
            # Получаем настроенный контекст браузера (переменные подтянутся из config)
            context = get_browser_context(
                playwright_instance=playwright,
                cookies_path=COOKIES_FILE
            )
            
            # 2. Сбор данных (Scraping)
            # Передаем контекст браузера в scraper.py для обхода страниц
            raw_pages_content = fetch_page_data(context)
            
            # Закрываем браузер сразу, как только закончили сетевую работу
            context.browser.close()
            print(f"[{__file__}] Браузер успешно закрыт.")

            # 3. Обработка данных (Parsing)
            # Передаем собранный HTML/JSON контент в parser.py для извлечения полей
            if raw_pages_content:
                print(f"[{__file__}] Начало парсинга контента...")
                scraped_results = parse_html_data(raw_pages_content)
            else:
                print(f"[{__file__}] Критическая ошибка: Нечего парсить (список страниц пуст).")
                sys.exit(1)

        # 4. Экспорт результатов (Export)
        if scraped_results:
            print(f"[{__file__}] Экспорт данных (Всего элементов: {len(scraped_results)})...")
            
            # Сохраняем в оба формата (на Upwork клиенты любят иметь выбор)
            save_to_csv(scraped_results, "output_results.csv")
            save_to_json(scraped_results, "output_results.json")
            
            print("=" * 70)
            print(f"[{__file__}] РАБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА УСПЕШНО")
            print("=" * 70)
        else:
            print(f"[{__file__}] Предупреждение: Парсер вернул пустой результат. Файлы не созданы.")

    except KeyError as ke:
        print(f"[{__file__}] Ошибка конфигурации или структуры: {ke}")
        sys.exit(1)
    except Exception as e:
        print(f"[{__file__}] Критический сбой в главном потоке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

--- app/browser.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext

def load_cookies_if_exist(context: BrowserContext, cookies_path: Path) -> None:
    """
    Загружает куки в контекст браузера, если файл существует.
    """
    if cookies_path.exists() and cookies_path.stat().st_size > 0:
        try:
            with open(cookies_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
            print(f"[{__file__}] Куки успешно загружены из {cookies_path.name}")
        except Exception as e:
            print(f"[{__file__}] Ошибка при загрузке кук: {e}")

def get_browser_context(
    playwright_instance, 
    headless: bool = None, 
    user_agent: str = None,
    cookies_path: Path = None
) -> BrowserContext:
    """
    Инициализирует настроенный браузер и возвращает изолированный контекст.
    """
    # 1. Автоматически определяем режим (Docker/переменные окружения или дефолт)
    # Если headless не передан, смотрим в .env или ставим True, если мы в Docker
    if headless is None:
        headless = os.getenv("HEADLESS", "0") == "1" or os.getenv("IS_DOCKER") == "1"

    # Дефолтный качественный User-Agent, если не передан кастомный
    if not user_agent:
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Anonymized/Chrome/120.0.0.0 Safari/537.36"
        )

    print(f"[{__file__}] Запуск Chromium (Headless={headless})...")

    # 2. Запуск браузера с флагами против падений в Docker
    browser: Browser = playwright_instance.chromium.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled" # Скрывает автоматизацию
        ]
    )

    # 3. Создание контекста с маскировкой параметров
    context: BrowserContext = browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        is_mobile=False,
        has_touch=False,
        locale="en-US",
        timezone_id="America/New_York"
    )

    # 4. Подкладываем куки, если передан путь (например, из AI_INPUT)
    if cookies_path:
        load_cookies_if_exist(context, cookies_path)

    return context


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    # Локальный тест
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    test_cookies = ROOT_DIR / "AI_INPUT" / "cookies.json"
    
    with sync_playwright() as p:
        ctx = get_browser_context(p, headless=False, cookies_path=test_cookies)
        page = ctx.new_page()
        page.goto("https://bot.sannysoft.com/") # Хороший сайт для проверки детекта
        page.wait_for_timeout(5000)
        ctx.browser.close()

--- app/config.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# =====================================================================
# 1. ПУТИ К ПАПКАМ СТРУКТУРЫ (Абсолютные)
# =====================================================================
APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent.resolve()

# Папки для работы с ИИ
AI_INPUT_DIR = ROOT_DIR / "AI_INPUT"
AI_OUTPUT_DIR = ROOT_DIR / "AI_OUTPUT"

# Входные и выходные данные для скрипта
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"

# Файлы окружения и зависимостей
COOKIES_FILE = AI_INPUT_DIR / "cookies.json"
HEADERS_FILE = AI_INPUT_DIR / "headers.json"

# Гарантируем, что рабочие папки проекта существуют
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 2. НАСТРОЙКИ ЗАПУСКА И БРАУЗЕРА (.env / Окружение)
# =====================================================================

# Режим работы браузера: "1" — без экрана, "0" — с экраном (дебаг)
# Если переменная IS_DOCKER установлена, принудительно включаем headless
IS_DOCKER = os.getenv("IS_DOCKER", "0") == "1"
HEADLESS = os.getenv("HEADLESS", "1") == "1" or IS_DOCKER

# Логирование и таймауты
TIMEOUT = int(os.getenv("SCRAPER_TIMEOUT", "30"))  # в секундах
RETRY_COUNT = int(os.getenv("SCRAPER_RETRY", "3"))

# Настройки сети и прокси
PROXY_URL = os.getenv("PROXY_URL", None)  # Формат: http://username:password@host:port


# =====================================================================
# 3. МАСКИРОВКА И КЛИЕНТСКИЕ ДАННЫЕ
# =====================================================================

# Реалистичный дефолтный User-Agent, если не передан кастомный в headers.json
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


# =====================================================================
# 4. ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ПУТЕЙ
# =====================================================================
if __name__ == "__main__":
    print(f"[{__file__}] Проверка путей конфигурации:")
    print(f"  Корень проекта (ROOT_DIR): {ROOT_DIR}")
    print(f"  Папка вывода (OUTPUT_DIR): {OUTPUT_DIR}")
    print(f"  Файл кук (COOKIES_FILE):   {COOKIES_FILE}")
    print(f"  Режим Headless:            {HEADLESS}")
    print(f"  Запуск в Docker:           {IS_DOCKER}")

--- app/exporter.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
from typing import List, Dict, Any
from app.config import OUTPUT_DIR

def save_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """
    Сохраняет список словарей в CSV файл.
    Автоматически берет ключи первого словаря в качестве заголовков.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в CSV.")
        return ""

    # Если расширение не указано, добавляем его
    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = OUTPUT_DIR / filename
    
    # Берем заголовки из ключей первого элемента
    fieldnames = list(data[0].keys())

    try:
        # encoding="utf-8-sig" нужен, чтобы Excel на Windows корректно читал кириллицу/эмодзи
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"[{__file__}] Данные успешно сохранены в CSV: {filepath.name} (Строк: {len(data)})")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в CSV: {e}")
        return ""

def save_to_json(data: List[Dict[str, Any]], filename: str, indent: int = 4) -> str:
    """
    Сохраняет данные в формате JSON с красивыми отступами.
    """
    if not data:
        print(f"[{__file__}] Предупреждение: Нет данных для сохранения в JSON.")
        return ""

    if not filename.endswith(".json"):
        filename += ".json"

    filepath = OUTPUT_DIR / filename

    try:
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
            
        print(f"[{__file__}] Данные успешно сохранены в JSON: {filepath.name}")
        return str(filepath)
    except Exception as e:
        print(f"[{__file__}] Ошибка при сохранении в JSON: {e}")
        return ""


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    test_data = [
        {"id": 1, "title": "Ноутбук", "price": 1200.50, "in_stock": True},
        {"id": 2, "title": "Смартфон", "price": 550.00, "in_stock": False},
    ]
    print(f"[{__file__}] Запуск теста экспортера...")
    save_to_csv(test_data, "test_products")
    save_to_json(test_data, "test_products.json")

--- app/utils.py (НЕ МЕНЯТЬ) ---
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from datetime import datetime

def log_message(level: str, message: str) -> None:
    """
    Универсальный форматированный логгер для вывода в консоль.
    Заменяет тяжелые библиотеки логирования простым и понятным для ИИ кодом.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")

def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """
    Генерирует случайную паузу. Помогает имитировать поведение 
    реального пользователя и обходить базовые лимиты запросов (Rate Limiting).
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def clean_price(price_string: str) -> float:
    """
    Утилита очистки строки цены (например, '$1,299.99' или '150.00 €') 
    и конвертации её в чистое число с плавающей точкой (float).
    Очень частый запрос от клиентов на Upwork.
    """
    if not price_string:
        return 0.0
        
    try:
        # Удаляем все пробельные символы
        cleaned = re.sub(r"\s+", "", price_string)
        # Оставляем только цифры, точки и запятые
        cleaned = re.sub(r"[^\d.,]", "", cleaned)
        
        # Если в цене есть и точка, и запятая (например, 1,250.50)
        if "," in cleaned and "." in cleaned:
            # Если запятая идет первой, это разделитель тысяч (US стиль) -> просто убираем её
            if cleaned.find(",") < cleaned.find("."):
                cleaned = cleaned.replace(",", "")
            # Если точка идет первой (EU стиль, например, 1.250,50) -> убираем точку, запятую меняем на точку
            else:
                cleaned = cleaned.replace(".", "").replace(",", ".")
        # Если есть только запятая (EU стиль без копеек или с копейками через запятую: '150,50')
        elif "," in cleaned and "." not in cleaned:
            cleaned = cleaned.replace(",", ".")
            
        return float(cleaned)
    except Exception:
        # Если очистить не удалось, возвращаем 0.0, чтобы скрипт не падал
        return 0.0


# Пример использования (для дебага самого файла)
if __name__ == "__main__":
    print(f"[{__file__}] Тест утилит:")
    
    log_message("info", "Запуск теста очистки цен...")
    
    # Тестируем разные форматы валют, которые могут прилететь с сайтов
    prices_to_test = ["$1,249.99", "350,00 €", " 1.500,75 руб ", "99"]
    
    for p in prices_to_test:
        print(f"  Исходная: {p:<15} -> Результат: {clean_price(p)}")

---

# ТЕКУЩИЙ ШАБЛОН МОДУЛЯ

Файл `app/scraper.py` — перепиши его полностью под план проекта:

# app/scraper.py
import os
from typing import List
from app.config import AI_INPUT_DIR

def load_local_html(file_path: str) -> str:
    """
    Открывает и считывает текстовое содержимое сохраненного HTML-файла.
    
    Args:
        file_path (str): Абсолютный или относительный путь к файлу.
        
    Returns:
        str: Строка с сырым HTML-кодом страницы.
        
    Raises:
        FileNotFoundError: Если целевой файл отсутствует на диске.
    """
    if not os.path.exists(file_path):
        print(f"[{__file__}] Ошибка: Файл не найден по пути {file_path}")
        raise FileNotFoundError(f"Файл {file_path} не найден.")
        
    print(f"[{__file__}] Чтение локального файла: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def fetch_page_data(context=None) -> List[str]:
    """
    Точка оркестрации для сбора данных, вызываемая из main.py.
    Собирает сырой HTML-контент из локального источника.
    Принимает необязательный аргумент context для совместимости с основным потоком main.py.
    
    Args:
        context (BrowserContext, optional): Контекст браузера Playwright.
        
    Returns:
        List[str]: Список строк, содержащих сырой HTML страниц.
    """
    print(f"[{__file__}] Запуск процесса сбора данных...")
    
    # Формируем путь к файлу на основе конфигурационных путей ядра
    target_file = os.path.join(AI_INPUT_DIR, "page.html")
    
    html_contents = []
    try:
        html_data = load_local_html(target_file)
        if html_data.strip():
            html_contents.append(html_data)
        else:
            print(f"[{__file__}] Предупреждение: Считанный файл page.html пуст.")
    except FileNotFoundError as e:
        print(f"[{__file__}] Критическая ошибка сбора данных: {e}")
        # Возвращаем пустой список, чтобы не вызывать критическое падение всей системы
    except Exception as e:
        print(f"[{__file__}] Непредвиденная ошибка при чтении файла: {e}")
        
    print(f"[{__file__}] Сбор данных завершен. Получено страниц: {len(html_contents)}")
    return html_contents

---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `app/scraper.py` (модуль: **scraper**).

## Требования

1. **Только функции** — без классов.
2. **Один файл** — весь код модуля в одном ответе.
3. **Следуй project_plan.md** — имена функций, сигнатуры, алгоритм.
4. **Не трогай ядро** — `main.py` уже вызывает `fetch_page_data()` и `parse_html_data()`. Сохрани эти имена или обнови только если план явно требует другие.
5. **Минимум зависимостей** — используй только то, что уже есть в проекте.
6. **Обработка ошибок** — try/except на уровне страниц/элементов, не падай на одной ошибке.
7. **Логирование** — `print(f"[{__file__}] ...")` как в шаблоне.

## Если модуль = scraper

- Отвечает **только** за сеть, навигацию, пагинацию, скролл, клики.
- Возвращает `List[str]` — список сырого HTML (или JSON-строк).
- Не парсит DOM — это задача parser.py.
- Используй `app.config` для таймаутов и путей.
- Используй `random_delay()` из `app.utils` между запросами.

## Если модуль = parser

- Отвечает **только** за извлечение данных из сырого контента.
- Принимает `List[str]`, возвращает `List[Dict[str, Any]]`.
- Используй BeautifulSoup для HTML.
- Сохрани функцию `parse_single_item()` для парсинга одного элемента.
- Поля результата — строго по project_plan.md.

---

# ФОРМАТ ОТВЕТА

1. Кратко (3–5 строк): что делает модуль.
2. Полный код файла `app/scraper.py` в одном блоке:

```python
# полный код здесь
```

3. Как протестировать локально (1–2 команды).

**ЗАПРЕЩЕНО:**
- Писать код для других файлов.
- Добавлять GUI, CLI, меню.
- Добавлять функции, которых нет в project_plan.md.
- Использовать классы.
