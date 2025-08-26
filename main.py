from fastapi import FastAPI
import models
from database import engine

# Importar routers
from routes.author import router as author_router
from routes.book import router as book_router

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Crear app
app = FastAPI(title="Library API", version="1.0.0")

# Registrar routers
app.include_router(author_router)
app.include_router(book_router)

@app.get("/")
def root():
    return {"message": "Library API - Welcome!"}