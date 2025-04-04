from core.domain.entities import Form, FormResponse
from core.domain.value_objects import FormUUID, FormResponseUUID


class IRepository:
    def get_all_forms(self) -> set[Form]:
        raise NotImplementedError

    def get_form_by_uuid(self, form_uuid: FormUUID) -> Form | None:
        raise NotImplementedError

    def get_form_response_by_uuid(
        self, form_uuid: FormResponseUUID
    ) -> FormResponse | None:
        raise NotImplementedError

    def save_form_response(self, form_response: FormResponse) -> None:
        raise NotImplementedError

    def save_form(self, form: Form) -> None:
        raise NotImplementedError
