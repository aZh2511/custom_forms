from core.domain.entities import Field, Form


def test_form_create_results_in_unique_forms(faker) -> None:
    form1 = Form.create(title=faker.sentence())
    form2 = Form.create(title=faker.sentence())

    assert form1 != form2


def test_form_representation(faker) -> None:
    title = faker.sentence()

    form = Form.create(title=title)

    assert str(form) == title


def test_field_create_results_in_unique_forms() -> None:
    field1 = Field.create()
    field2 = Field.create()

    assert field1 != field2


def test_add_field_to_form(faker) -> None:
    form = Form.create(title=faker.sentence())

    some_field = Field.create()
    form.add_field(some_field)

    assert some_field in form.fields
