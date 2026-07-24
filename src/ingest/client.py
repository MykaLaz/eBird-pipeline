import requests
from .config import EBIRD_API_KEY, EBIRD_BASE_URL


class EBirdClient:
    '''
    Make later according PEP
    '''

    def __init__(
        self, api_key: str = EBIRD_API_KEY, base_url: str = EBIRD_BASE_URL
    ) -> None:
        '''
        '''
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({"X-eBirdApiToken": api_key})

    def get_recent_observations(self, region_code: str) -> list[dict]:
        '''
        '''
        url = f"{self.base_url}/data/obs/{region_code}/recent"
        response = self._session.get(url, timeout=(5, 15))
        response.raise_for_status()
        return response.json()

    def get_historic_observations(self, region_code: str, year: int,  month: int, day: int) -> list[dict]:
        '''
        Fetch all observations for a region on one specific calendar date.

        Unlike get_recent_observations, this endpoint is idempotent — the same
        date always returns the same complete set of sightings, making it the
        right source for backfilling or scheduled daily ingestion.
        '''
        url = f'{self.base_url}/data/obs/{region_code}/historic/{year}/{month}/{day}'
        response = self._session.get(url, timeout=(5, 60))
        response.raise_for_status()
        return response.json()
