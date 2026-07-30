"""
app/parser.py

Scraper for professionele-koeling.nl

Requirements:
    pip install requests beautifulsoup4 pandas lxml
"""

from __future__ import annotations

import os
import re
import time
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.professionele-koeling.nl"
CATEGORY_URL = f"{BASE_URL}/koelkasten-kisten.html"

OUTPUT_FILE = "test_products.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 30
TEST_LIMIT = 2


def clean_text(value: str | None) -> str:
    if not value:
        return ""

    return re.sub(
        r"\s+",
        " ",
        value.replace("\xa0", " ")
    ).strip()


def normalize_price(value: str | None) -> str:
    if not value:
        return ""

    value = value.replace("€", "")
    value = value.replace(".", "")
    value = value.replace(",", ".")
    value = re.sub(r"[^0-9.]", "", value)

    return value


def get_soup(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    except Exception as exc:
        print(f"Failed: {url} -> {exc}")
        return None


def extract_product_links(category_url: str) -> list[str]:
    soup = get_soup(category_url)

    if not soup:
        return []

    links = []

    for a in soup.select("a[href]"):
        href = a.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if (
            url.startswith(BASE_URL)
            and url != category_url
            and ".html" in url
        ):
            links.append(url)

    return list(dict.fromkeys(links))


def extract_breadcrumb(soup: BeautifulSoup) -> str:
    candidates = [
        ".breadcrumb",
        ".breadcrumbs",
        "nav.breadcrumb",
    ]

    for selector in candidates:
        block = soup.select_one(selector)

        if block:
            return clean_text(block.get_text(" "))

    return ""


def extract_title(soup: BeautifulSoup) -> str:
    selectors = [
        "h1",
        ".product-title",
        ".page-title",
    ]

    for selector in selectors:
        item = soup.select_one(selector)

        if item:
            return clean_text(item.get_text(" "))

    return ""


def extract_description(soup: BeautifulSoup) -> str:
    selectors = [
        ".product-description",
        ".description",
        "#description",
        ".product-info",
    ]

    for selector in selectors:
        item = soup.select_one(selector)

        if item:
            return clean_text(item.get_text(" "))

    return ""


def extract_short_description(soup: BeautifulSoup) -> str:
    selectors = [
        ".short-description",
        ".product-short-description",
        ".summary",
    ]

    for selector in selectors:
        item = soup.select_one(selector)

        if item:
            return clean_text(item.get_text(" "))

    return ""


def extract_images(soup: BeautifulSoup) -> tuple[str, str]:
    selectors = [
        "img.product-image",
        ".product-image img",
        "img",
    ]

    for selector in selectors:
        img = soup.select_one(selector)

        if img:
            src = (
                img.get("data-src")
                or img.get("src")
                or ""
            )

            if src:
                url = urljoin(BASE_URL, src)
                name = os.path.basename(
                    urlparse(url).path
                )

                return url, name

    return "", ""


def extract_prices(soup: BeautifulSoup) -> tuple[str, str]:
    text = soup.get_text(" ")

    prices = re.findall(
        r"€\s*[\d\.,]+",
        text
    )

    prices = [
        normalize_price(p)
        for p in prices
    ]

    prices = [
        p for p in prices
        if p
    ]

    if len(prices) >= 2:
        return prices[0], prices[1]

    if len(prices) == 1:
        return prices[0], ""

    return "", ""


def extract_specs(soup: BeautifulSoup) -> tuple[str, str]:
    specs = []

    text = soup.get_text("\n")

    for line in text.split("\n"):
        line = clean_text(line)

        if ":" in line:
            key, value = line.split(":", 1)

            key = clean_text(key)
            value = clean_text(value)

            if key and value and len(key) < 80:
                specs.append(
                    (key, value)
                )

    names = []
    values = []

    for key, value in specs:
        names.append(key)
        values.append(value)

    return (
        ", ".join(names),
        ", ".join(values),
    )


def parse_product(url: str) -> dict:
    soup = get_soup(url)

    if not soup:
        return {
            "URL": url,
            "status": "failed",
        }

    price, sale_price = extract_prices(soup)

    image_url, image_name = extract_images(soup)

    specs, spec_detail = extract_specs(soup)

    return {
        "URL": url,
        "Breadcrumb": extract_breadcrumb(soup),
        "Title": extract_title(soup),
        "Short description": extract_short_description(soup),
        "imageurl": image_url,
        "image_name": image_name,
        "Price": price,
        "Sale price": sale_price,
        "Description": extract_description(soup),
        "Specs": specs,
        "Spec_detail": spec_detail,
    }


def save_csv(products: list[dict], filename: str) -> None:
    columns = [
        "URL",
        "Breadcrumb",
        "Title",
        "Short description",
        "imageurl",
        "image_name",
        "Price",
        "Sale price",
        "Description",
        "Specs",
        "Spec_detail",
    ]

    df = pd.DataFrame(products)

    for column in columns:
        if column not in df.columns:
            df[column] = ""

    df = df[columns]

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8-sig",
    )


def main() -> None:
    print("Collecting product URLs...")

    urls = extract_product_links(
        CATEGORY_URL
    )

    print(
        f"Found products: {len(urls)}"
    )

    urls = urls[:TEST_LIMIT]

    products = []

    for index, url in enumerate(urls, 1):
        print(
            f"[{index}/{len(urls)}] {url}"
        )

        product = parse_product(url)

        products.append(product)

        time.sleep(1)

    save_csv(
        products,
        OUTPUT_FILE
    )

    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()