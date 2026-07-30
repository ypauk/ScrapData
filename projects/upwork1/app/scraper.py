"""
app/scraper.py

Website scraper layer.

Responsibilities:
- Fetch category pages
- Collect product URLs
- Save raw HTML snapshots
- Provide URLs for parser.py

Stack:
requests + BeautifulSoup
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.professionele-koeling.nl"

START_URLS = [
    f"{BASE_URL}/koelkasten-kisten.html",
]

DATA_DIR = "data/raw_html"
OUTPUT_FILE = "data/product_urls.json"

REQUEST_TIMEOUT = 30
DELAY_SECONDS = 1


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}


def ensure_directories() -> None:
    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )


def fetch_page(url: str) -> str | None:
    """
    Download page HTML.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException as exc:
        print(
            f"Request failed: {url}"
        )
        print(exc)

        return None

def fetch_page_data(url: str) -> dict:
    """
    Fetch page data for main.py.

    Returns:
        {
            "url": url,
            "html": html,
            "soup": BeautifulSoup object
        }
    """

    html = fetch_page(url)

    if not html:
        return {
            "url": url,
            "html": "",
            "soup": None,
        }

    return {
        "url": url,
        "html": html,
        "soup": BeautifulSoup(
            html,
            "lxml"
        ),
    }


def save_html(
    html: str,
    name: str,
) -> str:
    """
    Save raw HTML snapshot.
    """

    filename = (
        f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    path = os.path.join(
        DATA_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(html)

    return path


def extract_links(
    html: str,
) -> list[str]:
    """
    Extract product URLs from category HTML.
    """

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    urls = []

    for link in soup.select(
        "a[href]"
    ):
        href = link.get("href")

        if not href:
            continue

        url = urljoin(
            BASE_URL,
            href
        )

        if (
            url.startswith(BASE_URL)
            and ".html" in url
        ):
            urls.append(url)

    return list(
        dict.fromkeys(urls)
    )


def scrape_category(
    url: str,
) -> list[str]:
    """
    Scrape one category page.
    """

    print(
        f"Downloading: {url}"
    )

    html = fetch_page(url)

    if not html:
        return []

    save_html(
        html,
        "category"
    )

    return extract_links(
        html
    )


def save_urls(
    urls: list[str],
) -> None:

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            urls,
            file,
            indent=2,
            ensure_ascii=False,
        )


def load_urls() -> list[str]:
    """
    Helper for parser.py
    """

    if not os.path.exists(
        OUTPUT_FILE
    ):
        return []

    with open(
        OUTPUT_FILE,
        encoding="utf-8",
    ) as file:

        return json.load(file)


def main() -> None:

    ensure_directories()

    all_urls = []

    for category in START_URLS:

        urls = scrape_category(
            category
        )

        all_urls.extend(
            urls
        )

        time.sleep(
            DELAY_SECONDS
        )


    all_urls = list(
        dict.fromkeys(all_urls)
    )

    save_urls(
        all_urls
    )

    print(
        f"Collected URLs: {len(all_urls)}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()