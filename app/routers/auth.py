from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel 
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
import secrets
from ..models.user import User
from ..routers.user import get_db
from fastapi.responses import JSONResponse
from ..models.user import UserCreate, User, create_tables


router = APIRouter()

templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginResponse(BaseModel):
    message: str

# Verifying password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post('/login/')
async def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user or not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        # Redirection to the verification page with email as a query parameter
        return JSONResponse(status_code=status.HTTP_200_OK, content={"email": user.email})
    
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )

