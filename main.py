# main.py
import argparse
import logging

from src.ingest.extract import backfill
from src.ingest.load import load_raw_observations

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)


def main():
    parser = argparse.ArgumentParser(description="eBird ingestion pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backfill_parser = subparsers.add_parser("backfill", help="Fetch historic observations")
    backfill_parser.add_argument("region_code")
    backfill_parser.add_argument("--days", type=int, default=30)

    load_parser = subparsers.add_parser("load", help="Load raw JSON into DuckDB")

    args = parser.parse_args()

    if args.command == "backfill":
        backfill(args.region_code, days=args.days)
    elif args.command == "load":
        load_raw_observations()


if __name__ == "__main__":
    main()
