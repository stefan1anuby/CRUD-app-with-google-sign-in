import os
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from fastapi import HTTPException

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

def get_authorization_url():
    flow = Flow.from_client_secrets_file(
        "client_secret.json",  # This file contains your OAuth 2.0 credentials
        scopes=scopes,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    return authorization_url, state

def exchange_authorization_code(code: str):
    flow = Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=scopes,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    request = requests.Request()
    
    try:
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, request, GOOGLE_CLIENT_ID, clock_skew_in_seconds=10
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Token verification failed: {e}")
    
    return id_info
