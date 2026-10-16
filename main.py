import argparse
import os
import sys
from harvester.core import NetworkClient, logger
from harvester.parsers import BooksScraperParser
from harvester.storage import DataExporter


def run_pipeline(max_pages: int, delay: float, export_format: str, output_dir: str):
    base_url = "https://books.toscrape.com/"
    start_url = "https://books.toscrape.com/catalogue/page-1.html"

    client = NetworkClient(base_delay=delay, max_retries=3, timeout=12)
    parser = BooksScraperParser()

    all_records = []
    current_url = start_url
    pages_scraped = 0

    print(f"[*] Starting scraper pipeline (Target limit: {max_pages} pages, Delay: {delay}s)...")

    while current_url and pages_scraped < max_pages:
        pages_scraped += 1
        html = client.get(current_url)

        if not html:
            logger.error(f"Could not retrieve page: {current_url}. Stopping pagination.")
            break

        records = parser.parse(html, base_url=current_url)
        all_records.extend(records)
        logger.info(f"Page {pages_scraped}: Scraped {len(records)} items (Total accumulated: {len(all_records)})")

        current_url = parser.get_next_page(html, current_url)
        if not current_url:
            logger.info("Reached end of pagination.")
            break

    # Exporting results
    os.makedirs(output_dir, exist_ok=True)
    if export_format in ["json", "both"]:
        json_path = os.path.join(output_dir, "scraped_data.json")
        DataExporter.export_json(all_records, json_path)

    if export_format in ["csv", "both"]:
        csv_path = os.path.join(output_dir, "scraped_data.csv")
        DataExporter.export_csv(all_records, csv_path)

    # Print summary
    DataExporter.print_analytics_summary(all_records)


def main():
    arg_parser = argparse.ArgumentParser(
        description="Enterprise Web Data Harvester & Automation Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument("--pages", type=int, default=2, help="Number of pages to crawl")
    arg_parser.add_argument("--delay", type=float, default=0.8, help="Polite delay between HTTP requests in seconds")
    arg_parser.add_argument("--format", choices=["json", "csv", "both"], default="both", help="Export file format")
    arg_parser.add_argument("--output-dir", type=str, default="output", help="Destination folder for exported data")

    args = arg_parser.parse_args()
    try:
        run_pipeline(
            max_pages=args.pages,
            delay=args.delay,
            export_format=args.format,
            output_dir=args.output_dir
        )
    except KeyboardInterrupt:
        print("\n[!] Execution stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
