from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
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

@router.post('/login/', response_model=LoginResponse)
async def login(request: Request, user: UserCreate,  db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user or not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        verification_successful = True 
        verification_link = f"http://127.0.0.1:8000/verification/verify?email={user.email}"
        return templates.TemplateResponse("index.html", {
                "request": request,  # This should be the Request object from the argument
                "email": user.email,
                "verified": verification_successful,
                "verification_link": verification_link  # Pass the verification link as a separate context variable
            })
    
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"}
        )

