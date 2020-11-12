import datetime
import logging
from typing import List

import backoff
import psycopg2
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

from src.config import CONFIG
from src.consts import DEFAULT_DATE, ES_MOVIES_INDEX_NAME, ES_GENRES_INDEX_NAME, ES_PERSONS_INDEX_NAME
from src.state import StateES
from src.wrappers import coroutine

logger = logging.getLogger(__name__)
DSN = {"dbname": CONFIG.DB_NAME, "user": CONFIG.DB_USER, "password": CONFIG.DB_PASSWORD, "host": CONFIG.DB_HOST,
       "port": CONFIG.DB_PORT}


def get_movies_by_ids(ids: List[str], cursor: _cursor) -> List[dict]:
    """
    Retrieves full movies data.
    """
    logger.debug(f"Looking for {len(ids)} movies")
    args = ",".join(cursor.mogrify("%s", (_id,)).decode() for _id in ids)
    cursor.execute(f"""
    SELECT
        fw.id as fw_id, 
        fw.title, 
        fw.description, 
        fw.rating, 
        fw.created_at, 
        fw.updated_at, 
        array_agg(g.name) as genres,
        array_agg(p.full_name) as names,
        array_agg(pfw.role) as roles,
        array_agg(p.id) as persons_ids
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN ({args})
    GROUP BY fw_id;
    """)
    movies = cursor.fetchall()
    logger.debug(f"Found {len(movies)} movies by ids")
    return movies


@backoff.on_exception(backoff.expo, psycopg2.errors.ConnectionException, max_time=CONFIG.PG_TIMEOUT_SEC)
@coroutine
def extract_movies_updated_due_to_movie_change(target, state: StateES):
    """
    Data producer for movies which necessary to be synced due to movies itself change.
    Assumes that if genre or person relation is added/deleted to/from movie - movie"s updated_at field will be changed.
    """
    curr_es_index = ES_MOVIES_INDEX_NAME
    with psycopg2.connect(**DSN, cursor_factory=DictCursor).cursor() as cursor:  # type: _cursor

        date_start = last_movie_synced_at = state.get_last_entity_synced_at(curr_es_index, curr_es_index)
        while updated_movies := _fetch_updated_movies(cursor, last_movie_synced_at):
            movies_ids_not_synced = [
                m["id"]
                for m in updated_movies
                if str(m["id"]) not in state.get_synced_entities(curr_es_index, curr_es_index)
            ]

            if movies_ids_not_synced:
                movies_to_send = get_movies_by_ids(movies_ids_not_synced, cursor)
                for movie in movies_to_send:
                    target.send(movie)
                    state.add_entity_synced(curr_es_index, curr_es_index, [str(movie["fw_id"])])

            logger.debug(f"Synced all movies updated after {last_movie_synced_at} Searching for more movies")
            last_movie_synced_at = updated_movies[-1]["updated_at"]
            state.set_last_entity_synced_at(curr_es_index, curr_es_index, last_movie_synced_at)

        logger.debug(f"Finished with movies updated due to movie data change after {date_start}")


@backoff.on_exception(backoff.expo, psycopg2.errors.ConnectionException, max_time=CONFIG.PG_TIMEOUT_SEC)
@coroutine
def extract_updated_movies_due_to_entity_change(entity_name: str, target, state: StateES):
    """
    Data producer for movies which necessary to be synced due to linked entities data change.
    """
    with psycopg2.connect(**DSN, cursor_factory=DictCursor).cursor() as cursor:  # type: _cursor
        date_start = last_entity_synced = state.get_last_entity_synced_at(entity_name, ES_MOVIES_INDEX_NAME)

        while updated_entities := fetch_updated_entities(entity_name, cursor, last_entity_synced):
            # we don"t care when movie"s data changed - updated_at will not be changed if person data changes
            # updated_at is used as cursor to iterate over movies
            last_movie_synced_by_entity_at = DEFAULT_DATE
            while linked_movies := fetch_movies_by_entities(entity_name, cursor, updated_entities,
                                                            last_movie_synced_by_entity_at):
                movies_ids_not_synced = [
                    m["id"]
                    for m in linked_movies
                    if str(m["id"]) not in state.get_synced_entities(ES_MOVIES_INDEX_NAME, ES_MOVIES_INDEX_NAME)
                ]

                if movies_ids_not_synced:
                    movies_to_send = get_movies_by_ids(movies_ids_not_synced, cursor)
                    for movie in movies_to_send:
                        target.send(movie)
                        state.add_entity_synced(ES_MOVIES_INDEX_NAME, ES_MOVIES_INDEX_NAME, [str(movie["fw_id"])])

                logger.debug(f"Synced all movies updated after {last_movie_synced_by_entity_at} "
                             f"for {entity_name} updated after {last_entity_synced}. Searching for more movies")

                last_movie_synced_by_entity_at = linked_movies[-1]["updated_at"]

            last_entity_synced = updated_entities[-1]["updated_at"]
            state.set_last_entity_synced_at(entity_name, ES_MOVIES_INDEX_NAME, last_entity_synced)

        logger.debug(f"All movies linked with persons updated after {date_start}, shutting down receiving coroutine")



