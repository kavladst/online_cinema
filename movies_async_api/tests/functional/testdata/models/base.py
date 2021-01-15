from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class EntityBase:
    id: str

    @abstractmethod
    def to_dict(self) -> dict:
        pass
