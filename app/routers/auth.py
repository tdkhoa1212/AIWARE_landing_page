from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..utils import authenticate_user
from ..models.auth import OAuth2PasswordRequestForm

router = APIRouter()

# OAuth2 scheme for password hashing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Return some token or session identifier
    return {"access_token": user.username, "token_type": "bearer"}
