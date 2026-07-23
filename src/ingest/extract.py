import json
import logging
from datetime import date
from pathlib import Path

from .client import EBirdClient

logger = logging.getLogger(__name__)


def save_observations(region_code: str, client: EBirdClient | None = None) -> Path:
    client = client or EBirdClient()
    observations = client.get_recent_observations(region_code)

    output_dir = Path("data/raw/observations") / f"date={date.today()}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{region_code}.json"

    output_path.write_text(json.dumps(observations, ensure_ascii=False))
    logger.info("Wrote %d observations to %s", len(observations), output_path)
    return output_path
