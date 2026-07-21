from pydantic import BaseModel

class subjectCreate(BaseModel):
    name: str 


class subjectResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int

    class Config:
        from_attributes = True