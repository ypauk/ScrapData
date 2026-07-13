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

Клиенту необходимо собрать данные с карточек автомобилей только на первой странице каталога новых автомобилей.

Необходимо извлечь следующие поля:

название автомобиля;
URL изображения;
цена;
тип топлива;
коробка передач;
город.

Результат можно предоставить в CSV или JSON.

Уверенность: 99% (это явно указано в описании проекта).

2. Какой конечный результат нужен

Подойдут следующие форматы:

CSV (предпочтительно)
JSON

База данных, API или другие форматы клиентом не требуются.

Уверенность: 100%

3. Как лучше решить задачу
Рекомендуемое решение

Python + requests + BeautifulSoup

Почему

Из предоставленного HTML видно, что:

карточки автомобилей уже присутствуют в HTML;
все необходимые поля находятся внутри <article class="proposition">;
данных достаточно для извлечения без взаимодействия с браузером;
требуется обработать только первую страницу.

Следовательно, использование браузерной автоматизации выглядит избыточным.

Если в процессе проверки окажется, что сервер возвращает тот же HTML по обычному HTTP-запросу, то это будет самым простым, быстрым и надежным решением.

Уверенность: 90%

(Без network.har нельзя на 100% подтвердить, что HTML полностью доступен через обычный запрос.)

4. Почему остальные варианты хуже
Playwright

Не рекомендуется.

Причины:

значительно медленнее;
выше расход ресурсов;
усложняет проект без необходимости;
нет признаков, что требуется выполнение JavaScript.
Selenium

Не рекомендуется.

Причины:

аналогично Playwright;
менее современный выбор для новых проектов;
избыточен для данной задачи.
Scrapy

Не рекомендуется.

Причины:

проект слишком маленький;
требуется только одна страница;
дополнительные возможности Scrapy здесь не дадут преимуществ.
API

Пока не рекомендуется.

Причина:

не предоставлен network.har, поэтому наличие подходящего API подтвердить невозможно.

5. Анализ сайта
Возможность	Статус	Основание
JavaScript Rendering	Не подтверждено	HTML уже содержит данные
React	Неизвестно	данных недостаточно
Vue	Неизвестно	данных недостаточно
Angular	Неизвестно	данных недостаточно
API	Неизвестно	HAR отсутствует
GraphQL	Неизвестно	HAR отсутствует
Infinite Scroll	Не обнаружено	клиент просит только первую страницу
Pagination	Вероятно есть	каталог автомобилей обычно постраничный, но подтвердить нельзя
Login	Не обнаружен	в материалах отсутствует
Cookies	Не требуются	cookies.json пустой
JWT	Неизвестно	данных нет
Bearer Token	Неизвестно	данных нет
CAPTCHA	Не обнаружена	данных нет
Cloudflare	Неизвестно	проверить невозможно
Rate Limits	Неизвестно	проверить невозможно
Download Files	Нет признаков	
Upload Files	Нет	
Lazy Loading	Возможно только для изображений	подтверждения нет
WebSocket	Неизвестно	
XHR/Fetch	Неизвестно	
Sitemap	Не проверялось	
robots.txt	Не проверялось	

Уверенность: 60%

(Многие пункты невозможно определить без HAR или доступа к сайту.)

6. Что необходимо собрать до начала разработки

Для данной задачи уже имеется:

✅ описание задачи;
✅ пример HTML;
✅ список необходимых полей.

Полезно дополнительно получить:

network.har (если потребуется поиск API);
пример ожидаемого CSV (необязательно).

В остальном информации достаточно.

Уверенность: 95%

7. Возможные сложности

Возможные риски:

изменение HTML-разметки сайта;
появление защиты от большого количества запросов;
изменение структуры карточек автомобилей;
изменение классов элементов;
возможное отсутствие некоторых полей у отдельных автомобилей.

Серьезных технических сложностей не ожидается.

8. Что нужно уточнить у клиента

Информации почти достаточно, но желательно уточнить:

Предпочтительный формат результата — CSV или JSON?
Нужен ли URL страницы автомобиля или только URL изображения?
Требуется ли сохранить цену только в долларах или также в гривнах?
Нужно ли учитывать автомобили с отсутствующими значениями некоторых полей?
Планируется ли в будущем сбор нескольких страниц или только первой?
9. Рекомендуемый стек технологий
Python
requests
BeautifulSoup

Другие технологии на текущий момент не требуются.

Уверенность: 90%

10. План разработки
Этап 1. Проверка доступности страницы

Цель

Убедиться, что необходимые данные доступны через обычный HTTP-запрос.

Результат

Понятно, можно ли использовать requests.

Зависимости