@backoff.on_exception(backoff.expo, psycopg2.errors.ConnectionException, max_time=CONFIG.PG_TIMEOUT_SEC)
@coroutine
def extract_updated_entities(index_name: str, target, state: StateES):
    """
    Data producer for updated entities since last sync.
    """
    with psycopg2.connect(**DSN, cursor_factory=DictCursor).cursor() as cursor:  # type: _cursor
        date_start = last_entity_synced = state.get_last_entity_synced_at(index_name, index_name)

        while updated_entities := fetch_updated_entities(index_name, cursor, last_entity_synced):
            not_synced_entity = [
                entity for entity in updated_entities
                if str(entity["id"]) not in state.get_synced_entities(index_name, index_name)
            ]
            for entity in not_synced_entity:
                target.send(entity)
                state.add_entity_synced(index_name, index_name, [str(entity["id"])])

            last_entity_synced = updated_entities[-1]["updated_at"]
            logger.debug(
                f"Synced all {index_name} updated after {last_entity_synced}. Searching for more {index_name}"
            )
            state.set_last_entity_synced_at(index_name, index_name, last_entity_synced)

        logger.debug(f"All {index_name} updated after {date_start} synced, shutting down receiving coroutine")


def fetch_updated_entities(index_name: str, cursor: _cursor, updated_after: datetime.datetime) -> List[dict]:
    if index_name == ES_MOVIES_INDEX_NAME:
        return _fetch_updated_movies(cursor, updated_after)
    elif index_name == ES_GENRES_INDEX_NAME:
        return _fetch_updated_genres(cursor, updated_after)
    elif index_name == ES_PERSONS_INDEX_NAME:
        return _fetch_updated_persons(cursor, updated_after)
    else:
        raise ValueError(f"Index {index_name} does not exist in fetch_updated_entities")


def fetch_movies_by_entities(index_name: str, cursor: _cursor, entities: List[dict],
                             updated_after: datetime.datetime) -> List[dict]:
    if index_name == ES_GENRES_INDEX_NAME:
        return _fetch_movies_by_genres(cursor, entities, updated_after)
    elif index_name == ES_PERSONS_INDEX_NAME:
        return _fetch_movies_by_persons(cursor, entities, updated_after)
    else:
        raise ValueError(f"Index {index_name} does not exist in fetch_movies_by_entities")


def _fetch_updated_movies(cursor: _cursor, updated_after: datetime.datetime) -> List[dict]:
    """
    Returns all movies updated after provided date.
    """
    cursor.execute(f"""
                SELECT id, updated_at
                FROM content.film_work
                WHERE updated_at > %s
                ORDER BY updated_at
                LIMIT {CONFIG.FETCH_FROM_PG_BY};
                """, (updated_after,))

    updated_movies = cursor.fetchall()
    logger.debug(f"Fetched {len(updated_movies)} linked movies")
    return updated_movies


def _fetch_updated_genres(cursor: _cursor, updated_after: datetime.datetime) -> List[dict]:
    """
    Returns all genres updated after provided date
    """
    cursor.execute(f"""
                SELECT
                    id,
                    name,
                    description,
                    updated_at
                FROM content.genre
                WHERE updated_at > %s
                ORDER BY updated_at
                LIMIT {CONFIG.FETCH_FROM_PG_BY};
                """, (updated_after,))
    updated_genres = cursor.fetchall()
    logger.debug(f"Fetched {len(updated_genres)} genres")
    return updated_genres


def _fetch_updated_persons(cursor: _cursor, updated_after: datetime.datetime) -> List[dict]:
    """
    Extracts all persons updated after provided date.
    """
    cursor.execute(f"""
                SELECT id, updated_at, full_name
                FROM content.person
                WHERE updated_at > %s
                ORDER BY updated_at
                LIMIT {CONFIG.FETCH_FROM_PG_BY};
                """, (updated_after,))
    updated_persons = cursor.fetchall()
    logger.debug(f"Fetched {len(updated_persons)} persons")
    return updated_persons


def _fetch_movies_by_genres(cursor: _cursor, genres: List[dict], movie_updated_after: datetime.datetime) -> List[dict]:
    """
    Returns all movies related to provided genres list.
    Also filters movies by provided updated_at field.
    """
    args = ",".join(cursor.mogrify("%s", (genre["id"],)).decode() for genre in genres)
    cursor.execute(f"""
                    SELECT fw.id, fw.updated_at 
                    FROM content.film_work fw 
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id 
                    WHERE updated_at > %s AND gfw.genre_id IN ({args}) 
                    ORDER BY fw.updated_at 
                    LIMIT {CONFIG.FETCH_FROM_PG_BY};
                    """, (movie_updated_after,))

    linked_movies = cursor.fetchall()
    logger.debug(f"Fetched {len(linked_movies)} linked movies")
    return linked_movies


def _fetch_movies_by_persons(cursor: _cursor, persons: List[dict], updated_after: datetime.datetime):
    """
    Extracts movies where provided persons participate.
    Also filters movies by updated_at.
    """
    args = ",".join(cursor.mogrify("%s", (person["id"],)).decode() for person in persons)
    cursor.execute(f"""
                    SELECT fw.id, fw.updated_at 
                    FROM content.film_work fw 
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id 
                    WHERE updated_at > %s AND pfw.person_id IN ({args}) 
                    ORDER BY fw.updated_at 
                    LIMIT {CONFIG.FETCH_FROM_PG_BY};
                    """, (updated_after,))

    linked_movies = cursor.fetchall()
    logger.debug(f"Fetched {len(linked_movies)} linked movies")
    return linked_movies
