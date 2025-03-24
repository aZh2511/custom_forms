from core.domain.entities.base import Aggregate
from core.domain.value_objects import FormUUID
from dataclasses import dataclass, field
from core.domain.entities.field import Field
from core.domain import exceptions


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

    def add_field(self, form_field: Field) -> None:
        if form_field in self.fields:
            raise exceptions.FormCanOnlyHaveUniqueFields()
        self.fields.add(form_field)

    def get_required_fields(self) -> set[Field]:
        required_fields = set()
        for field in self.fields:
            if not field.is_required:
                continue
            required_fields.add(field)
        return required_fields

    def __str__(self) -> str:
        return self.title

    def __hash__(self) -> int:
        return hash(self.uuid)
