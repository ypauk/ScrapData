Прочитал prompt по ссылке и выполнил требования из него: нужен только app/scraper.py, без requests/httpx, с использованием переданного PlaywrightEngine, с возвратом List[str] HTML-страниц товаров и без бизнес-парсинга. Контракт scrape_data(engine) -> List[str] и ограничения по модулю взяты из указанного prompt. 
GitHub
+1

Модуль делает:

открывает стартовую категорию через PlaywrightEngine;

получает HTML страниц категорий;

извлекает URL товаров только для навигации;

открывает страницы товаров;

возвращает список HTML-строк для последующего парсинга в parser.py.

Python
Run
#!/usr/bin/env python3
                        f"[{__file__}] failed loading product "
                        f"{product_url}: {exc}"
                    )


            current_url = _get_next_page_url(
                listing_html,
                current_url,
            )


            # Для тестовой задачи достаточно 2 товаров.
            # Ограничиваем результат после получения двух страниц товара.
            if len(raw_contents) >= 2:
                break


    except Exception as exc:
        print(f"[{__file__}] scraper fatal error: {exc}")


    print(
        f"[{__file__}] scraper finished, pages collected: "
        f"{len(raw_contents)}"
    )


    return raw_contents




def _extract_product_urls(html: str) -> List[str]:
    """
    Извлекает URL товаров из HTML категории.


    Это навигационная логика, а не извлечение данных товара.
    """


    urls = []


    try:
        soup = BeautifulSoup(html, "html.parser")


        selectors = [
            "li.item a.product-image",
            "li.item h2.product-name a",
            "h2.product-name a",
            "a.product-image",
        ]


        for selector in selectors:
            for link in soup.select(selector):


                href = link.get("href")


                if not href:
                    continue


                absolute_url = urljoin(BASE_URL, href)


                if absolute_url not in urls:
                    urls.append(absolute_url)


            if urls:
                break


    except Exception as exc:
        print(
            f"[{__file__}] product url extraction error: {exc}"
        )


    return urls




def _get_next_page_url(html: str, current_url: str):
    """
    Находит следующую страницу категории.
    """


    try:
        soup = BeautifulSoup(html, "html.parser")


        next_link = soup.select_one(
            "a.next"
        )


        if next_link and next_link.get("href"):
            return urljoin(
                current_url,
                next_link["href"],
            )


    except Exception as exc:
        print(
            f"[{__file__}] pagination parsing error: {exc}"
        )


    return None

Проверка локально:

Bash
python main.py

или, если в проекте есть тестовый запуск:

Bash
python -m app.scraper