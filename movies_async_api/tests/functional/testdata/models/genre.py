from dataclasses import dataclass

from tests.functional.testdata.models.base import EntityBase


@dataclass
class Genre(EntityBase):
    name: str
    description: str = 'Description of genre'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


@dataclass
class NestedGenre:
    id: str
    name: str
