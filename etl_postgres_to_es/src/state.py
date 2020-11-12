import abc
import datetime
import json
import logging
from typing import Any, List

from src.consts import DEFAULT_DATE, DATE_PARSE_PATTERN

logger = logging.getLogger(__name__)


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str = "state.json"):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, "w") as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict:
        if self.file_path is None:
            logger.info("No state file provided. Continue with in-memory state")
            return {}

        try:
            with open(self.file_path) as f:
                data = json.load(f)

            return data

        except FileNotFoundError:
            logger.debug("No previously saved state. Initializing it with empty dict")
            self.save_state({})


class State:

    def __init__(self, storage_file: str):
        self.storage = JsonFileStorage(storage_file)
        self.state = self.retrieve_state()
        self.cache_keys = set()

    def retrieve_state(self) -> dict:
        data = self.storage.retrieve_state()
        if not data:
            return {}
        return data

    def set_state(self, key: str, value: Any) -> None:
        """Set state for specific key"""
        self.state[key] = value

        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        """Retrieve state by specific key. Defaults to None."""
        return self.state.get(key)

    @property
    def last_full_state_sync_started_at(self) -> datetime.datetime:
        """
        date when last sync started. Necessary to check if other sync process stucked and re-launch it
        """
        date = self.get_state("last_full_state_sync_started_at")
        if date is None:
            return DEFAULT_DATE

        return datetime.datetime.strptime(date, DATE_PARSE_PATTERN)

    def set_last_full_state_sync_started_at(self, value: datetime.datetime):
        self.set_state("last_full_state_sync_started_at", str(value))

    def reset_caches(self):
        """
        Resets updated entities cache - we should sync again all of updated movies since last iteration finish.
        """
        for cache_key in self.cache_keys:
            self.set_state(cache_key, [])


class StateES(State):

    def get_last_entity_synced_at(self, entity_name: str, index_name: str) -> datetime.datetime:
        """
        updated_at of last entity retrieved from Postgres during sync by index in ES.
        """
        date = self.get_state(f"last_{entity_name}_synced_at_for_{index_name}")
        if date is None:
            return DEFAULT_DATE

        return datetime.datetime.strptime(date, DATE_PARSE_PATTERN)

    def get_synced_entities(self, entity_name: str, index_name: str) -> List[str]:
        """
        Cache stored as a tuple of entities ids.
        """
        entities = self.get_state(f"{entity_name}_synced_for_{index_name}")
        if entities is None:
            return []

        return list(entities)

    def set_last_entity_synced_at(self, entity_name: str, index_name: str, value: datetime.datetime):
        self.set_state(f"last_{entity_name}_synced_at_for_{index_name}", str(value))

    def add_entity_synced(self, entity_name: str, index_name: str, entity_ids: List[str]):
        self.set_state(
            f"{entity_name}_synced_for_{index_name}",
            self.get_synced_entities(entity_name, index_name) + entity_ids
        )
