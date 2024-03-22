from sqlalchemy import Column, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel 

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

class UserCreate(BaseModel):
    email: str
    password: str

def create_tables(engine):
    Base.metadata.create_all(bind=engine)

