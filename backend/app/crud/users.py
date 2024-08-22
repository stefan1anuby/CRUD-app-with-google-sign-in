from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone

from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate

def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_update.id)
    if db_user:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_last_login_date(db: Session, user_update: UserUpdate):
    db_user = User(
        **user_update,
        last_login_date=datetime.now(timezone.utc)
    )
    db.refresh(db_user)
    return user_update
    

def delete_user(db: Session, user_id: UUID):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
