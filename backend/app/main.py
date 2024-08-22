from fastapi import FastAPI, Depends, HTTPException
from app.routers import users
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import users as users_crud
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI OAuth2 app!"}