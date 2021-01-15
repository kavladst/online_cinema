from dataclasses import dataclass, field
from typing import List, Dict, Any

from tests.functional.testdata.models.base import EntityBase
from tests.functional.testdata.models.genre import NestedGenre
from tests.functional.testdata.models.person import NestedPerson


@dataclass
class Film(EntityBase):
    title: str = 'Title of film'
    imdb_rating: float = 5.0
    description: str = 'Description of film'
    directors_names: List[str] = field(default_factory=list)
    actors_names: List[str] = field(default_factory=list)
    writers_names: List[str] = field(default_factory=list)
    genre: List[NestedGenre] = field(default_factory=list)
    actors: List[NestedPerson] = field(default_factory=list)
    writers: List[NestedPerson] = field(default_factory=list)
    directors: List[NestedPerson] = field(default_factory=list)
    age_limit: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'imdb_rating': self.imdb_rating,
            'description': self.description,
            'directors_names': self.directors_names,
            'actors_names': self.actors_names,
            'writers_names': self.writers_names,
            'genre': [g.__dict__ for g in self.genre],
            'actors': [p.__dict__ for p in self.actors],
            'writers': [p.__dict__ for p in self.writers],
            'directors': [p.__dict__ for p in self.directors],
            'age_limit': self.age_limit
        }
