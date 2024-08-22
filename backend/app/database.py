import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
MARIADB_DATABASE = os.getenv("MARIADB_DATABASE")
MARIADB_HOST = os.getenv("MARIADB_HOST")

DATABASE_URL = f"mariadb+mariadbconnector://{MARIADB_USER}:{MARIADB_PASSWORD}@{MARIADB_HOST}:3306/{MARIADB_DATABASE}"

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()