Нет.

Этап 2. Извлечение данных

Цель

Получить все требуемые поля из карточек автомобилей.

Результат

Структурированный набор данных.

Зависимости

Успешное завершение этапа 1.

Этап 3. Экспорт

Цель

Сохранить данные в выбранный формат.

Результат

CSV или JSON.

Зависимости

Этап 2.

Этап 4. Проверка результата

Цель

Убедиться, что все карточки обработаны корректно.

Результат

Готовый файл без пропущенных данных.

Зависимости

Этап 3.

11. Оценка сложности
Параметр	Оценка
Сложность	2/10
Estimation	1–2 часа
Вероятность блокировок	Низкая (~10%)
Вероятность необходимости браузера	Низкая (~20%)
Вероятность изменения сайта	Средняя (~40%)
Общий риск	Низкий

Уверенность: 85%

12. Можно ли решить проще

Да.

Наиболее простое решение:

сначала проверить возможность получения HTML через обычный HTTP-запрос;
если данные уже присутствуют в ответе сервера — использовать requests;
извлекать информацию напрямую из HTML;
сохранить результат в CSV.

Дополнительно стоит проверить наличие скрытого API через network.har, но поскольку этот файл отсутствует, делать вывод о его наличии нельзя.

Таким образом, requests + HTML сейчас является наиболее простым решением.

13. Итоговая рекомендация
Рекомендуемое решение

Использовать:

Python
requests
BeautifulSoup
Почему это оптимально
задача небольшая;
требуется обработать только первую страницу;
HTML уже содержит все необходимые поля;
браузерная автоматизация, судя по предоставленным данным, не требуется;
решение будет самым простым, быстрым и надежным.
Что необходимо получить перед началом разработки

Обязательных дополнительных материалов нет.

Желательно иметь:

network.har (для проверки существования API, если потребуется оптимизация);
подтверждение предпочтительного формата результата (CSV или JSON).
Можно ли переходить к написанию кода?

Да, с высокой вероятностью можно.

Предоставленных материалов достаточно для начала реализации. Единственная рекомендуемая предварительная проверка — убедиться, что страница доступна через обычный HTTP-запрос. Если это подтвердится, использование браузера не понадобится.

SELF-CHECK
✅ Код не написан.
✅ Архитектура и функции не проектировались.
✅ Выбрана наиболее простая технология.
✅ Перечислены возможные риски.
✅ Указано, какой информации не хватает.
✅ Сформирован список вопросов клиенту.
✅ Предложено наиболее простое решение.
✅ Проект не усложнен без необходимости.

---

## План проекта (этап 2)

Почему выбран именно этот способ

Выбранный способ: requests + BeautifulSoup.

Почему не API

Использование API невозможно обосновать, так как:

network.har отсутствует;
признаки API в предоставленных материалах отсутствуют;
все требуемые поля уже содержатся в HTML карточек.
Почему не Playwright

Playwright не требуется, поскольку:

в предоставленном HTML уже присутствуют все необходимые данные;
не требуется авторизация;
клиент просит обработать только первую страницу;
нет признаков необходимости выполнения JavaScript для получения карточек.
Плюсы выбранного варианта
минимальная сложность;
высокая скорость;
минимальное количество зависимостей;
легко сопровождать;
полностью соответствует требованиям клиента.
Минусы
если сайт впоследствии начнет отдавать пустой HTML без JavaScript, потребуется перейти на браузерную автоматизацию;
без network.har невозможно окончательно подтвердить отсутствие внутреннего API.
1. Полный поток данных
URL
↓
requests
↓
HTML страницы
↓
scraper.fetch_page_data()
↓
сырая HTML-строка
↓
parser.parse_html_data()
↓
BeautifulSoup
↓
parse_single_item() для каждой карточки
↓
list[dict]
↓
main.py
↓
exporter.save_to_csv() / exporter.save_to_json()

Полный поток:

Пользователь запускает main.py.
main.py вызывает scraper.fetch_page_data().
scraper.py выполняет HTTP GET через requests.
Возвращает список из одного HTML-документа (List[str]).
main.py передает HTML в parser.parse_html_data().
parser.py создает объект BeautifulSoup.
Находит все <article class="proposition">.
Для каждой карточки вызывает parse_single_item().
Возвращает List[Dict].
main.py вызывает save_to_csv() или save_to_json().
2. Проектирование app/scraper.py
2.1 Интерфейс функций
Функция	Назначение	Возвращает
fetch_page_data()	Загружает первую страницу каталога	List[str]

Других функций не требуется.

Поскольку:

одна страница;
нет пагинации;
нет переходов;
нет кликов;
нет браузера.
2.2 Алгоритм обхода
Пагинация

