from core.domain.value_objects import (
    FieldUUID,
    FormUUID,
    FieldResponseUUID,
    FormResponseUUID,
)


def test_field_uuid_is_unique() -> None:
    uuid1 = FieldUUID()
    uuid2 = FieldUUID()

    assert uuid1 != uuid2


def test_form_uuid_is_unique() -> None:
    uuid1 = FormUUID()
    uuid2 = FormUUID()

    assert uuid1 != uuid2


def test_field_response_uuid_is_unique() -> None:
    uuid1 = FieldResponseUUID()
    uuid2 = FieldResponseUUID()

    assert uuid1 != uuid2


def test_form_response_uuid_is_unique() -> None:
    uuid1 = FormResponseUUID()
    uuid2 = FormResponseUUID()

    assert uuid1 != uuid2
