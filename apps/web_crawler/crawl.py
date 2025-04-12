import asyncio
import os
import csv
from apps.web_crawler.utils import save_building_markdown
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup

def read_links_from_csv(filename="dubai_buildings_links.csv"):
    urls = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader, None)  
            for row in csv_reader:
                if row and row[0].startswith("http"):
                    urls.append(row[0])
    else:
        print(f"File {filename} not found.")
    return urls

async def extract_and_save(crawler, url: str, output_name: str = "building_detail.md"):
    run_config = CrawlerRunConfig(extraction_strategy=None, cache_mode=CacheMode.BYPASS)
    result = await crawler.arun(url, config=run_config)
    html = result.html
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1")
    title = title.text.strip() if title else "N/A"

    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.startswith("http") and not any(x in src.lower() for x in ["icon", "logo", "placeholder", "svg"]):
            images.append(f"![image]({src})")
    images_md = "\n".join(images)

    def extract_text_from_li(text):
        li = soup.find("li", string=lambda t: t and text.lower() in t.lower())
        return li.text.strip() if li else "N/A"

    location = extract_text_from_li("Location")
    developer = extract_text_from_li("Developer")
    unit_types = extract_text_from_li("Unit type")
    completion = extract_text_from_li("Date of completion")

    description = soup.get_text(separator="\n", strip=True)

    markdown_content = f"""# {title}

**Location:** {location}

**Developer:** {developer}

**Completion:** {completion}

**Description:**
{description}

## Images:
{images_md}

## Unit Types:
{unit_types}
"""
    save_building_markdown(markdown_content, output_name)
    print(f" Saved: {output_name}")

async def run_crawler_process():
    print(" Starting the crawler process.")
    
    urls = read_links_from_csv("dubai_buildings_links.csv")
    if not urls:
        print(" No links found in the CSV file.")
        return

    print(f" Found {len(urls)} URLs in the CSV file.")
    browser_config = BrowserConfig(headless=True, verbose=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in urls:
            slug = url.strip('/').split('/')[-1]
            filename = f"{slug}.md"
            try:
                await extract_and_save(crawler, url, output_name=filename)
            except Exception as e:
                print(f" Failed for {url}: {e}")
    
    print(" All links processed.")
