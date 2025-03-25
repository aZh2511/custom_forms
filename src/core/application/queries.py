from uuid import UUID

from pydantic import BaseModel

from core.application.types import FromValueObjectType as _


class Query(BaseModel):
    pass


class ListAllFormsQuery(Query):
    class ResultDTO(BaseModel):
        uuid: _[UUID]

        class Config:
            from_attributes = True
