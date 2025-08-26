from pydantic import BaseModel


class AuthorRequest(BaseModel):
    name: str
    email: str


class BookRequest(BaseModel):
    title: str
    description: str
    author_id: str
