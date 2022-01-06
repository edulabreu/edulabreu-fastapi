from pydantic import BaseModel
from typing import List


# Article inside UserDisplay (o Article que esta dentro de UserDisplay)
class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []

    class Config:
        orm_mode = True


# User inside ArticleDisplay (User que esta sendo usado em ArticleDisplay)
class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creatorUser_id: int


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config:
        orm_mode = True
