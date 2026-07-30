# app/scraper.py

import re
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://professionele-koeling.nl"

OUTPUT_FILE = "products.csv"

CATEGORY_URLS = [
    # Add category URLs here
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}


session = requests.Session()
session.headers.update(HEADERS)


def get_soup(url):
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Request failed: {url} -> {e}")
        return None


def clean_text(value):
    if not value:
        return ""

    return re.sub(
        r"\s+",
        " ",
        value.get_text(" ", strip=True)
        if hasattr(value, "get_text")
        else str(value),
    ).strip()


def normalize_price(price):
    if not price:
        return ""

    price = price.replace("€", "")
    price = price.replace("\xa0", "")
    price = price.strip()

    price = price.replace(".", "")
    price = price.replace(",", ".")

    match = re.search(r"\d+(\.\d+)?", price)

    return match.group(0) if match else ""


def extract_image_name(url):
    if not url:
        return ""

    return url.split("/")[-1].split("?")[0]


def collect_product_urls(category_url):
    urls = set()

    soup = get_soup(category_url)

    if not soup:
        return []

    for link in soup.select("a[href]"):
        href = link.get("href")

        if not href:
            continue

        url = urljoin(BASE_URL, href)

        if "/product/" in url or "/p/" in url:
            urls.add(url)

    return list(urls)


def parse_breadcrumb(soup):
    items = []

    for el in soup.select(
        ".breadcrumb a, .breadcrumbs a, nav.breadcrumb a"
    ):
        items.append(clean_text(el))

    return " > ".join(items)


def parse_product(url):
    soup = get_soup(url)

    if not soup:
        return None

    data = {
        "URL": url,
        "Breadcrumb": "",
        "Title": "",
        "Short description": "",
        "imageurl": "",
        "image_name": "",
        "Price": "",
        "Sale price": "",
        "Description": "",
        "Specs": "",
        "Spec_detail": "",
    }

    try:
        data["Breadcrumb"] = parse_breadcrumb(soup)

        title = soup.select_one(
            "h1.product-title, h1.entry-title, h1"
        )
        data["Title"] = clean_text(title)

        short_desc = soup.select_one(
            ".short-description, .product-summary, .excerpt"
        )
        data["Short description"] = clean_text(short_desc)

        image = soup.select_one(
            "img.product-image, .woocommerce-product-gallery img, img"
        )

        if image:
            image_url = (
                image.get("data-large_image")
                or image.get("data-src")
                or image.get("src")
            )

            if image_url:
                image_url = urljoin(BASE_URL, image_url)

                data["imageurl"] = image_url
                data["image_name"] = extract_image_name(
                    image_url
                )

        price = soup.select_one(
            ".price, .product-price, .woocommerce-Price-amount"
        )

        data["Price"] = normalize_price(clean_text(price))

        sale = soup.select_one(
            ".sale-price, .onsale, ins"
        )

        data["Sale price"] = normalize_price(clean_text(sale))

        description = soup.select_one(
            ".description, .product-description, .woocommerce-product-details__short-description"
        )

        data["Description"] = clean_text(description)

        specs = []

        for row in soup.select(
            "table tr, .specifications tr, .attributes tr"
        ):
            cols = row.find_all(["td", "th"])

            if len(cols) >= 2:
                key = clean_text(cols[0])
                value = clean_text(cols[1])

                if key and value:
                    specs.append(
                        f"{key}: {value}"
                    )

        data["Specs"] = " | ".join(specs)
        data["Spec_detail"] = "\n".join(specs)

        return data

    except Exception as e:
        print(f"Parse error {url}: {e}")
        return None


def scrape(limit=None):
    product_urls = set()

    for category in CATEGORY_URLS:
        print(f"Category: {category}")

        urls = collect_product_urls(category)

        product_urls.update(urls)

        if limit and len(product_urls) >= limit:
            break

    product_urls = list(product_urls)

    if limit:
        product_urls = product_urls[:limit]

    print(f"Found products: {len(product_urls)}")

    products = []

    for index, url in enumerate(product_urls, 1):
        print(
            f"[{index}/{len(product_urls)}] {url}"
        )

        item = parse_product(url)

        if item:
            products.append(item)

        time.sleep(1)

    return products


def save_csv(products):
    if not products:
        print("No products found")
        return

    df = pd.DataFrame(products)

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

    df = df.reindex(columns=columns)

    Path(OUTPUT_FILE).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Saved {len(df)} products to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    # First run: test with 2 products
    products = scrape(limit=2)

    save_csv(products)