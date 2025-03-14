from crawl4ai import RateLimiter, CrawlerMonitor, DisplayMode, BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.async_dispatcher import SemaphoreDispatcher
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from apps.web_crawler.utils import RateLimiter

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple, List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    BASE_DELAY: Tuple[int, int]
    MAX_DELAY: int
    MAX_RETRIES: int
    RATE_LIMIT_CODES: List[int]
    CRAWLER_MONITOR_MAX_DISPLAY_ROWS: int
    MAX_CONCURRENT_REQUESTS: int
    SEARCH_DEPTH: int

    BASE_URL: str
    NS_SCHEMA: str

    model_config = SettingsConfigDict(env_file=".env")

# Create a single global settings object
settings = Settings()

rate_limiter = RateLimiter(
        base_delay=settings.BASE_DELAY,  
        max_delay=settings.MAX_DELAY,        
        max_retries=settings.MAX_RETRIES,         
        rate_limit_codes=settings.RATE_LIMIT_CODES  
    )

monitor = CrawlerMonitor(
        max_visible_rows=settings.CRAWLER_MONITOR_MAX_DISPLAY_ROWS,
        display_mode=DisplayMode.DETAILED 
    )

scorer = KeywordRelevanceScorer(
    keywords=["crawl", "example", "async", "configuration"],
    weight=0.7
)

strategy = BestFirstCrawlingStrategy(
    max_depth=settings.SEARCH_DEPTH,
    include_external=False,
    url_scorer=scorer,
    max_pages=1000,   
)

browser_config = BrowserConfig(headless=True, verbose=False)

run_config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2, 
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

dispatcher = SemaphoreDispatcher(
        semaphore_count=settings.MAX_CONCURRENT_REQUESTS,
        rate_limiter=rate_limiter,
        monitor=monitor,
)