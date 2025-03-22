from core.domain.entities.response import FieldResponse, FormResponse
from core.domain.value_objects import FormUUID, FieldResponseUUID, FieldUUID
import pytest


@pytest.fixture
def form_uuid() -> FormUUID:
    return FormUUID()


@pytest.fixture
def field_uuid() -> FieldUUID:
    return FieldUUID()


def test_add_response_ok(form_uuid, field_uuid) -> None:
    form_response = FormResponse.create(form_uuid)
    response = FieldResponse.create('value', for_field=field_uuid)

    form_response.add_field_response(response)

    response = form_response.get_response(field_uuid)
    assert response.value == 'value'


def test_add_response_for_same_form_field_overwrites_response(form_uuid, field_uuid) -> None:
    form_response = FormResponse.create(form_uuid)
    old_response = FieldResponse.create('value', for_field=field_uuid)
    form_response.add_field_response(old_response)

    new_response = FieldResponse.create('new_value', for_field=field_uuid)
    form_response.add_field_response(new_response)

    response = form_response.get_response(field_uuid)
    assert response.value == 'new_value'
    assert response.uuid == new_response.uuid
