from core.domain.entities import Field, Form



def test_form_create_results_in_unique_forms() -> None:
    form1 = Form.create()
    form2 = Form.create()

    assert form1 != form2


def test_field_create_results_in_unique_forms() -> None:
    field1 = Field.create()
    field2 = Field.create()

    assert field1 != field2
