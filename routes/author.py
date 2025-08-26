from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import dtos

from dependencies import get_db
from repositories.author import AuthorRepository
from repositories.book import BookRepository
from services.author import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"])

def get_author_service(db: Session = Depends(get_db)) -> AuthorService:
    author_repo = AuthorRepository(db)
    book_repo = BookRepository(db)
    return AuthorService(author_repo, book_repo)

@router.get("")
def get_authors(service: AuthorService = Depends(get_author_service)):
    return service.get_all_authors()

@router.post("")
def create_author(author: dtos.AuthorRequest, service: AuthorService = Depends(get_author_service)):
    result = service.create_author(author)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{author_id}")
def get_author(author_id: str, service: AuthorService = Depends(get_author_service)):
    author = service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}")
def update_author(author_id: str, author: dtos.AuthorRequest, service: AuthorService = Depends(get_author_service)):
    result = service.update_author(author_id, author)
    if not result:
        raise HTTPException(status_code=404, detail="Author not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/{author_id}")
def delete_author(author_id: str, service: AuthorService = Depends(get_author_service)):
    result = service.delete_author(author_id)
    if not result:
        raise HTTPException(status_code=404, detail="Author not found")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{author_id}/books")
def get_books_by_author(author_id: str, service: AuthorService = Depends(get_author_service)):
    books = service.get_author_books(author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return books