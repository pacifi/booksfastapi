from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URI = "sqlite:///./database.db" SQLITE
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/library_db"

# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
