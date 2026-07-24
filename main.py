# main.py
import argparse
import logging

from src.ingest.extract import backfill

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

def main():
    parser = argparse.ArgumentParser(description="eBird ingestion pipeline")
    parser.add_argument("region_code", help="eBird region code, e.g. US-NY")
    parser.add_argument("--days", type=int, default=30, help="Number of days to backfill")
    args = parser.parse_args()

    backfill(args.region_code, days=args.days)

if __name__ == "__main__":
    main()
