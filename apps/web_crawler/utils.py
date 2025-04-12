from urllib.parse import urljoin
from typing import List, Tuple
import requests
from xml.etree import ElementTree
import time
import random
import os

class RateLimiter:
    def __init__(
        self,
        base_delay: Tuple[float, float] = (1.0, 3.0),
        max_delay: float = 60.0,
        max_retries: int = 3,
        rate_limit_codes: List[int] = [429, 503]
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.rate_limit_codes = rate_limit_codes

    def wait_if_needed(self, response, attempt: int = 1) -> bool:
        if response.status_code in self.rate_limit_codes:
            delay = self._compute_delay(attempt)
            print(f"Rate limit triggered (status={response.status_code}). Sleeping for {delay:.2f}s.")
            time.sleep(delay)
            return True
        return False

    def _compute_delay(self, attempt: int) -> float:
        random_base = random.uniform(*self.base_delay)
        delay = random_base * (2 ** (attempt - 1))
        return min(delay, self.max_delay)


def get_included_urls(base_url: str, ns_schema: str):
    sitemap_endpoint = "/sitemap.xml"
    full_url = urljoin(base_url, sitemap_endpoint)

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        root = ElementTree.fromstring(response.content)
        namespace = {'ns': ns_schema}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


def process_result(result, idx=0):
    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)

    base_filename = "result"
    filename = f"{base_filename}_{idx}.md"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result.markdown)


import os

def save_building_markdown(content: str, filename: str = "building_detail.md"):
    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