Не используется.

Клиент явно указал:

собрать информацию первой страницы.

Следовательно:

нет ?page=2;
нет Next;
нет цикла.
Поведение на странице

После получения HTML:

ничего не выполнять.

Не требуется:

скролл;
ожидания;
клики;
раскрытие блоков.
Используемые утилиты

Использовать:

random_delay()

один раз:

HTTP запрос
↓
random_delay()
↓
вернуть HTML

Больше вызывать не требуется.

3. Проектирование app/parser.py
3.1 Интерфейс функций
Функция	Назначение	Вход	Выход
parse_html_data(html_list)	Обрабатывает список HTML	List[str]	List[dict]
parse_listing(soup)	Находит карточки автомобилей	BeautifulSoup	List[dict]
parse_single_item(card)	Извлекает поля одной карточки	Tag	dict

Дополнительные функции не требуются.

3.2 Спецификация полей
Название

Источник:

h2.proposition_name span.link

Если отсутствует:

None
URL изображения

Источник

picture img[src]

Если отсутствует

None
Цена

Источник

div.proposition_price strong

Очистка выполняется через

clean_price()

Если отсутствует

None
Топливо

Источник

div.proposition_information

Берется элемент, содержащий слово

Бензин
Дизель
Газ
Електро
Гібрид

Если отсутствует

None
Коробка

Источник

div.proposition_information

Берется элемент

Автомат
Механіка
CVT

Если отсутствует

None
Город

Источник

последний элемент блока

proposition_information

Если отсутствует

None
3.3 Финальная структура результата
{
  "title": "Skoda Octavia 2026",
  "image_url": "https://cdn.riastatic.com/photosnewr/auto/new_auto_storage/skoda-octavia__4032862-400x300x60.jpg",
  "price": 29440,
  "fuel": "Бензин, 1.4",
  "transmission": "Автомат",
  "city": "Миколаїв"
}

Добавлять другие поля не следует, так как клиент их не запрашивал.

4. Обработка ошибок
Сценарий	Стратегия
Timeout	Повторить запрос до 3 раз. Если неудачно — записать ошибку в лог и завершить работу.
HTTP 403	Записать в лог и остановить выполнение.
CAPTCHA	Записать в лог и остановить выполнение.
HTTP 404	Записать в лог, вернуть пустой список.
Ошибка сети	До 3 повторов, затем завершение.
Элемент отсутствует	Записать None, продолжить обработку.
Пустая страница	Вернуть пустой список.
Некорректный HTML	Пропустить поврежденную карточку, продолжить обработку остальных.
5. Оценка рисков
☐ Cloudflare — не подтверждено.
☐ Требуется авторизация — не обнаружено.
☐ Rate Limiting — не подтверждено.
☐ CAPTCHA — не обнаружена.
☐ Infinite Scroll — не обнаружен.
☐ Shadow DOM — не обнаружен.
☐ iframe — не обнаружен.
☐ WebSocket — не подтвержден.
☐ GraphQL API — не подтвержден.
☑ Возможны изменения структуры DOM в будущем.
6. Порядок реализации
parser.py — реализовать первым. Он не зависит от сети и может быть протестирован на предоставленном page.html.
scraper.py — реализовать вторым. После готовности парсера достаточно получить HTML и передать его на обработку.
Интеграция — подключить оба модуля к существующему main.py, не изменяя его интерфейсы.
Проверка экспорта — убедиться, что exporter.py корректно сохраняет данные в CSV и JSON.
Что останется неизвестным

Достоверно определить невозможно:

наличие скрытого API (нет network.har);
наличие защиты Cloudflare;
наличие ограничений по частоте запросов;
точные HTTP-заголовки, необходимые для успешного запроса;
используется ли JavaScript для формирования полной страницы.

ПРЕДПОЛОЖЕНИЕ: HTML страницы доступен напрямую через обычный HTTP-запрос, так как предоставленный фрагмент уже содержит все необходимые данные.

Краткое резюме
Выбранная технология: Python + requests + BeautifulSoup.
Основные функции scraper.py: fetch_page_data() — получение HTML первой страницы.
Основные функции parser.py: parse_html_data(), parse_listing(), parse_single_item() — извлечение данных из HTML.
Итоговая структура данных: List[Dict] с полями title, image_url, price, fuel, transmission, city.
Главные риски: возможные изменения HTML-разметки, неизвестное наличие API или антибот-защиты, которые нельзя подтвердить без network.har.

---

## Данные клиента



--- ФАЙЛ: description.txt ---
# Описание задачи клиента

