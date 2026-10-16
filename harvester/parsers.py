from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re


class BaseParser(ABC):
    """Abstract interface for HTML page parsing."""

    @abstractmethod
    def parse(self, html_content: str, base_url: str) -> List[Dict[str, Any]]:
        pass


class BooksScraperParser(BaseParser):
    """
    Parser for e-commerce catalog demo (books.toscrape.com).
    Demonstrates CSS selectors, regex data normalization, and defensive parsing.
    """

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def parse(self, html_content: str, base_url: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html_content, "html.parser")
        items = []

        articles = soup.select("article.product_pod")
        for article in articles:
            # 1. Extract Title
            title_tag = article.select_one("h3 a")
            title = title_tag.get("title", "").strip() if title_tag else "Unknown"

            # 2. Extract Relative & Full URL
            rel_url = title_tag.get("href", "") if title_tag else ""
            product_url = urljoin(base_url, rel_url)

            # 3. Extract Price (e.g. £51.77 -> float 51.77)
            price_tag = article.select_one(".price_color")
            price_raw = price_tag.text.strip() if price_tag else "0.0"
            price_match = re.search(r"[\d\.]+", price_raw)
            price = float(price_match.group()) if price_match else 0.0

            # 4. Extract Star Rating
            rating_tag = article.select_one("p.star-rating")
            rating_val = 0
            if rating_tag:
                classes = rating_tag.get("class", [])
                for cls in classes:
                    if cls in self.RATING_MAP:
                        rating_val = self.RATING_MAP[cls]
                        break

            # 5. Extract Availability
            stock_tag = article.select_one(".availability")
            in_stock = "In stock" in (stock_tag.text if stock_tag else "")

            items.append({
                "title": title,
                "price": price,
                "currency": "GBP",
                "rating": rating_val,
                "in_stock": in_stock,
                "url": product_url
            })

        return items

    def get_next_page(self, html_content: str, current_url: str) -> Optional[str]:
        """Detects pagination 'next' button and returns the absolute URL."""
        soup = BeautifulSoup(html_content, "html.parser")
        next_tag = soup.select_one("li.next a")
        if next_tag and next_tag.get("href"):
            return urljoin(current_url, next_tag["href"])
        return None
