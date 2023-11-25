import logging
from urllib.parse import urljoin

import requests
from requests import Response

from strava_data.strava_client.models.SegmentModel import SegmentModel
from windy_kom_hunter import settings

logger = logging.getLogger(__name__)


class StravaAPIFetchError(Exception):
    def __init__(self, response: Response | None, url: str | None):
        error_str = f"Strava API call failed for: {url}"
        if response:
            error_str += f" with code {response.status_code}: {response.text}"
        super().__init__(error_str)


class StravaAPIConnectionError(ConnectionError):
    pass


class StravaClient:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_starred_segments(self):
        base_url = settings.STRAVA_API_BASE_URL
        query_url = settings.STARRED_SEGMENTS_URL
        url = urljoin(base_url, query_url)
        header = {"Authorization": f"Bearer {self.access_token}"}

        logger.info("Getting starred segments")
        try:
            starred_segments_response = requests.get(url, headers=header)
            print(starred_segments_response.json())
        except ConnectionError as e:
            raise StravaAPIConnectionError from e
        except Exception as e:
            raise StravaAPIFetchError(starred_segments_response, url) from e
        if starred_segments_response.status_code != 200:
            raise StravaAPIFetchError(starred_segments_response, url)
        return [
            SegmentModel(**starred_segments_dict)
            for starred_segments_dict in starred_segments_response.json()
        ]


if __name__ == "__main__":
    a = StravaClient(access_token=settings.ACCESS_TOKEN).get_starred_segments()
