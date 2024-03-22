from fastapi import FastAPI, Request, Depends, HTTPException, Depends, status
from fastapi import APIRouter, Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import UserCreate, User, create_tables
from ..utils import send_verification_email
from pydantic import BaseModel 
from passlib.context import CryptContext
from sqlalchemy import inspect
from app.database import engine
import secrets

router = APIRouter()


class SignUpResponse(BaseModel):
    message: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_user_table():
    inspector = inspect(engine)
    if 'user' not in inspector.get_table_names():
        create_tables(engine)

def ensure_user_table(db: Session = Depends(get_db)):
    check_user_table()
    return db

# Sign up endpoint
@router.post("/signup/", response_model=SignUpResponse)
async def sign_up(user: UserCreate, db: Session = Depends(ensure_user_table)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        db_user = User(email=user.email, password=pwd_context.hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Send verification email 
        verification_link = f"http://127.0.0.1:8000/verification/verify?email={user.email}"
        send_verification_email(user.email, verification_link)

        return SignUpResponse(message="Sign up successful! Check your email for verification.")
    except OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
