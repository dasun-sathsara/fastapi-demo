from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    post_id: int


class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    post_id: int
    user_id: int

    class Config:
        orm_mode = True
