from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from app.Database import Base


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    company = Column(String(255), nullable=True)
    phone = Column(String(255))
    role = Column(String(255), nullable=True)
    select_field = Column(String(255))
    message = Column(String(1024))
