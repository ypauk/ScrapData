# РОЛЬ

Ты — Senior Python Web Scraping Engineer. Твоя задача — написать **только один файл**: `{{MODULE_FILE}}`.

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

{{ANALYSIS}}

---

## План проекта (этап 2)

Почему выбран именно этот способВыбран способ: Чтение локального HTML (page.html) с помощью BeautifulSoup.Плюсы:Надежность на 100%: Локальный файл уже предоставлен клиентом в page.html, он не изменится в процессе выполнения скрипта, исключены сетевые сбои.Отсутствие блокировок: Нет рисков получить бан от Cloudflare или натолкнуться на CAPTCHA, так как запросы к серверу OLX не выполняются.Скорость: Парсинг локального файла в памяти происходит мгновенно по сравнению с сетевыми запросами.Минимальная сложность: Не требуются прокси, ротация заголовков и управление браузерным контекстом.Минусы:Решение статично. Если клиенту потребуется собирать новые (актуальные) данные с сайта в будущем, скрипт потребует доработки сетевого слоя в scraper.py (с интеграцией прокси для обхода Cloudflare).Что останется неизвестнымПРЕДПОЛОЖЕНИЕ: Предполагается, что предоставленный page.html является исчерпывающим образцом разметки и клиенту на данном этапе нужно извлечь данные строго из этого файла (или аналогичных сохраненных вручную страниц), так как файлы cookies.json, headers.json и network.har пусты.Неизвестен желаемый формат выгрузки: Клиент не указал, нужен ли CSV, Excel или JSON (будет предусмотрена поддержка стандартов exporter.py).Неизвестна пагинация: Из предоставленного фрагмента HTML и описания неясно, содержит ли локальный файл разметку блока пагинации и нужно ли её обрабатывать.1. Полный поток данныхЛокальный файл page.html (из папки AI_INPUT_DIR)↓[Технология: Встроенное чтение файлов Python]↓[Сырые данные: Строка HTML]↓[Парсер: BeautifulSoup (lxml / html.parser)]↓[Структура: dict (поля: title, price, fuel)]↓[Список: list[dict]]↓[Экспортер: exporter.py → save_to_csv / save_to_json]Логика оркестрации:Пользователь запускает main.py.main.py вызывает функцию scraper.load_local_html(), которая считывает файл page.html из директории, указанной в config.py.main.py передает полученную строку HTML в parser.parse_listing().parser.py инициализирует BeautifulSoup, находит контейнеры объявлений и итерируется по ним.Для каждого контейнера вызывается parser.parse_single_item(), формирующая словарь с полями объявления.parser.py возвращает список словарей обратно в main.py.main.py отправляет полученный список в функции exporter.save_to_csv() или save_to_json() для записи в OUTPUT_DIR.2. Проектирование app/scraper.py (Сетевой сбор)Так как текущая стратегия базируется на обработке локального файла, модуль scraper.py выполняет роль поставщика сырых данных из локального источника, подготавливая интерфейс для возможного расширения под сеть.2.1. Интерфейс функцийload_local_html(file_path: str) -> strНазначение: Открывает и считывает текстовое содержимое сохраненного HTML-файла.Входные параметры: Путь к файлу (берется из config.py).Возвращаемое значение: Строка (str) с сырым HTML-кодом страницы.2.2. Алгоритм обходаЛогика пагинации: Отсутствует. Обрабатывается строго одна страница из предоставленного файла.Поведение на странице: Ожидание элементов не требуется, так как файл считывается целиком из файловой системы. Скроллинг и раскрытие табов не применяются.Используемые утилиты: В текущей конфигурации random_delay() не вызывается, так как сетевые запросы отсутствуют. При переходе на живой сайт задержка будет интегрирована между запросами страниц.3. Проектирование app/parser.py (Экстракция данных)3.1. Интерфейс функцийФункцияНазначениеВходные параметрыВозвращаемое значениеparse_listing(html: str)Инициализирует BS4, находит коллекцию всех карточек автомобилей на странице и передает каждую в parse_single_item.html: strlist[dict]parse_single_item(card: bs4.element.Tag)Извлекает целевые поля (название, цена, топливо) из структуры одной карточки товара.card: bs4.element.Tagdict3.2. Спецификация полейВыборка элементов строится строго на базе структуры предоставленного page.html:Главный контейнер карточки (card): Ищется элемент div с классом css-1sw7q4x.Название (title): Внутри карточки ищется тег h4 с классом css-wlcw7o. Значение по умолчанию: "".Цена (price): Внутри карточки ищется тег p с классом css-61fb99. Текст очищается с помощью utils.clean_price(). Значение по умолчанию: None.Вид топлива (fuel): Внутри карточки ищется блок с параметрами — div с классом css-13vv2xi. Внутри него выбираются дочерние элементы span с классом css-h59g4b. Вид топлива является третьим по счету элементом span (после года выпуска и типа КПП). Значение по умолчанию: "".3.3. Финальная структура результатаJSON{
  "title": "Продам ваз 2104 инжектор",
  "price": "51 165.64 грн.",
  "fuel": "Газ / бензин"
}
4. Обработка ошибокСценарийДействиеФайл page.html не найденСгенерировать исключение FileNotFoundError, записать критическую ошибку в логгер из app.utils, корректно завершить работу оркестратора.Элемент не найден (например, нет цены)Записать None в поле "price", залогировать предупреждение (Warning) с ID объявления, но не прерывать цикл обработки остальных карточек.Изменение структуры параметров (нет третьего span)Если в блоке css-13vv2xi содержится меньше 3 элементов span, присвоить полю "fuel" значение "" или "Не указано", продолжить выполнение.Пустой HTML-файлПроверить размер контента перед передачей в парсер. Если контент пуст — вернуть пустой список [] и зафиксировать в логе.5. Оценка рисков[ ] Cloudflare (защита) — Отсутствует при локальном парсинге[ ] Требуется авторизация (Login) — Не требуется[ ] Rate Limiting — Отсутствует[ ] CAPTCHA — Отсутствует[ ] Infinite Scroll — Отсутствует[ ] Shadow DOM — Не обнаружено[ ] iframe — Не используются для целевых данных[ ] WebSocket — Не используется[ ] GraphQL API — Не используется[x] Сложная структура DOM с частыми изменениями — Высокий риск при обновлении верстки сайта (классы css-... динамические).6. Порядок реализацииapp/parser.py — Разрабатывается в первую очередь. Поскольку в AI_INPUT уже загружен файл page.html, мы можем полностью реализовать, отладить и протестировать селекторы BeautifulSoup без необходимости настраивать сеть.app/scraper.py — Создается минимальная функция для безопасного чтения локального файла с диска с обработкой ошибок доступа.Интеграция в app/main.py — Связывание вызовов scraper.py, parser.py и передача готового списка словарей в функции exporter.py (save_to_csv / save_to_json).7. Краткое резюмеВыбранная технология: Python, BeautifulSoup (модуль bs4) для локального разбора HTML.Основные функции scraper.py: load_local_html() (чтение файла).Основные функции parser.py: parse_listing() (поиск карточек), parse_single_item() (сбор полей title, price, fuel).Итоговая структура данных: Список словарей вида [{"title": str, "price": str, "fuel": str}].Главные риски проекта: Смена динамических классов css-XXXXX на сайте OLX при генерации новых страниц в будущем (сломает селекторы парсера).

