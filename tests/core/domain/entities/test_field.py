from core.domain.entities import Field


def test_field_create_results_in_unique_forms() -> None:
    field1 = Field.create()
    field2 = Field.create()

    assert field1 != field2


def test_non_required_by_default() -> None:
    field = Field.create()

    assert not field.is_required


def test_mark_required() -> None:
    field = Field.create()

    field.mark_required()

    assert field.is_required is True


def test_mark_not_required() -> None:
    field = Field.create()
    field.mark_required()

    field.mark_not_required()

    assert not field.is_required
