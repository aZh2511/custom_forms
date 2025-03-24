from core.domain.entities.base import Entity
from core.domain.value_objects import FieldUUID
from dataclasses import dataclass
from typing import Any


@dataclass
class Field(Entity):
    uuid: FieldUUID
    value: Any = None

    _is_required: bool = False

    @property
    def is_required(self) -> bool:
        return self._is_required

    @classmethod
    def create(cls) -> "Field":
        return Field(
            uuid=FieldUUID(),
        )

    def mark_required(self) -> None:
        self._is_required = True

    def mark_not_required(self) -> None:
        self._is_required = False

    def __hash__(self) -> int:
        return hash(self.uuid)


@dataclass
class BooleanField(Field):
    value: bool     # todo: default


