import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'author'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String)
    email = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'book'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