Нужно собрать информацию с карточек авто первой страницы:
название автомобиля
урл картинки
цена
топливо
коробка
город

можно в любой формат, json или csv



URL: https://auto.ria.com/uk/newauto/search/?categoryId[]=1&yearFrom=0&yearTo=0&fuelId=undefined

Поля для извлечения:



--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---


--- ФАЙЛ: page.html ---
<article class="proposition"><a href="/uk/newauto/auto-skoda-octavia-2072584.html" target="_self" class="proposition_link"><span class="proposition_photo js-widget  " data-gaq="mainPhotoGallery" data-action="send_statistics" data-block="search" data-element="name" data-auto_id="2072584" data-autosalon_id="1273" data-user_id="2168096" data-model_id="652" data-marka_id="70" data-in_stock="1" data-sold="0" data-view_type="0" data-widget_type="0" data-version_type="103" data-body_id="545" data-count_ads="20"><span class="photo-car loaded"><picture data-gaq="mainPhoto"><source srcset="https://cdn.riastatic.com/photosnewr/auto/new_auto_storage/skoda-octavia__4032862-400x300x60.webp" type="image/webp"><img src="https://cdn.riastatic.com/photosnewr/auto/new_auto_storage/skoda-octavia__4032862-400x300x60.jpg" alt="Skoda Octavia 2026 Selection 1.4 TSI AT (150 к.с.)" title="Skoda Octavia 2026 Selection" width="400" height="300" fetchpriority="high" loading="eager" decoding="async"></picture></span><span class="proposition_notepad p-12"><svg class="svg size24 icon-favorite-head " title="Додати оголошення в обране"><use href="#i24_heart"></use></svg></span></span><div class="proposition_area"><h2 class="proposition_name" data-test="searchPage-itemContainerTitle"><span class="link">Skoda Octavia 2026</span><div class="proposition_equip overflowed"><span class="link">IV покоління/A8 (FL)<span class="dot">•</span>1.4 TSI AT (150 к.с.)<span class="dot">•</span>Selection</span></div></h2><div><div class="proposition_price"><span class="size20 green tooltip-price" data-tooltip="Ціна актуальна на 7/11/2026"><strong class="flex f-center gap-4">29&nbsp;440 $</strong></span><span class="dot">•</span><span>1&nbsp;308&nbsp;000</span>&nbsp;грн</div><div class="proposition_information" data-test="searchPage-itemAutoParameters"><span class="item flex f-center gap-8 overflowed " title=""><svg class="svg size16 f-16" aria-hidden="true"><use href="/newauto/images/search_icons.svg?v=36048597#i16_drive_stroke"></use></svg><span class="overflowed">Передній<span> привід</span></span></span><span class="item flex f-center gap-8 overflowed " title=""><svg class="svg size16 f-16" aria-hidden="true"><use href="/newauto/images/search_icons.svg?v=36048597#i16_automat"></use></svg><span class="overflowed">Автомат<span></span></span></span><span class="item flex f-center gap-8 overflowed " title="Бензин"><svg class="svg size16 f-16" aria-hidden="true"><use href="/newauto/images/search_icons.svg?v=36048597#i16_engine"></use></svg><span class="overflowed">Бензин,&nbsp;1.4<span> л</span></span></span><span class="item flex f-center gap-8 overflowed " title="Миколаїв"><svg class="svg size16 f-16" aria-hidden="true"><use href="/newauto/images/search_icons.svg?v=36048597#i16_pin"></use></svg><span class="overflowed">Миколаїв <span></span></span></span></div><div class="proposition_badges unscroll"><span class="badge badge--accent" title="Це авто в даний момент знаходиться на майданчику біля салону">В наявності</span><span class="badge badge--accent w500">Краща ціна</span><span class="badge badge--accent w500">Кредит до 1 року під 0.01%</span></div><div class="proposition_description size14">Skoda Octavia A8 Selection Plus в наявності

Додатково оскащена:
Тонування задніх та бічних задніх вікон
Спойлер кришки багажника

До комплектації входить:
Комбінований салон автомобіля
Атмосферна Ambient підсвітка салону
Бездротовий Android Auto/Car Play
Утримання в смузі руху
Розширений бортовий компьютер
Передні та задні парктроніки
Автоматичне світло, автоматичне дальнє світло
Вибір режимів руху
LED передні фари
Двозонний клімат-контроль Climatronic
Обігрів передніх сидінь з незалежним керуванням
Камера заднього огляду з омивачем
Круїз-контроль з обмежувачем швидкості "CRUISE CONTROL"
Підігрів керма
Підігрів лобового скла
Складання спинок задніх сидінь з багажника
та інше
</div></div></div></a></article>

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
