import csv
import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger("StorageEngine")


class DataExporter:
    """Handles multi-format data export and validation."""

    @staticmethod
    def export_json(data: List[Dict[str, Any]], filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(data)} records to JSON: {filepath}")

    @staticmethod
    def export_csv(data: List[Dict[str, Any]], filepath: str) -> None:
        if not data:
            logger.warning("No data to export.")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fieldnames = list(data[0].keys())

        # utf-8-sig ensures Excel on Windows opens non-ASCII characters seamlessly
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Saved {len(data)} records to CSV: {filepath}")

    @staticmethod
    def print_analytics_summary(data: List[Dict[str, Any]]) -> None:
        """Prints a human-readable executive summary of the scraped dataset."""
        if not data:
            print("\n[!] No records captured.")
            return

        total_items = len(data)
        prices = [item["price"] for item in data if "price" in item and item["price"] is not None]
        avg_price = sum(prices) / len(prices) if prices else 0.0
        min_price = min(prices) if prices else 0.0
        max_price = max(prices) if prices else 0.0

        ratings = [item["rating"] for item in data if "rating" in item]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0.0

        in_stock_count = sum(1 for item in data if item.get("in_stock"))

        print("\n" + "="*50)
        print("          HARVESTER RUN SUMMARY")
        print("="*50)
        print(f" Total items collected : {total_items}")
        print(f" In-stock items        : {in_stock_count} ({in_stock_count/total_items*100:.1f}%)")
        print(f" Average price         : £{avg_price:.2f}")
        print(f" Price range           : £{min_price:.2f} - £{max_price:.2f}")
        print(f" Average rating        : {avg_rating:.2f} / 5.0")
        print("="*50 + "\n")
