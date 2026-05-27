from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str
    nickname: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nickname: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PostCreate(BaseModel):
    content: str


class PostUpdate(BaseModel):
    content: str


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime
    author: UserOut


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None
    author: UserOut
    like_count: int = 0
    comment_count: int = 0

    @classmethod
    def from_post(cls, post) -> "PostOut":
        return cls(
            id=post.id,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=UserOut.model_validate(post.author),
            like_count=len(post.likes),
            comment_count=len(post.comments),
        )


class CommentCreate(BaseModel):
    content: str


class LikeOut(BaseModel):
    liked: bool
    like_count: int
