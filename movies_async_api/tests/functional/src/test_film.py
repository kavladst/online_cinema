import time
from typing import List, Dict, Tuple, Any

import pytest

from tests.functional.testdata.es_index_data import ES_MOVIES_INDEX_NAME, ES_PERSONS_INDEX_NAME
from tests.functional.testdata import film_samples
from tests.functional.testdata.film_samples import get_expected_film, get_expected_list_film
from tests.functional.utils.api_worker import get_from_api


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film_samples.FILM_SAMPLES_1[0])],
    ],
    indirect=True
)
def test_get_film_details(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    film_data = es_data_setup[0][1]
    response = get_from_api(f"film/{film_data['id']}/")
    assert response == get_expected_film(film_data)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film) for film in film_samples.FILM_SAMPLES_1]
    ],
    indirect=True
)
def test_get_all_films(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    films = [_[1] for _ in es_data_setup]
    response = get_from_api("film/")
    assert response == get_expected_list_film(films)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film) for film in film_samples.FILM_SAMPLES_1],
    ],
    indirect=True
)
def test_sort_films(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    films = [_[1] for _ in es_data_setup]
    for sort_field in ["imdb_rating", "title"]:
        for sort_order in ["asc", "desc"]:
            response = get_from_api("film/", {"sort": sort_field, "sort_order": sort_order})
            assert response == get_expected_list_film(films, sort_field=sort_field, sort_order=sort_order)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film) for film in film_samples.FILM_SAMPLES_1],
    ],
    indirect=True
)
def test_pagination_films(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    films = [_[1] for _ in es_data_setup]
    count_pages = 5
    page_size = len(films) // count_pages
    if len(films) % count_pages:
        count_pages += 1
    for page_number in range(1, count_pages + 1):
        response = get_from_api("film/", {"page[number]": page_number, "page[size]": page_size})
        assert response == get_expected_list_film(films, page_number=page_number, page_size=page_size)


@pytest.mark.parametrize(
    "redis_data_setup",
    [
        [(f"Film_{film_samples.FILM_SAMPLES_1[0]['id']}", film_samples.FILM_SAMPLES_1[0])]
    ],
    indirect=True
)
def test_cached_film(redis_data_setup: List[Tuple[str, Any]]):
    film_data = redis_data_setup[0][1]
    response = get_from_api(f"film/{film_data['id']}/")
    assert response == get_expected_film(film_data)


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film) for film in film_samples.FILM_SAMPLES_1]
    ],
    indirect=True
)
def test_search_films(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    response = get_from_api("film/search", {"query": film_samples.FILM_SEARCH_QUERY_FOR_SAMPLES_1})
    assert response == film_samples.FILM_SEARCH_SAMPLES_EXPECTED_1


@pytest.mark.parametrize(
    "es_data_setup",
    [
        [(ES_MOVIES_INDEX_NAME, film) for film in film_samples.FILM_SAMPLES_1] +
        [(ES_PERSONS_INDEX_NAME, person) for person in film_samples.RELATED_PERSON_SAMPLES_1]
    ],
    indirect=True
)
def test_filter_films(es_data_setup: List[Tuple[str, Dict[str, Any]]], redis_data_setup):
    time.sleep(1)
    films = [_[1] for _ in es_data_setup if _[0] == ES_MOVIES_INDEX_NAME]
    person_ids = [_[1]["id"] for _ in es_data_setup if _[0] == ES_PERSONS_INDEX_NAME]
    for person_id in person_ids:
        response = get_from_api("film", {"filter[actor]": person_id})
        assert response == get_expected_list_film(films, filter_by_actor_id=person_id)
