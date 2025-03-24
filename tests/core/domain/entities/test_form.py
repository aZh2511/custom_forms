import pytest

from core.domain.entities import Form
from core.domain.entities import BooleanField as Field
from core.domain.exceptions import FormCanOnlyHaveUniqueFields


@pytest.fixture
def form(faker) -> Form:
    return Form.create(title=faker.sentence())


def test_form_create_results_in_unique_forms(faker) -> None:
    form1 = Form.create(title=faker.sentence())
    form2 = Form.create(title=faker.sentence())

    assert form1 != form2


def test_form_representation(faker) -> None:
    title = faker.sentence()

    form = Form.create(title=title)

    assert str(form) == title


def test_add_field_to_form(form) -> None:
    some_field = Field.create()
    form.add_field(some_field)

    assert some_field in form.fields


def test_form_can_only_have_unique_fields(form) -> None:
    some_field = Field.create()
    form.add_field(some_field)

    with pytest.raises(FormCanOnlyHaveUniqueFields):
        form.add_field(some_field)


def test_required_fields_for_empty_form_are_also_empty(form, faker) -> None:
    required_fields = form.get_required_fields()

    assert required_fields == set()


def test_required_fields_returns_only_required_fields(form, faker) -> None:
    required_field = Field.create()
    required_field.mark_required()
    not_required_field = Field.create()

    form.add_field(required_field)
    form.add_field(not_required_field)

    required_fields = form.get_required_fields()

    assert required_fields == {
        required_field,
    }
