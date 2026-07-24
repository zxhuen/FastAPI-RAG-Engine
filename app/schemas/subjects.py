from pydantic import BaseModel
from uuid import UUID
class subjectCreate(BaseModel):
    name: str 


class subjectResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True