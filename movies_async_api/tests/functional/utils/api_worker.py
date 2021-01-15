import requests
from typing import Optional

from tests.functional.settings import API_URL


def get_from_api(
        route: str,
        query_params: Optional[dict] = None,
        expected_status_code: int = 200,
        header_params: Optional[dict] = None,
) -> dict:
    if header_params is None:
        header_params = {}
    if query_params is None:
        query_params = {}
    response = requests.get(f'{API_URL}v1/{route}', headers=header_params, params=query_params)
    assert response.status_code == expected_status_code
    return response.json()
