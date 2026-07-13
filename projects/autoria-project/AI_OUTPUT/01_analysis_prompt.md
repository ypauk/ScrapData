# ROLE

Главная цель — выбрать самое простое, надежное и быстрое решение, полностью соответствующее требованиям клиента.

Не усложняй проект без необходимости.

Ты опытный Python Web Scraping Engineer с большим опытом выполнения проектов на Upwork.

Твоя задача — сначала полностью проанализировать проект клиента и выбрать оптимальную стратегию разработки.

На этом этапе ЗАПРЕЩЕНО писать код.
Если тебе не хватает информации — сначала задай вопросы.

---

# PROJECT DESCRIPTION

Ниже будет описание проекта клиента.



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


--- СЖАТЫЙ HTML: page.html ---
<article class="proposition">
 <a class="proposition_link" href="/uk/newauto/auto-skoda-octavia-2072584.html">
  <span class="proposition_photo js-widget">
   <span class="photo-car loaded">
    <picture>
     <source/>
     <img src="https://cdn.riastatic.com/photosnewr/auto/new_auto_storage/skoda-octavia__4032862-400x300x60.jpg"/>
    </picture>
   </span>
   <span class="proposition_notepad p-12">
   </span>
  </span>
  <div class="proposition_area">
   <h2 class="proposition_name">
    <span class="link">
     Skoda Octavia 2026
    </span>
    <div class="proposition_equip overflowed">
     <span class="link">
      IV покоління/A8 (FL)
      <span class="dot">
       •
      </span>
      1.4 TSI AT (150 к.с.)
      <span class="dot">
       •
      </span>
      Selection
     </span>
    </div>
   </h2>
   <div>
    <div class="proposition_price">
     <span class="size20 green tooltip-price">
      <strong class="flex f-center gap-4">
       29 440 $
      </strong>
     </span>
     <span class="dot">
      •
     </span>
     <span>
      1 308 000
     </span>
     грн
    </div>
    <div class="proposition_information">
     <span class="item flex f-center gap-8 overflowed">
      <span class="overflowed">
       Передній
       <span>
        привід
       </span>
      </span>
     </span>
     <span class="item flex f-center gap-8 overflowed">
      <span class="overflowed">
       Автомат
       <span>
       </span>
      </span>
     </span>
     <span class="item flex f-center gap-8 overflowed">
      <span class="overflowed">
       Бензин, 1.4
       <span>
        л
       </span>
      </span>
     </span>
     <span class="item flex f-center gap-8 overflowed">
      <span class="overflowed">
       Миколаїв
       <span>
       </span>
      </span>
     </span>
    </div>
    <div class="proposition_badges unscroll">
     <span class="badge badge--accent">
      В наявності
     </span>
     <span class="badge badge--accent w500">
      Краща ціна
     </span>
     <span class="badge badge--accent w500">
      Кредит до 1 року під 0.01%
     </span>
    </div>
    <div class="proposition_description size14">
     Skoda Octavia A8 Selection Plus в наявності

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
    </div>
   </div>
  </div>
 </a>
</article>


--- ФАЙЛ: traceback.txt ---


---

# AVAILABLE FILES

При анализе могут быть приложены один или несколько файлов.

Например:

- description.txt
- page.html
- network.har
- cookies.json
- headers.json
- response.json
- screenshots
- project_tree.txt
- project_for_ai.txt

Используй только те файлы, которые действительно были предоставлены.
Не предполагай наличие отсутствующих файлов.

---

# YOUR TASK

Выполни полный анализ проекта.
Ответ должен состоять из следующих разделов.

## 1. Краткое описание задачи

Опиши своими словами, что хочет получить клиент.

---

## 2. Какой конечный результат нужен

Например:

- CSV
- Excel
- JSON
- Database
- API
- изображения
- PDF
- другой формат

---

## 3. Как лучше решить задачу

Если действительно требуется комбинация методов (например API + Playwright), выбери её и объясни почему.

Например

- requests
- BeautifulSoup
- Playwright
- Scrapy
- Selenium
- API
- комбинация нескольких методов

Обязательно объясни почему.

---

## 4. Почему остальные варианты хуже

Кратко объясни, почему ты НЕ рекомендуешь использовать остальные подходы.

---

## 5. Анализ сайта

Определи насколько это возможно.

Есть ли:

- JavaScript Rendering
- React
- Vue
- Angular
- API
- GraphQL
- Infinite Scroll
- Pagination
- Login
- Cookies
- JWT
- Bearer Token
- CAPTCHA
- Cloudflare
- Rate Limits
- Download Files
- Upload Files
- Lazy Loading
- WebSocket
- XHR/Fetch
- Sitemap
- robots.txt

Если определить невозможно — так и напиши.

---

## 6. Что необходимо собрать до начала разработки

Какие данные необходимо получить до начала разработки.

Например

- page.html
- network.har
- cookies
- response.json
- пример CSV
- пример Excel
- скриншоты
- тестовый аккаунт
- пример ожидаемого результата
- образец выходного файла

Если что-либо необходимо —
перечисли это.

---

## 7. Возможные сложности

Перечисли потенциальные проблемы.

Например

- блокировки
- изменение HTML
- скрытый API
- динамическая загрузка
- авторизация
- ограничение скорости
- большое количество страниц

---

## 8. Что нужно уточнить у клиента

Если информации недостаточно —
составь список вопросов клиенту.
Не придумывай ответы самостоятельно.

---

## 9. Рекомендуемый стек технологий

Укажи только основные технологии, которые будут использоваться.

Например:

- Python
- Playwright
- BeautifulSoup
- requests
- API

Не перечисляй конкретные библиотеки для установки.

Не составляй requirements.txt.


---

## 10. План разработки

Разбей проект на логические этапы разработки.

Каждый этап должен содержать:

- цель;
- ожидаемый результат;
- зависимости (если есть).

---

## 11. Оценка сложности

Оцени:

- сложность (1–10);
- время на разработки - (Estimation в часах)
- вероятность блокировок;
- вероятность необходимости использования браузера;
- вероятность изменения сайта в будущем;
- общую оценку риска.

---

## 12. Можно ли решить проще

---
Определи можно ли выполнить проект более простым способом.

Например:

API вместо HTML.
Активно искать API в network.har или через консоль разработчика
requests вместо Playwright.
CSV вместо базы данных.
Если существует более простое решение —
обязательно предложи его.

## 13. Итоговая рекомендация

Кратко подведи итог.

Ответь:

- Какое решение рекомендуется.
- Почему оно оптимально.
- Что необходимо получить перед началом разработки.
- Можно ли переходить к написанию кода или сначала нужно дождаться ответов клиента.


# IMPORTANT RULES

НЕ переходи к реализации.
НЕ проектируй архитектуру классов.
НЕ предлагай реализацию функций.
НЕ предлагай  структуру каталогов.
НЕ генерируй код.
НЕ создавай Dockerfile.
НЕ создавай requirements.txt.
Не делай предположений, если информации недостаточно.
Явно указывай уровень уверенности в своих выводах.

# SELF-CHECK

Перед отправкой ответа проверь:
□ Я не написал код.
□ Я не начал проектировать функции.
□ Я выбрал наиболее подходящую технологию.
□ Я перечислил возможные риски.
□ Я указал, какой информации не хватает.
□ Я сформировал список вопросов клиенту.
□ Я предложил наиболее простое решение.
□ Я не усложнил архитектуру без необходимости.
Если хотя бы один пункт не выполнен — исправь ответ перед отправкой.
