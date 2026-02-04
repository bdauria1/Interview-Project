from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
_engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL)
    return _engine

def get_session():
    engine = get_engine()
    SessionLocal.configure(bind=engine)
    return SessionLocal()