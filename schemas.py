from pydantic import BaseModel
from datetime import datetime


class SnippetBase(BaseModel):
    title: str
    content: str


class SnippetCreate(SnippetBase):
    user_id: int


class SnippetResponse(SnippetBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str  # todo: we can add a EmailStr
    bio: str


class UserCreate(UserBase):
    # password: str
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    snippets: list[SnippetResponse] = []

    class Config:
        from_attributes = True
