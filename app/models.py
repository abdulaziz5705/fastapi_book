from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.database import engine


class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    age: int | None = Field(default=None,gt=0)

    books: List["Book"] = Relationship(back_populates="author")




class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    pages: int = Field(gt=0)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")


def create_tables():
    SQLModel.metadata.create_all(engine)