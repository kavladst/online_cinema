import requests
from typing import Optional

from tests.functional.settings import API_URL


def get_from_api(route: str, params: Optional[dict] = None) -> dict:
    if params is None:
        params = {}
    response = requests.get(f"{API_URL}v1/{route}", params=params)
    assert response.status_code == 200
    return response.json()
