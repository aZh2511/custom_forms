from core.domain.entities.base import Aggregate
from core.domain.value_objects import FormUUID
from dataclasses import dataclass


# AggregateRoot
@dataclass
class Form(Aggregate):
    uuid: FormUUID

    @classmethod
    def create(cls) -> "Form":
        return Form(
            uuid=FormUUID(),
        )
