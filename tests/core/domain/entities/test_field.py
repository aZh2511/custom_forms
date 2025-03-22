from core.domain.entities import Field


def test_field_create_results_in_unique_forms() -> None:
    field1 = Field.create()
    field2 = Field.create()

    assert field1 != field2
