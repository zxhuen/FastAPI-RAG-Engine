from pydantic import BaseModel

class subjectCreate(BaseModel):
    name: str 


class subjectResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True