from sqlalchemy.orm import Session
import models


class AuthorRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """Obtener todos los autores"""
        return self.db.query(models.Author).all()

    def get_by_id(self, author_id: str):
        """Obtener un autor por ID"""
        return self.db.query(models.Author).get(author_id)

    def create(self, name: str, email: str):
        """Crear un nuevo autor"""
        db_author = models.Author(name=name, email=email)
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author

    def update(self, author_id: str, name: str, email: str):
        """Actualizar un autor"""
        db_author = self.get_by_id(author_id)
        if not db_author:
            return None

        db_author.name = name
        db_author.email = email
        self.db.commit()
        self.db.refresh(db_author)
        return db_author

    def delete(self, author_id: str):
        """Eliminar un autor"""
        db_author = self.get_by_id(author_id)
        if not db_author:
            return False

        self.db.delete(db_author)
        self.db.commit()
        return True

    def exists(self, author_id: str):
        """Verificar si existe un autor"""
        return self.db.query(models.Author).filter(models.Author.id == author_id).first() is not None