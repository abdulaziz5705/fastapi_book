from typing import Dict

from fastapi import APIRouter
from sqlmodel import select
from starlette import status

from app.schema import AuthorIn, AuthorOut
from app.database import SessionDep
from app.models import Author
router = APIRouter(
    tags=['Authors'],
)

@router.post("/authors/", status_code=status.HTTP_201_CREATED)
async def create_author(auth: AuthorIn, session: SessionDep)->AuthorOut:
    auth_in = Author(**auth.dict())
    session.add(auth_in)
    session.commit()
    session.refresh(auth_in)
    return auth_in

@router.get("/authors/", status_code=status.HTTP_200_OK)
async def get_authors(session: SessionDep )-> list[AuthorOut]:
    authors = session.exec(select(Author)).all()
    return authors

@router.delete("/authors/", status_code=status.HTTP_200_OK)
async def delete_author(auth_id: int, session: SessionDep)-> dict:
    author = session.exec(select(Author).where(Author.id == auth_id)).first()
    if not author:
        return {"massage": "Author not found"}
    session.delete(author)
    session.commit()
    return {"status": True, "detail": "Author deleted"}



@router.put("/authors/{auth_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_author(auth_id: int, auth_in: AuthorIn, session: SessionDep)->AuthorOut:
    auth = session.get(Author, auth_id)
    if not auth:
       print("No author found")
    auth.first_name = auth_in.first_name
    auth.last_name = auth_in.last_name
    auth.age = auth_in.age

    session.commit()
    return auth

@router.patch("/authors/{auth_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_auth(auth_id: int, auth_in: AuthorIn, session: SessionDep)->AuthorOut:
    auth = session.get(Author, auth_id)
    if not auth:
        print("No author found")
    auth.first_name = auth_in.first_name
    auth.last_name = auth_in.last_name
    auth.age = auth_in.age

    session.commit()
    return auth