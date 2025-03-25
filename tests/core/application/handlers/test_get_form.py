import pytest

from core.application.handlers import GetFormQueryHandler
from core.application.queries import GetFormQuery
from core.domain.entities.form import Form


@pytest.fixture
def handler(repository) -> GetFormQueryHandler:
    return GetFormQueryHandler(repository)


async def test_handler_returns_none_when_no_saved_forms(handler, faker) -> None:
    query = GetFormQuery(uuid=faker.uuid4())

    result = await handler.handle(query)

    assert result is None


async def test_handler_returns_actual_form(handler, repository) -> None:
    form1 = Form.create(title="form1")
    repository.save_form(form1)
    form2 = Form.create(title="form1")
    repository.save_form(form2)

    query = GetFormQuery(uuid=form1.uuid.value)
    result = await handler.handle(query)

    expected = GetFormQuery.ResultDTO.model_validate(form1)
    assert result == expected
