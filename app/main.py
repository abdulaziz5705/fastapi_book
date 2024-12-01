from fastapi import FastAPI

from .models import create_tables
from .routers import authors, books

app = FastAPI()

@app.on_event("startup")
async def startup():
    create_tables()


@app.get("/", tags=["main"])
async def root():
    return {"message": "Hell World"}


app.include_router(authors.router)
app.include_router(books.router)
