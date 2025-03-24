from enum import Enum
from typing import Any

from core.domain.entities.base import Entity
from core.domain.value_objects import FieldUUID


class FieldType(Enum):
    BOOLEAN = "boolean"


class Field(Entity):
    type: FieldType

    def __init__(self, uuid: FieldUUID, type: FieldType) -> None:
        self.uuid = uuid
        self.type = type
        self._is_required = False

    @property
    def is_required(self) -> bool:
        return self._is_required

    @classmethod
    def create(cls) -> "Field":
        return cls(
            uuid=FieldUUID(),
            type=cls.type,
        )

    def mark_required(self) -> None:
        self._is_required = True

    def mark_not_required(self) -> None:
        self._is_required = False

    def is_valid(self, value: Any) -> bool:
        is_none = value is None
        if is_none and self._is_required:
            return False
        return self._is_valid(value)

    def _is_valid(self, value: Any) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.uuid)



class BooleanField(Field):
    type: FieldType = FieldType.BOOLEAN

    def _is_valid(self, value: Any) -> bool:
        if not isinstance(value, bool):
            return False
        return True
