from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.core.config import load_config
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5431/restaurant")

engine = create_engine(load_config()["database"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
