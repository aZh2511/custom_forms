from presentation.api.forms import controllers
from core.application import queries, handlers
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/forms", tags=["forms"])


@router.get("")
async def list_all_forms(
    handler: handlers.ListFormsQueryHandler = Depends(
        controllers.list_all_forms_query_handler
    ),
) -> list[queries.ListAllFormsQuery.ResultDTO]:
    query = queries.ListAllFormsQuery()

    return await handler.handle(query)
