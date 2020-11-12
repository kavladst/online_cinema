from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID


class Roles(Enum):
    DIRECTOR = "director"
    ACTOR = "actor"
    WRITER = "writer"


@dataclass
class FullMovie:
    fw_id: UUID
    title: str
    description: Optional[str]
    rating: Optional[float]
    genres: List[str]
    names: List[str]
    roles: List[str]
    persons_ids: List[UUID]
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: UUID
    name: str
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


@dataclass(frozen=True)
class Person:
    full_name: str
    id: UUID
    role: Optional[Roles] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
