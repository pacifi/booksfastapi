import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'author'
    # id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    email = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'book'
    # id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String)
    description = Column(String)
    author_id = Column(UUID(as_uuid=True), ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
