from core.application.handlers import ListFormsQueryHandler
from core.application.queries import ListAllFormsQuery
import pytest
from core.domain.entities.form import Form
from pytest_unordered import unordered


@pytest.fixture
def handler(repository) -> ListFormsQueryHandler:
    return ListFormsQueryHandler(repository)


async def test_list_all_forms_query_handler_returns_empty_list_when_no_saved_forms(handler) -> None:
    query = ListAllFormsQuery()

    result = await handler.handle(query)

    assert result == []


async def test_list_all_forms_query_handler_returns_actual_forms(handler, repository) -> None:
    form1 = Form.create(title="form1")
    repository.save_form(form1)
    form2 = Form.create(title="form1")
    repository.save_form(form2)
    query = ListAllFormsQuery()

    result = await handler.handle(query)


    expected = [
        ListAllFormsQuery.ResultDTO.model_validate(form1),
        ListAllFormsQuery.ResultDTO.model_validate(form2),
    ]
    assert result == unordered(expected)
