from core.domain.entities import FormResponse
from core.domain.repositories import Repository
from core.domain import exceptions


class SubmitFormService:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def submit(self, response: FormResponse) -> None:
        form = self._repository.get_form_by_uuid(response.form_uuid)
        if form is None:
            raise exceptions.FormNotFound()

        required_fields = form.get_required_fields()
        responses_expected_for_fields = {field.uuid for field in required_fields}
        if not response.has_all_required_fields(responses_expected_for_fields):
            raise exceptions.FormDoesNotHaveAllRequiredFields

        for field_response in response.field_responses:
            is_valid = form.is_valid_input_for_field(
                field_response.value, field_response.field_uuid
            )
            if not is_valid:
                raise exceptions.InvalidFormSubmission()

        self._repository.save_form_response(response)
