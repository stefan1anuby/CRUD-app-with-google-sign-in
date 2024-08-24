import jwt
import os
import uuid

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.schemas import users as schema_users
from app.crud import users as users_crud
from app.database import get_db

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

API_SECRET_KEY = os.environ.get('SECRET_KEY','your_secret_key')
JWT_SIGN_ALGORITHM =  os.environ.get('JWT_SIGN_ALGORITHM','HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_access_token(data: str, expires_delta: timedelta = None):
    to_encode = {"sub" : data}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=JWT_SIGN_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: str):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data=data, expires_delta=expires)

def decode_token(token):
    options = {
        'verify_exp': True,  # Verify expiration
        'verify_iss': True,  # Verify issuer
    }
    return jwt.decode(token, API_SECRET_KEY, algorithms=[JWT_SIGN_ALGORITHM], options=options)


def get_user_from_token(db: Session = Depends(get_db), 
                     token: str = Depends(oauth2_scheme)
                    )-> schema_users.User:
    try:
        payload = decode_token(token)
        user_id: str = payload.get('sub')
        if user_id is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION
	
    user_db = users_crud.get_user_by_id(db, uuid.UUID(user_id))
    if not user_db:
        raise CREDENTIALS_EXCEPTION

    user_db_notes = [schema_users.Note(id=note.id, content=note.content) for note in user_db.notes]

    user = schema_users.User(id=user_db.id,
                             name=user_db.name,
                             email=user_db.email,
                             created_date=user_db.created_date,
                             last_login_date=user_db.last_login_date,
                             notes=user_db_notes)
    return user
    
