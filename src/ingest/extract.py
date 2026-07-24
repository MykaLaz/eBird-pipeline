import time
import json
import logging
from datetime import date, timedelta
from pathlib import Path

from .client import EBirdClient

logger = logging.getLogger(__name__)


def save_recent_observations(region_code: str, client: EBirdClient | None = None) -> Path:
    client = client or EBirdClient()
    observations = client.get_recent_observations(region_code)

    output_dir = Path("data/raw/observations") / f"date={date.today()}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{region_code}.json"

    output_path.write_text(json.dumps(observations, ensure_ascii=False))
    logger.info("Wrote %d observations to %s", len(observations), output_path)
    return output_path

def save_historic_observations(region_code: str, obs_date: date, client: EBirdClient | None = None) -> Path:
    client = client or EBirdClient()
    observations = client.get_historic_observations(
        region_code, obs_date.year, obs_date.month, obs_date.day
    )

    output_dir = Path("data/raw/observations") / f"date={obs_date}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{region_code}.json"

    output_path.write_text(json.dumps(observations, ensure_ascii=False))
    logger.info("Wrote %d observations for %s to %s", len(observations), obs_date, output_path)
    return output_path

def backfill(region_code: str, days: int = 30, client: EBirdClient | None = None, delay_seconds: float = 5.0) -> None:
    '''
    '''
    client = client or EBirdClient()
    start = date.today() - timedelta(days=days)
    current = start

    while current < date.today():
        try:
            save_historic_observations(region_code, current, client=client)
        except Exception:
            logger.error("Failed to fetch/save observations for %s", current, exc_info=True)
        current += timedelta(days=1)
        time.sleep(delay_seconds)
