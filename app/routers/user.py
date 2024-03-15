from fastapi import FastAPI, Request, Depends, HTTPException, Depends, status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.user import UserCreate, User
from ..utils import send_verification_email
from pydantic import BaseModel 
from passlib.context import CryptContext


router = APIRouter()
app = FastAPI()
# models.Base.metadata.create_all(bind=engine)

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

@app.post("/signup/", response_model=SignUpResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send verification email
    verification_link = f"http://127.0.0.1:8000/verify?email={user.email}"  # Update with your verification link
    send_verification_email(user.email, verification_link)

    return SignUpResponse(message="Sign up successful! Check your email for verification.")