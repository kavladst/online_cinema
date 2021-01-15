import hmac
from base64 import b64encode
from copy import deepcopy
from hashlib import sha256
from typing import Dict, Any, List, Optional

from tests.functional.settings import AUTH_SECRET_KEY


def get_expected_not_found_details(entity_name: str) -> dict:
    return {'detail': f'{entity_name} not found'}


def get_expected_age_limit_error_details() -> dict:
    return {'detail': 'film with an age limit'}


def get_valid_access_token() -> str:
    hashed_header = b64encode(str({'alg': 'HS256'}).encode())
    hashed_payload = b64encode(str({'exp': 9999999999}).encode())

    signature = hmac.new(
        AUTH_SECRET_KEY.encode(),
        hashed_header + hashed_payload,
        digestmod=sha256
    ).hexdigest()

    return f'{hashed_header.decode()}.{hashed_payload.decode()}.{signature}'


def get_expected_film(film: Dict[str, Any]) -> Dict[str, Any]:
    expected_film = deepcopy(film)
    expected_film['uuid'] = expected_film.pop('id')
    expected_film.pop('age_limit')
    for genre in expected_film['genre']:
        genre['uuid'] = genre.pop('id')
    for person_type in ['actors', 'writers', 'directors']:
        for person in expected_film[person_type]:
            person['uuid'] = person.pop('id')
            person['full_name'] = person.pop('name')
        expected_film.pop(f'{person_type}_names')
    return expected_film


def get_expected_short_film(film: Dict[str, Any]) -> dict:
    return {'uuid': film['id'], 'title': film['title'], 'imdb_rating': film['imdb_rating']}


def get_expected_list_film(
        films: List[Dict[str, Any]],
        page_size: int = 20,
        page_number: int = 1,
        sort_field: str = 'imdb_rating',
        sort_order: str = 'desc',
        filter_by_actor_id: Optional[str] = None,
        filter_by_writer_id: Optional[str] = None,
        filter_by_director_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    expected_list_film = [
        film for film in films
        if (
                (
                        (filter_by_actor_id is None) or
                        (filter_by_actor_id in [actor['id'] for actor in film['actors']])
                ) and
                (
                        (filter_by_writer_id is None) or
                        (filter_by_writer_id in [writer['id'] for writer in film['writers']])
                ) and
                (
                        (filter_by_director_id is None) or
                        (filter_by_director_id in [director['id'] for director in film['directors']])
                )
        )
    ]
    expected_list_film = sorted(expected_list_film, key=lambda film: film[sort_field], reverse=(sort_order == 'desc'))
    expected_list_film = [get_expected_short_film(film) for film in expected_list_film]
    return expected_list_film[(page_number - 1): (page_number - 1) + page_size]


def get_expected_genre(genre: Dict[str, Any], related_films: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    if related_films is None:
        related_films = []
    expected_genre = {'uuid': genre['id'], 'name': genre['name']}
    expected_genre['films'] = [
        get_expected_short_film(film) for film in related_films
        if expected_genre['name'] in [genre['name'] for genre in film['genre']]
    ]
    return expected_genre


def get_expected_short_genre(genre: Dict[str, Any]) -> Dict[str, Any]:
    return {'uuid': genre['id'], 'name': genre['name']}


def get_expected_list_genre(
        genres: List[Dict[str, Any]],
        page_size: int = 20,
        page_number: int = 1,
        sort_field: str = 'name',
        sort_order: str = 'asc'
) -> List[Dict[str, Any]]:
    expected_list_genre = sorted(genres, key=lambda genre: genre[sort_field], reverse=(sort_order == 'desc'))
    expected_list_genre = [get_expected_short_genre(genre) for genre in expected_list_genre]
    return expected_list_genre[(page_number - 1): (page_number - 1) + page_size]


def get_expected_person(
        person: Dict[str, Any],
        related_films: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    if related_films is None:
        related_films = []
    expected_person = {'uuid': person['id'], 'full_name': person['full_name'], 'roles': {}}
    for role in ['actor', 'writer', 'director']:
        expected_person['roles'][role] = []
        for film in related_films:
            if expected_person['full_name'] in [person['name'] for person in film[f'{role}s']]:
                expected_person['roles'][role].append(get_expected_short_film(film))
    return expected_person


def get_expected_short_person(person: Dict[str, Any]) -> Dict[str, Any]:
    return {'uuid': person['id'], 'full_name': person['full_name']}


def get_expected_list_person(
        persons: List[Dict[str, Any]],
        page_size: int = 20,
        page_number: int = 1,
        sort_field: str = 'full_name',
        sort_order: str = 'asc'
) -> List[Dict[str, Any]]:
    expected_list_person = sorted(persons, key=lambda person: person[sort_field], reverse=(sort_order == 'desc'))
    expected_list_person = [get_expected_short_person(person) for person in expected_list_person]
    return expected_list_person[(page_number - 1): (page_number - 1) + page_size]
