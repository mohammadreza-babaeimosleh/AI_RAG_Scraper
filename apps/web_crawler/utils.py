from urllib.parse import urljoin
from typing import List, Tuple 
import requests
from xml.etree import ElementTree
from urllib.parse import urljoin

import time
import random
from typing import Tuple, List

class RateLimiter:
    def __init__(self,
                 base_delay: Tuple[float, float] = (1.0, 3.0),
                 max_delay: float = 60.0,
                 max_retries: int = 3,
                 rate_limit_codes: List[int] = [429, 503]
    ):
        self.base_delay = base_delay       # e.g. (1.0, 3.0) 
        self.max_delay = max_delay         # e.g. 60.0
        self.max_retries = max_retries     # e.g. 3
        self.rate_limit_codes = rate_limit_codes

    def wait_if_needed(self, response, attempt: int=1) -> bool:
        """
        Decide whether we need to wait (and/or retry) based on the response.
        
        :param response: The HTTP response object (or status_code).
        :param attempt:  The current attempt number (1-based).
        :return: True if we are going to retry after waiting, False if not.
        """
        # If the response status code is in our rate_limit_codes, we do backoff
        if response.status_code in self.rate_limit_codes:
            # Compute a backoff delay
            delay = self._compute_delay(attempt)
            
            # Sleep for the computed delay
            print(f"Rate limit triggered (status={response.status_code}). "
                  f"Attempt #{attempt} sleeping for {delay:.2f} seconds.")
            time.sleep(delay)
            
            # Indicate that we will retry
            return True

        # If we got here, there's no need to wait for this response
        return False

    def _compute_delay(self, attempt: int) -> float:
        """
        Compute how long to wait. 
        This uses a basic exponential backoff combined with a random factor.
        """
        # For example, multiply a random base delay by 2^(attempt-1)
        # but cap it at self.max_delay
        random_base = random.uniform(*self.base_delay)
        delay = random_base * (2 ** (attempt - 1))
        return min(delay, self.max_delay)



def get_included_urls(base_url: str, ns_schema: str):

    sitemap_endpoint = "/sitemap.xml"
    full_url = urljoin(base_url, sitemap_endpoint)
    
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': ns_schema}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []


import os

def process_result(result, idx=0):

    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)

    base_filename = "result"

    filename = f"{base_filename}_{idx}.md"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result.markdown)
