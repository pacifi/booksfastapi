from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import dtos

from dependencies import get_db
from repositories.author import AuthorRepository
from repositories.book import BookRepository
from services.book import BookService

router = APIRouter(prefix="/books", tags=["books"])

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    book_repo = BookRepository(db)
    author_repo = AuthorRepository(db)
    return BookService(book_repo, author_repo)

@router.post("")
def create_book(book: dtos.BookRequest, service: BookService = Depends(get_book_service)):
    result = service.create_book(book)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{book_id}")
def get_book(book_id: str, service: BookService = Depends(get_book_service)):
    book = service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("")
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_all_books()

@router.put("/{book_id}")
def update_book(book_id: str, book: dtos.BookRequest, service: BookService = Depends(get_book_service)):
    result = service.update_book(book_id, book)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "Book not found":
            raise HTTPException(status_code=404, detail=result["error"])
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{book_id}")
def delete_book(book_id: str, service: BookService = Depends(get_book_service)):
    result = service.delete_book(book_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result