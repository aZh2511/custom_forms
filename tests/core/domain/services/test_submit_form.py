import pytest

from core.domain import exceptions
from core.domain.entities import BooleanField as Field
from core.domain.entities import FormResponse, Form, FieldResponse
from core.domain.services import SubmitFormService
from core.domain.value_objects import FormUUID


@pytest.fixture
def service(repository) -> SubmitFormService:
    return SubmitFormService(repository)


@pytest.fixture
def existing_form(repository, faker) -> Form:
    form = Form.create(title=faker.sentence())
    repository.add("form", form)
    return form


def test_if_form_does_not_exist_submission_fails(service) -> None:
    unknown_form_uuid = FormUUID()
    response_for_unknown_form = FormResponse.create(for_form_uuid=unknown_form_uuid)

    with pytest.raises(exceptions.NotFound):
        service.submit(response_for_unknown_form)


def test_if_form_does_not_have_all_required_fields_submission_fails(
    service, existing_form
) -> None:
    field1 = Field.create()
    field1.mark_required()
    existing_form.add_field(field1)
    field2 = Field.create()
    field2.mark_required()
    existing_form.add_field(field2)

    response = FormResponse.create(for_form_uuid=existing_form.uuid)
    field_response = FieldResponse.create(value=True, for_field=field1.uuid)
    response.add_field_response(field_response)

    with pytest.raises(exceptions.FormDoesNotHaveAllRequiredFields):
        service.submit(response)


def test_invalid_inputs_are_not_accepted(service, existing_form) -> None:
    field1 = Field.create()
    existing_form.add_field(field1)

    response = FormResponse.create(for_form_uuid=existing_form.uuid)
    field_response = FieldResponse.create(value="invalid", for_field=field1.uuid)
    response.add_field_response(field_response)

    with pytest.raises(exceptions.InvalidFormSubmission):
        service.submit(response)


def test_valid_submission_is_saved(service, existing_form, repository) -> None:
    response_value = True
    field1 = Field.create()
    existing_form.add_field(field1)

    response = FormResponse.create(for_form_uuid=existing_form.uuid)
    field_response = FieldResponse.create(value=response_value, for_field=field1.uuid)
    response.add_field_response(field_response)
    service.submit(response)

    saved_response = repository.get_form_response_by_uuid(response.uuid)

    assert saved_response is response
    assert field_response in saved_response.field_responses
    field_response_from_repository = saved_response.get_response(for_field=field1.uuid)
    assert field_response_from_repository.value == response_value
