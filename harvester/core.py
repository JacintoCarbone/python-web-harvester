import logging
import random
import time
from typing import Optional, Dict, Any
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("HarvesterCore")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
]


class NetworkClient:
    """
    Robust HTTP Client wrapper with exponential backoff,
    dynamic User-Agent headers, and automatic retries.
    """

    def __init__(self, base_delay: float = 1.0, max_retries: int = 3, timeout: int = 15):
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()

    def _get_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
            "Connection": "keep-alive",
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, custom_headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Executes an HTTP GET request with retries and delay.
        Returns HTML text if successful, or None on failure.
        """
        # Polite crawling delay with small random jitter
        jitter = random.uniform(0.1, 0.4)
        time.sleep(self.base_delay + jitter)

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Fetching URL (Attempt {attempt}/{self.max_retries}): {url}")
                response = self.session.get(
                    url,
                    params=params,
                    headers=self._get_headers(custom_headers),
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    return response.text
                elif response.status_code in [429, 503]:
                    backoff = (2 ** attempt) + random.uniform(0.5, 1.5)
                    logger.warning(f"Rate limited or server busy ({response.status_code}). Backing off for {backoff:.2f}s...")
                    time.sleep(backoff)
                else:
                    logger.error(f"HTTP Error {response.status_code} for {url}")
                    return None

            except requests.RequestException as e:
                logger.warning(f"Connection error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts.")
                    return None
        return None
