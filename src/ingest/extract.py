import time
import json
import logging
from datetime import date, timedelta
from pathlib import Path

from .client import EBirdClient

logger = logging.getLogger(__name__)


def save_recent_observations(
    region_code: str, client: EBirdClient | None = None
) -> Path:
    """Fetch recent observations for a region and write them to the raw data lake.

    Orchestration only: get_recent_observations decides how to talk to the
    API, this function decides what to do with the result (write to disk,
    partitioned by today's date). Intended for ad-hoc/manual use rather than
    the main ingestion path, since /recent is not idempotent — see
    get_recent_observations for why.

    Args:
        region_code: eBird region code to fetch.
        client: Reuse an existing EBirdClient (e.g. across a loop), or leave
        as None to create one internally.

    Returns:
        Path to the JSON file that was written.
    """
    client = client or EBirdClient()
    observations = client.get_recent_observations(region_code)

    output_dir = Path("data/raw/observations") / f"date={date.today()}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{region_code}.json"

    output_path.write_text(json.dumps(observations, ensure_ascii=False))
    logger.info("Wrote %d observations to %s", len(observations), output_path)
    return output_path


def save_historic_observations(
    region_code: str, obs_date: date, client: EBirdClient | None = None
) -> Path:
    """
    Fetch one day's historic observations and write them to the raw data lake.

    This is the core ingestion primitive: one region, one exact date, one
    file. Partitions by obs_date (the actual observation date), not today's
    date, so this works correctly whether called for today, yesterday, or
    as part of a historical backfill.

    Args:
        region_code: eBird region code to fetch.
        obs_date: The calendar date to fetch observations for.
        client: Reuse an existing EBirdClient (e.g. across a loop), or leave
        as None to create one internally.

    Returns:
        Path to the JSON file that was written.
    """
    client = client or EBirdClient()
    observations = client.get_historic_observations(
        region_code, obs_date.year, obs_date.month, obs_date.day
    )

    output_dir = Path("data/raw/observations") / f"date={obs_date}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{region_code}.json"

    output_path.write_text(json.dumps(observations, ensure_ascii=False))
    logger.info(
        "Wrote %d observations for %s to %s", len(observations), obs_date, output_path
    )
    return output_path


def backfill(
    region_code: str,
    days: int = 30,
    client: EBirdClient | None = None,
    delay_seconds: float = 5.0,
) -> None:
    """
    Backfill historic observations for the last `days` calendar days.

    Calls save_historic_observations once per day, walking backward from
    today using date arithmetic (so month/year boundaries and leap years are
    handled automatically, not hand-coded). A single client is built once
    and reused across every call, to share one session/connection rather
    than opening a new one per day.

    A failure on any single day is logged and skipped, rather than aborting
    the whole backfill — one bad day (e.g. a network timeout) shouldn't cost
    you the other 29.

    Args:
        region_code: eBird region code to backfill.
        days: How many days back from today to fetch.
        client: Reuse an existing EBirdClient, or leave as None to create one.
    """
    client = client or EBirdClient()
    start = date.today() - timedelta(days=days)
    current = start

    while current < date.today():
        try:
            save_historic_observations(region_code, current, client=client)
        except Exception:
            logger.error(
                "Failed to fetch/save observations for %s", current, exc_info=True
            )
        current += timedelta(days=1)
        time.sleep(delay_seconds)
