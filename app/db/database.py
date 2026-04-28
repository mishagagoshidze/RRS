from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./RRS.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()