from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_settings import Base, get_db
from main import app

import sys

sys.path.append('..')

SQLALCHEMY_DATABASE_URL_FOR_TESTING = "sqlite:///config/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL_FOR_TESTING, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
