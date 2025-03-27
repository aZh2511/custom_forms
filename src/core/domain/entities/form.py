from typing import Any

from core.domain.entities.base import Aggregate
from core.domain.value_objects import FormUUID, FieldUUID
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
        for form_field in self.fields:
            if not form_field.is_required:
                continue
            required_fields.add(form_field)
        return required_fields

    def _get_field(self, field_uuid: FieldUUID) -> Field | None:
        return next(filter(lambda f: f.uuid == field_uuid, self.fields), None)

    def is_valid_input_for_field(self, value: Any, field_uuid: FieldUUID) -> bool:
        maybe_field = self._get_field(field_uuid)
        if not maybe_field:
            raise exceptions.FormDoesNotHaveThisField()
        return maybe_field.is_valid(value)

    def __str__(self) -> str:
        return self.title

    def __hash__(self) -> int:
        return hash(self.uuid)
