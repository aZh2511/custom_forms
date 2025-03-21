from core.domain.entities.base import Entity
from core.domain.value_objects import FieldUUID
from dataclasses import dataclass


@dataclass
class Field(Entity):
    uuid: FieldUUID

    @classmethod
    def create(cls) -> "Field":
        return Field(
            uuid=FieldUUID(),
        )