---

## Данные клиента



--- ФАЙЛ: description.txt ---
надо извлечданные из одной страницы:
https://www.olx.ua/uk/transport/legkovye-avtomobili/

название
цена
вид топлива


--- ФАЙЛ: answers.txt ---
answer1
answer2
answer3
answer4
...

--- ФАЙЛ: cookies.json ---


--- ФАЙЛ: headers.json ---


--- ФАЙЛ: network.har ---


--- ФАЙЛ: page.html ---
<div data-cy="l-card" data-testid="l-card" data-visually-ready-trigger-element="true" id="926825655" class="css-1sw7q4x"><div class="css-ri9uxm"><div type="list" class="css-hvzem4"><div type="list" class="css-e59vz0"><a class="css-1tqlkj0" href="/d/uk/obyavlenie/prodam-vaz-2104-inzhektor-ID10IRGT.html?search_reason=search%7Corganic"><div type="list" class="css-11ow61k"><div class="css-gl6djm"><img src="https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=216x152;q=50" srcset="https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=150x113;q=50 150w, https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=200x150;q=50 200w, https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=270x203;q=50 300w, https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=360x270;q=50 400w, https://ireland.apollo.olxcdn.com:443/v1/files/j7i62vhov0t91-UA/image;s=510x383;q=50 600w" sizes="216px" alt="Продам ваз 2104 инжектор" class="css-8wsg1m"></div></div><div class="css-6gymc3"><div class="css-1av34ht"><div class="css-3xiokn"></div></div></div></a></div><div type="list" class="css-ih6nf2"><div data-cy="ad-card-title" data-testid="ad-card-title" class="css-u2ayx9"><a aria-label="Продам ваз 2104 инжектор" class="css-1tqlkj0" href="/d/uk/obyavlenie/prodam-vaz-2104-inzhektor-ID10IRGT.html?search_reason=search%7Corganic"><h4 data-nx-name="H4" data-nx-legacy="true" class="css-wlcw7o">Продам ваз 2104 инжектор</h4></a><p data-testid="ad-price" data-nx-name="P2" data-nx-legacy="true" class="css-61fb99">51 165.64 грн.<span data-nx-name="Label2" data-nx-legacy="true" class="css-zf56ej">Договірна</span><span data-nx-name="Label2" data-nx-legacy="true" class="css-zf56ej"></span></p></div><div class="css-16y676b"><div class="flex flex-wrap items-end gap-(--spacing50)"></div><div data-testid="slot-wrapper" class="css-1smnjed"></div></div><div class="css-49upc6"><p data-testid="location-date" data-nx-name="P4" data-nx-legacy="true" class="css-1453zif">Самар - Сьогодні о 21:30</p><div color="text-global-secondary" class="css-13vv2xi"><span class="css-t4djs0"><span data-nx-name="P5" data-nx-legacy="true" class="css-h59g4b"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" data-testid="millage-card-param-icon" class="css-156kzg6"><g clip-path="url(#millage_svg__a)"><path fill="currentColor" fill-rule="evenodd" d="M12 13c-.6 0-1 .4-1 1s.4 1 1 1 1-.4 1-1c0-.5-.4-1-1-1m5-4v1.4l-1.3 1.3-1 1c.2.4.3.8.3 1.3 0 1.7-1.3 3-3 3s-3-1.3-3-3 1.3-3 3-3c.5 0 .9.1 1.3.3l1-1L15.6 9zm-5-3c-4.4 0-8 3.6-8 8 0 2.3.4 3.8 1.4 5h13.1c1-1.2 1.4-2.7 1.4-5 .1-4.4-3.5-8-7.9-8m0-2c5.5 0 10 4.5 10 10 0 2.2-.3 4.7-2.3 6.7l-.7.3H5l-.7-.3c-2-2-2.3-4.5-2.3-6.7C2 8.5 6.5 4 12 4" clip-rule="evenodd"></path></g><defs><clipPath id="millage_svg__a"><path fill="#fff" d="M2 4h20v17H2z"></path></clipPath></defs></svg>2007  150 тис.км.</span><span data-nx-name="P5" data-nx-legacy="true" class="css-h59g4b"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="css-156kzg6"><path fill="currentColor" fill-rule="evenodd" d="M21 4a2 2 0 0 0-4 0c0 .738.405 1.376 1 1.723v4.863l-.414.414H13V5.745A1.99 1.99 0 0 0 14.042 4a2 2 0 0 0-4 0c0 .721.385 1.348.958 1.7V11H6V5.723A1.994 1.994 0 0 0 5 2a1.994 1.994 0 0 0-1 3.723v12.554c-.595.347-1 .984-1 1.723a2 2 0 0 0 4 0c0-.739-.405-1.376-1-1.723V13h5v5.3a1.99 1.99 0 0 0-.958 1.7 2 2 0 0 0 4 0A1.99 1.99 0 0 0 13 18.255V13h5.414L20 11.414V5.723c.595-.347 1-.985 1-1.723" clip-rule="evenodd"></path></svg>Механічна</span><span data-nx-name="P5" data-nx-legacy="true" class="css-h59g4b"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="css-156kzg6"><path fill="currentColor" d="M10.997 9H6V5h4.997z"></path><path fill="currentColor" fill-rule="evenodd" d="M16 3.042h3.408L22 5.579v13.422C22 20.206 21.201 22 19 22s-3-1.794-3-3v-6c0-.806-.55-.989-1.011-1H14v10H3V3.001l1-1h9l1 1V10h1c1.206 0 3 .799 3 3v6c.012.449.195 1 1 1 .806 0 .988-.55 1-1.011V6.421l-1.408-1.379H16l-1-1.041zM12 20H5V4.001h7z" clip-rule="evenodd"></path></svg>Газ / бензин</span></span></div></div><button type="button" data-testid="adAddToFavorites" aria-label="Підписатися: Продам ваз 2104 инжектор" aria-pressed="false" class="css-kmyhfy" data-nx-name="UnstyledButton"><div data-testid="favorite-icon" class="css-1iakee2">Підписатися</div><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1em" height="1em" class="css-py8enh"><path fill="currentColor" fill-rule="evenodd" d="M20.219 10.367 12 20.419 3.806 10.4A3.96 3.96 0 0 1 3 8c0-2.206 1.795-4 4-4a4.004 4.004 0 0 1 3.868 3h2.264A4 4 0 0 1 17 4c2.206 0 4 1.794 4 4 0 .868-.279 1.698-.781 2.367M17 2a6 6 0 0 0-5 2.686A6 6 0 0 0 7 2C3.692 2 1 4.691 1 8a5.97 5.97 0 0 0 1.232 3.633L10.71 22h2.582l8.501-10.399A5.94 5.94 0 0 0 23 8c0-3.309-2.692-6-6-6"></path></svg></button></div></div></div></div>

---

# ЯДРО ПРОЕКТА (НЕ МЕНЯТЬ)

Следующие файлы уже написаны и протестированы. Используй их интерфейсы, не дублируй логику:

{{CORE_FILES}}

---

# ТЕКУЩИЙ ШАБЛОН МОДУЛЯ

Файл `{{MODULE_FILE}}` — перепиши его полностью под план проекта:

{{MODULE_TEMPLATE}}

---

# ЗАДАЧА

Сгенерируй **полный рабочий код** для `{{MODULE_FILE}}` (модуль: **{{MODULE_NAME}}**).

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
2. Полный код файла `{{MODULE_FILE}}` в одном блоке:

```python
# полный код здесь
```

3. Как протестировать локально (1–2 команды).

**ЗАПРЕЩЕНО:**
- Писать код для других файлов.
- Добавлять GUI, CLI, меню.
- Добавлять функции, которых нет в project_plan.md.
- Использовать классы.
