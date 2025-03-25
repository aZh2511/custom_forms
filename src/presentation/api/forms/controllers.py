from core.application import handlers
from core.domain.repositories import IRepository
from infrastructure.repositories import MockedRepository


def get_repository() -> IRepository:
    return MockedRepository()


def list_all_forms_query_handler() -> handlers.ListFormsQueryHandler:
    return handlers.ListFormsQueryHandler(repository=get_repository())
