from uuid import UUID

from pydantic import BaseModel

from core.application.types import FromValueObjectType as _


class BaseResultDTO(BaseModel):
    class Config:
        from_attributes = True


class Query(BaseModel):
    pass


class ListAllFormsQuery(Query):
    class ResultDTO(BaseResultDTO):
        uuid: _[UUID]


class GetFormQuery(Query):
    uuid: UUID

    class ResultDTO(BaseResultDTO):
        uuid: _[UUID]
