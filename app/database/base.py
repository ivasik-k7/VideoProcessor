from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.config import database_config

engine = create_engine(database_config.DATABASE_URL, echo=True)


def initialize_db() -> None:
    """
    Initialize the database by creating tables based on the models.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a new database session.
    """
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()
