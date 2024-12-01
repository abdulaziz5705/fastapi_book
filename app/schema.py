from typing import List

from pydantic import BaseModel, Field


class AuthorIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    age: int = Field(gt=0)

class AuthorOut(AuthorIn):
    id: int


class BookIn(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    pages: int = Field(gt=1)
    author_id: int = Field(gt=0)
class BookOut(BookIn):
    id: int

