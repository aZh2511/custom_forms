from core.domain.repositories import IRepository
from core.domain.entities import Form
from core.domain.value_objects import FormUUID
from uuid import UUID


class MockedRepository(IRepository):
    _data = {
        "forms": {
            Form(
                uuid=FormUUID(UUID("a75e3929-5c4d-4014-94fd-59d5befeb5d6")),
                title="Mocked Form #1",
            ),
            Form(
                uuid=FormUUID(UUID("29edc97f-1d1d-41a5-a647-7c2533ed3123")),
                title="Mocked Form #2",
            ),
        }
    }

    def get_all_forms(self) -> set[Form]:
        return self._data["forms"]

    def get_form_by_uuid(self, form_uuid: FormUUID) -> Form | None:
        return next(
            filter(
                lambda f: f.uuid == form_uuid,
                self._data["forms"],
            ),
            None,
        )
