
import dtos
from repositories.author import AuthorRepository
from repositories.book import BookRepository


class BookService:

    def __init__(self, book_repo: BookRepository, author_repo: AuthorRepository):
        self.book_repo = book_repo
        self.author_repo = author_repo

    def get_all_books(self):
        """Obtener todos los libros"""
        return self.book_repo.get_all()

    def get_book_by_id(self, book_id: str):
        """Obtener un libro por ID"""
        return self.book_repo.get_by_id(book_id)

    def create_book(self, book_data: dtos.BookRequest):
        """Crear un libro con validaciones"""
        # Validar que el autor existe
        if not self.author_repo.exists(book_data.author_id):
            return {"error": "Author not found"}

        # Validaciones adicionales de negocio
        if len(book_data.title.strip()) < 3:
            return {"error": "Title must be at least 3 characters"}

        return self.book_repo.create(
            title=book_data.title,
            description=book_data.description,
            author_id=book_data.author_id
        )

    def update_book(self, book_id: str, book_data: dtos.BookRequest):
        """Actualizar un libro con validaciones"""
        # Verificar que el libro existe
        if not self.book_repo.get_by_id(book_id):
            return {"error": "Book not found"}

        # Verificar que el autor existe
        if not self.author_repo.exists(book_data.author_id):
            return {"error": "Author not found"}

        # Validaciones de negocio
        if len(book_data.title.strip()) < 3:
            return {"error": "Title must be at least 3 characters"}

        return self.book_repo.update(
            book_id=book_id,
            title=book_data.title,
            description=book_data.description,
            author_id=book_data.author_id
        )

    def delete_book(self, book_id: str):
        """Eliminar un libro"""
        success = self.book_repo.delete(book_id)
        if success:
            return {"message": "Book deleted successfully"}
        return {"error": "Book not found"}