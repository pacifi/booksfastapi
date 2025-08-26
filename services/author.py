
import dtos
from repositories.author import AuthorRepository
from repositories.book import BookRepository


class AuthorService:

    def __init__(self, author_repo: AuthorRepository, book_repo: BookRepository):
        self.author_repo = author_repo
        self.book_repo = book_repo

    def get_all_authors(self):
        """Obtener todos los autores"""
        return self.author_repo.get_all()

    def get_author_by_id(self, author_id: str):
        """Obtener un autor por ID"""
        return self.author_repo.get_by_id(author_id)

    def create_author(self, author_data: dtos.AuthorRequest):
        """Crear un nuevo autor con validaciones"""
        # Aquí puedes agregar validaciones de negocio
        # Por ejemplo: validar formato de email, nombres únicos, etc.

        return self.author_repo.create(
            name=author_data.name,
            email=author_data.email
        )

    def update_author(self, author_id: str, author_data: dtos.AuthorRequest):
        """Actualizar un autor con validaciones"""
        # Verificar que existe
        if not self.author_repo.get_by_id(author_id):
            return None

        return self.author_repo.update(
            author_id=author_id,
            name=author_data.name,
            email=author_data.email
        )

    def delete_author(self, author_id: str):
        """Eliminar un autor (con validaciones de negocio)"""
        # Verificar que no tenga libros asociados
        books = self.book_repo.get_by_author(author_id)
        if books:
            return {"error": "Cannot delete author with associated books", "books_count": len(books)}

        success = self.author_repo.delete(author_id)
        if success:
            return {"message": "Author deleted successfully"}
        return None

    def get_author_books(self, author_id: str):
        """Obtener libros de un autor"""
        # Verificar que el autor existe
        author = self.author_repo.get_by_id(author_id)
        if not author:
            return None

        return self.book_repo.get_by_author(author_id)