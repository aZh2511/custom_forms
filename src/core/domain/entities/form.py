from core.domain.entities.base import Aggregate
from core.domain.value_objects import FormUUID
from dataclasses import dataclass, field
from core.domain.entities.field import Field


# AggregateRoot
@dataclass
class Form(Aggregate):
    uuid: FormUUID
    title: str
    fields: set[Field] = field(default_factory=set)

    @classmethod
    def create(cls, title: str) -> "Form":
        return Form(
            uuid=FormUUID(),
            title=title,
        )

    def __str__(self) -> str:
        return self.title
