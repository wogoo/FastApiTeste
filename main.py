import os
from fastapi import FastAPI, HTTPException
from schema import Book as SchemaBook
from schema import Author as SchemaAuthor
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from models import Author as ModelAuthor
from models import Book
from models import Book as ModelBook

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/books")
def get_books():
    books = db.session.query(Book).all()
    return books

@app.get("/api/books/{book_title}")
async def get_book_by_title(book_title: str):
    book = db.session.query(Book).filter(Book.title == book_title).first()
    if book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with title: {book_title} does not exist"
        )
    return book

@app.post("/api/book", response_model=SchemaBook)
async def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/api/author", response_model=SchemaAuthor)
async def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author