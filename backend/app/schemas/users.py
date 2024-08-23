from datetime import datetime
import uuid
from pydantic import BaseModel, constr

class NoteBase(BaseModel):
    content: constr(min_length=10, max_length=500) 

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    id: uuid.UUID

class Note(NoteBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    name: str
    email: str

class UserUpdate(UserBase):
    id: uuid.UUID
    email: str | None = None
    last_login_date: datetime | None = None 
    name: str | None = None

class User(UserBase):
    id: uuid.UUID
    name: str
    email: str
    created_date: datetime
    last_login_date: datetime
    notes: list[Note] = []

    class Config:
        orm_mode = True


