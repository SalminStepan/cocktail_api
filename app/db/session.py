from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

