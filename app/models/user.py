from sqlalchemy import Column, Integer, String 
from app.database import Base
from pydantic import BaseModel 

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
