# from crawl4ai import RateLimiter, CrawlerMonitor, DisplayMode, BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode
# from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
# from crawl4ai.async_dispatcher import SemaphoreDispatcher
# from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
# from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
# from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

# from apps.web_crawler.utils import process_result, get_included_urls
# from apps.web_crawler.confiq import browser_config, run_config, dispatcher, settings

# import os
# from dotenv import load_dotenv

# load_dotenv()

# async def crawl(include_inner_url: bool = False):
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         if include_inner_url:
#             urls = get_included_urls(base_url=settings.BASE_URL, ns_schema=settings.NS_SCHEMA)
#         else:
#             urls = [settings.BASE_URL]

#         results = await crawler.arun_many(
#             urls=urls,
#             config=run_config,
#             dispatcher=dispatcher
#         )

#         for idx, result in enumerate(results):
#             if result.success:
#                 await process_result(result, idx)
#             else:
#                 print(f"Failed to crawl {result.url}: {result.error_message}")




from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from apps.web_crawler.config import BASE_URL, get_chrome_driver
from apps.web_crawler.utils import save_links_to_file

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def crawl_dubai_buildings():
    driver = get_chrome_driver()
    driver.get(BASE_URL)

    building_links = set()
    page_number = 1

    while True:
        print(f"in progress {page_number}...")

        for _ in range(3):
            scroll_down(driver)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/buildings/')]"))
            )
        except:
            print("Error to load ")

        buildings = driver.find_elements(By.XPATH, "//a[contains(@href, '/buildings/')]")

        for building in buildings:
            link = building.get_attribute("href")
            if link and "/buildings/" in link and "/page/" not in link:
                building_links.add(link)

        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            driver.execute_script("arguments[0].click();", next_button)
            page_number += 1
            time.sleep(5)
        except:
            print("There is no next page. Scraping complete.")
            break

    driver.quit()
    print(f"All buildings are : {len(building_links)}")
    save_links_to_file(building_links)
    print("Links saved.")
