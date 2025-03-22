from core.domain.entities.base import Entity
from core.domain.value_objects import FieldUUID
from dataclasses import dataclass
from typing import Any


@dataclass
class Field(Entity):
    uuid: FieldUUID
    value: Any = None
    allow_null: bool = False

    @classmethod
    def create(cls) -> "Field":
        return Field(
            uuid=FieldUUID(),
        )

    def __hash__(self) -> int:
        return hash(self.uuid)


@dataclass
class BooleanField(Field):
    value: bool     # todo: default


