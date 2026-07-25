import requests
from .config import EBIRD_API_KEY, EBIRD_BASE_URL


class EBirdClient:
    """
    A thin, authenticated wrapper around the eBird REST API.

    Holds a single requests.Session (with the API key attached as a default
    header) so that connection pooling and auth are handled once, rather than
    repeated on every call. Each public method maps to one eBird endpoint and
    returns the parsed JSON response as-is — no cleaning or validation here;
    that belongs to the staging layer downstream.

    """

    def __init__(
        self, api_key: str = EBIRD_API_KEY, base_url: str = EBIRD_BASE_URL
    ) -> None:
        """Set up the HTTP session used for every request this client makes.

        Args:
        api_key: eBird API key, sent as the X-eBirdApiToken header.
        base_url: Root URL for the eBird API (versioned, e.g. .../v2).
        """
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({"X-eBirdApiToken": api_key})

    def get_recent_observations(self, region_code: str) -> list[dict]:
        """Fetch the most recent observations for a region.

        Note: this is a rolling window (eBird's own recent-activity default),
        not a fixed date — the same call made on different days returns
        different, overlapping results. Not suitable for backfilling or
        repeatable daily ingestion; use get_historic_observations for that.

        Args:
            region_code: eBird region code (country, state/province, or county).
        Returns:
        A list of observation records as returned by the API.
        """
        url = f"{self.base_url}/data/obs/{region_code}/recent"
        response = self._session.get(url, timeout=(5, 15))
        response.raise_for_status()
        return response.json()

    def get_historic_observations(
        self, region_code: str, year: int, month: int, day: int
    ) -> list[dict]:
        """Fetch all observations for a region on one specific calendar date.

        Unlike get_recent_observations, this endpoint is idempotent — the
        same date always returns the same complete set of sightings, making
        it the right source for backfilling or scheduled daily ingestion.

        Args:
            region_code: eBird region code (country, state/province, or county).
            year, month, day: The exact calendar date to fetch.

        Returns:
            A list of observation records as returned by the API.
        """
        url = f"{self.base_url}/data/obs/{region_code}/historic/{year}/{month}/{day}"
        response = self._session.get(url, timeout=(5, 60))
        response.raise_for_status()
        return response.json()
