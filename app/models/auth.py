from pydantic import BaseModel

class OAuth2PasswordRequestForm(BaseModel):
    username: str
    password: str
