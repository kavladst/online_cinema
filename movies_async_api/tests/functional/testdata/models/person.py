from dataclasses import dataclass

from tests.functional.testdata.models.base import EntityBase


@dataclass
class Person(EntityBase):
    full_name: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'full_name': self.full_name
        }


@dataclass
class NestedPerson:
    id: str
    name: str
