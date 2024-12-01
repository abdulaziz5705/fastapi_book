from fastapi import APIRouter, HTTPException

from sqlmodel import select
from starlette import status
from typing_extensions import get_origin

from app.schema import BookIn, BookOut
from app.database import SessionDep
from app.models import Book
router = APIRouter(
    tags=['Books'],
)

@router.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookIn, session: SessionDep)-> BookOut:
    book_in = Book(**book.dict())
    session.add(book_in)
    session.commit()
    session.refresh(book_in)
    return book_in



@router.get("/books/", status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep)-> list[BookOut]:
    books = session.exec(select(Book)).all()
    return books


@router.put("/books/{book_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id: int, book_in: BookIn, session: SessionDep)->BookOut:
    book = session.get(Book, book_id)
    if not book:
       print("No author found")
    book.title = book_in.first_name
    book.description = book_in.last_name
    book.price = book_in.price
    book.pages = book_in.pages
    book.author = book_in.author

    session.commit()
    return book

@router.patch("/books/{book_id}")
def update_hero(book_id: int, book_in: BookIn, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    book_data = Book.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db

@router.delete("/books/")
async def delete_book(book_id: int, session: SessionDep)->BookOut:
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    book_db.delete(book_db)
    session.commit()
    return book_db

