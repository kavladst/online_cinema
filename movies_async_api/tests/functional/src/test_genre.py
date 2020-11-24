import time
from typing import List, Dict, Tuple, Any

import pytest

from tests.functional.testdata.es_index_data import ES_GENRES_INDEX_NAME, ES_MOVIES_INDEX_NAME
from tests.functional.testdata import genre_samples
from tests.functional.testdata.genre_samples import get_expected_genre, get_expected_list_genre
from tests.functional.utils.api_worker import get_from_api


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_GENRES_INDEX_NAME, genre_samples.GENRE_SAMPLES_1[0])] +
        [(ES_MOVIES_INDEX_NAME, film) for film in genre_samples.RELATED_FILM_SAMPLES_1],
    ],
    indirect=True
)
def test_get_genre_details(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    films = [_[1] for _ in es_data_setup if _[0] == ES_MOVIES_INDEX_NAME]
    genre = es_data_setup[0][1]
    time.sleep(1)
    response = get_from_api(f"genre/{genre['id']}/")
    assert response == get_expected_genre(genre, films)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_GENRES_INDEX_NAME, genre) for genre in genre_samples.GENRE_SAMPLES_1]
    ],
    indirect=True
)
def test_get_all_genres(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    genres = [_[1] for _ in es_data_setup]
    response = get_from_api("genre/")
    assert response == get_expected_list_genre(genres)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_GENRES_INDEX_NAME, genre) for genre in genre_samples.GENRE_SAMPLES_1],
    ],
    indirect=True
)
def test_pagination_genres(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    genres = [_[1] for _ in es_data_setup]
    count_pages = 5
    page_size = len(genres) // count_pages
    if len(genres) % count_pages:
        count_pages += 1
    for page_number in range(1, count_pages + 1):
        response = get_from_api("genre", {"page[number]": page_number, "page[size]": page_size})
        assert response == get_expected_list_genre(genres, page_number=page_number, page_size=page_size)


@pytest.mark.parametrize(
    "redis_data_setup",
    [
        [(f"Genre_{genre_samples.GENRE_SAMPLES_1[0]['id']}", genre_samples.GENRE_SAMPLES_1[0])]
    ],
    indirect=True
)
def test_cached_genre(redis_data_setup: List[Tuple[str, Any]]):
    genre_data = redis_data_setup[0][1]
    response = get_from_api(f"genre/{genre_data['id']}/")
    assert response == get_expected_genre(genre_data)
