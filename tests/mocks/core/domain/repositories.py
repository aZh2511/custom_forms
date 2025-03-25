from uuid import UUID

from core.domain.entities import Form, FormResponse
from core.domain.entities.base import Aggregate
from core.domain.repositories import IRepository
from collections import defaultdict

from core.domain.value_objects import FormUUID, FormResponseUUID


class TestsRepository(IRepository):
    def __init__(self) -> None:
        self._tables = defaultdict(set)

    def add(self, table_name: str, record: Aggregate) -> None:
        self._tables[table_name].add(record)

    def _get_by_id(self, table_name: str, uuid: UUID) -> Aggregate | None:
        maybe_record = next(
            filter(
                lambda r: r.uuid.value == uuid,
                self._tables[table_name],
            ),
            None,
        )
        return maybe_record

    def get_form_by_uuid(self, form_uuid: FormUUID) -> Form | None:
        return self._get_by_id("form", form_uuid.value)

    def get_form_response_by_uuid(
        self, form_uuid: FormResponseUUID
    ) -> FormResponse | None:
        return self._get_by_id("form_response", form_uuid.value)

    def save_form_response(self, form_response: FormResponse) -> None:
        self.add("form_response", form_response)
