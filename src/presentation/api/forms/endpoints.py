from presentation.api.forms import controllers
from core.application import queries, handlers
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

router = APIRouter(prefix="/forms", tags=["forms"])


@router.get("")
async def list_all_forms(
    handler: handlers.ListFormsQueryHandler = Depends(
        controllers.list_all_forms_query_handler
    ),
) -> list[queries.ListAllFormsQuery.ResultDTO]:
    query = queries.ListAllFormsQuery()

    return await handler.handle(query)


@router.get("/{form_uuid}")
async def get_form_by_uuid(
    form_uuid: UUID,
    handler: handlers.GetFormQueryHandler = Depends(controllers.get_form_query_handler),
) -> queries.GetFormQuery.ResultDTO:
    query = queries.GetFormQuery(uuid=form_uuid)
    form = await handler.handle(query)
    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The requested form does not exist."}],
        )
    return form
