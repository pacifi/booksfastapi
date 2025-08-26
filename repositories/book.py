from sqlalchemy.orm import Session

from models import Book, Author


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Book).all()

    def get_by_id(self, id: str):
        return self.db.query(Book).get(id)

    def get_by_author(self, author_id: int):
        return self.db.query(Author).filter(Book.author_id == author_id).all()

    def create(self, title: str, description: str, author_id: str):
        db_book = Book(
            title=title,
            description=description,
            author_id=author_id
        )

        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def update(self, id: str, title: str, description: str, author_id: str):
        db_book = self.get_by_id(id)
        if not db_book:
            return None
        db_book.title = title
        db_book.description = description
        db_book.author_id = author_id
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, id: str):
        db_book = self.get_by_id(id)
        if not db_book:
            return False
        self.db.delete(db_book)
        self.db.commit()
        return True
