from pydantic import BaseModel

class OAuth2PasswordRequestForm(BaseModel):
    email: str
    password: str
