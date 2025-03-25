from typing import Generic, TypeVar, Any

from core.application import commands, queries
from core.domain.repositories import IRepository

CommandType = TypeVar("CommandType", bound=commands.Command)
QueryType = TypeVar("QueryType", bound=queries.Query)


class CommandHandler(Generic[CommandType]):
    async def handle(self, command: CommandType) -> Any:
        raise NotImplementedError


class QueryHandler(Generic[QueryType]):
    async def handle(self, query: QueryType) -> Any:
        raise NotImplementedError


class ListFormsQueryHandler(QueryHandler[queries.ListAllFormsQuery]):
    def __init__(self, repository: IRepository) -> None:
        self._repository = repository

    async def handle(self, query: queries.ListAllFormsQuery) -> list[queries.ListAllFormsQuery.ResultDTO]:
        all_forms = self._repository.get_all_forms()
        return [
            queries.ListAllFormsQuery.ResultDTO.model_validate(form)
            for form in all_forms
        ]
