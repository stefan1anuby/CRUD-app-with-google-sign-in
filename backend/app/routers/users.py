from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.utils import google_auth
from app.crud import users as crud_users
from app.schemas import users as schema_users
from app.schemas import responses as schema_responses
from app.utils.jwt import create_access_token, create_refresh_token, get_user_from_token

router = APIRouter()

# TODO: I should change it to "/login/{provider}"
@router.get("/login/google", response_model=schema_responses.OAuth2LoginResponse, summary="Initiate Google Login", tags=["Authentication"])
def login_google():
    """
    Initiates the OAuth2 flow for Google login.

    This endpoint returns the Google authorization URL that the client needs
    to redirect the user to in order to authenticate with Google.
    
   Returns:
        :return authorization_url: The URL where the user needs to authenticate with Google.
        :return state: A unique state parameter to help prevent CSRF attacks.
    """
    authorization_url, state = google_auth.get_google_authorization_url()
    
    return schema_responses.OAuth2LoginResponse(
			authorization_url=authorization_url,
			state=state
		)

# TODO: I should change it to "/auth/{provider}/callback"
@router.get("/auth/google/callback", response_model=schema_responses.TokenResponse, summary="Google OAuth2 Callback", tags=["Authentication"])
def auth_google_callback(code: Annotated[str, Query()], db: Session = Depends(get_db)):
    """
    Handles the callback from Google OAuth2 and exchanges the code for user information and JWT tokens.

    Parameters:
        :param code: Authorization code from Google.

    Returns:
        :return access_token: The JWT access token for API access.
        :return refresh_token: The JWT refresh token for obtaining new access tokens.
    """

    try:
        id_info = google_auth.exchange_authorization_code(code)
    except ValueError:
        raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
    
    email = id_info.get("email")
    name = id_info.get("name")

    if not email or not name:
        raise HTTPException(status_code=400, detail="Failed to retrieve user information from Google")

    user = crud_users.get_user_by_email(db, email=email)
    if not user:
        
		#User needs to be created
        user_create = schema_users.UserCreate(name=name, email=email)
        user = crud_users.create_user(db, user=user_create)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to create a new user")
   

    else:
        #User logged in and the account was already created
        user_update = schema_users.UserUpdate(id = user.id,
                                          last_login_date=datetime.now(timezone.utc))
        user = crud_users.update_user(db, user_update)
        if not user:
            raise HTTPException(status_code=500, detail="Failed to update the user when trying to log in")
   
    try:
        access_token = create_access_token(data=str(user.id))
        refresh_token = create_refresh_token(data=str(user.id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tokens")


    return schema_responses.TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.get("/me", response_model=schema_users.User, summary="Get Current User", tags=["Me"])
def protected_route(user: schema_users.User = Depends(get_user_from_token)):
    """
    Gets the info of the logged user
    
    Parameters:
        None (the user is identified by the token).
    
    Returns:
        - The user information.
    """
    return schema_users.User(id=user.id,
                             name=user.name,
                             email=user.email,
                             created_date=user.created_date,
                             last_login_date=user.last_login_date)

@router.put("/me/name", response_model=schema_users.User, summary="Change My Name", tags=["Me"])
def change_my_name(new_name: Annotated[str, Query(min_length=5,max_length=100)], user: schema_users.User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Allows the authenticated user to change their name.

    Parameters:
        :param new_name: The new name to be set for the user.

    Returns:
        :return: The updated user information.
    """

    user_update = schema_users.UserUpdate(id=user.id, name=new_name)
    updated_user = crud_users.update_user(db, user_update)

    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user name")
    
    return schema_users.User(id=updated_user.id,
                             name=updated_user.name,
                             email=updated_user.email,
                             created_date=updated_user.created_date,
                             last_login_date=updated_user.last_login_date)

@router.delete("/me", response_model=schema_responses.DeleteAccountResponse, summary="Delete My Account", tags=["Me"])
def delete_my_account(user: schema_users.User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
   	Allows the authenticated user to delete their account.

    Returns:
        :return message: Confirmation message.
    """
    deleted_user = crud_users.delete_user(db, user.id)
    if not deleted_user:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return schema_responses.DeleteAccountResponse(
        message="User account deleted successfully"
    )

@router.post("/me/notes", response_model=schema_users.Note, summary="Add a Note", tags=["Me, Notes"])
def add_note_for_user(note: schema_users.NoteCreate, user: schema_users.User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Allows the authenticated user to add a note.

    Parameters:
        :param note: The note content.

    Returns:
        :return: The created note.
    """
    note =  crud_users.create_note_for_user(db, user_id=user.id, note=note)
    if not note:
        raise HTTPException(status_code=500, detail="Failed to create note for user")
    
    return schema_users.Note(content=note.content,
                             id=note.id)


@router.get("/me/notes", response_model=list[schema_users.Note], summary="Get My Notes", tags=["Me", "Notes"])
def get_my_notes(user: schema_users.User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Retrieves all notes for the authenticated user.
    
    Parameters:
        None (the user is identified by the token).
    
    Returns:
        - A list of notes.
    """
    return crud_users.get_notes_by_user(db, user_id=user.id)

@router.delete("/me/notes/{note_id}", response_model=schema_responses.DeleteAccountResponse, summary="Delete a Note", tags=["User"])
def delete_note(note_id: UUID, user: schema_users.User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    """
    Deletes a note by its ID for the authenticated user.
    
    Parameters:
        :param note_id: The ID of the note to delete.

    Returns:
        - Confirmation message.
    """
    note = crud_users.delete_note_by_id(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return schema_responses.DeleteAccountResponse(
        message="Note deleted successfully"
    )