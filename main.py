import uuid
from http.client import HTTPException

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

import dtos
import models

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors")
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors


@app.post("/authors")
def create_author(authors: dtos.AuthorRequest, db: Session = Depends(get_db)):
    db_autor = models.Author(
        name=authors.name,
        email=authors.email,
    )
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor


@app.get("/authors/{author_id}")
def get_author(author_id: str, db: Session = Depends(get_db)):
    author = db.query(models.Author).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.put("/authors/{author_id}")
def update_author(author_id: str, author: dtos.AuthorRequest, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).get(author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author.name = author.name
    db_author.email = author.email
    db.commit()
    db.refresh(db_author)

    return db_author


@app.delete("/authors/{author_id}")
def delete_author(author_id: str, db: Session = Depends(get_db)):
    db_author = db.query(models.Author).get(author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted"}


@app.post("/books")
def create_book(book: dtos.BookRequest, db: Session = Depends(get_db)):
    author = db.query(models.Author).get(book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = models.Book(
        title=book.title,
        description=book.description,
        author_id=author.id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/{book_id}")
def get_book(book_id: str, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    db_books = db.query(models.Book).all()
    return db_books


@app.get("/authors/{author_id}/books")
def get_books_by_author(author_id: str, db: Session = Depends(get_db)):
    author = db.query(models.Author).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books


@app.put("/books/{book_id}")
def update_book(book_id: str, book: dtos.BookRequest, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.description = book.description
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted"}
