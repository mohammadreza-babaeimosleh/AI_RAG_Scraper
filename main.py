
import sys
import os
from apps.web_crawler.crawl import scrape_building_detail, scrape_multiple_buildings

def main():
    if len(sys.argv) < 2:
        print(" Usage: python main.py --input <URL or .txt file>")
        return

    if sys.argv[1] != "--input":
        print(" Invalid argument. Use --input")
        return

    input_arg = sys.argv[2]

    if input_arg.endswith(".txt") and os.path.exists(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        if not urls:
            print("⚠️ No URLs found in the file.")
            return
        print(f" Running in multi-url mode with {len(urls)} links from {input_arg}")
        scrape_multiple_buildings(urls)

    elif input_arg.startswith("http"):
        print(" Running in single-url mode.")
        scrape_building_detail(input_arg)
    else:
        print(" Invalid input. Provide a URL or path to a .txt file.")

if __name__ == "__main__":
    main()
