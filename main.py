import asyncio
from apps.building_scraper.crawler import crawl_dubai_buildings
from apps.web_crawler.crawl import run_crawler_process

async def main():
    print(" STEP 1: Crawling buildings...")
    crawl_dubai_buildings() 

    print("\n STEP 2: Scraping building content...")
    await run_crawler_process()

if __name__ == "__main__":
    asyncio.run(main())
