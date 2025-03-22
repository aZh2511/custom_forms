from core.domain.entities.base import Entity, Aggregate
from core.domain.value_objects import FormUUID, FieldUUID, FieldResponseUUID, FormResponseUUID
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FieldResponse(Entity):
    uuid: FieldResponseUUID
    value: Any
    field_uuid: FieldUUID

    @classmethod
    def create(cls, value: Any, for_field: FieldUUID) -> "FieldResponse":
        return cls(
            uuid=FieldResponseUUID(),
            value=value,
            field_uuid=for_field,
        )

    def __hash__(self) -> int:
        return hash(self.uuid)


@dataclass
class FormResponse(Aggregate):
    uuid: FormResponseUUID
    form_uuid: FormUUID
    field_responses: set[FieldResponse] = field(default_factory=set)

    @classmethod
    def create(cls, for_form_uuid: FormUUID) -> "FormResponse":
        return cls(
            uuid=FormResponseUUID(),
            form_uuid=for_form_uuid,
        )

    def add_field_response(self, field_response: FieldResponse) -> None:
        maybe_field = self.get_response(field_response.field_uuid)
        if maybe_field:
            self.field_responses.remove(maybe_field)
        # todo: what if adding same response
        self.field_responses.add(field_response)

    def get_response(self, for_field: FieldUUID) -> FieldResponse | None:
        existing_response = next(
            filter(lambda r: r.field_uuid == for_field, self.field_responses),
            None
        )
        return existing_response
