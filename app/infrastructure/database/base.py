from typing import Generator
from app.infrastructure.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}'
                f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

engine = create_engine(DATABASE_URL, pool_size=20, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator:
    with SessionLocal() as session:
        yield session