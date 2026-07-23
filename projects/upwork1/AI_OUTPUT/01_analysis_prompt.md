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

URL:

Поля для извлечения:

Summary
OVERVIEW: We are a recruitment business building an accurate contact database of UK care homes. We already know WHICH homes we need - your job is to find and verify the correct named decision-maker and contact details for each one, and enter them into a spreadsheet we provide. Accuracy is the number one priority. We verify every submission against the official CQC register and against our own records, so guessed, padded or generic-only entries will be rejected and returned for correction before payment.

WHAT WE PROVIDE:
- A list of the specific care homes we need contacts for (name, town, postcode).
- A blank Google Sheet to enter your findings into. It has a worked SAMPLE ROW at the top showing the exact format required - please copy that format exactly. You will NOT have access to our main database; you work only in the sheet we share.

WHAT YOU DO - FOR EACH HOME ON THE LIST:
Find and enter the following into the columns provided:
- First Name, Last Name of the correct named contact (see targeting rules below)
- Job Title (use the wording shown in the sample)
- Company Type (as shown in the sample dropdown options)
- CSA: always enter "No"
- Tier: always enter "3"
- Company Name (the care home name), HYPERLINKED to the home's OWN website (not a directory, not the CQC page)
- Region, Postal Town
- Email - a direct/named email where possible

TARGETING RULES - WHO TO CONTACT (based on operator size, which you must verify from the operator's website, CQC record or LinkedIn - do not guess):
- BAND A (independent/single home, ~under 40 beds): target the Registered Manager / Home Manager. Fallback: Owner / Director.
- BAND B (mid-size, ~40-80 beds, or 2-10 homes in a group): target the Operations Director / Director of Care, or Group HR / Recruitment Manager. Fallback: individual Home Manager.
- BAND C (large group, 80+ beds or 10+ homes): target the HR Director / Head of HR, or Head of Recruitment / Talent Acquisition. Fallback: Operations Director. Do NOT use an individual home manager as primary for Band C.
Always find the top role first; only use the fallback if the top role genuinely cannot be found, and note why.

RULES FOR EVERY ROW:
- One NAMED person per home, not a department inbox. If only a generic inbox (info@, hr@, careers@) exists, still record it but clearly flag it as "generic - no named POC found". Do not pass a generic inbox off as a named contact.
- Record the source (website/LinkedIn URL) where you found the contact so we can verify it.
- No guessing and no filler. If you cannot find something, flag it - do not invent it.

PROCESS & PAYMENT:
- Work is delivered in the shared sheet only. We review, de-duplicate and run our Do Not Contact checks on our side before anything is used.
- Fixed price is per batch/region. Payment is released once we have verified that batch for accuracy and completeness against CQC.
- We will start with one region as a paid trial. Strong, accurate work leads to ongoing batches across all remaining UK regions.

TO APPLY: Briefly tell us (1) your experience with B2B/contact research and data entry, (2) how you would confirm a care operator's size and find the right named decision-maker, and (3) answer the screening question about your method.

--- ФАЙЛ: answers.txt ---


--- ФАЙЛ: cookies.json ---
[]


--- ФАЙЛ: headers.json ---
{}


--- ФАЙЛ: network.har ---


--- ФАЙЛ: notes.txt ---


--- СЖАТЫЙ HTML: page.html ---


--- ФАЙЛ: proxies.txt ---


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
