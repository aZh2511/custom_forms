from core.domain.entities import BooleanField


def test_wrong_type_value_is_invalid() -> None:
    field = BooleanField.create()
    incorrect_type_value = "some_string"

    assert not field.is_valid(incorrect_type_value)


def test_boolean_type_value_is_valid(faker) -> None:
    field = BooleanField.create()
    boolean_type = faker.boolean()

    assert field.is_valid(boolean_type) is True
