import argparse
import asyncio
import logging
from apps.web_crawler.crawl import crawl

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="python main.py --include_inner_url"
    )

    parser.add_argument(
        "--include_inner_url",
        action="store_true",
        help="If provided, include the inner URL in processing."
    )

    args = parser.parse_args()

    if args.include_inner_url:
        logger.warning("The --include_inner_url flag was set!")
        asyncio.run(crawl(include_inner_url=True))
    else:
        logger.warning("The --include_inner_url flag was NOT set.")
        asyncio.run(crawl(include_inner_url=False))

if __name__ == "__main__":
    main()
