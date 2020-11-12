import logging
import time
from datetime import datetime, timezone

import psycopg2.extras

from src.config import CONFIG
from src.consts import ES_MOVIES_INDEX_NAME, ES_GENRES_INDEX_NAME, ES_PERSONS_INDEX_NAME
from src.filters import transform_movie_data, transform_genre_data, load_essences, transform_person_data
from src.producers import (
    extract_movies_updated_due_to_movie_change,
    extract_updated_movies_due_to_entity_change,
    extract_updated_entities,
)
from src.state import StateES
from src.utils import ensure_es_index_exists

logger = logging.getLogger(__name__)

if CONFIG.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def run_etl_process(state: StateES):
    """
    Starts to periodically launch all of ETL pipelines.
    """
    ensure_es_index_exists(CONFIG.ELASTIC_URL, ES_MOVIES_INDEX_NAME)
    ensure_es_index_exists(CONFIG.ELASTIC_URL, ES_GENRES_INDEX_NAME)
    ensure_es_index_exists(CONFIG.ELASTIC_URL, ES_PERSONS_INDEX_NAME)

    while True:
        logger.info("Starting full sync")
        started_at = datetime.now(timezone.utc)
        state.set_last_full_state_sync_started_at(started_at)

        movies_loader = load_essences(ES_MOVIES_INDEX_NAME)
        movies_transformer = transform_movie_data(movies_loader)
        extract_movies_updated_due_to_movie_change(movies_transformer, state)
        extract_updated_movies_due_to_entity_change(ES_GENRES_INDEX_NAME, movies_transformer, state)
        extract_updated_movies_due_to_entity_change(ES_PERSONS_INDEX_NAME, movies_transformer, state)
        movies_loader.close()

        genres_loader = load_essences(ES_GENRES_INDEX_NAME)
        genres_transformer = transform_genre_data(genres_loader)
        extract_updated_entities(ES_GENRES_INDEX_NAME, genres_transformer, state)
        genres_loader.close()

        load = load_essences(ES_PERSONS_INDEX_NAME)
        transform = transform_person_data(load)
        extract_updated_entities(ES_PERSONS_INDEX_NAME, transform, state)
        load.close()

        state.reset_caches()
        logger.info("Full sync completed. Sleeping.")
        time.sleep(CONFIG.UPDATES_CHECK_INTERVAL_SEC)


if __name__ == "__main__":
    logger.info("Starting ETL process")
    state = StateES(f"{CONFIG.ETL_STATE_STORAGE_FOLDER}/state.json")
    psycopg2.extras.register_uuid()
    run_etl_process(state)
