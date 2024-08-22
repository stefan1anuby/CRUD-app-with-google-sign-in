from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class OAuth2LoginResponse(BaseModel):
    authorization_url: str
    state: str
    
class DeleteAccountResponse(BaseModel):
    message: str