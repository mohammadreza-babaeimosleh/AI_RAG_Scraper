from crawl4ai import RateLimiter, CrawlerMonitor, DisplayMode, BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.async_dispatcher import SemaphoreDispatcher
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

from apps.web_crawler.utils import process_result, get_included_urls
from apps.web_crawler.confiq import browser_config, run_config, dispatcher, settings

import os
from dotenv import load_dotenv

load_dotenv()

async def crawl(include_inner_url: bool = False):
    async with AsyncWebCrawler(config=browser_config) as crawler:
        if include_inner_url:
            urls = get_included_urls(base_url=settings.BASE_URL, ns_schema=settings.NS_SCHEMA)
        else:
            urls = [settings.BASE_URL]

        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        )

        for idx, result in enumerate(results):
            if result.success:
                await process_result(result, idx)
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")




