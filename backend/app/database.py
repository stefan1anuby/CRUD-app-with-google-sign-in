import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


STAGE = os.getenv("STAGE")

if STAGE == "DEV":
    MARIADB_USER = os.getenv("MARIADB_USER")
    MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
    MARIADB_DATABASE = os.getenv("MARIADB_DATABASE")
    MARIADB_HOST = os.getenv("MARIADB_HOST")
    DATABASE_URL = f"mariadb+mariadbconnector://{MARIADB_USER}:{MARIADB_PASSWORD}@{MARIADB_HOST}:3306/{MARIADB_DATABASE}"
    
    engine = create_engine(
        DATABASE_URL
    )
elif STAGE == "TEST":
    print("WARNING!!! THE IN_MEMORY_DATABASE IS SET FOR TEST PURPOSES !!!")
    IN_MEMORY_SQLITE_URL = "sqlite:///:memory:"
    
    engine = create_engine(IN_MEMORY_SQLITE_URL, echo=True, connect_args={"check_same_thread": False}, 
        poolclass=StaticPool)
else:
    raise ValueError("ERROR: PLEASE SET THE STAGE ENV VARIABLE TO 'DEV' OR 'TEST'")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()