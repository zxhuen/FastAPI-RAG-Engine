from pydantic import BaseModel

class PremiumType(BaseModel):
    name: str

class UserResponse(BaseModel):    
    email: str
    display_name: str
    avatar_url: str
    premium_type: PremiumType

    class Config:
        from_attributes = True

