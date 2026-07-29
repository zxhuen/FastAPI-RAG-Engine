from pydantic import BaseModel


class PremiumType(BaseModel):
    name: str
    daily_limit: int
    max_flashcardset: int


class Usage(BaseModel):
    used_today: int


class UserResponse(BaseModel):
    email: str
    display_name: str
    avatar_url: str
    premium_type: PremiumType
    usage: Usage

    class Config:
        from_attributes = True
